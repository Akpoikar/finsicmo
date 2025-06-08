import time
from sqlalchemy import select, update
from ..db.schema import companies, investors, bids
from ..db.session import get_session
from ..logic.calculator import recalculate_outputs
from ..logic.toggle_handler import set_toggle, check_all_ok
from ..utils.display import (
    format_company_table,
    format_investor_table,
    print_error,
    print_success
)

def update_bid(investor_id: int, company_id: int, shares: int) -> bool:
    """Update investor bid for a company"""
    with get_session() as session:
        existing = session.execute(
            select(bids).where(
                bids.c.investor_id == investor_id,
                bids.c.company_id == company_id
            )
        ).first()
        
        if existing:
            session.execute(
                update(bids)
                .where(
                    bids.c.investor_id == investor_id,
                    bids.c.company_id == company_id
                )
                .values(shares_bid=shares)
            )
        else:
            session.execute(
                bids.insert().values(
                    investor_id=investor_id,
                    company_id=company_id,
                    shares_bid=shares
                )
            )
    return True

def get_investor_data():
    """Get all investors and their bids"""
    with get_session() as session:
        investors_data = session.execute(select(investors)).fetchall()
        companies_data = session.execute(select(companies)).fetchall()
        
        result = []
        for inv in investors_data:
            inv_bids = session.execute(
                select(bids).where(bids.c.investor_id == inv.id)
            ).fetchall()
            
            # Convert to dict for easier lookup
            bids_dict = {
                next(c.name for c in companies_data if c.id == b.company_id): b.shares_bid
                for b in inv_bids
            }
            
            result.append({
                "id": inv.id,
                "name": inv.name,
                "bids": bids_dict
            })
        
        return result, companies_data

def main_loop():
    """Main CLI loop for Team 2"""
    print("\nWelcome to Simulation Game 2 - Team 2 Interface")
    
    while True:
        investors_data, companies_data = get_investor_data()
        
        print("\nCurrent Company Data:")
        print(format_company_table([
            {
                "name": c.name,
                "price": c.price,
                "shares": c.shares
            }
            for c in companies_data
        ]))
        
        print("\nCurrent Bids:")
        print(format_investor_table(investors_data))
        
        print("\nOptions:")
        print("1. Update bid")
        print("2. Mark bid as final")
        print("3. Check if Team 1 is ready")
        print("4. View results")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            try:
                investor_id = int(input("Enter investor ID: "))
                company_id = int(input("Enter company ID: "))
                shares = int(input("Enter shares to bid: "))
                
                if update_bid(investor_id, company_id, shares):
                    print_success("Bid updated successfully!")
                    set_toggle(f"bid_{investor_id}_{company_id}", "team2", "TBD")
                else:
                    print_error("Failed to update bid")
            except ValueError:
                print_error("Invalid input values")
        
        elif choice == "2":
            try:
                investor_id = int(input("Enter investor ID: "))
                company_id = int(input("Enter company ID: "))
                set_toggle(f"bid_{investor_id}_{company_id}", "team2", "OK")
                print_success(f"Bid for investor {investor_id} on company {company_id} marked as final")
            except ValueError:
                print_error("Invalid input values")
        
        elif choice == "3":
            if check_all_ok():
                print_success("All data is finalized!")
            else:
                print("Waiting for Team 1 to finalize data...")
        
        elif choice == "4":
            if check_all_ok():
                recalculate_outputs()
                print("\nFinal Results:")
                # TODO: Add results display
            else:
                print_error("Cannot view results until all data is finalized")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print_error("Invalid choice")
        
        time.sleep(0.5)  # prevent screen flicker

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nExiting...") 