# Doc Research Specialist TODO

## Completed ✅
- Added: Data (4), Text (3) tools
- Max tokens: 8192 → 16384 (Haiku limit)
- Total: 22 → 26 tools (now 27 with http_request + MCP tools when configured)
- Prompt updated
- **http_request**: Added for fetching docs from URLs, GitHub, APIs (2025-10-09)
- **Context7 MCP**: Added live library documentation lookup (2025-10-09)
  - Requires MCP_SERVER_URL environment variable
  - Tools: resolve-library-id, get-library-docs
  - Gracefully degrades if MCP server unavailable

## Future
- **Tavily search**: Current information retrieval (requires TAVILY_API_KEY)
- **Doc caching**: Intelligent research cache with indexing
