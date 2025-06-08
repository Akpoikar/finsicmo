from sqlalchemy import select, update
from ..db.schema import toggles
from ..db.session import get_session

# Constants - might move these to config later
TEAM1 = "team1"
TEAM2 = "team2"
STATUS_OK = "OK"
STATUS_TBD = "TBD"

def set_toggle(field: str, team: str, status: str) -> bool:
    if team not in (TEAM1, TEAM2):
        return False  # silent fail for now
    
    with get_session() as session:
        existing = session.execute(
            select(toggles).where(toggles.c.field_name == field)
        ).first()
        
        if not existing:
            session.execute(
                toggles.insert().values(
                    field_name=field,
                    status_team1=STATUS_TBD,
                    status_team2=STATUS_TBD
                )
            )
        
        status_field = f"status_{team}"
        session.execute(
            update(toggles)
            .where(toggles.c.field_name == field)
            .values(**{status_field: status})
        )
    
    return True

def reset_team2_toggles():
    """Reset all Team 2 toggles to TBD when Team 1 updates data"""
    with get_session() as session:
        session.execute(
            update(toggles)
            .values(status_team2=STATUS_TBD)
        )

def check_all_ok() -> bool:
    """Check if all toggles are set to OK for both teams"""
    with get_session() as session:
        all_toggles = session.execute(select(toggles)).fetchall()
        return all(
            t.status_team1 == STATUS_OK and t.status_team2 == STATUS_OK
            for t in all_toggles
        )

# Left this in from testing - might be useful later
'''
def _debug_toggles():
    with get_session() as session:
        all_toggles = session.execute(select(toggles)).fetchall()
        for t in all_toggles:
            print(f"{t.field_name}: T1={t.status_team1}, T2={t.status_team2}")
''' 