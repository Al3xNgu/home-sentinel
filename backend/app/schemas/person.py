from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PersonCreate(BaseModel):
    name: str

# Could potentially require different things from PersonCreate in future
class PersonUpdate(BaseModel):
    name: str

class PersonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime