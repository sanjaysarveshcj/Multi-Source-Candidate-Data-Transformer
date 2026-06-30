from typing import List, Dict, Set
from collections import defaultdict
import difflib

from app.models.raw_candidate import RawCandidate
from app.logging.logger import logger


class IdentityResolver:
    """
    Groups a flat list of RawCandidate objects into lists of candidates
    that belong to the same person, based on matching PII.
    """

    def _extract_skill_names(self, cand: RawCandidate) -> Set[str]:
        if not cand.skills:
            return set()
        skills = set()
        for s in cand.skills:
            if isinstance(s, dict):
                val = s.get("name") or s.get("skill") or s.get("title")
                if val:
                    skills.add(val.lower().strip())
            elif isinstance(s, str):
                skills.add(s.lower().strip())
        return skills
        
    def _extract_companies(self, cand: RawCandidate) -> Set[str]:
        if not cand.experience:
            return set()
        comps = set()
        for e in cand.experience:
            if isinstance(e, dict) and e.get("company"):
                comps.add(e.get("company").lower().strip())
        return comps

    def _extract_education(self, cand: RawCandidate) -> Set[str]:
        if not cand.education:
            return set()
        edus = set()
        for e in cand.education:
            if isinstance(e, dict) and e.get("institution"):
                edus.add(e.get("institution").lower().strip())
        return edus

    def _has_supporting_evidence(self, cand1: RawCandidate, cand2: RawCandidate) -> bool:
        # 1. Check shared skills
        skills1 = self._extract_skill_names(cand1)
        skills2 = self._extract_skill_names(cand2)
        if skills1.intersection(skills2):
            return True
            
        # 2. Check shared companies
        comps1 = self._extract_companies(cand1)
        comps2 = self._extract_companies(cand2)
        if comps1.intersection(comps2):
            return True
            
        # 3. Check shared education
        edu1 = self._extract_education(cand1)
        edu2 = self._extract_education(cand2)
        if edu1.intersection(edu2):
            return True
            
        return False

    def _is_name_similar(self, name1: str, name2: str) -> bool:
        n1 = name1.lower().replace(" ", "")
        n2 = name2.lower().replace(" ", "")
        if not n1 or not n2:
            return False
            
        # Subset match (e.g. "sanjaysarvesh" in "sanjaysarveshcj")
        if n1 in n2 or n2 in n1:
            return True
            
        # Or difflib ratio > 0.85
        if difflib.SequenceMatcher(None, n1, n2).ratio() > 0.85:
            return True
            
        return False

    def group(self, candidates: List[RawCandidate]) -> List[List[RawCandidate]]:
        if not candidates:
            return []

        logger.info(f"Resolving identities for {len(candidates)} raw candidates...")
        
        # We'll use a Union-Find (Disjoint Set) to group candidates by index.
        parent = {i: i for i in range(len(candidates))}
        
        def find(i: int) -> int:
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
            
        def union(i: int, j: int):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_j] = root_i

        # PHASE 1: Exact Matches
        email_map: Dict[str, int] = {}
        phone_map: Dict[str, int] = {}
        link_map: Dict[str, int] = {}
        name_map: Dict[str, int] = {}

        for i, cand in enumerate(candidates):
            # Match by email
            for email in cand.emails:
                if email:
                    email_key = email.lower().strip()
                    if email_key in email_map:
                        union(i, email_map[email_key])
                    else:
                        email_map[email_key] = i

            # Match by phone
            for phone in cand.phones:
                if phone:
                    phone_key = phone.strip()
                    if phone_key in phone_map:
                        union(i, phone_map[phone_key])
                    else:
                        phone_map[phone_key] = i

            # Match by links (LinkedIn, GitHub)
            if cand.links:
                for link_val in [cand.links.get("linkedin"), cand.links.get("github")]:
                    if link_val:
                        link_key = link_val.lower().strip()
                        # normalize a bit
                        link_key = link_key.replace("https://", "").replace("http://", "").replace("www.", "")
                        if link_key in link_map:
                            union(i, link_map[link_key])
                        else:
                            link_map[link_key] = i

            # Match by exact name (fallback)
            if cand.full_name:
                name_key = cand.full_name.lower().strip()
                if name_key in name_map:
                    union(i, name_map[name_key])
                else:
                    name_map[name_key] = i

        # PHASE 2: Fuzzy Name + Supporting Evidence
        # Build initial clusters
        clusters: Dict[int, List[int]] = defaultdict(list)
        for i in range(len(candidates)):
            clusters[find(i)].append(i)
            
        root_indices = list(clusters.keys())
        
        for i in range(len(root_indices)):
            for j in range(i + 1, len(root_indices)):
                root_i = find(root_indices[i])
                root_j = find(root_indices[j])
                
                if root_i == root_j:
                    continue
                    
                # Cross check candidates in cluster i vs cluster j
                merged = False
                for idx_i in clusters[root_i]:
                    cand_i = candidates[idx_i]
                    if not cand_i.full_name:
                        continue
                        
                    for idx_j in clusters[root_j]:
                        cand_j = candidates[idx_j]
                        if not cand_j.full_name:
                            continue
                            
                        # Rule 6 check
                        if self._is_name_similar(cand_i.full_name, cand_j.full_name):
                            if self._has_supporting_evidence(cand_i, cand_j):
                                union(idx_i, idx_j)
                                merged = True
                                break
                    if merged:
                        break

        # Final Grouping by root parent
        groups: Dict[int, List[RawCandidate]] = defaultdict(list)
        for i, cand in enumerate(candidates):
            root = find(i)
            groups[root].append(cand)
            
        result = list(groups.values())
        logger.info(f"Identity resolution complete: merged {len(candidates)} records into {len(result)} distinct candidates.")
        return result
