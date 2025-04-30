from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- Generic Models ---

class StatusResponse(BaseModel):
    """ Standard response model for status messages. """
    status: str = "success"
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# --- SolidWorks Operation Specific Models ---

class CreatePartRequest(BaseModel):
    """ Request model for creating a new part document. """
    part_name: str = Field(..., description="Desired name for the new part document (without extension).")
    template_path: Optional[str] = Field(None, description="Optional path to a specific part template (.prtdot). If None, uses SolidWorks default.")

class CreatePartResponse(StatusResponse):
    """ Response model after creating a part. """
    document_path: Optional[str] = Field(None, description="Full path to the newly created (but likely unsaved) document or its identifier.")
    part_name: str

class SketchParameter(BaseModel):
    """ Represents parameters for a single sketch entity (example). """
    entity_type: str = Field(..., description="Type of sketch entity (e.g., 'line', 'circle', 'rectangle').")
    parameters: Dict[str, Any] = Field(..., description="Dictionary of parameters specific to the entity type (e.g., {'center': [0,0], 'radius': 10} for circle).")

class AddSketchRequest(BaseModel):
    """ Request model for adding a sketch to a plane. """
    plane_name: str = Field(..., description="Name of the plane to sketch on (e.g., 'Front Plane', 'Top Plane').")
    sketch_entities: List[SketchParameter] = Field(..., description="List of entities to add to the sketch.")

class AddSketchResponse(StatusResponse):
    """ Response model after adding a sketch. """
    sketch_name: Optional[str] = Field(None, description="Name of the created sketch feature.")

class ExtrudeRequest(BaseModel):
    """ Request model for creating an extrude feature. """
    depth_mm: float = Field(..., gt=0, description="Depth of the extrusion in millimeters.")
    direction: str = Field("forward", description="Direction of extrusion ('forward', 'backward', 'midplane').") # Example, refine later
    # Add other extrusion options like 'reverse_direction', 'type' (Boss/Cut), etc.
    sketch_name: Optional[str] = Field(None, description="Name of the sketch to extrude. If None, assumes the currently active/selected sketch.")

class ExtrudeResponse(StatusResponse):
    """ Response model after creating an extrude feature. """
    feature_name: Optional[str] = Field(None, description="Name of the created extrude feature.")

class SaveAsRequest(BaseModel):
    """ Request model for saving the active document. """
    file_path: str = Field(..., description="Full path including filename and extension where the document should be saved.")
    file_format: Optional[str] = Field(None, description="Desired save format (e.g., 'SLDPRT', 'STEP', 'PDF', 'STL'). If None, derived from file_path extension or defaults to native.")
    overwrite: bool = Field(False, description="Whether to overwrite the file if it already exists.")

class SaveAsResponse(StatusResponse):
    """ Response model after saving a document. """
    saved_path: Optional[str] = Field(None, description="The actual path the file was saved to.")

# Add more models as needed for other operations (Revolve, Fillet, Assembly, Drawing, etc.)
