from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel
from lammpsinputbuilder.model.workflow_builder_model import WorkflowBuilderModel
from lammpsinputbuilder.workflow_builder import WorkflowBuilder

app = FastAPI()

class WorkflowLammpsInputs(BaseModel):
    data: str = ""
    input: str = ""
    data_filename: str = "model.data"


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/lammps/generate_lammps_from_workflow", response_model=WorkflowLammpsInputs)
def create_workflow(workflow: Annotated[WorkflowBuilderModel, Body()]) -> WorkflowLammpsInputs:

    # Convert the data model into a WorkflowBuilder object
    dict_obj = workflow.model_dump()
    workflow2 = WorkflowBuilder()
    workflow2.from_dict(dict_obj, version=0)

    # Generate the LAMMPS inputs
    job_folder = workflow2.generate_inputs()

    # Get the data and input files
    data_file = job_folder / "model.data"
    input_file = job_folder / "workflow.input"
    
    # Write the response
    result = WorkflowLammpsInputs()
    result.data = data_file.read_text()
    result.input = input_file.read_text()
    result.data_filename = data_file.name

    return result

