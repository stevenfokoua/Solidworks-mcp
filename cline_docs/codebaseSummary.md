# Codebase Summary: SolidWorks MCP Server

*Initial Version - Project Scaffolding*

## Overview
This document provides a high-level summary of the SolidWorks MCP Server codebase structure and key components. It will be updated as the project evolves.

## Key Components and Their Interactions
- **`main.py`:** Entry point for the FastAPI application. Defines API endpoints, handles incoming requests, and orchestrates calls to the SolidWorks interface.
- **`sw_interface.py`:** Contains the `SWInterface` class responsible for all direct interaction with the SolidWorks COM API using `pywin32`. Encapsulates low-level SolidWorks operations.
- **`models.py`:** Defines Pydantic models for API request/response data structures. Ensures data validation and provides clear schemas for API interactions.
- **`config.py`:** (Placeholder) Intended for application configuration settings, such as SolidWorks ProgID, default paths, or logging settings.
- **`tests/`:** (Placeholder) Directory for `pytest` test files.

## Data Flow
1.  Client (e.g., script, UI) sends an HTTP request to a FastAPI endpoint defined in `main.py`.
2.  FastAPI validates the request payload using Pydantic models defined in `models.py`.
3.  The endpoint handler in `main.py` calls appropriate methods on the `SWInterface` class in `sw_interface.py`.
4.  `SWInterface` methods use `pywin32` to interact with the SolidWorks COM API, performing the requested actions (e.g., creating a part, adding a feature).
5.  `SWInterface` returns results or status back to the endpoint handler.
6.  The endpoint handler formats the response (potentially using Pydantic models) and sends it back to the client.

## External Dependencies
- **FastAPI:** Web framework.
- **Uvicorn:** ASGI server.
- **Pydantic:** Data validation.
- **pywin32:** Windows COM interaction (specifically for SolidWorks API).
- **SolidWorks Application:** The server requires a licensed and running instance of SolidWorks to interact with via COM.

*Dependency versions are managed in `requirements.txt`.*

## Recent Significant Changes
- Initial project structure and core files created.
- Documentation (`cline_docs`) initialized.

## User Feedback Integration and Its Impact on Development
*(N/A at this stage)*

## Additional Reference Documents
*(No additional documents created yet)*
