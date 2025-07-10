import os
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Get the Groq API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in your environment or .env file")

# Initialize the MCP client
client = MCPClient.from_config_file("browser_mcp.json") 

# Initialize the Groq LLM
llm = ChatOpenAI(model="gpt-4o-mini")

agent = MCPAgent(llm=llm, client=client, max_steps=30, memory_enabled=True)

# Function to interact with Groq using MCP
async def get_response_from_groq(prompt):
    try:
        print(prompt)
        response = await agent.run(prompt)
        return response
    except Exception as e:
        raise Exception(f"Error during agent execution: {e}")
    finally:
        response = await agent.run(prompt)
        print(response)
    