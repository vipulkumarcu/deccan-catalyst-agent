import json
from typing import List, Dict, Any, Callable

class ToolManager:
    """
    Orchestrates 'Function Calling' for the Nexus Agent.
    Maintains the mapping between LLM schemas and local Python execution.
    """
    def __init__(self):
        self._tool_definitions: List[Dict[str, Any]] = []
        self._execution_registry: Dict[str, Callable] = {}

    def register_tool(self, definition: Dict[str, Any], function: Callable):
        tool_name = definition.get("function", {}).get("name")
        if not tool_name:
            raise ValueError("Nexus Error: Tool definition is missing a name.")
        self._tool_definitions.append(definition)
        self._execution_registry[tool_name] = function

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return self._tool_definitions

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        try:
            if tool_name not in self._execution_registry:
                return f"Error: Tool '{tool_name}' is not registered."

            target_function = self._execution_registry[tool_name]
            result = target_function(**arguments)

            # Returning JSON string makes it easier for the LLM to parse
            return json.dumps(result)

        except Exception as e:
            return f"Execution Failure in {tool_name}: {str(e)}"