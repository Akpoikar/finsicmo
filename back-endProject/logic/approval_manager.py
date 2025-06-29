from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..db.schema import ApprovalToggle
from ..db.session import get_session
from config import ApprovalStatus

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
                    "team1_status": self._status_to_string(toggle.team1_status),
                    "team2_status": self._status_to_string(toggle.team2_status)
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
    
    def get_field_status(self, field_name: str) -> Dict[str, int]:
        with get_session() as db:
            toggle = db.query(ApprovalToggle).filter(
                ApprovalToggle.field_name == field_name
            ).first()
            
            if not toggle:
                return {
                    "team1_status": ApprovalStatus.TBD,
                    "team2_status": ApprovalStatus.TBD
                }
            
            return {
                "team1_status": toggle.team1_status,
                "team2_status": toggle.team2_status
            }
    
    def _status_to_string(self, status: int) -> str:
        return "OK" if status == ApprovalStatus.OK else "TBD" 