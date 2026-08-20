from pydantic import BaseModel
from enum import Enum
class Token(BaseModel):
    access_token:str
    token_type:str
class Roles(str,Enum):
    ADMIN = 'admin'
    USER = 'user'