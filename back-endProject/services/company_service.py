from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..db.schema import Company, ApprovalToggle
from ..db.session import get_session
from ..logic.approval_manager import ApprovalManager
from ..logic.validation_engine import ValidationEngine
from ..logic.status_manager import StatusManager
from config import Config, ApprovalStatus

class CompanyService:
    def __init__(self):
        self.config = Config.game
        self.approval_manager = ApprovalManager()
        self.validation_engine = ValidationEngine()
        self.status_manager = StatusManager()
    
    def get_all_companies(self) -> List[Dict]:
        with get_session() as db:
            companies = db.query(Company).all()
            return [
                {
                    "id": company.id,
                    "name": company.name,
                    "price": company.price,
                    "shares": company.shares,
                    "status": self._get_company_status(company.id)
                }
                for company in companies
            ]
    
    def update_company(self, company_id: int, price: Optional[float] = None, 
                      shares: Optional[int] = None) -> bool:
        if price is None and shares is None:
            return False
        
        company = self.get_company_by_id(company_id)
        if not company:
            return False
        
        new_price = price if price is not None else company["price"]
        new_shares = shares if shares is not None else company["shares"]
        
        is_valid, error_message = self.validation_engine.validate_company_data(
            company["name"], new_price, new_shares
        )
        
        if not is_valid:
            return False
        
        with get_session() as db:
            company_obj = db.query(Company).filter(Company.id == company_id).first()
            if not company_obj:
                return False
            
            if price is not None:
                company_obj.price = price
            if shares is not None:
                company_obj.shares = shares
            
            self.approval_manager.set_approval_status(
                f"company_{company_id}", "team1", ApprovalStatus.TBD
            )
            self.approval_manager.reset_team2_approvals()
            
            return True
    
    def create_company(self, name: str, price: float, shares: int) -> Optional[int]:
        is_valid, error_message = self.validation_engine.validate_company_data(name, price, shares)
        
        if not is_valid:
            return None
        
        with get_session() as db:
            company = Company(name=name, price=price, shares=shares)
            db.add(company)
            db.flush()
            
            self.approval_manager.create_company_approval(company.id)
            
            return company.id
    
    def get_company_by_id(self, company_id: int) -> Optional[Dict]:
        with get_session() as db:
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                return None
            
            return {
                "id": company.id,
                "name": company.name,
                "price": company.price,
                "shares": company.shares,
                "status": self._get_company_status(company.id)
            }
    
    def _get_company_status(self, company_id: int) -> str:
        field_status = self.approval_manager.get_field_status(f"company_{company_id}")
        return self.status_manager.get_company_status_display(
            field_status["team1_status"], 
            field_status["team2_status"]
        ) 