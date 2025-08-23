"""Product Pete: A Product Manager AI assistant built with Strands Agents"""

import os
from pathlib import Path
from strands_tools import calculator, current_time, file_read, file_write  # type: ignore
from prompts import SYSTEM_PROMPT  # type: ignore

# Load environment variables
try:
    from dotenv import load_dotenv
    for i in range(4):
        env_path = Path(__file__).parents[i] / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from utilities import (AgentChatInterface, SessionTracker, setup_agent_logging, 
                          create_strands_agent, add_mcp_tools, call_agent_with_context,
                          suppress_output_during_execution, BRIGHT_MAGENTA, BRIGHT_CYAN, 
                          CYAN, YELLOW, GREEN, BOLD, RESET)
    
    class ProductPeteChatInterface(AgentChatInterface):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.session = None
            self.logger = None
            
        def initialize_agent(self) -> bool:
            """Initialize Product Pete with utilities."""
            print(f"Initializing {self.agent_name}...")
            
            try:
                @suppress_output_during_execution
                def create_components():
                    logger = setup_agent_logging("Product Pete")
                    
                    # Basic tools
                    tools = [calculator, current_time, file_read, file_write]
                    
                    # Add MCP tools (Atlassian)
                    tools = add_mcp_tools(tools, "http://localhost:9000/mcp/", logger)
                    
                    # Model config
                    model_config = {
                        "model_id": "claude-3-5-sonnet-20241022",
                        "max_tokens": 4096,
                        "temperature": 0.3
                    }
                    
                    # Create agent
                    agent = create_strands_agent(model_config, tools, SYSTEM_PROMPT, logger)
                    session = SessionTracker("Product Pete")
                    
                    return agent, session, logger
                
                self.agent, self.session, self.logger = create_components()
                
                print(f"{self.agent_name} is ready!")
                print("Ask me any product management question or type 'help' for examples.")
                print("=" * 60)
                print(f"Logs: {Path(__file__).parents[2] / '.logs' / 'product_pete_chat.log'}")
                
                return True
                
            except Exception as e:
                print(f"Failed to initialize {self.agent_name}: {e}")
                return False
        
        async def process_query(self, user_input: str) -> bool:
            """Process user queries with special commands."""
            if user_input.lower() in ["exit", "quit", "bye"]:
                return False
            elif user_input.lower() == "help":
                self._show_help()
                return True
            elif user_input.lower() == "stats":
                self._show_stats()
                return True
            elif user_input.lower() == "context":
                self._show_context()
                return True
            elif not user_input:
                return True
            
            # Process query using utility function
            print(f"{self.agent_name}: Processing your request...")
            
            result = call_agent_with_context(self.agent, user_input, self.session, self.logger)
            
            if not result.get('success', False):
                print(f"{self.agent_name}: {result.get('response', 'Query failed')}")
            
            return True
        
        def _show_help(self):
            """Show help information."""
            print(f"\n{BRIGHT_MAGENTA}{BOLD}Product Pete Help{RESET}")
            print(f"\n{BRIGHT_CYAN}Core Capabilities:{RESET}")
            print(f"  {GREEN}• User Stories{RESET} - Create and refine user stories")
            print(f"  {GREEN}• Product Planning{RESET} - Roadmaps and feature prioritization") 
            print(f"  {GREEN}• Requirements{RESET} - Analysis and gap identification")
            print(f"  {GREEN}• Communication{RESET} - Stakeholder updates and reports")
            print(f"  {GREEN}• Agile/Scrum{RESET} - Sprint planning and backlog management")
            print(f"\n{BRIGHT_CYAN}Commands:{RESET}")
            for cmd, desc in [("stats", "Session statistics"), ("context", "Recent conversation"), 
                             ("help", "This help"), ("exit", "End session")]:
                print(f"  {YELLOW}{cmd}{RESET} - {desc}")
        
        def _show_stats(self):
            """Show session statistics."""
            stats = self.session.get_stats()
            print(f"\n{BRIGHT_CYAN}Session Stats:{RESET}")
            for key, value in stats.items():
                if key != "session_id":
                    print(f"  {key.title()}: {value}")
        
        def _show_context(self):
            """Show conversation context."""
            context = self.session.get_context()
            print(f"\n{BRIGHT_CYAN}Context:{RESET}")
            print(context if context else f"{CYAN}No context yet{RESET}")
        
        async def _cleanup(self):
            """Cleanup with session summary."""
            if self.session:
                stats = self.session.get_stats()
                print(f"\nSession complete: {stats['queries']} queries")
    
    def main():
        """Main entry point."""
        capabilities = [
            "User Story Creation and refinement",
            "Product Planning and roadmap assistance", 
            "Requirements Analysis and gap identification",
            "Stakeholder Communication and updates",
            "Agile/Scrum Support and sprint planning"
        ]
        
        examples = [
            "Create a user story for authentication",
            "Help me prioritize Q2 features",
            "Review requirements for gaps",
            "stats (session statistics)",
            "context (conversation context)"
        ]
        
        required_env_vars = {"ANTHROPIC_API_KEY": "AI model access"}
        
        chat_interface = ProductPeteChatInterface(
            agent_name="Product Pete",
            agent_factory=lambda: None,
            capabilities=capabilities,
            examples=examples,
            required_env_vars=required_env_vars
        )
        
        import asyncio
        asyncio.run(chat_interface.run())
    
    main()