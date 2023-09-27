import subprocess
import chromadb
from chromadb import Settings
from chromadb.utils import embedding_functions

## do something with the databse to search for a fiel
client = chromadb.Client()
default_ef = embedding_functions.DefaultEmbeddingFunction()
col = client.get_or_create_collection(name='music', embedding_function=default_ef)

result = col.query(
  query_texts=['printemp'],
  n_results=1
)
print(col.get())
print(result)