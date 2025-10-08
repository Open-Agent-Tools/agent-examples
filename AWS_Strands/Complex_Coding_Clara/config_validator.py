"""
Configuration Validator for Complex Coding Clara

Validates agent configurations to prevent common misconfigurations,
particularly around model IDs and inference profiles.
"""

import re
from typing import Dict, List, Tuple


class ConfigValidator:
    """Validates agent configurations for AWS Bedrock models."""

    # Valid inference profile patterns
    VALID_INFERENCE_PROFILES = [
        r"^us\.",  # US region profiles (us.anthropic.*, us.meta.*, us.amazon.*)
        r"^eu\.",  # EU region profiles
        r"^ap\.",  # Asia-Pacific region profiles
    ]

    # Model IDs that require inference profiles
    REQUIRES_INFERENCE_PROFILE = [
        "meta.llama3-3-70b-instruct-v1:0",
        "meta.llama3-1-70b-instruct-v1:0",
        "meta.llama3-1-8b-instruct-v1:0",
        # Add more models as needed
    ]

    @classmethod
    def validate_model_id(cls, model_id: str, agent_name: str = "Unknown") -> Tuple[bool, str]:
        """
        Validate a model ID for proper configuration.

        Args:
            model_id: The model ID to validate
            agent_name: Name of the agent being validated (for error messages)

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not model_id:
            return False, f"{agent_name}: Model ID is empty"

        # Check if model requires inference profile
        if model_id in cls.REQUIRES_INFERENCE_PROFILE:
            return (
                False,
                f"{agent_name}: Model '{model_id}' requires inference profile. "
                f"Use 'us.{model_id}' instead.",
            )

        # Check if it's a valid inference profile format
        is_inference_profile = any(
            re.match(pattern, model_id) for pattern in cls.VALID_INFERENCE_PROFILES
        )

        if not is_inference_profile:
            # Check if it might need a prefix
            for required_model in cls.REQUIRES_INFERENCE_PROFILE:
                if required_model in model_id:
                    return (
                        False,
                        f"{agent_name}: Model ID format may be incorrect. "
                        f"Consider using 'us.{model_id}' for inference profile.",
                    )

        return True, f"{agent_name}: Model ID '{model_id}' is valid"

    @classmethod
    def validate_agent_config(
        cls, agent_config: Dict, agent_name: str = "Unknown"
    ) -> Tuple[bool, List[str]]:
        """
        Validate complete agent configuration.

        Args:
            agent_config: Dictionary containing agent configuration
            agent_name: Name of the agent

        Returns:
            Tuple of (all_valid: bool, messages: List[str])
        """
        messages = []
        all_valid = True

        # Validate model_id
        model_id = agent_config.get("model_id")
        if model_id:
            is_valid, msg = cls.validate_model_id(model_id, agent_name)
            messages.append(msg)
            if not is_valid:
                all_valid = False
        else:
            messages.append(f"{agent_name}: Warning - No model_id found in configuration")
            all_valid = False

        # Validate max_tokens
        max_tokens = agent_config.get("max_tokens")
        if max_tokens:
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                messages.append(
                    f"{agent_name}: Invalid max_tokens value: {max_tokens} (must be positive integer)"
                )
                all_valid = False
            elif max_tokens < 1024:
                messages.append(
                    f"{agent_name}: Warning - max_tokens is low ({max_tokens}), may cause truncation"
                )
        else:
            messages.append(f"{agent_name}: Warning - No max_tokens specified")

        # Validate temperature
        temperature = agent_config.get("temperature")
        if temperature is not None:
            if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 1:
                messages.append(
                    f"{agent_name}: Invalid temperature value: {temperature} (must be 0-1)"
                )
                all_valid = False

        # Validate region
        region = agent_config.get("region_name")
        if region:
            valid_regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
            if region not in valid_regions:
                messages.append(
                    f"{agent_name}: Warning - Unusual region '{region}', "
                    f"common regions are: {', '.join(valid_regions)}"
                )
        else:
            messages.append(f"{agent_name}: Warning - No region specified, using default")

        return all_valid, messages

    @classmethod
    def get_corrected_model_id(cls, model_id: str) -> str:
        """
        Attempt to automatically correct a model ID.

        Args:
            model_id: The potentially incorrect model ID

        Returns:
            Corrected model ID with inference profile prefix if needed
        """
        if model_id in cls.REQUIRES_INFERENCE_PROFILE:
            return f"us.{model_id}"

        # Check if already has a valid prefix
        for pattern in cls.VALID_INFERENCE_PROFILES:
            if re.match(pattern, model_id):
                return model_id

        # If it looks like it might need a prefix (contains known model patterns)
        if any(req_model in model_id for req_model in cls.REQUIRES_INFERENCE_PROFILE):
            if not model_id.startswith(("us.", "eu.", "ap.")):
                return f"us.{model_id}"

        return model_id


def validate_all_agents() -> Dict[str, Tuple[bool, List[str]]]:
    """
    Validate all agent configurations in the system.

    Returns:
        Dictionary mapping agent names to validation results
    """
    results = {}

    # List of all agents to validate
    agent_modules = [
        ("architect", "agents.architect.agent"),
        ("senior_coder", "agents.senior_coder.agent"),
        ("fast_coder", "agents.fast_coder.agent"),
        ("test_engineer", "agents.test_engineer.agent"),
        ("code_reviewer", "agents.code_reviewer.agent"),
        ("debug", "agents.debug.agent"),
        ("documentation", "agents.documentation.agent"),
        ("python_specialist", "agents.python_specialist.agent"),
        ("web_specialist", "agents.web_specialist.agent"),
        ("database_specialist", "agents.database_specialist.agent"),
        ("devops_specialist", "agents.devops_specialist.agent"),
        ("data_science_specialist", "agents.data_science_specialist.agent"),
        ("agile_specialist", "agents.agile_specialist.agent"),
        ("doc_research_specialist", "agents.doc_research_specialist.agent"),
    ]

    for agent_name, module_path in agent_modules:
        try:
            # Import the agent module
            parts = module_path.split(".")
            if len(parts) == 3:  # agents.agent_name.agent
                from importlib import import_module

                module = import_module(f".{parts[1]}.{parts[2]}", package="agents")

                # Extract model configuration
                if hasattr(module, "model"):
                    model = module.model
                    config = {
                        "model_id": getattr(model, "model_id", None),
                        "region_name": getattr(model, "region_name", None),
                        "max_tokens": getattr(model, "max_tokens", None),
                        "temperature": getattr(model, "temperature", None),
                    }

                    is_valid, messages = ConfigValidator.validate_agent_config(
                        config, agent_name
                    )
                    results[agent_name] = (is_valid, messages)
                else:
                    results[agent_name] = (False, [f"{agent_name}: Model not found in module"])
        except Exception as e:
            results[agent_name] = (False, [f"{agent_name}: Error loading module - {str(e)}"])

    return results


if __name__ == "__main__":
    """Run configuration validation when executed directly."""
    print("=" * 70)
    print("Configuration Validator - Complex Coding Clara")
    print("=" * 70)
    print()

    # Test individual model IDs
    test_cases = [
        ("meta.llama3-3-70b-instruct-v1:0", "Test Engineer (OLD)"),
        ("us.meta.llama3-3-70b-instruct-v1:0", "Test Engineer (FIXED)"),
        ("us.anthropic.claude-sonnet-4-5-20250929-v1:0", "Senior Coder"),
        ("us.amazon.nova-lite-v1:0", "Documentation"),
    ]

    print("Testing Model ID Validation:")
    print("-" * 70)
    for model_id, name in test_cases:
        is_valid, msg = ConfigValidator.validate_model_id(model_id, name)
        status = "✅" if is_valid else "❌"
        print(f"{status} {msg}")

    print()
    print("=" * 70)
    print("Validating All Agent Configurations")
    print("=" * 70)
    print()

    results = validate_all_agents()

    valid_count = sum(1 for is_valid, _ in results.values() if is_valid)
    total_count = len(results)

    for agent_name, (is_valid, messages) in sorted(results.items()):
        status = "✅" if is_valid else "❌"
        print(f"\n{status} {agent_name.upper()}")
        for msg in messages:
            print(f"   {msg}")

    print()
    print("=" * 70)
    print(f"Validation Summary: {valid_count}/{total_count} agents passed")
    print("=" * 70)
