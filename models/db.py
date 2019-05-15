from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'todo'
USERNAME = 'root'
PASSWORD = 'qwe123'
Db_Uri = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOST, PORT, DATABASE)

engine = create_engine(Db_Uri)
Base = declarative_base(engine)
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())

