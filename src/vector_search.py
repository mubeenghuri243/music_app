from src.database import db_collection
from src.embeddings import get_embedding


def vector_search(combine):
    embedding_query=get_embedding(combine)
    pipeline=db_collection.aggregate([{"$vectorSearch":
              {
            "index":"search_music_index",
            "path":"embedding",
            "queryVector":embedding_query,
            "numCandidates":100,
            "limit":10
            
        }}])
    results=[]
    for r in pipeline:
        results.append({
        "song_id":r["song_id"],
        "title":r["title"],
        "artist":r["artist"],
        "genre":r["genre"],
        "popularity":r["popularity"],
        "album":r["album"],
        "mood":r["mood"],
        "language":r["language"],
        "release_year":r["release_year"],
        "description":r["description"]
    })
    return results
    