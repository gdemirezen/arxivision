from tools.openalex_search_tool import search_openalex
from typing import List, Dict

class OpenAlexAgent:
    def search(self, keywords: str) -> List[Dict]:
        print(f"OpenAlexAgent: Searching for '{keywords}'...")
        results = search_openalex(keywords)
        print(f"OpenAlexAgent: Found {len(results)} papers.")
        return results
