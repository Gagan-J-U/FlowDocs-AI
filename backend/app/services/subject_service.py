from app.models.subject import Subject


def create_subject(db, data):
    subject = Subject(name=data.name)

    db.add(subject)
    db.commit()
    db.refresh(subject)

    return subject


def get_subjects(db):
    return db.query(Subject).all()