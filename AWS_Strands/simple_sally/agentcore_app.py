"""
AgentCore App for Simple Sally

Bedrock AgentCore deployment using Strands framework.
"""

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from agent import create_agent

app = BedrockAgentCoreApp()

# Initialize the Simple Sally agent
sally = create_agent()

@app.entrypoint
def agent_invocation(payload, context):
    """
    Main entrypoint for Bedrock AgentCore.

    Args:
        payload: Dict containing 'prompt' key with user message
        context: Execution context from Bedrock AgentCore

    Returns:
        Dict with 'result' key containing agent response
    """
    try:
        # Extract user prompt from payload
        user_message = payload.get("prompt", "")

        # Use the Strands agent to process the message
        response = sally(user_message)

        # Return in expected format
        return {"result": response}

    except Exception as e:
        # Handle errors gracefully
        return {"result": f"I apologize, but I encountered an error: {str(e)}"}

if __name__ == "__main__":
    app.run()