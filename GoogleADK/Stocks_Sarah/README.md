# Stocks Agent

A specialized stock operations agent designed to handle stock market interactions through a MCP server integration.

## Prerequisites

Requires first setting up the MCP server.

## Usage

See the main [getting-started.md](../ADK-getting-started.md) for installation and setup instructions.

## Environment Variables

The following environment variables need to be configured:

- `ROBINHOOD_USERNAME`: Your Robinhood username
- `ROBINHOOD_PASSWORD`: Your Robinhood password
- `GOOGLE_MODEL`: Optional Google model override (defaults to "gemini-pro")

## Agent Capabilities

The Stocks_Sarah agent specializes in:

**Stock Operations:**
- Get stock quotes
- Buy and sell stocks
- Get account information