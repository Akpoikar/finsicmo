from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db.schema import Company, Investor, Bid
from ..db.session import get_session
from config import Config, ApprovalStatus

class ValidationEngine:
    def __init__(self):
        self.config = Config.game
    
    def validate_company_data(self, name: str, price: float, shares: int) -> Tuple[bool, str]:
        if not name or len(name.strip()) == 0:
            return False, "Company name cannot be empty"
        
        if not self._validate_price(price):
            return False, f"Price must be between ${self.config.min_price} and ${self.config.max_price}"
        
        if not self._validate_shares(shares):
            return False, f"Shares must be between 1 and {self.config.max_shares}"
        
        if not self._validate_company_name_unique(name):
            return False, "Company name must be unique"
        
        return True, "Valid company data"
    
    def validate_investor_data(self, name: str) -> Tuple[bool, str]:
        if not name or len(name.strip()) == 0:
            return False, "Investor name cannot be empty"
        
        if not self._validate_investor_name_unique(name):
            return False, "Investor name must be unique"
        
        return True, "Valid investor data"
    
    def validate_bid_data(self, investor_id: int, company_id: int, shares: int) -> Tuple[bool, str]:
        if shares < 0:
            return False, "Bid shares cannot be negative"
        
        if not self._validate_investor_exists(investor_id):
            return False, "Investor does not exist"
        
        if not self._validate_company_exists(company_id):
            return False, "Company does not exist"
        
        if not self._validate_bid_within_limits(company_id, shares):
            return False, "Bid exceeds company share limits"
        
        return True, "Valid bid data"
    
    def validate_approval_status(self, status: str) -> Tuple[bool, str]:
        try:
            status_enum = ApprovalStatus[status.upper()]
            return True, "Valid approval status"
        except KeyError:
            return False, "Invalid approval status. Use 'TBD' or 'OK'"
    
    def validate_game_state(self) -> Tuple[bool, str]:
        with get_session() as db:
            company_count = db.query(Company).count()
            investor_count = db.query(Investor).count()
            
            if company_count == 0:
                return False, "No companies available for simulation"
            
            if investor_count == 0:
                return False, "No investors available for simulation"
            
            if company_count > self.config.max_companies:
                return False, f"Too many companies. Maximum allowed: {self.config.max_companies}"
            
            if investor_count > self.config.max_investors:
                return False, f"Too many investors. Maximum allowed: {self.config.max_investors}"
            
            return True, "Valid game state"
    
    def get_validation_summary(self) -> Dict:
        with get_session() as db:
            companies = db.query(Company).all()
            investors = db.query(Investor).all()
            bids = db.query(Bid).all()
            
            return {
                "total_companies": len(companies),
                "total_investors": len(investors),
                "total_bids": len(bids),
                "companies_with_bids": len(set(bid.company_id for bid in bids)),
                "investors_with_bids": len(set(bid.investor_id for bid in bids)),
                "validation_errors": self._get_validation_errors(db)
            }
    
    def _validate_price(self, price: float) -> bool:
        return self.config.min_price <= price <= self.config.max_price
    
    def _validate_shares(self, shares: int) -> bool:
        return 0 < shares <= self.config.max_shares
    
    def _validate_company_name_unique(self, name: str) -> bool:
        with get_session() as db:
            existing = db.query(Company).filter(Company.name == name).first()
            return existing is None
    
    def _validate_investor_name_unique(self, name: str) -> bool:
        with get_session() as db:
            existing = db.query(Investor).filter(Investor.name == name).first()
            return existing is None
    
    def _validate_investor_exists(self, investor_id: int) -> bool:
        with get_session() as db:
            investor = db.query(Investor).filter(Investor.id == investor_id).first()
            return investor is not None
    
    def _validate_company_exists(self, company_id: int) -> bool:
        with get_session() as db:
            company = db.query(Company).filter(Company.id == company_id).first()
            return company is not None
    
    def _validate_bid_within_limits(self, company_id: int, shares: int) -> bool:
        with get_session() as db:
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                return False
            
            existing_bids = db.query(func.sum(Bid.shares_bid)).filter(
                Bid.company_id == company_id
            ).scalar() or 0
            
            return existing_bids + shares <= company.shares * 2  # Allow some oversubscription
    
    def _get_validation_errors(self, db: Session) -> List[str]:
        errors = []
        
        companies = db.query(Company).all()
        for company in companies:
            if company.price <= 0:
                errors.append(f"Company '{company.name}' has invalid price: ${company.price}")
            if company.shares <= 0:
                errors.append(f"Company '{company.name}' has invalid shares: {company.shares}")
        
        return errors 