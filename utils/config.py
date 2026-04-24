import os
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

class Config:
    """
    This class holds all our 'Settings'.
    If we need to add more keys later (like a Google Search key),
    we add them here.
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # We can set a default model here so we don't have to type it every time.
    MODEL_NAME = "llama-3.3-70b-versatile"

# A quick safety check:
if not Config.GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set in your .env file!")