#!/usr/bin/env python3
"""
Agent Examples Installation Script
Cross-platform installation with interactive prompts
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

    @classmethod
    def disable(cls):
        """Disable colors on Windows without ANSI support"""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = cls.NC = ''


# Disable colors on Windows if needed
if platform.system() == 'Windows' and not os.environ.get('ANSICON'):
    Colors.disable()


def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.BLUE}{'=' * 40}{Colors.NC}")
    print(f"{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.NC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.NC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.NC}")


def run_command(cmd: list[str], capture_output: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command"""
    try:
        return subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Command failed: {' '.join(cmd)}")
            print_error(f"Error: {e.stderr if e.stderr else str(e)}")
            sys.exit(1)
        return e


def check_python():
    """Check Python version"""
    print(f"{Colors.YELLOW}Checking Python installation...{Colors.NC}")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required, found {version_str}")
        sys.exit(1)

    print_success(f"Python {version_str} found")


def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            check=True
        )
        print_success("pip found")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is required but not found")
        sys.exit(1)


def create_venv():
    """Create virtual environment"""
    venv_path = Path(".venv")

    if venv_path.exists():
        print_info(".venv already exists")
        response = input("Recreate it? [y/N]: ").strip().lower()
        if response == 'y':
            print(f"{Colors.YELLOW}Removing existing .venv...{Colors.NC}")
            shutil.rmtree(venv_path)
        else:
            return False

    response = input("Create virtual environment? (recommended) [Y/n]: ").strip().lower()
    if response in ('', 'y', 'yes'):
        print(f"{Colors.YELLOW}Creating virtual environment...{Colors.NC}")
        run_command([sys.executable, "-m", "venv", ".venv"])
        print_success("Virtual environment created")
        print_warning("Restart this script from within the virtual environment:")

        if platform.system() == "Windows":
            print(f"  {Colors.BLUE}.venv\\Scripts\\activate{Colors.NC}")
        else:
            print(f"  {Colors.BLUE}source .venv/bin/activate{Colors.NC}")
        print(f"  {Colors.BLUE}python install.py{Colors.NC}")

        return True

    return False


def upgrade_pip():
    """Upgrade pip to latest version"""
    print(f"{Colors.YELLOW}Upgrading pip...{Colors.NC}")
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        capture_output=True
    )
    print_success("pip upgraded")


def check_uv():
    """Check if uv is installed"""
    return shutil.which("uv") is not None


def install_dependencies():
    """Install project dependencies"""
    print(f"{Colors.YELLOW}Installing dependencies...{Colors.NC}")

    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print_error("requirements.txt not found")
        sys.exit(1)

    # Check for uv
    has_uv = check_uv()

    if has_uv:
        print_info("Using uv for faster installation...")
        cmd = ["uv", "pip", "install", "-r", "requirements.txt"]
    else:
        print_info("Using pip (install 'uv' for faster installs: pip install uv)")
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

    run_command(cmd)
    print_success("Dependencies installed")


def setup_env_file():
    """Setup environment file"""
    print(f"\n{Colors.YELLOW}Setting up environment file...{Colors.NC}")

    env_file = Path(".env")
    example_env = Path("example_env")

    if not example_env.exists():
        print_warning("example_env not found, skipping .env creation")
        return

    if env_file.exists():
        print_info(".env already exists, skipping")
        return

    shutil.copy(example_env, env_file)
    print_success("Created .env from example_env")
    print_warning("IMPORTANT: Edit .env and add your API keys")
    print_info("Required: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY")


def verify_installation():
    """Verify that key packages are installed"""
    print(f"\n{Colors.YELLOW}Verifying installation...{Colors.NC}")

    packages = [
        ("google.adk", "GoogleADK"),
        ("strands", "Strands"),
        ("anthropic", "Anthropic"),
    ]

    failed = []
    for module, name in packages:
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_warning(f"{name} not installed (may be optional)")
            failed.append(name)

    if failed:
        print_warning(f"Some packages couldn't be verified: {', '.join(failed)}")
    else:
        print_success("All core packages verified")


def print_next_steps():
    """Print next steps after installation"""
    print_header("Installation Complete!")

    print(f"{Colors.BLUE}Next steps:{Colors.NC}")
    print("1. Edit .env and add your API keys")
    print("2. Run GoogleADK agents: cd GoogleADK && adk web")
    print("3. Run Strands agents: python AWS_Strands/<agent>/agent.py")
    print("")
    print(f"{Colors.BLUE}Documentation:{Colors.NC}")
    print("- README.md - Quick start guide")
    print("- INSTALL.md - Detailed installation info")
    print("- CLAUDE.md - Development guide")
    print("")


def main():
    """Main installation flow"""
    print_header("Agent Examples Installation")
    print_info(f"Platform: {platform.system()} {platform.machine()}")

    # Check prerequisites
    check_python()
    check_pip()

    # Create venv if requested
    if create_venv():
        sys.exit(0)  # Exit so user can activate venv

    # Upgrade pip
    upgrade_pip()

    # Install dependencies
    install_dependencies()

    # Setup environment
    setup_env_file()

    # Verify
    verify_installation()

    # Success
    print_next_steps()

    # Venv activation reminder
    if Path(".venv").exists() and not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_warning("Note: Virtual environment exists but may not be activated")
        if platform.system() == "Windows":
            print(f"  To activate: {Colors.BLUE}.venv\\Scripts\\activate{Colors.NC}")
        else:
            print(f"  To activate: {Colors.BLUE}source .venv/bin/activate{Colors.NC}")
        print("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Installation cancelled{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
