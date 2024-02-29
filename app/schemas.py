from pydantic import BaseModel

class BaseURL(BaseModel) : 
    target_url : str 

class URL(BaseURL) : 
    is_active : bool
    clicks : int

class URLInfo(URL) : 
    key : str
    admin_key : str