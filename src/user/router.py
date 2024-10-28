from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from src.user.schemas import User
from . import service
from src.database import get_db

router = APIRouter()


@router.get("/users", response_model=Page[User])
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users with pagination"""
    return service.get_all_users(db)


@router.get("/user/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific user by ID"""
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a user by ID"""
    result = service.delete_user_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return {"message": "User deleted successfully"}


@router.post("/user", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: User,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    # Check if email already exists
    existing_user = service.get_user_by_email(db, user.email_address)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return service.create_user(db, user)


@router.put("/user/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user: User,
    db: Session = Depends(get_db)
):
    """Update a user's information"""
    updated_user = service.update_user(db, user_id, user.model_dump(exclude_unset=True))
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return updated_user


@router.patch("/user/{user_id}/points")
async def update_user_points(
    user_id: int,
    points_change: int,
    db: Session = Depends(get_db)
):
    """Update a user's points"""
    updated_user = service.update_user_points(db, user_id, points_change)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return {"message": "Points updated successfully", "new_points": updated_user.points}