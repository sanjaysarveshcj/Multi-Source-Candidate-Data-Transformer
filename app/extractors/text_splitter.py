import re
from typing import List
from app.logging.logger import logger

class TextSplitter:
    """
    Splits unstructured text (like a concatenated PDF or TXT) into multiple distinct
    candidate text blocks using a distance-based contact heuristic (Emails).
    """

    def split(self, text: str) -> List[str]:
        # Regex to find emails
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        
        matches = list(email_pattern.finditer(text))
        
        if not matches:
            return [text]
            
        # Group matches into clusters
        clusters = []
        current_cluster = [matches[0]]
        
        for i in range(1, len(matches)):
            prev = matches[i-1]
            curr = matches[i]
            # If emails are within 1500 characters of each other, they belong to the same candidate
            # 1500 chars is roughly half a page of dense text, easily covering headers.
            if curr.start() - prev.end() < 1500:
                current_cluster.append(curr)
            else:
                clusters.append(current_cluster)
                current_cluster = [curr]
        
        clusters.append(current_cluster)
        
        if len(clusters) == 1:
            return [text]
            
        chunks = []
        last_split = 0
        
        for i in range(1, len(clusters)):
            cluster = clusters[i]
            first_email_start = cluster[0].start()
            
            # Search back up to 300 characters to find the boundary
            search_start = max(last_split, first_email_start - 300)
            prefix = text[search_start:first_email_start]
            
            lines = prefix.split('\n')
            
            # We want to split at least 2 lines before the email line to capture the name
            if len(lines) >= 3:
                split_idx = first_email_start - len('\n'.join(lines[-2:])) - 1
            elif len(lines) >= 2:
                split_idx = first_email_start - len(lines[-1]) - 1
            else:
                split_idx = first_email_start - len(lines[-1])
                
            chunks.append(text[last_split:split_idx].strip())
            last_split = split_idx
            
        chunks.append(text[last_split:].strip())
        
        # Filter out empty chunks
        chunks = [c for c in chunks if len(c.strip()) > 50]
        
        logger.info(f"Split document into {len(chunks)} distinct candidates based on email clusters.")
        return chunks
