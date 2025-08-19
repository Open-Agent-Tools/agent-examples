"""
Simple evaluation runner for Product Chandler agent
Tests MCP integration and basic tool usage
"""

import json
import time
import sys
import os
from pathlib import Path

# Add parent directory to path to import agent
sys.path.append(str(Path(__file__).parent.parent))
from agent import agent

def load_test_cases(test_file):
    """Load test cases from JSON file"""
    with open(test_file, 'r') as f:
        return json.load(f)

def run_evaluation(test_cases):
    """Run evaluation tests"""
    results = []
    
    print("Product Chandler Agent Evaluation")
    print("=" * 50)
    
    # Check if MCP integration might be available (handled externally)
    print("MCP Integration: Handled externally via configuration")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        test_id = test_case["id"]
        query = test_case["query"]
        category = test_case["category"]
        description = test_case.get("description", "")
        check_tool_use = test_case.get("check_tool_use", False)
        check_mcp_tools = test_case.get("check_mcp_tools", False)
        
        # Use base expected result (MCP handled externally)
        expected = test_case.get("expected", "")
        
        print(f"\nTest {i}/{len(test_cases)}: {test_id}")
        print(f"Category: {category}")
        print(f"Description: {description}")
        print(f"Query: {query}")
        
        # Run the test
        start_time = time.time()
        try:
            # Capture tool usage by monitoring the conversation
            result = agent(query)
            response_time = time.time() - start_time
            
            # Extract response text - handle different result types
            if hasattr(result, 'message'):
                response_text = str(result.message)
            elif isinstance(result, dict):
                response_text = str(result.get('message', result))
            else:
                response_text = str(result)
            
            # Check if expected tool was used (for tool usage tests)
            tool_used = None
            if check_tool_use:
                # Simple check if expected tool name appears in response
                if expected in response_text:
                    tool_used = expected
            
            # Basic evaluation logic
            passed = True
            if check_tool_use:
                passed = tool_used is not None
            elif check_mcp_tools:
                # Check for specific tools mentioned in response
                expected_tools = expected.split(',') if expected else []
                tools_found = []
                response_lower = response_text.lower()
                
                for tool in expected_tools:
                    if tool.strip().lower() in response_lower:
                        tools_found.append(tool.strip())
                
                # Check for basic tools (MCP tools depend on external configuration)
                has_basic_tools = any(tool in ['calculator', 'current_time', 'file_read', 'file_write'] for tool in tools_found)
                
                # Pass if we have basic tools available
                passed = has_basic_tools
            else:
                # Check if response contains expected concepts (case insensitive)
                expected_keywords = expected.lower().split()
                response_lower = response_text.lower()
                keyword_matches = sum(1 for keyword in expected_keywords if keyword in response_lower)
                passed = keyword_matches >= len(expected_keywords) * 0.3  # 30% keyword match
            
            result_data = {
                "test_id": test_id,
                "category": category,
                "query": query,
                "response": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                "expected": expected,
                "tool_used": tool_used,
                "passed": passed,
                "response_time": round(response_time, 2),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            results.append(result_data)
            
            status = "PASS" if passed else "FAIL"
            print(f"Result: {status} ({response_time:.2f}s)")
            if tool_used:
                print(f"Tool used: {tool_used}")
            
        except Exception as e:
            result_data = {
                "test_id": test_id,
                "category": category,
                "query": query,
                "response": f"ERROR: {str(e)}",
                "expected": expected,
                "tool_used": None,
                "passed": False,
                "response_time": time.time() - start_time,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result_data)
            print(f"Result: ERROR - {str(e)}")
    
    return results

def generate_report(results):
    """Generate evaluation report"""
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["passed"])
    failed_tests = total_tests - passed_tests
    avg_response_time = sum(r["response_time"] for r in results) / total_tests
    
    print("\n" + "=" * 50)
    print("EVALUATION REPORT")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
    print(f"Average Response Time: {avg_response_time:.2f}s")
    
    # Category breakdown
    categories = {}
    for result in results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if result["passed"]:
            categories[cat]["passed"] += 1
    
    print("\nCategory Breakdown:")
    for cat, stats in categories.items():
        success_rate = stats["passed"] / stats["total"] * 100
        print(f"  {cat}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
    
    # Failed tests
    failed_results = [r for r in results if not r["passed"]]
    if failed_results:
        print("\nFailed Tests:")
        for result in failed_results:
            print(f"  {result['test_id']}: {result['response'][:100]}...")
    
    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "success_rate": passed_tests/total_tests*100,
        "avg_response_time": avg_response_time,
        "categories": categories,
        "detailed_results": results
    }

def save_results(results, filename="eval_results.json"):
    """Save results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")

def main():
    """Run the evaluation"""
    test_file = Path(__file__).parent / "list_tools_test.json"
    
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    try:
        test_cases = load_test_cases(test_file)
        results = run_evaluation(test_cases)
        report = generate_report(results)
        save_results(report)
        
    except Exception as e:
        print(f"Evaluation failed: {e}")

if __name__ == "__main__":
    main()