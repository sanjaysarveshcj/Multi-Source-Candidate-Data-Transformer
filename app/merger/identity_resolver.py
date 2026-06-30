from typing import List, Dict, Set
from collections import defaultdict

from app.models.raw_candidate import RawCandidate
from app.logging.logger import logger


class IdentityResolver:
    """
    Groups a flat list of RawCandidate objects into lists of candidates
    that belong to the same person, based on matching PII.
    """

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

        # Dictionaries to map values to candidate indices
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

        # Group by root parent
        groups: Dict[int, List[RawCandidate]] = defaultdict(list)
        for i, cand in enumerate(candidates):
            root = find(i)
            groups[root].append(cand)
            
        result = list(groups.values())
        logger.info(f"Identity resolution complete: merged {len(candidates)} records into {len(result)} distinct candidates.")
        return result
