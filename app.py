from flask import Flask  ,render_template , request , jsonify , session , redirect , url_for
from src.config import SECRET_KEY
from src.recommender import get_recommend_genre
from src.vector_search import vector_search
from src.database import watch_history_collection
from datetime import datetime
from datetime import timedelta
import os 
from src.audio_search import recognize_audio
import uuid


app=Flask(__name__)
app.secret_key=SECRET_KEY

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
        combine_recommendation=genre+","+interests_str+","+language
        recommendations=vector_search(combine_recommendation)
        session["recommendations"]=recommendations
        
        
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    return render_template("search.html" , recommendations=recommendations)
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
      results=vector_search(combine)
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
        watch_history_collection.insert_one({
           
            "song_id":song["song_id"],
            "title":song["title"],
            "artist":song["artist"],
            "genre":song["genre"],
            "played_at":datetime.utcnow()
        })
         
        total=len(results)
        prev_index=(index-1)%total
        next_index=(index+1)%total
        return render_template("player.html", results=results , song=song , prev_index=prev_index , next_index=next_index )
    else:
        return redirect(url_for("home"))
@app.route("/history")
def history():
    history=list(watch_history_collection.find({"played_at":{"$gte":datetime.utcnow()-timedelta(days=7)}}).sort("played_at" , -1))
    for item in history:
        item.pop("_id", None)
    session["results"]=history
    
    return render_template("history.html" , history=history)
    
@app.route("/recognize", methods=["POST"])
def upload_files():
    if "audio" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save with unique name
    temp_filename = f"temp_{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
    temp_filepath = os.path.abspath(temp_filename)
    file.save(temp_filepath)

    try:
        song_info = recognize_audio(temp_filepath)
        if song_info:
            title, artist = song_info
            results = vector_search(f"{title},{artist}")
            session["results"] = results
            return redirect(url_for("playlist"))
        else:
            return jsonify({"error": "Song Not Found"}), 404
    finally:
        # Always clean up uploaded file
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

@app.route("/")
def home():
    return render_template("home.html")

if __name__=='__main__':
    app.run(debug=True)
    

      
        

    

   






    
    
    
    
    
    
    
    
    
    
    
    
    

   
    
    


