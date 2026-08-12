from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int