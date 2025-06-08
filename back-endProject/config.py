import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "simulation_game")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Game settings
NUM_COMPANIES = 3
NUM_INVESTORS = 3

# Sample data
SAMPLE_COMPANIES = [
    {"name": "TechCorp", "price": 10.0, "shares": 1000},
    {"name": "BioMed", "price": 15.0, "shares": 750},
    {"name": "GreenEnergy", "price": 12.5, "shares": 500},
]

SAMPLE_INVESTORS = [
    {"name": "Angel Fund"},
    {"name": "Growth Capital"},
    {"name": "Tech Ventures"},
]

# Status flags
STATUS_OK = "OK"
STATUS_TBD = "TBD"

# Display settings
TABLE_FORMAT = "grid"
MAX_NAME_LENGTH = 50 