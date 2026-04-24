import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the secret key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Check if key is there
if not api_key:
    print("ERROR: GROQ_API_KEY not found in .env file")
else:
    # 3. Setup the Groq client
    client = Groq(api_key=api_key)

    try:
        print("--- Connecting to Groq (High Speed) ---")

        # 4. Ask the question
        # We use 'llama-3.3-70b-versatile', it is smart and free
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'System Online' if you can hear me."}
            ]
        )

        # 5. Print the response
        print("Response: " + completion.choices[0].message.content)
        print("SUCCESS: Your agent brain is ready!")

    except Exception as e:
        print("ERROR: Something went wrong: " + str(e))