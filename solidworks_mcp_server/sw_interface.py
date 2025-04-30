import win32com.client
import pythoncom
import os
import time
from contextlib import contextmanager

# SolidWorks constants (Verify these values against the SolidWorks API documentation for your version)
# Found via SolidWorks API Help: Search for "SwDocumentTypes_e", "SwSaveAsOptions_e", etc.
swDocumentTypes = {
    "swDocPART": 1,
    "swDocASSEMBLY": 2,
    "swDocDRAWING": 3,
}
swSaveAsOptions = {
    "swSaveAsOptions_Silent": 1,      # Save document silently.
    "swSaveAsOptions_Copy": 2,        # Save document as a copy.
    # Add others as needed
}
swFileSaveError = {
    "swGenericSaveError": 1,          # Generic save error.
    "swReadOnlySaveError": 2,         # File is read-only.
    "swFileNameContainsAtSign": 4,    # File name contains the @ character.
    "swFileLockError": 8,             # File is locked by another user.
    "swFileSaveFormatNotAvailable": 16, # Save As file format is not available.
    "swFileSaveCancelled": 32,        # File save is cancelled by user.
    "swFileSaveRequiresRepair": 64,   # File needs repair. Use ISldWorks::CheckFileBeforeSave.
    "swFileSaveAsDoNotOverwrite": 128, # File exists and user selected not to overwrite.
    "swFileSaveAsInvalidFileExtension": 256, # Invalid file extension for the specified document type.
    "swFileSaveAsNameExceedsMaxPathLength": 512, # File name exceeds the maximum path length allowed by the operating system.
    "swFileSaveAsNotSupported": 1024, # Save As operation is not supported for this document type or state.
}
swUserPreferenceStringValue = {
    "swDefaultTemplatePart": 0,       # Default template for part documents.
    "swDefaultTemplateAssembly": 1,   # Default template for assembly documents.
    "swDefaultTemplateDrawing": 2,    # Default template for drawing documents.
    # Add others as needed
}
# Add more constants as needed (e.g., for sketch relations, feature types, units)

@contextmanager
def com_context():
    """ Context manager for COM initialization and uninitialization. """
    try:
        pythoncom.CoInitialize()
        yield
    finally:
        pythoncom.CoUninitialize()

