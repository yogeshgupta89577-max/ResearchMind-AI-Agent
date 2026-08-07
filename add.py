import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("ZAI_API_KEY"))