from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.user import UserOut


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class CommentOut(BaseModel):
    id: int
    case_id: int
    user_id: int
    content: str
    user: Optional[UserOut] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
