from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from fastapi.responses import JSONResponse

router = APIRouter()

class CreateUsers(BaseModel):
    email : str
    username : str
    firstname : str
    lastname : str
    hash_password : str
    role : str

# db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/create_user')
def create_user( new_user : CreateUsers):
    user_model = Users(
        email = new_user.email,
        username = new_user.username,
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        hash_password = new_user.hash_password,
        is_active = True,
        role = new_user.role
    )

    # db.add(user_model)
    # db.commit()

    # return JSONResponse(status_code=201, content={'message' : 'User created successfully!!!'})
    return user_model