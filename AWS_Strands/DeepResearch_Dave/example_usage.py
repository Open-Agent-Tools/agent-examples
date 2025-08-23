"""
Example usage of Deep Research Dave agent.

This file demonstrates various ways to use the Deep Research Dave agent
for different types of research tasks.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from agent import DeepResearchDave

# Load .env file from root directory
try:
    from dotenv import load_dotenv

    for i in range(4):
        env_path = Path(__file__).parents[i] / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded environment from: {env_path}")
            break
except ImportError:
    pass

# Set up logging for examples
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def example_quick_research():
    """Example: Quick research for immediate insights."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Quick Research")
    print("="*60)
    
    dave = DeepResearchDave()
    
    # Quick research on a trending topic
    query = "Latest trends in AI agent frameworks and tools 2025"
    print(f"Research Query: {query}")
    print("\nConducting quick research...")
    
    try:
        result = await dave.quick_research(query, max_sources=5)
        print("\n--- Quick Research Results ---")
        print(result)
        
    except Exception as e:
        print(f"Error in quick research: {str(e)}")

async def example_comparative_analysis():
    """Example: Comparative analysis between options."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Comparative Analysis")
    print("="*60)
    
    dave = DeepResearchDave()
    
    # Compare different AI agent frameworks
    options = ["AWS Strands", "LangChain", "Crew AI", "Google ADK"]
    criteria = ["ease of use", "documentation quality", "community support", "feature set", "cost"]
    
    print(f"Comparing: {', '.join(options)}")
    print(f"Criteria: {', '.join(criteria)}")
    print("\nConducting comparative analysis...")
    
    try:
        result = await dave.compare_options(options, criteria)
        print("\n--- Comparative Analysis Results ---")
        print(result)
        
    except Exception as e:
        print(f"Error in comparative analysis: {str(e)}")

async def example_comprehensive_research_session():
    """Example: Full research session with multiple phases."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Comprehensive Research Session")
    print("="*60)
    
    dave = DeepResearchDave()
    
    topic = "Best practices for implementing RAG (Retrieval-Augmented Generation) systems"
    research_type = "comprehensive"
    
    print(f"Research Topic: {topic}")
    print(f"Research Type: {research_type}")
    print("\nStarting comprehensive research session...")
    
    try:
        # Phase 1: Planning
        print("\n--- Phase 1: Research Planning ---")
        planning = await dave.start_research_session(topic, research_type)
        print(planning)
        
        # Check session status
        status = dave.get_session_status()
        print(f"\nSession Status: {status['current_phase']} - {status['status']}")
        
        # Phase 2: Information Gathering
        print("\n--- Phase 2: Information Gathering ---")
        phase_instructions = """
        Focus on gathering information about:
        1. RAG architecture patterns and components
        2. Vector database selection and optimization
        3. Embedding models and chunking strategies
        4. Retrieval algorithms and ranking methods
        5. Performance optimization and scaling considerations
        6. Common challenges and solutions
        7. Real-world implementation case studies
        """
        
        findings = await dave.conduct_research_phase(phase_instructions)
        print(findings)
        
        # Phase 3: Analysis & Synthesis
        print("\n--- Phase 3: Analysis & Synthesis ---")
        focus_areas = [
            "architecture patterns",
            "performance optimization", 
            "implementation challenges",
            "best practices"
        ]
        
        analysis = await dave.synthesize_findings(focus_areas)
        print(analysis)
        
        # Phase 4: Final Report
        print("\n--- Phase 4: Research Report Generation ---")
        report = await dave.generate_research_report("comprehensive")
        print(report)
        
        # Final session status
        final_status = dave.get_session_status()
        print(f"\n--- Final Session Summary ---")
        print(f"Topic: {final_status['topic']}")
        print(f"Duration: {final_status['duration_minutes']:.1f} minutes")
        print(f"Sources: {final_status['sources_count']}")
        print(f"Categories: {final_status['findings_categories']}")
        print(f"Insights: {final_status['insights_count']}")
        print(f"Confidence: {final_status['confidence_level']}")
        print(f"Status: {final_status['status']}")
        
    except Exception as e:
        print(f"Error in comprehensive research: {str(e)}")

