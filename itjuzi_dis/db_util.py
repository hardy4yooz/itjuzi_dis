# coding:utf-8

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
url = 'mysql+pymysql://root:root@192.168.0.7/spider_tools?charset=utf8'
engine = create_engine(url, echo=False)


class DB_Util(object):
    @staticmethod
    def get_session(url=None):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    @staticmethod
    def init_db():
        Base.metadata.create_all(engine)


class JuziCompany(Base):
    __tablename__ = 't_juzi_company'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=True)
    slogan = Column(String(100), nullable=True)
    scope = Column(String(30), nullable=True)
    sub_scope = Column(String(30), nullable=True)
    city = Column(String(30),nullable=True)
    area = Column(String(30),nullable=True)
    home_page = Column(String(100), nullable=True)
    tags = Column(String(200))
    company_intro = Column(String(500), nullable=True)
    company_full_name = Column(String(100), nullable=True)
    found_time = Column(String(10), nullable=True)
    company_size = Column(String(20), nullable=True)
    company_status = Column(String(20), nullable=True)
    info_id = Column(String(20), nullable=False)


class JuziTeam(Base):
    __tablename__ = 't_juzi_team'
    id = Column(Integer, primary_key=True)
    company_id = Column(String(20), nullable=False)
    tm_m_name = Column(String(100), nullable=True)
    tm_m_title = Column(String(100), nullable=True)
    tm_m_intro = Column(String(500), nullable=True)


class JuziTz(Base):
    __tablename__ = 't_juzi_tz'
    company_id = Column(String(20), nullable=False)
    id = Column(Integer, primary_key=True)
    tz_time = Column(String(100), nullable=True)
    tz_round = Column(String(20), nullable=True)
    tz_finades = Column(String(100), nullable=True)
    tz_capital = Column(String(500), nullable=True)


class JuziProduct(Base):
    __tablename__ = 't_juzi_product'
    company_id = Column(String(20), nullable=False)
    id = Column(Integer, primary_key=True)
    pdt_name = Column(String(100), nullable=True)
    pdt_type = Column(String(100), nullable=True)
    pdt_intro = Column(String(500), nullable=True)
