from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import re

load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text, model="text-embedding-3-small"):
   # Remove quebras de linha indesejadas
   text = text.replace('\n', ' ')

   return client.embeddings.create(input = [text], model=model).data[0].embedding

def openai_CHATGPT(system_prompt, user_query):
   response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}    
    ]
   )

   return response.choices[0].message.content
