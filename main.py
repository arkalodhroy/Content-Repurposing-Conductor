import os

from dotenv import load_dotenv
from google_agents import Agent, OpenSearchTool

from content_validator import verify_platform_constraints

load_dotenv()
if os.environ.get("GOOGLE_API_KEY") == "no":
    os.environ.pop("GOOGLE_API_KEY", None)


search_tool = OpenSearchTool(
    api_key=os.getenv("SEARCH_API_KEY"), engine_id=os.getenv("SEARCH_ENGINE_ID")
)

# Define the agent clearly at the module level
agent = Agent(
    instructions_file="context.md",
    api_key=os.getenv("GEMINI_API_KEY"),
    tools=[search_tool, verify_platform_constraints],
)

if __name__ == "__main__":
    agent.run()
