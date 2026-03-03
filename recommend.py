from huggingface_hub import InferenceClient
from pymongo import MongoClient
hf_client=InferenceClient(token="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")

mon_client=MongoClient("mongodb+srv://mubeenghuri243_db_user:u8c9BZx6JWO92aWc@vector-search-practice.eu4zkpn.mongodb.net/?appName=vector-search-practice", tlsAllowInvalidCertificates=True)

db=mon_client["music_app"]
db_collection=db["songs"]

def get_embedding(text):
    result=hf_client.feature_extraction(
        text,
        model="BAAI/bge-small-en-v1.5"
    )
    return result.tolist()


user={
  "age": 22,
  "interests": ["pop", "lofi", "chill"],
  "preferred_language": "English"
}  


if user["age"]<18:
    
    recommended_genre="upbeat, trending, clean content"
    
elif user["age"]>=18 and user["age"]<=30:
    
    recommended_genre="pop, EDM, hip-hop, indie"
    
elif user["age"]>=30 and user["age"]<=45:
    
    recommended_genre="classics, soft rock, melodic"
    
else:
    recommended_genre="old classics, devotional, calm music"
  
    


interests_str=",".join(user["interests"])

combine=recommended_genre+","+interests_str
emb_query=get_embedding(combine)
pipline=db_collection.aggregate([{"$vectorSearch":
    {
        "index":"music_index",
        "path":"embedding",
        "queryVector":emb_query,
        "numCandidates":100,
        "limit":10
            
    }}])
for r in pipline:
    print(f"{r["song_id"]}, {r["title"]}, {r["artist"]},{r["genre"]},{r["popularity"]},{r["album"]},{r["mood"]},{r["language"]},{r["release_year"]},{r["description"]}")
    print("---")





 
    
