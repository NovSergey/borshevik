import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
#
SqlAlchemyBase = dec.declarative_base()
__factory = None



def global_init(user, password, host, database):
    global __factory
    if __factory:
        return
    conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}".format(user, password, host, database)
    print(f"Подключение к базе данных по адресу {conn_str}")
    engine = sa.create_engine(url=conn_str)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)
    try:
        print(
            f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

def global_init_sql(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=True)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()


