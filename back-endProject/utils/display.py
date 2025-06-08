from typing import List, Dict
from tabulate import tabulate

def format_company_table(companies: List[Dict]) -> str:
    headers = ["Company", "Price", "Shares", "Status"]
    rows = [
        [
            c["name"],
            f"${c['price']:.2f}",
            f"{c['shares']:,}",
            c.get("status", "TBD")
        ]
        for c in companies
    ]
    return tabulate(rows, headers=headers, tablefmt="grid")

def format_investor_table(investors: List[Dict]) -> str:
    if not investors:
        return "No investor data available"
    
    companies = list(investors[0]["bids"].keys())
    
    headers = ["Investor"] + companies
    rows = []
    for inv in investors:
        row = [inv["name"]]
        row.extend([
            f"{inv['bids'].get(company, 0):,}" 
            for company in companies
        ])
        rows.append(row)
    
    return tabulate(rows, headers=headers, tablefmt="grid")

def format_results(results: List[Dict]) -> str:
    headers = [
        "Company",
        "Total Bid",
        "Capital Raised",
        "Status"
    ]
    rows = [
        [
            r["company"],
            f"{r['total_bid']:,}",
            f"${r['capital']:,.2f}",
            r["status"]
        ]
        for r in results
    ]
    return tabulate(rows, headers=headers, tablefmt="grid")

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def print_error(msg: str):
    print(f"{RED}Error: {msg}{RESET}")

def print_success(msg: str):
    print(f"{GREEN}{msg}{RESET}")

# Example usage - remove later
if __name__ == "__main__":
    test_companies = [
        {"name": "TechCo", "price": 10.5, "shares": 1000},
        {"name": "BioFirm", "price": 15.75, "shares": 500},
    ]
    print("\nTest company table:")
    print(format_company_table(test_companies)) 