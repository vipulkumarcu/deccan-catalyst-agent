"""
Nexus AI Configuration Module
Centralizes environment variables, model parameters, and system constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from local .env file
load_dotenv()

class Config:
    """
    Static configuration class to manage global settings.
    Provides a single source of truth for all modules.
    """

    # --- AI Engine Credentials ---
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # --- Model Configuration ---
    # Llama 3.3 70B Versatile is optimized for reasoning and assessment tasks
    MODEL_NAME = "llama-3.3-70b-versatile"

    # --- System Paths ---
    # Centralized location for session storage
    SESSION_DIR = "sessions"

    @classmethod
    def validate(cls):
        """
        Critical safety check to ensure environment variables are loaded.
        Prevents the application from starting in a broken state.
        """
        if not cls.GROQ_API_KEY:
            # Raising an error is better than a print statement for debugging
            raise EnvironmentError(
                "NEXUS CONFIG ERROR: 'GROQ_API_KEY' not found in environment. "
                "Ensure your .env file is correctly configured in the project root."
            )

# Execute validation on module import
Config.validate()