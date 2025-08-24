"""
Example usage of Quick Research Quinten Agent

This script demonstrates various quick research capabilities including:
- Rapid information gathering
- Quick comparisons
- Fact checking
- Trend analysis
"""

import asyncio
import json
from agent import QuickResearchQuinten


async def main():
    """Run example research queries."""
    
    # Initialize the agent
    quinten = QuickResearchQuinten()
    
    print("=" * 80)
    print("Quick Research Quinten - Example Usage")
    print("=" * 80)
    
    # Example 1: Quick Research
    print("\n📚 Example 1: Quick Research on a Technical Topic")
    print("-" * 40)
    result = await quinten.quick_research("What are the main features of Python 3.13?")
    print(result)
    
    # Example 2: Comparison
    print("\n⚖️ Example 2: Quick Comparison")
    print("-" * 40)
    result = await quinten.compare_options(
        ["FastAPI", "Flask", "Django"],
        ["performance", "learning curve", "features", "use cases"]
    )
    print(result)
    
    # Example 3: Fact Checking
    print("\n✅ Example 3: Fact Checking")
    print("-" * 40)
    result = await quinten.fact_check("Python is the most popular programming language in 2025")
    print(result)
    
    # Example 4: Trend Analysis
    print("\n📈 Example 4: Trend Analysis")
    print("-" * 40)
    result = await quinten.trend_analysis("AI agent frameworks")
    print(result)
    
    # Example 5: Session Status
    print("\n📊 Example 5: Session Status")
    print("-" * 40)
    status = quinten.get_session_status()
    if status:
        print(f"Last research session summary:")
        print(json.dumps(status, indent=2))
    else:
        print("No active session")
    
    # Cleanup
    quinten.cleanup()
    print("\n✅ Agent cleanup completed")


async def interactive_mode():
    """Run the agent in interactive mode."""
    
    quinten = QuickResearchQuinten()
    
    print("=" * 80)
    print("Quick Research Quinten - Interactive Mode")
    print("=" * 80)
    print("\nAvailable commands:")
    print("  - Type any research query")
    print("  - 'compare X vs Y' - Quick comparison")
    print("  - 'fact check: [claim]' - Verify a claim")
    print("  - 'trends: [topic]' - Analyze current trends")
    print("  - 'status' - Show session status")
    print("  - 'quit' or 'exit' - Exit the program")
    print("-" * 80)
    
    while True:
        try:
            query = input("\n🔍 Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            # Process the query
            query_lower = query.lower()
            
            if query_lower == 'status':
                status = quinten.get_session_status()
                if status:
                    print(f"\n📊 Session Status:")
                    print(json.dumps(status, indent=2))
                else:
                    print("No active session")
                    
            elif 'compare' in query_lower and ('vs' in query_lower or 'versus' in query_lower):
                # Extract options for comparison
                import re
                pattern = r'compare\s+(.*?)\s+(?:vs|versus)\s+(.*?)(?:\s+for\s+(.*))?$'
                match = re.search(pattern, query_lower)
                if match:
                    options = [match.group(1).strip(), match.group(2).strip()]
                    criteria = None
                    if match.group(3):
                        criteria = [c.strip() for c in match.group(3).split(',')]
                    print("\n⚖️ Conducting comparison...")
                    result = await quinten.compare_options(options, criteria)
                    print(result)
                else:
                    print("❌ Could not parse comparison. Use format: 'compare X vs Y'")
                    
            elif query_lower.startswith('fact check:') or query_lower.startswith('verify:'):
                if query_lower.startswith('fact check:'):
                    claim = query[11:].strip()
                else:
                    claim = query[7:].strip()
                print("\n✅ Fact checking...")
                result = await quinten.fact_check(claim)
                print(result)
                
            elif query_lower.startswith('trends:'):
                topic = query[7:].strip()
                print("\n📈 Analyzing trends...")
                result = await quinten.trend_analysis(topic)
                print(result)
                
            else:
                # Default to quick research
                print("\n🔍 Researching...")
                result = await quinten.quick_research(query)
                print(result)
                
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Cleanup
    quinten.cleanup()
    print("\n✅ Agent cleanup completed")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # Run in interactive mode
        asyncio.run(interactive_mode())
    else:
        # Run examples
        asyncio.run(main())