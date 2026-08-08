from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from config.settings import settings
from contextlib import contextmanager


engine = create_engine(settings.DATABASE_URL, future=True, pool_pre_ping=True)


Base = automap_base()

Base.prepare(autoload_with=engine)
Job = Base.classes.Job
JobMeta = Base.classes.JobMeta
JobPlatform = Base.classes.JobPlatform
Company = Base.classes.Company

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
