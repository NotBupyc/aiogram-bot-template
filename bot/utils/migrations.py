from alembic.op import get_bind
from sqlalchemy.orm import Session


def get_session() -> Session:
    bind = get_bind()
    return Session(bind=bind)