from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
import httpx
from datetime import date
import asyncio

CROSSREF_MAILTO = "your-email@example.com"  # or read from .env
MAX_DOIS = 200  # max DOIs per request

def parse_crossref_data(data, doi):
    title = data.get('title', [""])[0]
    authors_list = data.get('author', [])
    authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in authors_list]
    
    pub_date = None
    for key in ['published-print', 'published-online', 'issued']:
        if key in data:
            parts = data[key].get('date-parts', [[None]])
            if parts and parts[0][0]:
                year = parts[0][0]
                month = parts[0][1] if len(parts[0]) > 1 else 1
                day = parts[0][2] if len(parts[0]) > 2 else 1
                pub_date = date(year, month, day)
                break

    peer_review = data.get('review', None)

    return {
        "doi": doi,
        "title": title,
        "authors": authors,
        "published_date": pub_date,
        "peer_review": peer_review,
        "raw": data
    }

async def fetch_single(doi):
    url = f"https://api.crossref.org/works/{doi}"
    headers = {"User-Agent": f"MyCrossrefApp (mailto:{CROSSREF_MAILTO})"}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            data = r.json().get('message', {})
            return parse_crossref_data(data, doi)
    except Exception as e:
        return {"doi": doi, "error": str(e)}

@api_view(['POST'])
def get_article_info_by_dois(request):
    dois = request.data
    if not isinstance(dois, list):
        return Response({"error": "Request body must be a JSON array of DOIs"}, status=400)
    if len(dois) > MAX_DOIS:
        return Response({"error": f"Maximum {MAX_DOIS} DOIs allowed per request"}, status=400)

    results = asyncio.run(asyncio.gather(*[fetch_single(doi) for doi in dois]))
    
    fetched = {}
    errors = {}

    for info in results:
        doi = info.get('doi')
        if 'error' in info:
            errors[doi] = info['error']
            continue

        # Save or update in DB
        obj, created = Article.objects.update_or_create(
            doi=doi,
            defaults={
                "title": info['title'],
                "authors": info['authors'],
                "published_date": info['published_date'],
                "peer_review": info['peer_review'],
                "raw": info['raw']
            }
        )
        fetched[doi] = ArticleSerializer(obj).data

    return Response({"fetched": fetched, "errors": errors})
