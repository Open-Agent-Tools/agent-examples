"""
Agent Health Check System for Complex Coding Clara

Tests all 14 specialist agents with simple tasks to verify they respond correctly.
Provides health monitoring and success rate tracking.
"""

import time
from typing import Dict, List, Tuple
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class AgentHealthMonitor:
    """Monitor and test agent health across the system."""

    def __init__(self):
        self.results: Dict[str, Dict] = {}
        self.agent_tools = {}

    def load_agents(self) -> bool:
        """
        Load all agent tools.

        Returns:
            True if agents loaded successfully, False otherwise
        """
        try:
            from agents import (
                architect,
                senior_coder,
                fast_coder,
                test_engineer,
                code_reviewer,
                debug,
                documentation,
                python_specialist,
                web_specialist,
                database_specialist,
                devops_specialist,
                data_science_specialist,
                agile_specialist,
                doc_research_specialist,
            )

            self.agent_tools = {
                "architect": architect,
                "senior_coder": senior_coder,
                "fast_coder": fast_coder,
                "test_engineer": test_engineer,
                "code_reviewer": code_reviewer,
                "debug": debug,
                "documentation": documentation,
                "python_specialist": python_specialist,
                "web_specialist": web_specialist,
                "database_specialist": database_specialist,
                "devops_specialist": devops_specialist,
                "data_science_specialist": data_science_specialist,
                "agile_specialist": agile_specialist,
                "doc_research_specialist": doc_research_specialist,
            }
            return True
        except Exception as e:
            print(f"❌ Error loading agents: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_agent(self, agent_name: str, agent_tool, test_task: str) -> Tuple[bool, str, float]:
        """
        Test a single agent with a simple task.

        Args:
            agent_name: Name of the agent
            agent_tool: The agent tool function
            test_task: Simple test task for the agent

        Returns:
            Tuple of (success: bool, response: str, duration: float)
        """
        start_time = time.time()

        try:
            response = agent_tool(test_task)
            duration = time.time() - start_time

            # Check if response indicates an error
            response_str = str(response)
            is_error = (
                "error" in response_str.lower()
                and ("configuration error" in response_str.lower()
                     or "validation" in response_str.lower()
                     or "failed" in response_str.lower())
            )

            success = not is_error and len(response_str) > 10

            return success, response_str, duration

        except Exception as e:
            duration = time.time() - start_time
            return False, f"Exception: {str(e)}", duration

    def run_health_check(self, verbose: bool = True) -> Dict[str, Dict]:
        """
        Run health checks on all agents.

        Args:
            verbose: Print detailed output during testing

        Returns:
            Dictionary containing test results for each agent
        """
        if not self.agent_tools:
            print("Loading agents...")
            if not self.load_agents():
                return {}

        # Define simple test tasks for each agent
        test_tasks = {
            "architect": "Describe in 2 sentences what system architecture planning involves.",
            "senior_coder": "Write a simple Python function that adds two numbers.",
            "fast_coder": "Create a basic Python function that returns 'Hello World'.",
            "test_engineer": "Write a simple unit test for a function that adds two numbers.",
            "code_reviewer": "Review this code: def add(a,b): return a+b",
            "debug": "Explain how to debug a Python ImportError.",
            "documentation": "Write a one-line docstring for a function that adds two numbers.",
            "python_specialist": "What is a Python list comprehension? One sentence.",
            "web_specialist": "What is React? One sentence.",
            "database_specialist": "What is SQL? One sentence.",
            "devops_specialist": "What is Docker? One sentence.",
            "data_science_specialist": "What is pandas? One sentence.",
            "agile_specialist": "What is a user story? One sentence.",
            "doc_research_specialist": "Explain what technical documentation is. One sentence.",
        }

        if verbose:
            print("=" * 70)
            print("Agent Health Check - Complex Coding Clara")
            print("=" * 70)
            print()

        for agent_name, agent_tool in self.agent_tools.items():
            test_task = test_tasks.get(
                agent_name, "Respond with a brief greeting and your role."
            )

            if verbose:
                print(f"Testing {agent_name}...", end=" ", flush=True)

            success, response, duration = self.test_agent(agent_name, agent_tool, test_task)

            self.results[agent_name] = {
                "success": success,
                "response": response,
                "duration": duration,
                "test_task": test_task,
            }

            if verbose:
                status = "✅" if success else "❌"
                print(f"{status} ({duration:.2f}s)")
                if not success:
                    # Print first 200 chars of error
                    error_preview = response[:200] + ("..." if len(response) > 200 else "")
                    print(f"   Error: {error_preview}")

        return self.results

    def print_summary(self):
        """Print a summary of health check results."""
        if not self.results:
            print("No results to display. Run health check first.")
            return

        print()
        print("=" * 70)
        print("Health Check Summary")
        print("=" * 70)
        print()

        successful = [name for name, result in self.results.items() if result["success"]]
        failed = [name for name, result in self.results.items() if not result["success"]]

        total = len(self.results)
        success_count = len(successful)
        success_rate = (success_count / total * 100) if total > 0 else 0

        print(f"Total Agents: {total}")
        print(f"Successful: {success_count} ({success_rate:.1f}%)")
        print(f"Failed: {len(failed)}")
        print()

        if successful:
            print("✅ Working Agents:")
            for name in sorted(successful):
                duration = self.results[name]["duration"]
                print(f"   • {name} ({duration:.2f}s)")
            print()

        if failed:
            print("❌ Failed Agents:")
            for name in sorted(failed):
                duration = self.results[name]["duration"]
                print(f"   • {name} ({duration:.2f}s)")
                error_msg = self.results[name]["response"]
                # Print first line of error
                first_line = error_msg.split("\n")[0][:100]
                print(f"     Error: {first_line}...")
            print()

        # Print timing statistics
        durations = [r["duration"] for r in self.results.values() if r["success"]]
        if durations:
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)

            print("⏱️  Performance Metrics (successful agents):")
            print(f"   Average: {avg_duration:.2f}s")
            print(f"   Fastest: {min_duration:.2f}s")
            print(f"   Slowest: {max_duration:.2f}s")
            print()

        print("=" * 70)

    def generate_report(self, output_file: str = "health_check_report.md"):
        """
        Generate a detailed markdown report of health check results.

        Args:
            output_file: Path to output markdown file
        """
        if not self.results:
            print("No results to generate report. Run health check first.")
            return

        report_lines = [
            "# Agent Health Check Report",
            "",
            f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
        ]

        total = len(self.results)
        success_count = sum(1 for r in self.results.values() if r["success"])
        success_rate = (success_count / total * 100) if total > 0 else 0

        report_lines.extend([
            f"- **Total Agents:** {total}",
            f"- **Successful:** {success_count} ({success_rate:.1f}%)",
            f"- **Failed:** {total - success_count}",
            "",
            "## Detailed Results",
            "",
        ])

        for agent_name in sorted(self.results.keys()):
            result = self.results[agent_name]
            status = "✅ PASS" if result["success"] else "❌ FAIL"

            report_lines.extend([
                f"### {agent_name}",
                "",
                f"**Status:** {status}",
                f"**Duration:** {result['duration']:.2f}s",
                f"**Test Task:** {result['test_task']}",
                "",
            ])

            if result["success"]:
                response_preview = result["response"][:300]
                report_lines.extend([
                    "**Response Preview:**",
                    "```",
                    response_preview + ("..." if len(result["response"]) > 300 else ""),
                    "```",
                    "",
                ])
            else:
                report_lines.extend([
                    "**Error:**",
                    "```",
                    result["response"],
                    "```",
                    "",
                ])

        report_content = "\n".join(report_lines)

        with open(output_file, "w") as f:
            f.write(report_content)

        print(f"📄 Report generated: {output_file}")


def main():
    """Main function to run health checks."""
    monitor = AgentHealthMonitor()

    print("Starting agent health check...")
    print()

    results = monitor.run_health_check(verbose=True)

    if results:
        monitor.print_summary()
        monitor.generate_report()
    else:
        print("❌ Failed to run health checks")
        return 1

    # Return exit code based on success rate
    success_count = sum(1 for r in results.values() if r["success"])
    total = len(results)

    if success_count == total:
        print("✅ All agents passed!")
        return 0
    elif success_count > 0:
        print(f"⚠️  {total - success_count} agent(s) failed")
        return 1
    else:
        print("❌ All agents failed!")
        return 1


if __name__ == "__main__":
    exit(main())
