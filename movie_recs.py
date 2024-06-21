import os
from dotenv import load_dotenv
import pymongo
import requests

load_dotenv()

database_url = os.getenv("DATABASE_URL")
hf_token = os.getenv("HF_TOKEN")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


print(database_url)
print(hf_token)

client = pymongo.MongoClient(database_url)
db = client.sample_mflix
collection = db.movies


def generate_embedding(text: str) -> list:
    headers = {"Authorization": f"Bearer {hf_token}"}
    response = requests.post(embedding_url, headers=headers, json={"inputs": [text]})
    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status code {response.status_code}: {response.text}"
        )

    # Assuming the first element of the response JSON is the embedding
    embedding = response.json()

    # Flatten the list if it's nested
    if isinstance(embedding[0], list):
        embedding = [float(num) for sublist in embedding for num in sublist]
    else:
        embedding = [float(num) for num in embedding[0]]

    return embedding


# for doc in collection.find({"plot": {"$exists": True}}).limit(50):
#     doc["plot_embedding"] = generate_embedding(doc["plot"])
#     collection.replace_one({"_id": doc["_id"]}, doc)


query = "imaginary character from outer space at war"


results = collection.aggregate(
    [
        {
            "$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "plot_embedding",
                "numCandidates": 100,
                "limit": 4,
                "index": "PlotSematicSearch",
            }
        }
    ]
)

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')
