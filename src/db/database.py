from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, echo=False)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

def save(model: SQLModel) -> None:
    with Session(engine) as session:
        session.add(model)
        session.commit()