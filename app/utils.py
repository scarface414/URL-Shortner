import secrets
import string

from sqlalchemy.orm import Session 
from fastapi.exceptions import HTTPException

from . import crud
# remove circular dependancy using this instead of 
# form .crud import function_name()

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_key(db : Session , length: int = 5) -> str: 
    key = create_random_key(length)
    while crud.get_db_url_by_key(db,key) : 
        key = create_random_key(length)
    return key

def verify_custom_key_unique(db : Session, custom_key : str) -> bool :
    is_unique = False if crud.get_db_url_by_key(db,custom_key) else True
    return is_unique