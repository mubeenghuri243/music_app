from src.config import HF_TOKEN
from huggingface_hub import InferenceClient

hf_client=InferenceClient(token=HF_TOKEN)

def get_embedding(text):
    result=hf_client.feature_extraction(
        text,
        model="BAAI/bge-small-en-v1.5"
    )
    return result.tolist()