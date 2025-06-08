from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base

# TODO: move this to config file later
DB_URL = "postgresql://postgres:postgres@localhost:5432/simulation_game"

# tried both psycopg2 and asyncpg, this works better for now
engine = create_engine(DB_URL)
metadata = MetaData()

companies = Table(
    'companies', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('price', Float),
    Column('shares', Integer),
)

investors = Table(
    'investors', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
)

# debug print removed
# print("Creating tables...")

bids = Table(
    'bids', metadata,
    Column('id', Integer, primary_key=True),
    Column('investor_id', Integer, ForeignKey('investors.id')),
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('shares_bid', Integer),
)

toggles = Table(
    'toggles', metadata,
    Column('field_name', String(50), primary_key=True),
    Column('status_team1', String(10)),  # OK or TBD
    Column('status_team2', String(10)),
)

calculated_outputs = Table(
    'calculated_outputs', metadata,
    Column('company_id', Integer, ForeignKey('companies.id'), primary_key=True),
    Column('total_bid', Integer),
    Column('capital_raised', Float),
    Column('subscription_status', String(20)),
)

def init_db():
    metadata.create_all(engine)
    # maybe add some sample data here later
    return engine 