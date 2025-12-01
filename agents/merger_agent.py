from typing import List, Dict

class MergerAgent:
    def merge(self, list1: List[Dict], list2: List[Dict], limit: int = 10) -> List[Dict]:
        print("MergerAgent: Merging lists...")
        # Merge by title (normalized)
        seen_titles = set()
        merged_list = []
        
        for paper in list1 + list2:
            title_norm = paper['title'].lower().strip()
            if title_norm not in seen_titles:
                seen_titles.add(title_norm)
                merged_list.append(paper)
        
        print(f"MergerAgent: Merged into {len(merged_list)} unique papers. Returning top {limit}.")
        return merged_list[:limit]
