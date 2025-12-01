import arxiv
import datetime
import time
from typing import List, Dict

def search_arxiv(keywords: str, limit: int = 10) -> List[Dict]:
    """
    Searches Arxiv for papers matching the keywords from the last week.
    """
    time.sleep(1)

    today = datetime.datetime.now(datetime.timezone.utc)
    last_week = today - datetime.timedelta(days=7)
    
    client = arxiv.Client()
    search = arxiv.Search(
        query = keywords,
        max_results = 25, # Fetch more to filter
        sort_by = arxiv.SortCriterion.SubmittedDate,
        sort_order = arxiv.SortOrder.Descending
    )
    
    papers = []
    try:
        for result in client.results(search):
            if result.published >= last_week:
                papers.append({
                    "source": "Arxiv",
                    "title": result.title,
                    "abstract": result.summary,
                    "authors": [a.name for a in result.authors],
                    "url": result.entry_id,
                    "date": result.published.strftime("%Y-%m-%d")
                })
            else:
                # Since results are sorted by date descending, once we hit older papers we can stop
                break
                
        return papers[:limit]
    except Exception as e:
        print(f"Error searching Arxiv: {e}")
        return []
