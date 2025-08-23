"""
Basic test to validate Deep Research Dave agent structure.
"""

import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))

def test_import_structure():
    """Test that all components can be imported."""
    try:
        from agent import DeepResearchDave, ResearchSession
        from prompts import SYSTEM_PROMPT
        print("+ All imports successful")
        return True
    except ImportError as e:
        print(f"- Import failed: {e}")
        return False

def test_research_session_basic():
    """Test basic ResearchSession functionality."""
    try:
        from agent import ResearchSession
        
        session = ResearchSession("Test Topic", "quick")
        assert session.topic == "Test Topic"
        assert session.research_type == "quick"
        assert session.status == "initialized"
        
        # Test adding source
        source = {"url": "https://example.edu", "title": "Test"}
        session.add_source(source)
        assert len(session.sources) == 1
        assert session.sources[0]["credibility"] == "high"
        
        # Test adding finding
        session.add_finding("category1", {"finding": "test finding"})
        assert "category1" in session.findings
        
        # Test adding insight
        session.add_insight("test insight", ["source1"])
        assert len(session.insights) == 1
        
        # Test summary
        summary = session.get_summary()
        assert summary["topic"] == "Test Topic"
        assert summary["sources_count"] == 1
        
        print("+ ResearchSession basic functionality works")
        return True
        
    except Exception as e:
        print(f"- ResearchSession test failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization without external dependencies."""
    try:
        from agent import DeepResearchDave
        
        # Test initialization
        dave = DeepResearchDave()
        assert dave.model_provider == "anthropic/claude-3-5-sonnet-20241022"
        assert dave.agent is None
        assert dave.current_session is None
        
        # Test custom model provider
        dave_custom = DeepResearchDave(model_provider="test/model")
        assert dave_custom.model_provider == "test/model"
        
        print("+ DeepResearchDave initialization works")
        return True
        
    except Exception as e:
        print(f"- Agent initialization test failed: {e}")
        return False

def test_prompt_structure():
    """Test that system prompt is properly structured."""
    try:
        from prompts import SYSTEM_PROMPT
        
        # Check prompt is non-empty string
        assert isinstance(SYSTEM_PROMPT, str)
        assert len(SYSTEM_PROMPT) > 100
        
        # Check for key research concepts
        key_terms = [
            "research", "analysis", "sources", "findings", 
            "methodology", "evaluation", "synthesis"
        ]
        
        prompt_lower = SYSTEM_PROMPT.lower()
        found_terms = [term for term in key_terms if term in prompt_lower]
        
        assert len(found_terms) >= 5, f"Only found {len(found_terms)} key terms: {found_terms}"
        
        print("+ System prompt structure is valid")
        return True
        
    except Exception as e:
        print(f"- Prompt structure test failed: {e}")
        return False

def main():
    """Run all basic tests."""
    print("Deep Research Dave - Basic Validation Tests")
    print("=" * 50)
    
    tests = [
        test_import_structure,
        test_research_session_basic,
        test_agent_initialization,
        test_prompt_structure,
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"- {test_func.__name__} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All basic validation tests passed!")
        return True
    else:
        print("FAILED: Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)