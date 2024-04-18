from pydantic import BaseModel

class CreateUserForm(BaseModel):
    userId : str
    email : str
    name : str
    password : str
    phoneNo : str
    
class UserAuth(BaseModel):
    userId: str
    password: str

class UserResponse(BaseModel):
    userId: str
    email : str
    name : str
    phoneNo : str