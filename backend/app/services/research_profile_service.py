from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi import status

from app.models.research_profile import (
    ResearchProfile
)

from app.schemas.research_profile import (
    ResearchProfileCreate
)

from app.embeddings.embedding_service import (
    generate_embedding,
    generate_embeddings
)

from app.research.profile_embedding import (
    build_profile_text
)

from app.vectorstore.research_faiss import (
    search_profiles,
    rebuild_profile_index
)


# ==========================================
# CREATE OR UPDATE PROFILE
# ==========================================

def upsert_research_profile(

    db: Session,

    user_id: str,

    payload: ResearchProfileCreate
):

    profile = (

        db.query(
            ResearchProfile
        )

        .filter(
            ResearchProfile.user_id
            == user_id
        )

        .first()
    )

    if profile is None:

        profile = ResearchProfile(

            user_id=user_id
        )

        db.add(
            profile
        )

    profile.bio = payload.bio

    profile.institution = (
        payload.institution
    )

    profile.department = (
        payload.department
    )

    profile.skills = (
        payload.skills
    )

    profile.interests = (
        payload.interests
    )

    profile.github_url = (
        payload.github_url
    )

    profile.linkedin_url = (
        payload.linkedin_url
    )

    profile.website_url = (
        payload.website_url
    )

    profile.visibility = (
        payload.visibility
    )

    db.commit()

    db.refresh(
        profile
    )

    rebuild_research_index(
        db
    )

    return profile


# ==========================================
# GET PROFILE
# ==========================================

def get_profile(

    db: Session,

    user_id: str
):

    profile = (

        db.query(
            ResearchProfile
        )

        .filter(
            ResearchProfile.user_id
            == user_id
        )

        .first()
    )

    if profile is None:

        raise HTTPException(

            status_code=
            status.HTTP_404_NOT_FOUND,

            detail=
            "Research profile not found"
        )

    return profile


# ==========================================
# DISCOVER RESEARCHERS
# ==========================================

def discover_researchers(

    db: Session,

    query: str,

    current_user_id: str | None = None,

    top_k: int = 10
):

    query_embedding = (
        generate_embedding(
            query
        )
    )

    matches = search_profiles(

        query_embedding=query_embedding,

        top_k=top_k * 2
    )

    profile_ids = [

        match["profile_id"]

        for match in matches
    ]

    if not profile_ids:

        return []

    profiles = (

        db.query(
            ResearchProfile
        )

        .filter(
            ResearchProfile.id.in_(
                profile_ids
            )
        )

        .all()
    )

    profile_map = {

        profile.id: profile

        for profile in profiles
    }

    results = []

    for match in matches:

        profile = profile_map.get(
            match["profile_id"]
        )

        if not profile:
            continue

        if (

            current_user_id

            and

            profile.user_id
            == current_user_id
        ):
            continue

        results.append({
            "profile": profile,
            "score": match["score"],
            "username": (
                profile.user.username
                if profile.user
                else None
            ),
        })

        if len(results) >= top_k:
            break

    return results


# ==========================================
# SIMILAR RESEARCHERS
# ==========================================

def similar_researchers(
    db: Session,
    user_id: str,
    top_k: int = 10
):
    profile = (
        db.query(ResearchProfile)
        .filter(ResearchProfile.user_id == user_id)
        .first()
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research profile not found"
        )

    profile_text = build_profile_text(profile)
    query_embedding = generate_embedding(profile_text)
    matches = search_profiles(
        query_embedding=query_embedding,
        top_k=top_k * 2,
    )

    profile_ids = [match["profile_id"] for match in matches]
    if not profile_ids:
        return []

    profiles = (
        db.query(ResearchProfile)
        .filter(
            ResearchProfile.id.in_(profile_ids),
            ResearchProfile.visibility != "private"
        )
        .all()
    )

    profile_map = {profile.id: profile for profile in profiles}
    results = []

    for match in matches:
        profile = profile_map.get(match["profile_id"])
        if not profile:
            continue
        if profile.user_id == user_id:
            continue

        results.append({
            "profile": profile,
            "score": match["score"],
        })
        if len(results) >= top_k:
            break

    return results


# ==========================================
# REBUILD RESEARCH INDEX
# ==========================================

def rebuild_research_index(

    db: Session
):

    profiles = (

        db.query(
            ResearchProfile
        )

        .filter(
            ResearchProfile.visibility
            != "private"
        )

        .all()
    )

    if not profiles:

        return

    profile_texts = []

    profile_ids = []

    for profile in profiles:

        profile_texts.append(

            build_profile_text(
                profile
            )
        )

        profile_ids.append(
            profile.id
        )

    embeddings = (
        generate_embeddings(
            profile_texts
        )
    )

    rebuild_profile_index(

        embeddings=embeddings,

        profile_ids=profile_ids
    )