from .models import URL
from sqlalchemy.orm import Session 

from .utils import create_random_key, create_unique_key
import secrets
from typing import Union

from .schemas import BaseURL

def get_db_url_by_key(db : Session , url_key : str) -> URL : 
    return db.query(URL).filter(URL.key == url_key , URL.is_active == True).first()

def get_db_url_by_admin_key(db : Session, admin_key : str) -> URL :
    return db.query(URL).filter(URL.admin_key == admin_key , URL.is_active == True).first()

def create_db_url(db : Session , url : BaseURL , custom_key : Union[str, None] = None) -> URL:
    key = create_unique_key(db, 5) if custom_key is None else custom_key
    admin_key = f"{key}_{create_random_key(8)}"

    short_url = URL( 
        target_url = url.target_url,
        key = key,
        admin_key = admin_key,
        is_active = True,
        clicks = 0,
    )

    db.add(short_url)
    db.commit()
    db.refresh(short_url)

    return short_url


def update_db_url_clicks(db : Session , db_url : URL) -> URL : 
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_db_url_by_key(db : Session , db_url : URL) : 
    db_url.is_active = False
    db.commit()
    db.refresh(db_url)
    return db_url