import logging
from lib.sqlalchemy import create_engine

#DATABASE CONNECTION
logging.log(logging.INFO, "")
logging.log(logging.INFO, "LOCAL")
# Running in development, so use a local MySQL database.

engine = create_engine("mysql+mysqldb://root@localhost/Articles?charset=utf8", echo=False, pool_size=20)

# [otd:1901] http://stackoverflow.com/questions/28824401/sqlalchemy-attempting-to-twice-delete-many-to-many-secondary-relationship
engine.dialect.supports_sane_rowcount = engine.dialect.supports_sane_multi_rowcount = False


logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
