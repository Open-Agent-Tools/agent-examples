"""
Evaluation tests for Deep Research Dave agent capabilities.
"""

import asyncio
import pytest
import sys
import os
from unittest.mock import patch, AsyncMock

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from AWS_Strands.DeepResearch_Dave import DeepResearchDave, ResearchSession

class TestDeepResearchDave:
    """Test suite for Deep Research Dave agent."""
    
    def setup_method(self):
        """Set up test environment."""
        self.dave = DeepResearchDave()
    
    def test_research_session_creation(self):
        """Test research session initialization."""
        session = ResearchSession("Test Topic", "comprehensive")
        
        assert session.topic == "Test Topic"
        assert session.research_type == "comprehensive"
        assert session.status == "initialized"
        assert session.current_phase == "planning"
        assert len(session.sources) == 0
        assert len(session.findings) == 0
        assert len(session.insights) == 0
    
    def test_session_source_management(self):
        """Test adding and managing sources."""
        session = ResearchSession("Test Topic")
        
        source = {
            "url": "https://example.edu/research",
            "title": "Academic Research Paper",
            "description": "Test academic source"
        }
        
        session.add_source(source)
        
        assert len(session.sources) == 1
        assert session.sources[0]["url"] == source["url"]
        assert session.sources[0]["credibility"] == "high"  # .edu domain
        assert "added_at" in session.sources[0]
    
    def test_session_findings_management(self):
        """Test adding and organizing findings."""
        session = ResearchSession("Test Topic")
        
        finding = {
            "key_point": "Important finding",
            "evidence": "Supporting evidence",
            "confidence": "high"
        }
        
        session.add_finding("technical", finding)
        
        assert "technical" in session.findings
        assert len(session.findings["technical"]) == 1
        assert session.findings["technical"][0]["key_point"] == "Important finding"
        assert "discovered_at" in session.findings["technical"][0]
    
    def test_session_insights_tracking(self):
        """Test insight generation and tracking."""
        session = ResearchSession("Test Topic")
        
        insight = "Key insight from research"
        evidence = ["source1", "source2"]
        
        session.add_insight(insight, evidence)
        
        assert len(session.insights) == 1
        assert session.insights[0]["insight"] == insight
        assert session.insights[0]["evidence"] == evidence
        assert "generated_at" in session.insights[0]
    
    def test_credibility_assessment(self):
        """Test source credibility assessment logic."""
        session = ResearchSession("Test Topic")
        
        # High credibility sources
        high_sources = [
            {"url": "https://research.example.edu", "title": "Academic paper"},
            {"url": "https://data.gov", "title": "Government data"},
            {"url": "https://arxiv.org/paper", "title": "ArXiv preprint"},
            {"url": "https://example.com", "title": "Official Documentation"}
        ]
        
        for source in high_sources:
            session.add_source(source)
            assert session.sources[-1]["credibility"] == "high"
        
        # Medium credibility sources
        medium_sources = [
            {"url": "https://stackoverflow.com/questions", "title": "SO answer"},
            {"url": "https://github.com/repo", "title": "GitHub repository"},
            {"url": "https://medium.com/article", "title": "Medium article"}
        ]
        
        for source in medium_sources:
            session.add_source(source)
            assert session.sources[-1]["credibility"] == "medium"
        
        # Sources needing verification
        unknown_source = {"url": "https://random-blog.com", "title": "Blog post"}
        session.add_source(unknown_source)
        assert session.sources[-1]["credibility"] == "needs_verification"
    
    def test_session_summary(self):
        """Test session summary generation."""
        session = ResearchSession("Test Topic", "quick")
        
        # Add some data
        session.add_source({"url": "https://example.com", "title": "Test"})
        session.add_finding("category1", {"finding": "test"})
        session.add_insight("test insight")
        session.update_phase("analysis")
        session.update_confidence("high")
        
        summary = session.get_summary()
        
        assert summary["topic"] == "Test Topic"
        assert summary["research_type"] == "quick"
        assert summary["sources_count"] == 1
        assert summary["findings_categories"] == 1
        assert summary["insights_count"] == 1
        assert summary["current_phase"] == "analysis"
        assert summary["confidence_level"] == "high"
        assert "duration_minutes" in summary
    
    def test_agent_initialization(self):
        """Test agent creation and configuration."""
        # Test default initialization
        dave = DeepResearchDave()
        assert dave.model_provider == "anthropic/claude-3-5-sonnet-20241022"
        assert dave.agent is None
        assert dave.current_session is None
        
        # Test custom model provider
        dave_custom = DeepResearchDave(model_provider="openai/gpt-4")
        assert dave_custom.model_provider == "openai/gpt-4"
    
    @patch('strands.agents.Agent')
    def test_agent_creation(self, mock_agent_class):
        """Test agent creation with mocked dependencies."""
        mock_agent = AsyncMock()
        mock_agent_class.return_value = mock_agent
        
        dave = DeepResearchDave()
        agent = dave.create_agent()
        
        # Verify agent was created with correct parameters
        mock_agent_class.assert_called_once()
        call_args = mock_agent_class.call_args
        
        assert call_args[1]['name'] == 'DeepResearchDave'
        assert call_args[1]['model_provider'] == dave.model_provider
        assert call_args[1]['temperature'] == 0.1
        assert len(call_args[1]['tools']) >= 3  # web_search, context7, atlassian
        
        assert agent == mock_agent
    
    @pytest.mark.asyncio
    async def test_research_session_flow(self):
        """Test complete research session workflow."""
        with patch.object(self.dave, 'robust_agent_call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Mocked agent response"
            
            # Start research session
            response = await self.dave.start_research_session("Test Topic", "comprehensive")
            
            assert self.dave.current_session is not None
            assert self.dave.current_session.topic == "Test Topic"
            assert self.dave.current_session.research_type == "comprehensive"
            assert self.dave.current_session.status == "active"
            assert self.dave.current_session.current_phase == "planning"
            assert response == "Mocked agent response"
            
            # Conduct research phase
            phase_response = await self.dave.conduct_research_phase("Test instructions")
            assert self.dave.current_session.current_phase == "information_gathering"
            assert phase_response == "Mocked agent response"
            
            # Synthesize findings
            synthesis_response = await self.dave.synthesize_findings(["test", "analysis"])
            assert self.dave.current_session.current_phase == "analysis_synthesis"
            assert synthesis_response == "Mocked agent response"
            
            # Generate report
            report_response = await self.dave.generate_research_report("comprehensive")
            assert self.dave.current_session.current_phase == "documentation"
            assert self.dave.current_session.status == "completed"
            assert report_response == "Mocked agent response"
    
    @pytest.mark.asyncio
    async def test_quick_research(self):
        """Test quick research functionality."""
        with patch.object(self.dave, 'robust_agent_call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Quick research results"
            
            result = await self.dave.quick_research("Test query", max_sources=3)
            
            assert result == "Quick research results"
            mock_call.assert_called_once()
            
            # Verify prompt contains expected elements
            call_args = mock_call.call_args[0][0]
            assert "Test query" in call_args
            assert "3 most relevant sources" in call_args
            assert "Key Points" in call_args
    
    @pytest.mark.asyncio  
    async def test_comparative_analysis(self):
        """Test comparative analysis functionality."""
        with patch.object(self.dave, 'robust_agent_call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Comparative analysis results"
            
            options = ["Option A", "Option B", "Option C"]
            criteria = ["cost", "performance", "reliability"]
            
            result = await self.dave.compare_options(options, criteria)
            
            assert result == "Comparative analysis results"
            mock_call.assert_called_once()
            
            # Verify prompt contains expected elements
            call_args = mock_call.call_args[0][0]
            assert all(option in call_args for option in options)
            assert all(criterion in call_args for criterion in criteria)
            assert "Comparison Matrix" in call_args
            assert "Scoring Framework" in call_args
    
    @pytest.mark.asyncio
    async def test_robust_agent_call_retry_logic(self):
        """Test retry logic in robust agent calls."""
        with patch.object(self.dave, 'create_agent') as mock_create:
            mock_agent = AsyncMock()
            mock_create.return_value = mock_agent
            
            # Test successful call
            mock_agent.run.return_value = "Success response"
            result = await self.dave.robust_agent_call("test prompt")
            assert result == "Success response"
            assert mock_agent.run.call_count == 1
            
            # Test retry on failure then success
            mock_agent.run.side_effect = [Exception("First fail"), "Success after retry"]
            result = await self.dave.robust_agent_call("test prompt", max_retries=2)
            assert result == "Success after retry"
            assert mock_agent.run.call_count == 3  # 1 from previous + 2 from retry test
            
            # Test max retries exceeded
            mock_agent.run.side_effect = Exception("Persistent failure")
            with pytest.raises(Exception, match="Persistent failure"):
                await self.dave.robust_agent_call("test prompt", max_retries=2)
    
    def test_session_status_tracking(self):
        """Test session status retrieval."""
        # No session initially
        assert self.dave.get_session_status() is None
        
        # Create session and check status
        session = ResearchSession("Test", "quick")
        session.add_source({"url": "test.com", "title": "Test"})
        session.add_finding("category", {"test": "finding"})
        session.add_insight("test insight")
        
        self.dave.current_session = session
        status = self.dave.get_session_status()
        
        assert status is not None
        assert status["topic"] == "Test"
        assert status["sources_count"] == 1
        assert status["findings_categories"] == 1
        assert status["insights_count"] == 1
        assert "duration_minutes" in status

class TestResearchQuality:
    """Test suite for research quality and standards."""
    
    def test_comprehensive_research_criteria(self):
        """Test comprehensive research meets quality standards."""
        session = ResearchSession("AI Frameworks Comparison", "comprehensive")
        
        # Simulate adding diverse, high-quality sources
        sources = [
            {"url": "https://arxiv.org/framework-comparison", "title": "Academic comparison"},
            {"url": "https://framework-a-docs.com", "title": "Official documentation A"},
            {"url": "https://framework-b-docs.com", "title": "Official documentation B"},
            {"url": "https://github.com/framework-a", "title": "Framework A repository"},
            {"url": "https://stackoverflow.com/framework-questions", "title": "Community discussion"}
        ]
        
        for source in sources:
            session.add_source(source)
        
        # Check source diversity
        credibility_levels = [s["credibility"] for s in session.sources]
        assert "high" in credibility_levels
        assert "medium" in credibility_levels
        
        # Should have multiple categories of findings
        session.add_finding("performance", {"metric": "speed", "value": "high"})
        session.add_finding("usability", {"metric": "learning_curve", "value": "moderate"})
        session.add_finding("ecosystem", {"metric": "community_size", "value": "large"})
        
        assert len(session.findings) >= 3
        
        # Should have synthesized insights
        session.add_insight("Framework A excels in performance", ["source1", "source2"])
        session.add_insight("Framework B has better documentation", ["source3"])
        
        assert len(session.insights) >= 2
        
        summary = session.get_summary()
        assert summary["sources_count"] >= 5
        assert summary["findings_categories"] >= 3
        assert summary["insights_count"] >= 2

# Integration tests (require actual agent setup)
class TestIntegration:
    """Integration tests for real agent interactions."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_quick_research(self):
        """Test quick research with real agent (requires API keys)."""
        # Skip if no environment setup
        if not os.getenv('ANTHROPIC_API_KEY'):
            pytest.skip("No API key configured")
        
        dave = DeepResearchDave()
        
        try:
            result = await dave.quick_research("Python testing frameworks comparison")
            
            # Verify response structure
            assert len(result) > 100  # Should be substantial
            assert "pytest" in result.lower() or "unittest" in result.lower()
            
        except Exception as e:
            pytest.fail(f"Integration test failed: {str(e)}")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_comparative_analysis(self):
        """Test comparative analysis with real agent (requires API keys)."""
        if not os.getenv('ANTHROPIC_API_KEY'):
            pytest.skip("No API key configured")
        
        dave = DeepResearchDave()
        
        try:
            result = await dave.compare_options(
                options=["pytest", "unittest"],
                criteria=["ease of use", "features", "community"]
            )
            
            # Verify response contains comparison elements
            assert "pytest" in result and "unittest" in result
            assert "ease of use" in result.lower()
            assert "features" in result.lower()
            
        except Exception as e:
            pytest.fail(f"Integration test failed: {str(e)}")

if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"])