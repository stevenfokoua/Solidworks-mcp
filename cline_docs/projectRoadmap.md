# Project Roadmap: SolidWorks MCP Server

## High-Level Goals
- [ ] Create an MCP server to automate SolidWorks operations via API calls.
- [ ] Expose core SolidWorks functionalities (part creation, sketching, features, saving).
- [ ] Provide a flexible interface for scripting complex design workflows.
- [ ] Ensure robust error handling and communication with SolidWorks.

## Key Features
- [ ] **Core API:**
    - [ ] Start/Connect to SolidWorks instance.
    - [ ] Create new Part/Assembly/Drawing documents.
    - [ ] Save documents in various formats (SLDPRT, STEP, PDF, etc.).
- [ ] **Part Modeling:**
    - [ ] Create 2D sketches on specified planes.
    - [ ] Add sketch entities (lines, circles, rectangles).
    - [ ] Apply sketch relations (coincident, parallel, etc.).
    - [ ] Create Extrude features (Boss/Cut).
    - [ ] Create Revolve features.
    - [ ] Create Fillet/Chamfer features.
- [ ] **Assembly Modeling:** (Future Goal)
    - [ ] Insert components.
    - [ ] Add mates.
- [ ] **Drawing Generation:** (Future Goal)
    - [ ] Create standard views.
    - [ ] Add dimensions and annotations.

## Completion Criteria
- The MCP server can reliably execute a sequence of basic part creation commands (e.g., New Part -> Sketch Circle -> Extrude -> Save as STEP).
- Core API endpoints are documented and tested.
- Basic error handling for SolidWorks communication issues is implemented.

## Progress Tracker
- [x] Initial project scaffolding complete.
- [x] Documentation files created.
- [x] Python virtual environment setup instructions provided.
- [ ] Basic FastAPI server running.
- [ ] Implement `create_new_part` endpoint.
- [ ] Implement basic SolidWorks connection logic in `SWInterface`.

## Completed Tasks
- Initial project scaffolding (directories, placeholder files).
- Created core documentation (`projectRoadmap.md`, `currentTask.md`, `techStack.md`, `codebaseSummary.md`).
- Created `requirements.txt`.
- Created `userInstructions/setup_environment.md`.
