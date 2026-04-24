class ToolManager:
    """
    This class will manage all the 'Hands' of our agent.
    When we get the challenge at 5 PM, we will add real tools here.
    """
    def __init__(self):
        self.tools_list = []

    def get_tool_definitions(self):
        """
        This returns a list of tools that we tell the AI it can use.
        """
        # We will fill this with JSON-like descriptions later
        return self.tools_list

    def execute_tool(self, tool_name, arguments):
        """
        This is the 'Switch Case' that runs the actual Python code
        when the AI asks to use a tool.
        """
        # We will add 'if/else' statements here for each tool
        return f"Tool {tool_name} not implemented yet."