from huggingface_hub import InferenceClient
from pymongo import MongoClient
hf_client=InferenceClient(token="")

mon_client=MongoClient("", tlsAllowInvalidCertificates=True)

db=mon_client["music_app"]
db_collection=db["songs"]

def get_embedding(text):
    result=hf_client.feature_extraction(
        text,
        model="BAAI/bge-small-en-v1.5"
    )
    return result.tolist()

query= "relaxing music for studying"
embedding_query=get_embedding(query)

pipline=db_collection.aggregate([{"$vectorSearch":{
    "index":"music_index",
    "path":"embedding",
    "queryVector":embedding_query,
    "numCandidates":100,
    "limit":10
        
    
}}])

for p in pipline:
    print(f"{p["song_id"]}, {p["title"]}, {p["artist"]},{p["genre"]},{p["popularity"]},{p["album"]},{p["mood"]},{p["language"]},{p["release_year"]},{p["description"]}")
    # print(f"{p["title"]}")
    # print(f"{p["artist"]}")
    # print(f"{p["genre"]}")
    # print(f"{p["popularity"]}")
    # print(f"{p["album"]}")
    # print(f"{p["mood"]}")
    # print(f"{p["language"]}")
    # print(f"{p["release_year"]}")
    # print(f"{p["description"]}")
    print("---")
    
    
    
    
   
  
