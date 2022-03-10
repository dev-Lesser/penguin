import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import pymysql
pymysql.install_as_MySQLdb()

USER_NAME       = os.environ['USER_NAME']
USER_PASSWORD   = os.environ['USER_PASSWORD']
DB_HOST         = os.environ['DB_HOST']
DB_NAME         = os.environ['DB_NAME']

DATABASES = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    USER_NAME,
    USER_PASSWORD,
    DB_HOST,
    DB_NAME
)
ENGINE = create_engine(
    DATABASES,
    encoding="utf-8",
    echo=True,
)

BASE = declarative_base()


def create_db_engine(db_conn_string, debug_mode=True):
    return create_engine(
        db_conn_string,
        echo=debug_mode,
        pool_size=10,
        max_overflow=0,
        pool_recycle=3600,
        pool_pre_ping=True,
        pool_use_lifo=True,
        encoding="utf-8"
    )


def create_db_session(engine):
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return session()


@contextmanager
def db_session(engine):
    engine = create_db_engine(db_conn_string = DATABASES)
    db = create_db_session(engine)
    try:
        yield db
    except:
        db.rollback()
        print('db connection rollback')
    finally:
        print('db connection closed')
        db.close()
