class ResearchProfile(Base):
    __tablename__ = "research_profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    full_name = Column(String)

    bio = Column(Text)

    institution = Column(String)

    research_interests = Column(JSON)

    skills = Column(JSON)