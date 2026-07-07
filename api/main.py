from fastapi import FastAPI
from contextlib import asynccontextmanager
from ingestion.scheduler import (start_scheduler,stop_scheduler)
'''from api.services.embedding_service import (semantic_search , hybrid_search)'''
from fastapi.middleware.cors import CORSMiddleware
from api.routes import search_router, papers_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    print("🚀 Starting Research Intelligence Platform...")

    start_scheduler()

    yield

    stop_scheduler()

    print("🛑 Shutting down Research Intelligence Platform...")

app = FastAPI(
    title="Research Intelligence Platform",
    lifespan=lifespan,
) #object of FastAPI class, this will represent the entire backend application

app.include_router(search_router)

app.include_router(papers_router)

app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173",],allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"],)

@app.get("/") # this is root route, whenever the browser visits a particular url, it sends a HTTP request which is get, it tells to run the function below.
def home(): # fastAPI knows whenver we have a GET call, go to home function
    return{"message": "Research Intelligence Platform API"} # FastAPI automatically converts dictionaries into JSON, so it sends it back to the browser.

'''@app.get("/semantic-search")
def semantic_search_endpoint(q: str,response_model=list[SemanticSearchResult]):

    return semantic_search(q)

@app.get("/hybrid-search")
def hybrid_search_endpoint(q: str):
    return hybrid_search(q)'''

