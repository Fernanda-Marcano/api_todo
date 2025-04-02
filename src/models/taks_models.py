from pydantic import BaseModel, Field
from typing import Text, List, Optional
from enum import Enum
from datetime import datetime

#gt=mayor que
#ge = mayor o igual
#lt = menor que
#le = menor o igual

class StatusEnum(str, Enum):
    pending = 'pending'
    process = 'process'
    completed = 'completed'

class TaskModel(BaseModel):
    id: str 
    title: str = Field(min_length=5, max_length=50)
    description: Text = Field(min_length=5, max_length=200)
    status: StatusEnum = StatusEnum.pending
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: Text = Field(min_length=5, max_length=200)
    status: list[StatusEnum]
    updated_at: datetime = datetime.now()

