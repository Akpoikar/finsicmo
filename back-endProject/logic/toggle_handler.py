from typing import List, Optional
from sqlalchemy.orm import Session
from ..db.schema import ApprovalToggle, Company, Bid
from ..db.session import get_session
from config import ApprovalStatus
from ..logic.approval_manager import ApprovalManager
from ..logic.status_manager import StatusManager

class ApprovalManager:
    def __init__(self):
        self.status_enum = ApprovalStatus
    
    def set_approval_status(self, field_name: str, team: str, status: ApprovalStatus) -> bool:
        if team not in ["team1", "team2"]:
            return False
        
        with get_session() as db:
            toggle = db.query(ApprovalToggle).filter(
                ApprovalToggle.field_name == field_name
            ).first()
            
            if not toggle:
                toggle = ApprovalToggle(
                    field_name=field_name,
                    team1_status=ApprovalStatus.TBD,
                    team2_status=ApprovalStatus.TBD
                )
                db.add(toggle)
            
            if team == "team1":
                toggle.team1_status = status
            else:
                toggle.team2_status = status
            
            return True
    
    def reset_team2_approvals(self) -> None:
        with get_session() as db:
            db.query(ApprovalToggle).update({
                ApprovalToggle.team2_status: ApprovalStatus.TBD
            })
    
    def check_all_approved(self) -> bool:
        with get_session() as db:
            toggles = db.query(ApprovalToggle).all()
            return all(
                toggle.team1_status == ApprovalStatus.OK and 
                toggle.team2_status == ApprovalStatus.OK
                for toggle in toggles
            )
    
    def get_pending_approvals(self) -> List[Dict]:
        with get_session() as db:
            toggles = db.query(ApprovalToggle).all()
            return [
                {
                    "field_name": toggle.field_name,
                    "team1_status": toggle.team1_status.value,
                    "team2_status": toggle.team2_status.value
                }
                for toggle in toggles
            ]
    
    def create_company_approval(self, company_id: int) -> None:
        field_name = f"company_{company_id}"
        self.set_approval_status(field_name, "team1", ApprovalStatus.TBD)
        self.set_approval_status(field_name, "team2", ApprovalStatus.TBD)
    
    def create_bid_approval(self, investor_id: int, company_id: int) -> None:
        field_name = f"bid_{investor_id}_{company_id}"
        self.set_approval_status(field_name, "team1", ApprovalStatus.TBD)
        self.set_approval_status(field_name, "team2", ApprovalStatus.TBD)

def set_toggle(field: str, team: str, status: str) -> bool:
    """Set approval toggle for a field."""
    manager = ApprovalManager()
    status_manager = StatusManager()
    
    status_enum = status_manager.string_to_status(status)
    if status_enum is None:
        return False
    
    return manager.set_approval_status(field, team, status_enum)

def reset_team2_toggles() -> None:
    """Reset all Team 2 toggles to TBD."""
    manager = ApprovalManager()
    manager.reset_team2_approvals()

def check_all_ok() -> bool:
    """Check if all toggles are approved."""
    manager = ApprovalManager()
    return manager.check_all_approved()

def get_pending_approvals() -> list:
    """Get all pending approvals."""
    manager = ApprovalManager()
    return manager.get_pending_approvals()

def get_field_status(field_name: str) -> dict:
    """Get status for a specific field."""
    manager = ApprovalManager()
    return manager.get_field_status(field_name)

# Left this in from testing - might be useful later
'''
def _debug_toggles():
    with get_session() as session:
        all_toggles = session.execute(select(toggles)).fetchall()
        for t in all_toggles:
            print(f"{t.field_name}: T1={t.status_team1}, T2={t.status_team2}")
''' 