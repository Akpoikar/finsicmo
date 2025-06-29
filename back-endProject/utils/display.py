from typing import List, Dict, Optional
from tabulate import tabulate
from config import Config

class DisplayFormatter:
    def __init__(self):
        self.config = Config.display
        self.colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "reset": "\033[0m"
        }
    
    def format_company_table(self, companies: List[Dict]) -> str:
        if not companies:
            return "No company data available"
        
        headers = ["ID", "Company", "Price", "Shares", "Status"]
        rows = []
        
        for company in companies:
            status = company.get("status", "TBD")
            status_color = self._get_status_color(status)
            
            rows.append([
                company.get("id", ""),
                self._truncate_text(company["name"]),
                f"${company['price']:.2f}",
                f"{company['shares']:,}",
                f"{status_color}{status}{self.colors['reset']}"
            ])
        
        return tabulate(rows, headers=headers, tablefmt=self.config.table_format)
    
    def format_investor_table(self, investors: List[Dict]) -> str:
        if not investors:
            return "No investor data available"
        
        companies = list(investors[0]["bids"].keys()) if investors[0]["bids"] else []
        headers = ["Investor"] + companies
        
        rows = []
        for investor in investors:
            row = [self._truncate_text(investor["name"])]
            row.extend([
                f"{investor['bids'].get(company, 0):,}" 
                for company in companies
            ])
            rows.append(row)
        
        return tabulate(rows, headers=headers, tablefmt=self.config.table_format)
    
    def format_results_table(self, results: List[Dict]) -> str:
        if not results:
            return "No results available"
        
        headers = [
            "Company",
            "Total Bid",
            "Capital Raised",
            "Subscription Status",
            "Price",
            "Shares Offered"
        ]
        
        rows = []
        for result in results:
            status_color = self._get_subscription_color(result["subscription_status"])
            
            rows.append([
                self._truncate_text(result["company_name"]),
                f"{result['total_bid']:,}",
                f"${result['capital_raised']:,.2f}",
                f"{status_color}{result['subscription_status']}{self.colors['reset']}",
                f"${result['price']:.2f}",
                f"{result['shares_offered']:,}"
            ])
        
        return tabulate(rows, headers=headers, tablefmt=self.config.table_format)
    
    def format_approval_status(self, approvals: List[Dict]) -> str:
        if not approvals:
            return "No approval data available"
        
        headers = ["Field", "Team 1", "Team 2", "Overall Status"]
        rows = []
        
        for approval in approvals:
            team1_color = self._get_status_color(approval["team1_status"])
            team2_color = self._get_status_color(approval["team2_status"])
            
            overall_status = "Complete" if (
                approval["team1_status"] == "OK" and approval["team2_status"] == "OK"
            ) else "Pending"
            overall_color = self._get_status_color(overall_status)
            
            rows.append([
                self._truncate_text(approval["field_name"]),
                f"{team1_color}{approval['team1_status']}{self.colors['reset']}",
                f"{team2_color}{approval['team2_status']}{self.colors['reset']}",
                f"{overall_color}{overall_status}{self.colors['reset']}"
            ])
        
        return tabulate(rows, headers=headers, tablefmt=self.config.table_format)
    
    def _truncate_text(self, text: str) -> str:
        if len(text) > self.config.max_name_length:
            return text[:self.config.max_name_length - 3] + "..."
        return text
    
    def _get_status_color(self, status: str) -> str:
        status_lower = status.lower()
        if status_lower in ["ok", "complete"]:
            return self.colors["green"]
        elif status_lower == "tbd":
            return self.colors["yellow"]
        else:
            return self.colors["red"]
    
    def _get_subscription_color(self, status: str) -> str:
        status_lower = status.lower()
        if "over" in status_lower:
            return self.colors["green"]
        elif "fully" in status_lower:
            return self.colors["blue"]
        else:
            return self.colors["yellow"]
    
    def print_error(self, message: str) -> None:
        print(f"{self.colors['red']}Error: {message}{self.colors['reset']}")
    
    def print_success(self, message: str) -> None:
        print(f"{self.colors['green']}{message}{self.colors['reset']}")
    
    def print_warning(self, message: str) -> None:
        print(f"{self.colors['yellow']}Warning: {message}{self.colors['reset']}")
    
    def print_info(self, message: str) -> None:
        print(f"{self.colors['blue']}{message}{self.colors['reset']}")

formatter = DisplayFormatter()

def format_company_table(companies: List[Dict]) -> str:
    return formatter.format_company_table(companies)

def format_investor_table(investors: List[Dict]) -> str:
    return formatter.format_investor_table(investors)

def format_results_table(results: List[Dict]) -> str:
    return formatter.format_results_table(results)

def format_approval_status(approvals: List[Dict]) -> str:
    return formatter.format_approval_status(approvals)

def print_error(message: str) -> None:
    formatter.print_error(message)

def print_success(message: str) -> None:
    formatter.print_success(message)

def print_warning(message: str) -> None:
    formatter.print_warning(message)

def print_info(message: str) -> None:
    formatter.print_info(message)

# Example usage - remove later
if __name__ == "__main__":
    test_companies = [
        {"name": "TechCo", "price": 10.5, "shares": 1000},
        {"name": "BioFirm", "price": 15.75, "shares": 500},
    ]
    print("\nTest company table:")
    print(format_company_table(test_companies)) 