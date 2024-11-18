from typing import Annotated
import requests

from uuid import uuid4

from fastapi import FastAPI, Body, Depends
from lammpsinputbuilder.model.workflow_builder_model import WorkflowBuilderModel
from lammpsinputbuilder.workflow_builder import WorkflowBuilder

app = FastAPI()

# Address of the storage service
STORAGE_SERVICE_ADDRESS = "http://localhost:50001"
JOB_SERVICE_ADDRESS = "http://localhost:50002"

def submit_json_to_storage_service(file_content: str) -> str:
    request_url = f"{STORAGE_SERVICE_ADDRESS}/v2/submit_lammps_workflow_input/"
    response = requests.post(request_url, json={"data": file_content})

    if response.status_code != 200:
        raise Exception(f"Failed to submit file to storage service: {response.status_code}")
    
    return response.text

def submit_lammps_workflow_generation_job(file_id: str) -> str:
    request_url = f"{JOB_SERVICE_ADDRESS}/v2/lammps/submit_lammps_workflow_generation/"
    response = requests.post(request_url, json={"job_type": "lammps", "files": [file_id]})

    if response.status_code != 200:
        raise Exception(f"Failed to submit job to job service: {response.status_code}")
    
    return response.text

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v2/lammps/submit_lammps_workflow_generation", )
def submit_lammps_workflow(workflow: Annotated[WorkflowBuilderModel, Body()]) -> str:

    # Send the workflow definition to the storage service
    file_id = submit_json_to_storage_service(workflow.model_dump_json())

    # Submit the job to the Job Service
    job_id = submit_lammps_workflow_generation_job(file_id)

    return str(job_id)

