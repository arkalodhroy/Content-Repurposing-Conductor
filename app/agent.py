import json
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini

# Import ADK's built-in search tool class and instantiate it
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.genai import types

google_search = GoogleSearchTool(bypass_multi_tools_limit=True)

# Load environmental keys directly from the root folder directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

if os.environ.get("GOOGLE_API_KEY") == "no":
    os.environ.pop("GOOGLE_API_KEY", None)


# 1. Embedded Validation Tool Function
def verify_platform_constraints(content: str, platform: str, max_limit: int) -> str:
    """Validates if the generated content fits the platform's character limits."""
    char_count = len(content)
    is_valid = char_count <= max_limit

    result = {
        "platform": platform,
        "character_count": char_count,
        "max_limit": max_limit,
        "is_valid": is_valid,
        "remaining_characters": max_limit - char_count,
    }
    return json.dumps(result)


# 2. Embedded System Instructions Configuration
system_instruction = """Act as an expert content repurposing engine. First, ask the user for the target platform and the desired language for the output.

When searching for the platform's current character limits and formatting requirements, construct a precise Google Search query. If the user's platform matches one of our target domains (LinkedIn, X/Twitter, Instagram, Threads, Reddit, Medium, or Substack), append the specific 'site:' operator to your query (e.g., 'site:linkedin.com/help' or 'site:medium.com'). If the platform is not in this list, search broadly for its official documentation pages.

Ingest long-form text and structurally decompose it to fit that platform, adapting the tone as requested and ensuring the output is formatted correctly. If the draft exceeds the limits, use the validation tool to compress the text until it is compliant. Include relevant hashtags."""

# 3. Define the Root Agent
root_agent = Agent(
    name="content_conductor",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=system_instruction,
    tools=[google_search, verify_platform_constraints],
)

# 4. Declare the Core App Loop
app = App(
    root_agent=root_agent,
    name="app",
)