async def example_technical_research():
    """Example: Technical research focused on specific technologies."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Technical Research")
    print("="*60)
    
    dave = DeepResearchDave()
    
    # Technical deep dive on a specific framework
    query = """
    Analyze the AWS Strands agent framework in detail:
    
    1. Architecture and design patterns
    2. Key components and their interactions  
    3. Integration capabilities with MCP tools
    4. Performance characteristics and limitations
    5. Comparison with similar frameworks
    6. Best use cases and implementation scenarios
    7. Documentation quality and community support
    """
    
    print("Technical Research Query:")
    print(query)
    print("\nConducting technical research...")
    
    try:
        result = await dave.quick_research(query, max_sources=8)
        print("\n--- Technical Research Results ---")
        print(result)
        
    except Exception as e:
        print(f"Error in technical research: {str(e)}")

async def example_market_research():
    """Example: Market research and trend analysis."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Market Research")
    print("="*60)
    
    dave = DeepResearchDave()
    
    # Start market research session
    topic = "AI agent market landscape and growth opportunities 2025"
    
    try:
        # Quick market overview
        market_query = """
        Research the current AI agent market including:
        
        1. Market size and growth projections
        2. Key market segments and applications
        3. Major players and competitive landscape
        4. Investment trends and funding patterns
        5. Technology adoption rates by industry
        6. Regulatory considerations and challenges
        7. Future market opportunities and threats
        """
        
        print("Market Research Query:")
        print(market_query)
        print("\nConducting market research...")
        
        result = await dave.quick_research(market_query, max_sources=10)
        print("\n--- Market Research Results ---")
        print(result)
        
    except Exception as e:
        print(f"Error in market research: {str(e)}")

async def example_multi_model_comparison():
    """Example: Using different model providers."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Multi-Model Comparison")
    print("="*60)
    
    # Test different model providers if available
    models = [
        "anthropic/claude-3-5-sonnet-20241022",
        # "openai/gpt-4",  # Uncomment if API key available
        # "google/gemini-pro",  # Uncomment if API key available
    ]
    
    query = "Compare Python web frameworks: FastAPI vs Flask vs Django"
    
    for model in models:
        print(f"\n--- Testing with {model} ---")
        
        try:
            dave = DeepResearchDave(model_provider=model)
            result = await dave.quick_research(query, max_sources=3)
            
            print(f"Model: {model}")
            print("Result length:", len(result))
            print("First 200 characters:", result[:200] + "...")
            
        except Exception as e:
            print(f"Error with {model}: {str(e)}")

async def example_error_handling():
    """Example: Demonstrating error handling and recovery."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Error Handling")
    print("="*60)
    
    dave = DeepResearchDave()
    
    # Test with invalid/challenging inputs
    test_cases = [
        "",  # Empty query
        "x" * 1000,  # Very long query
        "Research something that doesn't exist: flibbertigibbet quantum marshmallow",  # Nonsensical
        "What is 2+2?",  # Simple math (not really research)
    ]
    
    for i, query in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: {query[:50]}{'...' if len(query) > 50 else ''} ---")
        
        try:
            result = await dave.quick_research(query, max_sources=2)
            print("Success - Response length:", len(result))
            print("Preview:", result[:100] + "...")
            
        except Exception as e:
            print(f"Expected error handling: {str(e)}")

async def main():
    """Run all examples."""
    print("Deep Research Dave - Usage Examples")
    print("=" * 60)
    
    # Check for API keys and show which are available
    api_keys = {
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
    }
    
    available_keys = [name for name, key in api_keys.items() if key]
    
    if available_keys:
        print("Available API Keys:")
        for key_name in available_keys:
            key_value = api_keys[key_name]
            masked = f"{key_value[:10]}...{key_value[-5:]}" if key_value else "None"
            print(f"  {key_name}: {masked}")
        print()
    else:
        print("WARNING: No API keys found in environment.")
        print("Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY to run examples.")
        print("Examples will use mock responses for demonstration.")
        return
    
    # Run examples sequentially
    examples = [
        example_quick_research,
        example_comparative_analysis, 
        example_technical_research,
        example_market_research,
        example_multi_model_comparison,
        example_comprehensive_research_session,  # Longest, run near end
        example_error_handling,
    ]
    
    for example_func in examples:
        try:
            await example_func()
            
            # Brief pause between examples
            await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\nExamples interrupted by user.")
            break
        except Exception as e:
            print(f"\n\nUnexpected error in {example_func.__name__}: {str(e)}")
            continue
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())