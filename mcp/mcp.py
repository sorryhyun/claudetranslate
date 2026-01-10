#!/usr/bin/env python3
"""
MCP Server - Dynamic tool loading from subdirectories.

Each subdirectory represents a tool group with:
- schema.json: Tool definitions
- Python modules with handle() functions
"""

import json
import os
import sys
from importlib import import_module
from typing import Any, Dict, List


class MCPServer:
    """MCP server with dynamic tool loading."""

    def __init__(self):
        self.tools: Dict[str, Any] = {}  # tool_name -> module
        self.schemas: List[Dict] = []
        self._load_tool_groups()

    def _load_tool_groups(self) -> None:
        """Discover and load all tool groups from subdirectories."""
        server_dir = os.path.dirname(os.path.abspath(__file__))

        for name in os.listdir(server_dir):
            group_path = os.path.join(server_dir, name)
            if not os.path.isdir(group_path) or name.startswith('_'):
                continue

            schema_path = os.path.join(group_path, "schema.json")
            if not os.path.exists(schema_path):
                continue

            # Load schema
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)

            # Load tool modules
            group_module = import_module(f".{name}", package="mcp")
            if hasattr(group_module, "TOOLS"):
                for tool_name, module in group_module.TOOLS.items():
                    self.tools[tool_name] = module

            self.schemas.extend(schema.get("tools", []))

    def handle_initialize(self, request_id: Any) -> Dict:
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "translator", "version": "1.0.0"}
            }
        }

    def handle_tools_list(self, request_id: Any) -> Dict:
        """Handle tools/list request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": self.schemas}
        }

    def handle_tool_call(self, request_id: Any, params: Dict) -> Dict:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
            }

        try:
            module = self.tools[tool_name]
            result = module.handle(arguments)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(result, indent=2, ensure_ascii=False)
                    }]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": str(e)}
            }

    def run(self) -> None:
        """Main server loop."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                continue

            method = request.get("method")
            request_id = request.get("id")
            params = request.get("params", {})

            if method == "initialize":
                response = self.handle_initialize(request_id)
            elif method == "notifications/initialized":
                continue
            elif method == "tools/list":
                response = self.handle_tools_list(request_id)
            elif method == "tools/call":
                response = self.handle_tool_call(request_id, params)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            output = json.dumps(response) + "\n"
            sys.stdout.write(output)
            sys.stdout.flush()


def main():
    """Entry point."""
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()
