"""
Test suite for Quick Research Quinten Agent

Tests the agent's ability to:
- Conduct rapid research
- Perform quick comparisons
- Fact check claims
- Analyze trends
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from agent import QuickResearchQuinten


async def test_quick_research():
    """Test basic quick research functionality."""
    print("\n🧪 Testing Quick Research...")
    quinten = QuickResearchQuinten()
    
    try:
        result = await quinten.quick_research("Python type hints best practices", max_sources=3)
        assert result, "Quick research should return results"
        assert len(result) > 100, "Research should provide substantial content"
        print("✅ Quick research test passed")
        return True
    except Exception as e:
        print(f"❌ Quick research test failed: {e}")
        return False
    finally:
        quinten.cleanup()


async def test_comparison():
    """Test comparison functionality."""
    print("\n🧪 Testing Comparison...")
    quinten = QuickResearchQuinten()
    
    try:
        result = await quinten.compare_options(
            ["REST API", "GraphQL"],
            ["performance", "complexity", "use cases"]
        )
        assert result, "Comparison should return results"
        assert "REST" in result or "GraphQL" in result, "Should mention compared options"
        print("✅ Comparison test passed")
        return True
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        return False
    finally:
        quinten.cleanup()


async def test_fact_check():
    """Test fact checking functionality."""
    print("\n🧪 Testing Fact Check...")
    quinten = QuickResearchQuinten()
    
    try:
        result = await quinten.fact_check("Python was created by Guido van Rossum")
        assert result, "Fact check should return results"
        assert any(word in result.upper() for word in ["TRUE", "CORRECT", "ACCURATE", "YES"]), \
            "Should verify this true fact"
        print("✅ Fact check test passed")
        return True
    except Exception as e:
        print(f"❌ Fact check test failed: {e}")
        return False
    finally:
        quinten.cleanup()


async def test_trend_analysis():
    """Test trend analysis functionality."""
    print("\n🧪 Testing Trend Analysis...")
    quinten = QuickResearchQuinten()
    
    try:
        result = await quinten.trend_analysis("serverless computing")
        assert result, "Trend analysis should return results"
        assert any(word in result.lower() for word in ["trend", "current", "recent", "development"]), \
            "Should discuss trends"
        print("✅ Trend analysis test passed")
        return True
    except Exception as e:
        print(f"❌ Trend analysis test failed: {e}")
        return False
    finally:
        quinten.cleanup()


async def test_session_tracking():
    """Test session tracking functionality."""
    print("\n🧪 Testing Session Tracking...")
    quinten = QuickResearchQuinten()
    
    try:
        # Should have no session initially
        status = quinten.get_session_status()
        assert status is None, "Should have no session initially"
        
        # Run a query to create session
        await quinten.quick_research("test query")
        
        # Should have session now
        status = quinten.get_session_status()
        assert status is not None, "Should have session after research"
        assert status["query"] == "test query", "Should track query"
        assert status["status"] == "completed", "Should be completed"
        
        print("✅ Session tracking test passed")
        return True
    except Exception as e:
        print(f"❌ Session tracking test failed: {e}")
        return False
    finally:
        quinten.cleanup()


async def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Quick Research Quinten - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Quick Research", test_quick_research),
        ("Comparison", test_comparison),
        ("Fact Check", test_fact_check),
        ("Trend Analysis", test_trend_analysis),
        ("Session Tracking", test_session_tracking),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = await test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, passed_test in results:
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{name:20} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    # Check for required environment variables
    import os
    
    required_vars = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("⚠️ Warning: Missing environment variables (some tests may fail):")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nAt least one API key is required for testing.")
    
    # Run tests
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)