from typing import List, Dict, Optional, Tuple
from .approval_manager import ApprovalManager
from .calculation_engine import CalculationEngine
from .validation_engine import ValidationEngine
from .status_manager import StatusManager
from ..db.session import get_session
from config import ApprovalStatus

class GameCoordinator:
    def __init__(self):
        self.approval_manager = ApprovalManager()
        self.calculation_engine = CalculationEngine()
        self.validation_engine = ValidationEngine()
        self.status_manager = StatusManager()
    
    def get_game_status(self) -> Dict:
        """Get comprehensive game status including validation and approval state."""
        with get_session() as db:
            validation_summary = self.validation_engine.get_validation_summary()
            market_stats = self.calculation_engine.calculate_market_statistics(db)
            pending_approvals = self.approval_manager.get_pending_approvals()
            
            return {
                "validation": validation_summary,
                "market_statistics": market_stats,
                "pending_approvals": pending_approvals,
                "all_approved": self.approval_manager.check_all_approved(),
                "game_ready": self._is_game_ready()
            }
    
    def validate_and_update_company(self, company_id: int, price: Optional[float] = None, 
                                  shares: Optional[int] = None) -> Tuple[bool, str]:
        """Validate and update company data with proper error handling."""
        if price is None and shares is None:
            return False, "No changes specified"
        
        # Get current company data for validation
        with get_session() as db:
            from ..db.schema import Company
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                return False, "Company not found"
            
            new_price = price if price is not None else company.price
            new_shares = shares if shares is not None else company.shares
            
            is_valid, error_message = self.validation_engine.validate_company_data(
                company.name, new_price, new_shares
            )
            
            if not is_valid:
                return False, error_message
            
            # Update the data
            if price is not None:
                company.price = price
            if shares is not None:
                company.shares = shares
            
            # Reset approvals
            self.approval_manager.set_approval_status(
                f"company_{company_id}", "team1", ApprovalStatus.TBD
            )
            self.approval_manager.reset_team2_approvals()
            
            return True, "Company updated successfully"
    
    def validate_and_update_bid(self, investor_id: int, company_id: int, shares: int) -> Tuple[bool, str]:
        """Validate and update bid data with proper error handling."""
        is_valid, error_message = self.validation_engine.validate_bid_data(
            investor_id, company_id, shares
        )
        
        if not is_valid:
            return False, error_message
        
        with get_session() as db:
            from ..db.schema import Bid
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
            
            return True, "Bid updated successfully"
    
    def approve_field(self, field_name: str, team: str) -> Tuple[bool, str]:
        """Approve a specific field for a team."""
        is_valid, error_message = self.validation_engine.validate_approval_status("OK")
        
        if not is_valid:
            return False, error_message
        
        success = self.approval_manager.set_approval_status(field_name, team, ApprovalStatus.OK)
        if success:
            return True, f"Field '{field_name}' approved for {team}"
        else:
            return False, f"Failed to approve field '{field_name}' for {team}"
    
    def get_simulation_results(self) -> Dict:
        """Get complete simulation results if all data is approved."""
        if not self.approval_manager.check_all_approved():
            return {
                "ready": False,
                "message": "Cannot calculate results until all data is approved"
            }
        
        with get_session() as db:
            company_results = self.calculation_engine.calculate_company_outputs(db)
            investor_summary = self.calculation_engine.calculate_investor_summary(db)
            market_stats = self.calculation_engine.calculate_market_statistics(db)
            
            return {
                "ready": True,
                "company_results": company_results,
                "investor_summary": investor_summary,
                "market_statistics": market_stats
            }
    
    def get_approval_summary(self) -> Dict:
        """Get detailed approval summary with status information."""
        pending_approvals = self.approval_manager.get_pending_approvals()
        formatted_approvals = self.status_manager.format_approval_data(pending_approvals)
        
        team1_pending = sum(1 for a in formatted_approvals if a["team1_status"] == "TBD")
        team2_pending = sum(1 for a in formatted_approvals if a["team2_status"] == "TBD")
        complete = sum(1 for a in formatted_approvals if a["overall_status"] == "Complete")
        
        return {
            "total_fields": len(formatted_approvals),
            "team1_pending": team1_pending,
            "team2_pending": team2_pending,
            "complete": complete,
            "all_approved": self.approval_manager.check_all_approved(),
            "approvals": formatted_approvals
        }
    
    def _is_game_ready(self) -> bool:
        """Check if the game is ready to run simulation."""
        is_valid, _ = self.validation_engine.validate_game_state()
        return is_valid and self.approval_manager.check_all_approved() 