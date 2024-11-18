from typing import Annotated
from uuid import uuid4
from pathlib import Path
from fastapi import FastAPI, Body

app = FastAPI()

# Create the local storage folder for the files stored 
local_storage_prefix = Path("/tmp/mdcloud/v2/storage_service/")
if not local_storage_prefix.exists():
    local_storage_prefix.mkdir(parents=True)

@app.get("")
async def root():
    return {"message": "Hello World"}

@app.post("/v2/submit_lammps_workflow_input")
def submit_lammps_workflow(workflow: Annotated[str, Body()]) -> str:

    file_id = uuid4()

    # Create a job directory for the file
    job_folder = local_storage_prefix / str(file_id)
    job_folder.mkdir(parents=True)

    # Write the workflow file
    workflow_file = job_folder / "workflow.json"
    workflow_file.write_text(workflow.data)

    # Return the fileID
    return str(file_id)