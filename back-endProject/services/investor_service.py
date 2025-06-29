from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..db.schema import Investor, Bid, Company, ApprovalToggle
from ..db.session import get_session
from ..logic.approval_manager import ApprovalManager
from ..logic.validation_engine import ValidationEngine
from ..logic.status_manager import StatusManager
from config import Config, ApprovalStatus

class InvestorService:
    def __init__(self):
        self.config = Config.game
        self.approval_manager = ApprovalManager()
        self.validation_engine = ValidationEngine()
        self.status_manager = StatusManager()
    
    def get_all_investors_with_bids(self) -> List[Dict]:
        with get_session() as db:
            investors = db.query(Investor).all()
            companies = db.query(Company).all()
            
            result = []
            for investor in investors:
                bids = db.query(Bid).filter(Bid.investor_id == investor.id).all()
                bids_dict = {
                    next(c.name for c in companies if c.id == b.company_id): b.shares_bid
                    for b in bids
                }
                
                result.append({
                    "id": investor.id,
                    "name": investor.name,
                    "bids": bids_dict
                })
            
            return result
    
    def update_bid(self, investor_id: int, company_id: int, shares: int) -> bool:
        is_valid, error_message = self.validation_engine.validate_bid_data(
            investor_id, company_id, shares
        )
        
        if not is_valid:
            return False
        
        with get_session() as db:
            existing_bid = db.query(Bid).filter(
                Bid.investor_id == investor_id,
                Bid.company_id == company_id
            ).first()
            
            if existing_bid:
                existing_bid.shares_bid = shares
            else:
                new_bid = Bid(
                    investor_id=investor_id,
                    company_id=company_id,
                    shares_bid=shares
                )
                db.add(new_bid)
            
            self.approval_manager.set_approval_status(
                f"bid_{investor_id}_{company_id}", "team2", ApprovalStatus.TBD
            )
            
            return True
    
    def create_investor(self, name: str) -> Optional[int]:
        is_valid, error_message = self.validation_engine.validate_investor_data(name)
        
        if not is_valid:
            return None
        
        with get_session() as db:
            investor = Investor(name=name)
            db.add(investor)
            db.flush()
            return investor.id
    
    def get_investor_by_id(self, investor_id: int) -> Optional[Dict]:
        with get_session() as db:
            investor = db.query(Investor).filter(Investor.id == investor_id).first()
            if not investor:
                return None
            
            bids = db.query(Bid).filter(Bid.investor_id == investor_id).all()
            companies = db.query(Company).all()
            
            bids_dict = {
                next(c.name for c in companies if c.id == b.company_id): b.shares_bid
                for b in bids
            }
            
            return {
                "id": investor.id,
                "name": investor.name,
                "bids": bids_dict
            }
    
    def get_bid_status(self, investor_id: int, company_id: int) -> str:
        field_status = self.approval_manager.get_field_status(f"bid_{investor_id}_{company_id}")
        return self.status_manager.get_bid_status_display(
            field_status["team1_status"], 
            field_status["team2_status"]
        )
    
    def approve_bid(self, investor_id: int, company_id: int) -> bool:
        return self.approval_manager.set_approval_status(
            f"bid_{investor_id}_{company_id}", "team2", ApprovalStatus.OK
        ) 