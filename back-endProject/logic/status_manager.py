from typing import Dict, List, Optional
from config import ApprovalStatus

class StatusManager:
    def __init__(self):
        self.status_enum = ApprovalStatus
    
    def status_to_string(self, status: int) -> str:
        """Convert numeric status to string representation."""
        return "OK" if status == ApprovalStatus.OK else "TBD"
    
    def string_to_status(self, status_str: str) -> Optional[int]:
        """Convert string status to numeric representation."""
        status_upper = status_str.upper()
        if status_upper == "OK":
            return ApprovalStatus.OK
        elif status_upper == "TBD":
            return ApprovalStatus.TBD
        return None
    
    def get_company_status_display(self, team1_status: int, team2_status: int) -> str:
        """Get human-readable company status."""
        if team1_status == ApprovalStatus.OK and team2_status == ApprovalStatus.OK:
            return "Complete"
        elif team1_status == ApprovalStatus.OK:
            return "Pending Team 2"
        elif team2_status == ApprovalStatus.OK:
            return "Pending Team 1"
        else:
            return "TBD"
    
    def get_bid_status_display(self, team1_status: int, team2_status: int) -> str:
        """Get human-readable bid status."""
        if team1_status == ApprovalStatus.OK and team2_status == ApprovalStatus.OK:
            return "Approved"
        elif team2_status == ApprovalStatus.OK:
            return "Pending Team 1"
        elif team1_status == ApprovalStatus.OK:
            return "Pending Team 2"
        else:
            return "TBD"
    
    def get_overall_status(self, team1_status: int, team2_status: int) -> str:
        """Get overall approval status."""
        if team1_status == ApprovalStatus.OK and team2_status == ApprovalStatus.OK:
            return "Complete"
        else:
            return "Pending"
    
    def format_approval_data(self, approvals: List[Dict]) -> List[Dict]:
        """Format approval data for display."""
        formatted = []
        for approval in approvals:
            team1_status = approval.get("team1_status", ApprovalStatus.TBD)
            team2_status = approval.get("team2_status", ApprovalStatus.TBD)
            
            if isinstance(team1_status, str):
                team1_status = self.string_to_status(team1_status) or ApprovalStatus.TBD
            if isinstance(team2_status, str):
                team2_status = self.string_to_status(team2_status) or ApprovalStatus.TBD
            
            formatted.append({
                "field_name": approval["field_name"],
                "team1_status": self.status_to_string(team1_status),
                "team2_status": self.status_to_string(team2_status),
                "overall_status": self.get_overall_status(team1_status, team2_status)
            })
        
        return formatted
    
    def get_status_color(self, status: str) -> str:
        """Get color code for status display."""
        status_lower = status.lower()
        if status_lower in ["ok", "complete", "approved"]:
            return "\033[92m"  # Green
        elif status_lower == "tbd":
            return "\033[93m"  # Yellow
        else:
            return "\033[91m"  # Red
    
    def get_subscription_color(self, status: str) -> str:
        """Get color code for subscription status display."""
        status_lower = status.lower()
        if "over" in status_lower:
            return "\033[92m"  # Green
        elif "fully" in status_lower:
            return "\033[94m"  # Blue
        else:
            return "\033[93m"  # Yellow 