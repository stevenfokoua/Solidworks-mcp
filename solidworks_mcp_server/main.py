from fastapi import FastAPI, HTTPException, Depends
from .sw_interface import SWInterface, ConnectionError  # Import ConnectionError too
from .models import CreatePartRequest, CreatePartResponse, StatusResponse # Import relevant models
# from .models import ExtrudeRequest # Keep others commented for now
import pythoncom # Needed for exception handling if COM errors bubble up

app = FastAPI(
    title="SolidWorks MCP Server",
    description="An MCP server to automate SolidWorks operations via API calls.",
    version="0.1.0",
)

# --- Dependency Injection for SWInterface ---
# This makes testing easier and manages the instance lifecycle.
# We create it once and reuse it for requests.
sw_interface_instance = SWInterface() # Instantiate globally

def get_sw_interface():
    # In a real-world scenario with thread safety concerns for COM,
    # you might need a more sophisticated way to manage instances per thread/request.
    # For simplicity now, we use a single global instance.
    # Ensure COM context is managed within SWInterface methods using `with com_context():`
    return sw_interface_instance

# --- Event Handlers ---
@app.on_event("startup")
async def startup_event():
    """ Attempt initial connection on startup to fail early if SW isn't available. """
    print("FastAPI server starting up...")
    try:
        # Trigger initial connection attempt
        sw_app = get_sw_interface().get_sw_app()
        print(f"Initial connection to SolidWorks successful (Version: {sw_app.RevisionNumber()}).")
    except ConnectionError as e:
        print(f"WARNING: Failed to connect to SolidWorks on startup: {e}")
        print("Server will continue running, but SolidWorks operations will fail until connection is established.")
    except Exception as e:
        print(f"ERROR: Unexpected error during startup connection attempt: {e}")
        # Depending on policy, you might want to raise an exception here to stop the server
        # raise RuntimeError(f"Failed to initialize SolidWorks connection on startup: {e}")

@app.on_event("shutdown")
def shutdown_event():
    """ Clean up resources on shutdown. """
    print("FastAPI server shutting down...")
    # sw_interface = get_sw_interface()
    # if sw_interface:
    #     sw_interface.close_connection() # Optional: release COM reference if needed
    print("Shutdown complete.")


# --- API Endpoints ---

@app.get("/", response_model=StatusResponse)
async def read_root():
    """ Basic health check endpoint. """
    return StatusResponse(message="SolidWorks MCP Server is running.")

@app.post("/mcp/create_part", response_model=CreatePartResponse, status_code=201)
async def create_part(
    request: CreatePartRequest,
    sw: SWInterface = Depends(get_sw_interface) # Inject dependency
):
    """ Creates a new SolidWorks part document using default or specified template. """
    try:
        print(f"Received request to create part: {request.part_name}")
        part_doc = sw.create_new_part(template_path=request.template_path)
        doc_title = part_doc.GetTitle() # Get the actual title assigned by SW
        print(f"SolidWorks created part document: {doc_title}")
        # Note: The document is created in SW but not saved yet by this endpoint.
        return CreatePartResponse(
            status="success",
            message=f"Part document '{doc_title}' created successfully in SolidWorks.",
            part_name=request.part_name, # Return requested name for reference
            document_path=doc_title # Return SW assigned title/identifier
        )
    except ConnectionError as e:
        print(f"ERROR: ConnectionError in create_part - {e}")
        raise HTTPException(status_code=503, detail=f"SolidWorks connection error: {str(e)}")
    except FileNotFoundError as e: # Catch template not found error
        print(f"ERROR: FileNotFoundError in create_part - {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except (RuntimeError, pythoncom.com_error) as e: # Catch SW runtime or COM errors
        print(f"ERROR: SolidWorks/COM Error in create_part - {e}")
        raise HTTPException(status_code=500, detail=f"SolidWorks API error during part creation: {str(e)}")
    except Exception as e:
        import traceback
        print(f"ERROR: Unexpected error in create_part - {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {str(e)}")


# @app.post("/mcp/extrude", status_code=200) # Keep commented for now
# async def extrude_feature(request: ExtrudeRequest, sw: SWInterface = Depends(get_sw_interface)):
#     """ Adds an extrude feature to the active part. (Requires active sketch) """
#     try:
#         # Assuming a sketch is pre-selected or context is known
#         feature_name = sw.extrude_feature(request.depth_mm) # Use injected sw
#         return {"status": "success", "message": f"Extrude feature created: {feature_name}"} # Replace with ExtrudeResponse model
#     except ConnectionError as e:
#         raise HTTPException(status_code=503, detail=f"SolidWorks connection error: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to extrude feature: {str(e)}")

# --- Add more endpoints for sketch, save, etc. ---


if __name__ == "__main__":
    import uvicorn
    print("Starting server directly via main.py (for debugging)...")
    # Use --reload for development to automatically pick up code changes
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
