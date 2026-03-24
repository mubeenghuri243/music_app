from dotenv import load_dotenv
import os 
load_dotenv()


HF_TOKEN=os.getenv("HF_TOKEN")
MONGO_URI=os.getenv("MONGO_URI")
SECRET_KEY="mysecret_key"
ACR_HOST=os.getenv("ACR_HOST")
ACR_KEY=os.getenv("ACR_KEY")
ACR_SECRET=os.getenv("ACR_SECRET")



