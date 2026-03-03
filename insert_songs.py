from huggingface_hub import InferenceClient
import pandas as pd

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
df = pd.read_csv(r'D:\music_app\music_dataset_100_songs.csv')


for index, row in df.iterrows():
        embedding=get_embedding(row["description"])
        song_dic={
            "song_id":row["song_id"],
            "title":row["title"],
            "artist":row["artist"],
            "genre":row["genre"],
            "album":row["album"],
            "popularity":row["popularity"],
            "mood":row["mood"],
            "language":row["language"],
            "release_year":row["release_year"],
            "description":row["description"],
            "embedding":embedding
            
        }
        db_collection.insert_one(song_dic)
        print(f"Inserted:{row['title']}")