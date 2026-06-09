from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.api.dependencies.auth import (
    get_current_user
)

from app.models.user import User

from app.schemas.research_profile import (
    ResearchProfileCreate
)

from app.services.research_profile_service import (
    upsert_research_profile,
    get_profile,
    discover_researchers,
    similar_researchers,
)


router = APIRouter(

    prefix="/research",

    tags=["Research"]
)


# ==========================================
# CREATE / UPDATE PROFILE
# ==========================================

@router.put("/profile")
def update_profile(

    payload: ResearchProfileCreate,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return upsert_research_profile(

        db=db,

        user_id=current_user.id,

        payload=payload
    )


# ==========================================
# CURRENT USER PROFILE
# ==========================================

@router.get("/profile")
def my_profile(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_profile(

        db=db,

        user_id=current_user.id
    )


# ==========================================
# GET PROFILE BY USER ID
# ==========================================

@router.get("/profile/{user_id}")
def profile_by_user(

    user_id: str,

    db: Session = Depends(
        get_db
    )
):

    return get_profile(

        db=db,

        user_id=user_id
    )


# ==========================================
# DISCOVER RESEARCHERS
# ==========================================

@router.get("/discover")
def discover(

    query: str = Query(...),

    top_k: int = Query(
        10,
        ge=1,
        le=50
    ),

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    matches = discover_researchers(

        db=db,

        query=query,

        current_user_id=
        current_user.id,

        top_k=top_k
    )

    return [
        {
            "id": match["profile"].id,
            "user_id": match["profile"].user_id,
            "username": (
                match["profile"].user.username
                if match["profile"].user
                else None
            ),
            "bio": match["profile"].bio,
            "institution": match["profile"].institution,
            "department": match["profile"].department,
            "skills": match["profile"].skills,
            "interests": match["profile"].interests,
            "github_url": match["profile"].github_url,
            "linkedin_url": match["profile"].linkedin_url,
            "website_url": match["profile"].website_url,
            "visibility": match["profile"].visibility,
            "created_at": match["profile"].created_at,
            "updated_at": match["profile"].updated_at,
            "similarity_score": match["score"],
        }
        for match in matches
        if match.get("profile")
    ]


# ==========================================
# SIMILAR RESEARCHERS
# ==========================================

@router.get("/similar")
def similar(
    top_k: int = Query(
        10,
        ge=1,
        le=50
    ),
    db: Session = Depends(
        get_db
    ),
    current_user: User = Depends(
        get_current_user
    )
):
    matches = similar_researchers(
        db=db,
        user_id=current_user.id,
        top_k=top_k
    )

    return [
        {
            "id": match["profile"].id,
            "user_id": match["profile"].user_id,
            "username": (
                match["profile"].user.username
                if match["profile"].user
                else None
            ),
            "bio": match["profile"].bio,
            "institution": match["profile"].institution,
            "department": match["profile"].department,
            "skills": match["profile"].skills,
            "interests": match["profile"].interests,
            "github_url": match["profile"].github_url,
            "linkedin_url": match["profile"].linkedin_url,
            "website_url": match["profile"].website_url,
            "visibility": match["profile"].visibility,
            "created_at": match["profile"].created_at,
            "updated_at": match["profile"].updated_at,
            "similarity_score": match["score"],
        }
        for match in matches
        if match.get("profile")
    ]
