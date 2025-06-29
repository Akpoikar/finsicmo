import os
from enum import IntEnum
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class ApprovalStatus(IntEnum):
    TBD = 0
    OK = 1

class SimulationType(Enum):
    GAME_1 = "game_1"
    GAME_2 = "game_2"

@dataclass
class DatabaseConfig:
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASS", "postgres")
    host: str = os.getenv("DB_HOST", "localhost")
    port: str = os.getenv("DB_PORT", "5432")
    name: str = os.getenv("DB_NAME", "simulation_game")
    
    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

@dataclass
class GameConfig:
    max_companies: int = 5
    max_investors: int = 5
    max_shares: int = 10000
    max_price: float = 1000.0
    min_price: float = 1.0

@dataclass
class DisplayConfig:
    table_format: str = "grid"
    max_name_length: int = 50
    refresh_interval: float = 0.5

class Config:
    db = DatabaseConfig()
    game = GameConfig()
    display = DisplayConfig()
    
    sample_companies: List[Dict] = [
        {"name": "TechCorp", "price": 10.0, "shares": 1000},
        {"name": "BioMed", "price": 15.0, "shares": 750},
        {"name": "GreenEnergy", "price": 12.5, "shares": 500},
    ]
    
    sample_investors: List[Dict] = [
        {"name": "Angel Fund"},
        {"name": "Growth Capital"},
        {"name": "Tech Ventures"},
    ] 