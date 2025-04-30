# Configuration settings for the SolidWorks MCP Server

# Example: SolidWorks Application ProgID
# This usually doesn't change, but could be configurable if needed.
SOLIDWORKS_PROGID = "SldWorks.Application"

# Example: Default visibility for new SolidWorks instances
SOLIDWORKS_VISIBLE_BY_DEFAULT = True

# Example: Default directory for saving files (if not specified in request)
# Use None or an empty string if no default is desired.
# DEFAULT_SAVE_DIRECTORY = "C:/Users/Patcher/Documents/SolidWorks_MCP_Output"
DEFAULT_SAVE_DIRECTORY = None

# Example: Logging configuration (can be expanded significantly)
LOG_LEVEL = "INFO" # e.g., DEBUG, INFO, WARNING, ERROR
LOG_FILE = None # e.g., "solidworks_mcp_server.log" to log to a file

# Add other configuration variables as needed, e.g.:
# - Default part/assembly/drawing templates
# - API keys for external services (if integrated later)
# - Timeout settings for SolidWorks operations

# Consider using environment variables or a .env file for sensitive information
# (e.g., using Pydantic's BaseSettings) for better security and flexibility.
