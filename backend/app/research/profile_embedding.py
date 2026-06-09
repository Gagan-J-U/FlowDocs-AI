from app.models.research_profile import (
    ResearchProfile
)


def build_profile_text(
    profile: ResearchProfile
):

    sections = []

    if profile.institution:

        sections.append(
            f"Institution: {profile.institution}"
        )

    if profile.department:

        sections.append(
            f"Department: {profile.department}"
        )

    if profile.skills:

        sections.append(
            f"Skills: {profile.skills}"
        )

    if profile.interests:

        sections.append(
            f"Research Interests: {profile.interests}"
        )

    if profile.bio:

        sections.append(
            f"Bio: {profile.bio}"
        )

    return "\n".join(
        sections
    )