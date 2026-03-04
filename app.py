from flask import Flask  ,render_template , request , jsonify
from huggingface_hub import InferenceClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
load_dotenv()


app=Flask(__name__)

hf_client=InferenceClient(token=os.getenv("HF_TOKEN"))

mon_client=MongoClient(os.getenv("MONGO_URI"), tlsAllowInvalidCertificates=True)

db=mon_client["music_app"]
db_collection=db["songs"]

def get_embedding(text):
    result=hf_client.feature_extraction(
        text,
        model="BAAI/bge-small-en-v1.5"
    )
    return result.tolist()
def get_recommend_genre(age):
    
    if age<18:
        recommend_genre="upbeat, trending, clean content"
    elif age>=18 and age<=30:
        recommend_genre="pop, EDM, hip-hop, indie"
    elif age>=30 and age<=45:
        recommend_genre="classics, soft rock, melodic"
    else:
        recommend_genre="old classics, devotional, calm music"

    return recommend_genre
@app.route("/user_input" , methods=['POST'])
def user_input():
    try:
        age=request.form.get("age")
        interests=request.form.get("interests")
        language=request.form.get("language")
        query=request.form.get("query")
        
        if not age or not interests or not language or not query:
            return jsonify({"error":"All fileds is required"})
        
        age=int(age)
        genre=get_recommend_genre(age)
        interests_str=interests
        combine=genre+","+interests_str+","+language+","+query
        embedding_query=get_embedding(combine)
        pipline=db_collection.aggregate([{"$vectorSearch":
              {
            "index":"music_index",
            "path":"embedding",
            "queryVector":embedding_query,
            "numCandidates":100,
            "limit":10
            
        }}])
        results=[]
        for r in pipline:
            
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
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
        
    return jsonify(results)

        
    
@app.route("/")
def home():
    return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)
    


      
        

    

   






    
    
    
    
    
    
    
    
    
    
    
    
    

   
    
    


