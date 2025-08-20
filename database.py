import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

try:
    # Pega as informações do arquivo .env
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    # Cria cliente do Supabase
    if url and key:
        supabase = create_client(url, key)
except Exception as e:
    print(e)