class SWInterface:
    """
    A wrapper class for interacting with the SolidWorks COM API.
    Manages the connection and provides methods for common operations.
    Handles COM initialization per thread.
    """
    def __init__(self, visible=True):
        self.sw_app = None
        self.visible = visible
        # Connection attempt is deferred until the first operation that needs it.

    def _ensure_connection(self):
        """ Ensures SolidWorks is connected, attempting connection if needed. """
        if self.sw_app:
            # Basic check: Try accessing a simple property to see if COM object is still valid
            try:
                _ = self.sw_app.Visible # Accessing a property
                return # Connection seems ok
            except pythoncom.com_error as e:
                print(f"COM error accessing existing SW instance ({e}), attempting to reconnect.")
                self.sw_app = None # Force reconnect
            except Exception as e:
                 print(f"Unexpected error checking SW connection ({e}), attempting to reconnect.")
                 self.sw_app = None # Force reconnect

        if not self.sw_app:
            print("Attempting to establish SolidWorks connection...")
            with com_context(): # Ensure COM is initialized for this thread
                try:
                    # Try to get a running instance first (more efficient)
                    self.sw_app = win32com.client.GetActiveObject("SldWorks.Application")
                    print("Successfully connected to running SolidWorks instance.")
                    # Ensure visibility matches preference if connecting to existing instance
                    try:
                        self.sw_app.Visible = self.visible
                    except Exception as vis_e:
                        print(f"Warning: Could not set visibility on existing SW instance: {vis_e}")

                except pythoncom.com_error: # Specific error if GetActiveObject fails
                    print("No running SolidWorks instance found. Attempting to start a new one.")
                    try:
                        # Dispatch starts a new instance if not running
                        self.sw_app = win32com.client.Dispatch("SldWorks.Application")
                        # Allow some time for SolidWorks to initialize
                        time.sleep(5) # Adjust as needed
                        self.sw_app.Visible = self.visible
                        # Optional: Maximize window? sw.Frame.Cmd(1001) # swCommands_e.swCommands_MaximizeWindow
                        print(f"Started a new SolidWorks instance (Visible: {self.visible}).")
                    except pythoncom.com_error as dispatch_e:
                        print(f"COM Error: Failed to start SolidWorks via Dispatch: {dispatch_e}")
                        self.sw_app = None
                    except Exception as start_e:
                        print(f"Unexpected Error: Failed to start SolidWorks: {start_e}")
                        self.sw_app = None
                except Exception as get_active_e:
                     print(f"Unexpected Error: Failed to get active SolidWorks object: {get_active_e}")
                     self.sw_app = None

            if not self.sw_app:
                raise ConnectionError("Fatal: Could not connect to or start SolidWorks.")

    def get_sw_app(self):
        """ Returns the SolidWorks application object, ensuring connection. """
        self._ensure_connection()
        return self.sw_app

    def create_new_part(self, template_path=None):
        """
        Creates a new empty part document using the specified template or the default.
        Args:
            template_path (str, optional): Full path to the part template (.prtdot).
                                           If None, uses the user's default part template.
        Returns:
            object: The newly created SolidWorks ModelDoc2 object.
        Raises:
            RuntimeError: If the part document cannot be created.
            ConnectionError: If connection to SolidWorks fails.
        """
        with com_context():
            sw = self.get_sw_app()
            if template_path:
                if not os.path.exists(template_path):
                    raise FileNotFoundError(f"Specified template not found: {template_path}")
                print(f"Creating new part using template: {template_path}")
                doc = sw.NewDocument(template_path, 0, 0.0, 0.0) # Args: TemplatePath, PaperSize, Width, Height (Width/Height often 0 for parts)
            else:
                # Get default part template path
                default_template = sw.GetUserPreferenceStringValue(swUserPreferenceStringValue["swDefaultTemplatePart"])
                if not default_template or not os.path.exists(default_template):
                     print(f"Warning: Default part template path not found or invalid ('{default_template}'). Attempting NewPart().")
                     # Fallback to simple NewPart() which might use a system default or fail
                     doc = sw.NewPart()
                else:
                    print(f"Creating new part using default template: {default_template}")
                    doc = sw.NewDocument(default_template, 0, 0.0, 0.0)

            if not doc:
                raise RuntimeError("Failed to create new part document. Check SolidWorks templates and settings.")

            # Activate the document window (optional, but good practice)
            sw.ActivateDoc3(doc.GetTitle(), False, 0, 0) # Args: Name, BringToTop, Option, ErrorCode

            print(f"New part document '{doc.GetTitle()}' created successfully.")
            return doc # Return the document object itself

    def add_sketch(self, sketch_params):
        """ Placeholder for adding a sketch to a plane. """
        with com_context():
            sw = self.get_sw_app()
            # 1. Get active document (assume it's a part)
            # 2. Select plane (e.g., "Front Plane")
            # 3. Create sketch
            # 4. Add sketch entities based on sketch_params
            print(f"Placeholder: Adding sketch with params: {sketch_params}")
            return "Sketch1" # Placeholder name

    def extrude_feature(self, depth_mm):
        """ Placeholder for creating an extrude feature. """
        with com_context():
            sw = self.get_sw_app()
            # 1. Get active document
            # 2. Ensure a sketch is active/selected
            # 3. Get FeatureManager
            # 4. Call FeatureExtrusion3 or similar method
            # Convert depth_mm to meters for SolidWorks API (typically uses meters)
            depth_m = depth_mm / 1000.0
            print(f"Placeholder: Extruding feature to depth: {depth_mm}mm ({depth_m}m)")
            return "Boss-Extrude1" # Placeholder name

    def save_as(self, path, file_format="SLDPRT", overwrite=False):
        """ Placeholder for saving the active document. """
        with com_context():
            sw = self.get_sw_app()
            doc = sw.ActiveDoc
            if not doc:
                raise RuntimeError("No active document found to save.")

            # Determine save options
            options = swSaveAsOptions["swSaveAsOptions_Silent"]
            if overwrite:
                # Note: Silent save usually overwrites by default.
                # Explicit overwrite handling might involve checking file existence first
                # or potentially using different API calls if available.
                pass
            else:
                # If not overwriting, check if file exists
                if os.path.exists(path):
                     raise FileExistsError(f"File already exists and overwrite is False: {path}")
                 # Alternatively, use swSaveAsOptions_UpdateInactiveViews? Check API docs.

            print(f"Placeholder: Saving active document '{doc.GetTitle()}' to '{path}' as format '{file_format}' (Overwrite: {overwrite})")

            # Example of potential call structure (needs actual implementation)
            # errors = 0
            # warnings = 0
            # success = doc.SaveAsNotify(path, options, errors, warnings)
            # if success == 0: # swFileSaveError_e.swFileSaveOkay (typically 0)
            #    print("Save successful.")
            # else:
            #    # Map error code back to swFileSaveError enum for better message
            #    error_msg = f"Save failed with code: {success}"
            #    for name, code in swFileSaveError.items():
            #        if code == success:
            #            error_msg = f"Save failed: {name} ({success})"
            #            break
            #    print(f"{error_msg}. Errors: {errors}, Warnings: {warnings}")
            #    raise IOError(f"Failed to save document to {path}. Reason: {error_msg}")
            return path # Return the path on successful placeholder execution

    def close_connection(self):
        """ Releases the COM object. Does NOT close the SolidWorks application itself. """
        # Releasing the COM object is generally handled by pythoncom.CoUninitialize()
        # in the context manager or at script exit. Explicitly setting to None helps.
        if self.sw_app:
            print("Releasing SolidWorks COM object reference.")
            self.sw_app = None
        # COM context manager handles CoUninitialize

