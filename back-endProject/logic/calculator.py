from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db.schema import Company, Bid, CalculatedOutput
from ..db.session import get_session
from config import Config
from ..logic.calculation_engine import CalculationEngine

class SimulationCalculator:
    def __init__(self):
        self.config = Config.game
    
    def calculate_company_outputs(self, db: Session) -> List[Dict]:
        companies = db.query(Company).all()
        results = []
        
        for company in companies:
            total_bid = db.query(func.sum(Bid.shares_bid)).filter(
                Bid.company_id == company.id
            ).scalar() or 0
            
            capital_raised = company.price * min(total_bid, company.shares)
            subscription_status = self._determine_subscription_status(total_bid, company.shares)
            
            self._update_or_create_output(db, company.id, total_bid, capital_raised, subscription_status)
            
            results.append({
                "company_name": company.name,
                "total_bid": total_bid,
                "capital_raised": capital_raised,
                "subscription_status": subscription_status,
                "price": company.price,
                "shares_offered": company.shares
            })
        
        return results
    
    def _determine_subscription_status(self, total_bid: int, shares_offered: int) -> str:
        if total_bid > shares_offered:
            return "Over-subscribed"
        elif total_bid == shares_offered:
            return "Fully-subscribed"
        else:
            return "Under-subscribed"
    
    def _update_or_create_output(self, db: Session, company_id: int, total_bid: int, 
                                capital_raised: float, subscription_status: str) -> None:
        existing_output = db.query(CalculatedOutput).filter(
            CalculatedOutput.company_id == company_id
        ).first()
        
        if existing_output:
            existing_output.total_bid = total_bid
            existing_output.capital_raised = capital_raised
            existing_output.subscription_status = subscription_status
        else:
            new_output = CalculatedOutput(
                company_id=company_id,
                total_bid=total_bid,
                capital_raised=capital_raised,
                subscription_status=subscription_status
            )
            db.add(new_output)
    
    def get_investor_summary(self, db: Session) -> List[Dict]:
        investors = db.query(Company).join(Bid).group_by(Company.id).all()
        summary = []
        
        for company in investors:
            bids = db.query(Bid).filter(Bid.company_id == company.id).all()
            total_investors = len(set(bid.investor_id for bid in bids))
            avg_bid = sum(bid.shares_bid for bid in bids) / len(bids) if bids else 0
            
            summary.append({
                "company_name": company.name,
                "total_investors": total_investors,
                "average_bid": avg_bid,
                "total_bids": len(bids)
            })
        
        return summary

def recalculate_outputs():
    """Recalculate all simulation outputs."""
    calculator = CalculationEngine()
    with get_session() as db:
        return calculator.calculate_company_outputs(db)

def get_investor_summary():
    """Get investor summary statistics."""
    calculator = CalculationEngine()
    with get_session() as db:
        return calculator.calculate_investor_summary(db)

def get_market_statistics():
    """Get overall market statistics."""
    calculator = CalculationEngine()
    with get_session() as db:
        return calculator.calculate_market_statistics(db)
