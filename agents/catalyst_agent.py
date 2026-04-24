from groq import Groq
from utils.config import Config
from prompts.system_prompts import SYSTEM_PROMPT

class CatalystAgent:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.MODEL_NAME
        # Memory starts empty
        self.resume_text = ""
        self.jd_text = ""
        self.chat_history = []

    def set_context(self, resume, jd):
        """Saves the documents into memory so the agent always knows the 'Truth'."""
        self.resume_text = resume
        self.jd_text = jd
        # Clear history for a new candidate
        self.chat_history = []

    def get_response(self, user_input):
        """The main thinking loop."""

        # We build the 'Mega-Prompt' here
        full_context_prompt = f"""
        {SYSTEM_PROMPT}

        --- CONTEXT DOCUMENTS ---
        CANDIDATE RESUME: {self.resume_text}
        TARGET JOB DESCRIPTION: {self.jd_text}

        --- INSTRUCTIONS ---
        Analyze the input above and respond to the user's message.
        """

        # Prepare messages for Groq (History + New Input)
        messages = [{"role": "system", "content": full_context_prompt}]

        # Add past conversation so it doesn't forget
        for msg in self.chat_history:
            messages.append(msg)

        # Add the current message
        messages.append({"role": "user", "content": user_input})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5 # Keeps responses professional/stable
            )

            ai_reply = completion.choices[0].message.content

            # Save this turn to memory
            self.chat_history.append({"role": "user", "content": user_input})
            self.chat_history.append({"role": "assistant", "content": ai_reply})

            return ai_reply

        except Exception as e:
            return f"Brain Error: {str(e)}"

    def generate_chat_title(self):
        """Generates a clean, spaced title for the sidebar."""
        try:
            prompt = "Generate a 3-word title with spaces (e.g., 'React Developer Assessment') for this session based on the documents. Return ONLY the title, no quotes."
            messages = [
                {"role": "system", "content": "You are a professional coordinator."},
                {"role": "user", "content": f"Resume: {self.resume_text[:400]}... JD: {self.jd_text[:400]}... {prompt}"}
            ]
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            # Ensure it's just text
            return completion.choices[0].message.content.strip().replace('"', '')
        except:
            return "New Assessment"