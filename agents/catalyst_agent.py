import json
from groq import Groq
from utils.config import Config
from prompts.system_prompts import SYSTEM_PROMPT
from tools.tool_manager import ToolManager

class CatalystAgent:
    """
    The core intelligence engine for Nexus AI.
    Handles document context injection, conversation state, and response generation
    using an agentic 'Think-Act-Observe' loop.
    """

    def __init__(self):
        # Initialize the Groq client using centralized configuration
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.MODEL_NAME
        self.tools = ToolManager()  # The agent's interface for external actions

        # In-memory storage for active session context
        self.resume_text: str = ""
        self.jd_text: str = ""
        self.chat_history: list = []

    def set_context(self, resume: str, jd: str):
        """
        Injects document data into memory and resets the chat history for a fresh start.
        """
        self.resume_text = resume
        self.jd_text = jd
        self.chat_history = []

    def get_response(self, user_input: str) -> str:
        """
        Inference loop with Function Calling support.
        Orchestrates multi-step reasoning by executing tools when requested by the LLM.
        """
        # 1. Construct the 'Source of Truth' context
        mega_prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            "--- START OF CONTEXT ---\n"
            f"CANDIDATE RESUME:\n{self.resume_text}\n\n"
            f"TARGET JOB DESCRIPTION:\n{self.jd_text}\n"
            "--- END OF CONTEXT ---"
        )

        messages = [{"role": "system", "content": mega_prompt}]
        messages.extend(self.chat_history)
        messages.append({"role": "user", "content": user_input})

        # 2. Retrieve Tool Definitions
        tool_defs = self.tools.get_tool_definitions()

        try:
            # 3. Initial Inference Call (Allowing for Tool Use)
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tool_defs if tool_defs else None,
                tool_choice="auto",
                temperature=0.1
            )

            # --- THE "DOC SWAP" SANITY CHECK ---
            # If the model is confused by the swapped docs, this catches it.
            if "Nexus Engine Error" in str(completion):
                 return "I've detected a logic mismatch in the documents. Please ensure the Resume and JD are in their correct slots."

            response_message = completion.choices[0].message
            tool_calls = response_message.tool_calls

            # --- SAFETY GATE: Handle empty or malformed responses ---
            if not response_message.content and not tool_calls:
                return "I'm analyzing your profile against the JD. Could you tell me more about your recent technical projects?"

            # 4. Execute Tools if requested (The Agentic Loop)
            if tool_calls:
                # Add the assistant's tool-call request to the message history
                messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                        # Execute the tool via ToolManager
                        tool_output = self.tools.execute_tool(function_name, function_args)
                    except Exception as tool_error:
                        # Prevent tool execution errors from crashing the main loop
                        tool_output = f"Execution Error in {function_name}: {str(tool_error)}"

                    # Feed the observation back into the conversation
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_output,
                    })

                # Second call: Translate tool results into natural language
                second_completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                final_reply = second_completion.choices[0].message.content
            else:
                # Direct response if no tools were required
                final_reply = response_message.content

            # 5. Update Persistent Memory and Return
            if final_reply:
                self.chat_history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "assistant", "content": final_reply})
                return final_reply

            return "The assessment engine encountered a processing delay. Please try again."

        except Exception as e:
            # Professional error reporting for the UI
            return f"Nexus Engine Error: {str(e)}"

    def generate_chat_title(self) -> str:
        """
        Generates a concise 3-word title for the UI sidebar using a lightweight inference call.
        """
        if not self.resume_text or not self.jd_text:
            return "New Assessment"

        try:
            context_snippet = f"Resume: {self.resume_text[:200]}... JD: {self.jd_text[:200]}..."
            messages = [
                {"role": "system", "content": "You are a concise administrative assistant."},
                {"role": "user", "content": f"{context_snippet}\n\nTask: Generate a 3-word title. Return ONLY text."}
            ]
            completion = self.client.chat.completions.create(model=self.model, messages=messages, max_tokens=15)
            return completion.choices[0].message.content.strip().replace('"', '')
        except:
            return "Skill Assessment"