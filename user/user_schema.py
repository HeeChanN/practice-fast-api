from pydantic import BaseModel

class CreateUserForm(BaseModel):
    userId : str
    email : str
    name : str
    password : str
    phoneNo : str
    
class UserAuth(BaseModel):
    email: str
    password: str

