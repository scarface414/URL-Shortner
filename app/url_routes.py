from fastapi import APIRouter , status , Depends , Request
# from db import Session , engine

from .schemas import BaseURL
from .crud import get_db_url_by_key, create_db_url , get_db_url_by_admin_key, update_db_url_clicks , deactivate_db_url_by_key
from .utils import raise_not_found

import validators

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from .db import engine, Base, Session
from .models import URL
from .schemas import URLInfo

from typing import Optional, Union

router = APIRouter()

# Dependency
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# session = Session(bind=engine)


@router.get("/")    
async def hello() : 
    return "Welcome to URL shortner project"

@router.post(
        "/url" , 
        response_model=URLInfo,  
        status_code = status.HTTP_201_CREATED,
        name = "Create URL, Optional Custom Key Parameter"
    )
async def create_url(
        url : BaseURL,  
        request : Request,
        session = Depends(get_db), 
        custom_key : Union[str, None] = None
    ) : 
    if not validators.url(url.target_url) : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Invalid URL")

    if custom_key : 
        if not custom_key.isupper(): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Custom Key should be in UpperCase")
        if len(custom_key) < 5: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Custom Key too short")

    short_url = create_db_url(session, url, custom_key)

    return short_url



@router.get("/{url_key}" , status_code = status.HTTP_200_OK)
async def redirect_url(
        url_key : str,
        session = Depends(get_db)
    ):

    short_url = get_db_url_by_key(session , url_key)

    if not short_url :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Invalid URL Key")
    
    update_db_url_clicks(session, short_url)
    return RedirectResponse(short_url.target_url)

@router.get(
        "/admin/{admin_key}" , 
        response_model=URLInfo ,  
        status_code = status.HTTP_200_OK ,
        name = "adminstrative info"
    )
async def get_url_info(
        admin_key : str,  
        session = Depends(get_db)
    ) : 
    
    short_url = get_db_url_by_admin_key(session , admin_key)

    if not short_url :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Invalid URL Key")

    return short_url


@router.get("/admin/{url_key}", status_code= status.HTTP_200_OK)
async def peek_url(
        url_key : str , 
        session = Depends(get_db)
    ) : 
    pass
    
@router.delete("/admin/{url_key}")
async def delete_url(
    url_key : str,
    request : Request,
    session = Depends(get_db)
) : 
    short_url = get_db_url_by_key(session, url_key)
    if not short_url : 
        raise_not_found(request)
    
    short_url = deactivate_db_url_by_key(session, short_url)
    message = f"Successfully deleted shortened URL for '{short_url.target_url}'"
    return {"detail": message}


    
    