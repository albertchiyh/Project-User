from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    email_address: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    interest_list: Optional[List[str]] = None
    points: Optional[int] = None
    auth_token: Optional[str] = None
