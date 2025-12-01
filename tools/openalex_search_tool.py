import requests
import datetime
import time
from typing import List, Dict

def search_openalex(keywords: str, limit: int = 10) -> List[Dict]:
    """
    Searches OpenAlex for papers matching the keywords from the last week.
    """

    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    last_week_str = last_week.strftime("%Y-%m-%d")
    
    url = "https://api.openalex.org/works"
    params = {
        "search": keywords,
        "filter": f"from_publication_date:{last_week_str}",
        "per_page": limit,
        "sort": "publication_date:desc"
    }
    
    time.sleep(1)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        papers = []
        for item in data.get("results", []):
            authors = [a.get("author", {}).get("display_name", "Unknown") for a in item.get("authorships", [])]
            
            papers.append({
                "source": "OpenAlex",
                "title": item.get("display_name"),
                "abstract": "Abstract not directly available via OpenAlex API simple view.", # Placeholder
                "authors": authors,
                "url": item.get("doi") or item.get("id"),
                "date": item.get("publication_date")
            })
            
        return papers
        
    except Exception as e:
        print(f"Error searching OpenAlex: {e}")
        return []
