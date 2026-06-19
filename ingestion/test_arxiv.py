import requests
import feedparser
from ingest_paper import fetch_papers


url="http://export.arxiv.org/api/query"
params={"search_query":"all:machine learning","start":0, "max_results":1}
response= requests.get(url,params=params)
feed= feedparser.parse(response.text)
paper= feed.entries[0]

print("TITLE:")
print(paper.title)

print("\nABSTRACT:")
print(paper.summary)

print("\nPUBLISHED:")
print(paper.published)

print("\nARXIV URL:")
print(paper.id)

papers = fetch_papers(
    query="id:2306.04338v1",
    max_results=1
)
