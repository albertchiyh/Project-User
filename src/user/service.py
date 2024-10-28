from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from src.user.models import UserProfile
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by their ID"""
    return (db.query(UserProfile)
            .filter(UserProfile.user_id == user_id).first())

def get_user_by_email(db: Session, email: str):
    """Retrieve a user by their email address"""
    return (db.query(UserProfile)
            .filter(UserProfile.email_address == email).first())

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all users with pagination"""
    return paginate(db, select(UserProfile).order_by(UserProfile.user_id))

def create_user(db: Session, user: UserProfile):
    new_user = UserProfile(
        email_address=user.email_address,
        name=user.name,
        password=user.password,
        age=user.age,
        sex=user.sex,
        interest_list=user.interest_list,
        points=0,
        auth_token=None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, update_data: dict):
    """Update user information"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # If password is being updated, hash it
    if 'password' in update_data:
        update_data['password'] = pwd_context.hash(update_data['password'])
    
    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user_by_id(db: Session, user_id: int):
    """Delete a user by their ID"""
    user = (db.query(UserProfile)
            .filter(UserProfile.user_id == user_id).first())
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user_points(db: Session, user_id: int, points_change: int):
    """Update user points"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.points += points_change
    db.commit()
    db.refresh(user)
    return user

def update_auth_token(db: Session, user_id: int, new_token: str):
    """Update user's authentication token"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.auth_token = new_token
    db.commit()
    db.refresh(user)
    return user