# Example usage (for testing purposes)
if __name__ == '__main__':
    sw_interface = None
    try:
        print("--- Testing SWInterface ---")
        sw_interface = SWInterface(visible=True)

        print("\nAttempting to create new part...")
        part_doc = sw_interface.create_new_part() # Use default template
        if part_doc:
            print(f"Successfully created/retrieved part document: {part_doc.GetTitle()}")

            # --- Placeholder calls ---
            # print("\nAttempting to add sketch...")
            # sketch_name = sw_interface.add_sketch({"type": "circle", "center": (0,0), "radius": 10})
            # print(f"Placeholder sketch created: {sketch_name}")

            # print("\nAttempting to extrude...")
            # feature_name = sw_interface.extrude_feature(25) # 25mm
            # print(f"Placeholder feature created: {feature_name}")

            # print("\nAttempting to save...")
            # save_dir = os.path.join(os.getcwd(), "test_output")
            # os.makedirs(save_dir, exist_ok=True)
            # save_path = os.path.join(save_dir, "TestPart_Output.SLDPRT")
            # try:
            #     sw_interface.save_as(save_path, overwrite=True)
            #     print(f"Placeholder save executed for: {save_path}")
            # except FileExistsError as fee:
            #     print(fee)
            # except IOError as ioe:
            #     print(ioe)
            # --- End Placeholder calls ---

        else:
            print("Failed to create part document.")

    except ConnectionError as ce:
        print(f"Connection Error during test: {ce}")
    except FileNotFoundError as fnf:
        print(f"File Not Found Error during test: {fnf}")
    except RuntimeError as rt:
        print(f"Runtime Error during test: {rt}")
    except Exception as e:
        import traceback
        print(f"An unexpected error occurred during test: {e}")
        traceback.print_exc()
    finally:
        # The COM context manager handles CoUninitialize
        if sw_interface:
             # sw_interface.close_connection() # Explicitly release reference
             print("\n--- Test Finished ---")
             # Keep SW open if it was started/connected for manual inspection
             print("(SolidWorks instance remains open if connected/started)")
