#!/bin/bash
# Agent Examples Installation Script
# Supports: macOS, Linux, Windows (Git Bash/WSL)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    CYGWIN*)    PLATFORM=Cygwin;;
    MINGW*)     PLATFORM=MinGw;;
    MSYS*)      PLATFORM=Git-Bash;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo -e "${BLUE}=================================${NC}"
echo -e "${BLUE}Agent Examples Installation${NC}"
echo -e "${BLUE}Platform: ${PLATFORM}${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""

# Check Python
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${RED}Error: pip is required but not found.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip found${NC}"

# Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv

    # Activate based on platform
    if [[ "$PLATFORM" == "MinGw" ]] || [[ "$PLATFORM" == "Git-Bash" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
    echo -e "${GREEN}✓ Virtual environment created and activated${NC}"
fi

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
python3 -m pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
if command -v uv &> /dev/null; then
    echo -e "${BLUE}Using uv for faster installation...${NC}"
    uv pip install -r requirements.txt
else
    echo -e "${BLUE}Using pip (install 'uv' for faster installs: pip install uv)${NC}"
    python3 -m pip install -r requirements.txt
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Setup environment file
echo ""
echo -e "${YELLOW}Setting up environment file...${NC}"
if [ ! -f .env ]; then
    cp example_env .env
    echo -e "${GREEN}✓ Created .env from example_env${NC}"
    echo -e "${YELLOW}⚠ IMPORTANT: Edit .env and add your API keys${NC}"
    echo -e "${BLUE}   Required: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY${NC}"
else
    echo -e "${BLUE}ℹ .env already exists, skipping${NC}"
fi

# Verify installation
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"
if python3 -c "import google.adk; import strands; import anthropic" 2>/dev/null; then
    echo -e "${GREEN}✓ Core packages verified${NC}"
else
    echo -e "${RED}⚠ Some packages may not have installed correctly${NC}"
fi

# Success
echo ""
echo -e "${GREEN}=================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Edit .env and add your API keys"
echo "2. Run GoogleADK agents: cd GoogleADK && adk web"
echo "3. Run Strands agents: python AWS_Strands/<agent>/agent.py"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "- README.md - Quick start guide"
echo "- INSTALL.md - Detailed installation info"
echo "- CLAUDE.md - Development guide"
echo ""

# Activation reminder if venv was created
if [ -d ".venv" ]; then
    echo -e "${YELLOW}Note: To activate the virtual environment later:${NC}"
    if [[ "$PLATFORM" == "MinGw" ]] || [[ "$PLATFORM" == "Git-Bash" ]]; then
        echo "  source .venv/Scripts/activate"
    else
        echo "  source .venv/bin/activate"
    fi
    echo ""
fi
