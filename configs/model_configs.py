from enum import Enum
import logging
import warnings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")

class Models(Enum):
    """
    Defines a collection of supported AI model identifiers.
    """
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI = "gemini-2.5-flash-preview-05-20"
    CLAUDE_SONNET = "anthropic/claude-sonnet-4-20250514"
    CLAUDE_HAIKU = "anthropic/claude-3-5-haiku-20241022"
    GEMMA = "ollama_chat/gemma3:27b"
    GEMMA_4B = "ollama_chat/gemma3:4b"

    def __str__(self) -> str:
        """Returns the string value of the enum member."""
        return str(self.value)

    def __repr__(self) -> str:
        """Returns the official string representation."""
        return f"<{self.__class__.__name__}.{self.name}: '{self.value}'>"

# Define a simple default model function directly
def default_model() -> str:
    """
    Returns the default  model, which is GEMINI_2_0_FLASH.
    """
    logger.info(f"Using default model: {Models.GEMINI_2_0_FLASH.value}")
    return str(Models.GEMINI_2_0_FLASH)

