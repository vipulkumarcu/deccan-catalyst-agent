import os
from groq import Groq
from dotenv import load_dotenv

# 1. Loading the secret key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Checking if key is there
if not api_key:
    print("ERROR: GROQ_API_KEY not found in .env file")
else:
    # 3. Setting up the Groq client
    client = Groq(api_key=api_key)

    try:
        print("--- Connecting to Groq (High Speed) ---")

        # 4. Asking the question
        # Using 'llama-3.3-70b-versatile'
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'System Online' if you can hear me."}
            ]
        )

        # 5. Printing the response
        print("Response: " + completion.choices[0].message.content)
        print("SUCCESS: Your agent brain is ready!")

    except Exception as e:
        print("ERROR: Something went wrong: " + str(e))