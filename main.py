from flask import Flask  ,render_template , request , jsonify , session , redirect , url_for
from huggingface_hub import InferenceClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
load_dotenv()


app=Flask(__name__)
app.secret_key="mysecret_key"

hf_client=InferenceClient(token=os.getenv("HF_TOKEN"))

mon_client=MongoClient(os.getenv("MONGO_URI"), tlsAllowInvalidCertificates=True)

db=mon_client["music_app"]
db_collection=db["songs"]

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
        if not age or not interests or not language :
            return jsonify({"error":"All fileds is required"})
        age=int(age)
        
        genre=get_recommend_genre(age)
        interests_str=interests
        
        session["interests"]=interests_str
        session["language"]=language
        session["genre"]=genre
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    return render_template("search.html")
@app.route("/user_search", methods=['GET' , 'POST'])
def user_search():
    if request.method=="GET":
      return render_template("search.html")
    
    if request.method=="POST":
      genre=session.get("genre")
      interests=session.get("interests")
      language=session.get("language")
      
      search_query=request.form.get("search_query")
      if not search_query:
          return jsonify({"Error":"Search Query Is Required"})
          
      combine=genre+","+interests+","+language+","+search_query
      embedding_query=get_embedding(combine)
      pipline=db_collection.aggregate([{"$vectorSearch":
              {
            "index":"search_music_index",
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
    session["results"]=results
    return redirect(url_for("playlist"))

  
@app.route("/playlist", methods=["GET"])
def playlist():
    results=session.get("results")
    if not results:
        return redirect(url_for("home"))
    return render_template("playlist.html", results=results)
@app.route("/player")
def player():
    
    results=session.get("results" , [])
    index=request.args.get("index",0, type=int)
    if results:
        song=results[index] 
        total=len(results)
        prev_index=(index-1)%total
        next_index=(index+1)%total
        return render_template("player.html", results=results , song=song , prev_index=prev_index , next_index=next_index )
    else:
        return redirect(url_for("home"))
        
    
    
@app.route("/")
def home():
    return render_template("home.html")

if __name__=='__main__':
    app.run(debug=True)
  
      
        

    

   






    
    
    
    
    
    
    
    
    
    
    
    
    

   
    
    


