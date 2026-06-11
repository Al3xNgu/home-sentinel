from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PersonPhotoResponse(BaseModel):
    id: int
    person_id: int
    image_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)