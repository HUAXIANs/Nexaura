import os
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions # <--- 导入 ClientOptions

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Create a Supabase client instance
# Set a longer timeout (e.g., 30 seconds) to mitigate potential network issues
# 使用 ClientOptions 来创建配置
options = ClientOptions(postgrest_client_timeout=30)
supabase: Client = create_client(url, key, options)