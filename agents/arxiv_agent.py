from tools.arxiv_search_tool import search_arxiv
from typing import List, Dict

class ArxivAgent:
    def search(self, keywords: str) -> List[Dict]:
        print(f"ArxivAgent: Searching for '{keywords}'...")
        results = search_arxiv(keywords)
        print(f"ArxivAgent: Found {len(results)} papers.")
        return results
