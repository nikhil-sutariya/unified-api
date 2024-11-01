from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TeamMembers(BaseModel):
    id: int
    name: str
    role: str

class Project(BaseModel):
    id: int
    name: str
    start_date: str
    end_date: str
    team_members: List[TeamMembers]

class User(BaseModel):
    id: Optional[str]
    project_id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

class UserRespnse(User):
    id: Optional[str]

    class Config:
        json_encoders = {
            datetime: lambda date: date.strftime("%A, %b %d %Y %H:%M %p")
        }

class UserCreate(BaseModel):
    project_id: int
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None

class StandardResponse(BaseModel):
    success: bool
    message: str
    data: User | List[User] | None
