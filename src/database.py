
from src.config import MONGO_URI
from pymongo import MongoClient



mon_client=MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)

db=mon_client["music_app"]
db_collection=db["songs"]
watch_history_collection=db["watch_history"]


search_index_model={
    "name":"search_music_index",
    "definition":{
        
        "mappings":{
            "dynamic":False,
            "fields":{
                "embedding":{
                    "type":"knnVector",
                    "dimensions":384,
                    "similarity":"cosine"
                }
                
            }
        }
    }
}
existing_index=[]
for idx in db_collection.list_search_indexes():
    existing_index.append(idx["name"])
    
if "search_music_index" not in existing_index:
        result=db_collection.create_search_index(model=search_index_model)
        print(f"Index Name:{result}")
else:
        print("Index is already existing")
        