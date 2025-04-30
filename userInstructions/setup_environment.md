# Setting Up the Python Environment for SolidWorks MCP Server

Follow these steps to set up the necessary Python environment to run the SolidWorks MCP server. These commands should be run in your terminal (like PowerShell or Command Prompt) in the project's root directory (`c:/Users/Patcher/Documents/Projects/Solidworks-mcp`).

1.  **Navigate to the Server Directory:**
    Open your terminal and change the directory to where the server code resides:
    ```powershell
    cd solidworks_mcp_server
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to isolate project dependencies. If you don't have Python installed, download and install it from [python.org](https://www.python.org/). Ensure Python is added to your system's PATH during installation.
    ```powershell
    python -m venv .venv
    ```
    This command creates a folder named `.venv` within the `solidworks_mcp_server` directory containing the virtual environment.

3.  **Activate the Virtual Environment:**
    You need to activate the environment each time you work on the project in a new terminal session.
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
    *(Note: If you are using Command Prompt (cmd.exe), the activation command is `.\.venv\Scripts\activate.bat`. If using Git Bash, it's `source ./.venv/Scripts/activate`)*

    Once activated, your terminal prompt should change to indicate the active environment (e.g., `(.venv) PS C:\Users\Patcher\Documents\Projects\Solidworks-mcp\solidworks_mcp_server>`).

4.  **Install Dependencies:**
    With the virtual environment active, install the required Python packages listed in `requirements.txt`:
    ```powershell
    pip install -r requirements.txt
    ```
    This command will download and install FastAPI, Uvicorn, Pydantic, and pywin32 into your virtual environment.

5.  **Verify Installation (Optional):**
    You can list the installed packages to confirm:
    ```powershell
    pip list
    ```
    You should see `fastapi`, `uvicorn`, `pydantic`, and `pywin32` among the listed packages.

6.  **Running the Server (Development):**
    To start the FastAPI server for development (which will automatically reload when you save changes to the code):
    ```powershell
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```
    Make sure you are still in the `solidworks_mcp_server` directory with the virtual environment activated. You should see output indicating the server is running, typically on `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) by navigating to `http://127.0.0.1:8000/docs` in your web browser.

7.  **Deactivating the Virtual Environment:**
    When you are finished working, you can deactivate the environment:
    ```powershell
    deactivate
    ```

You have now successfully set up the Python environment for the SolidWorks MCP server project.
