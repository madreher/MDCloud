from pydantic import BaseModel

class WorkflowLammpsInputsResponse(BaseModel):
    data: str = ""
    input: str = ""
    data_filename: str = "model.data"