import time
from sqlalchemy import select, update
from ..db.schema import companies
from ..db.session import get_session
from ..logic.calculator import recalculate_outputs
from ..logic.toggle_handler import set_toggle, check_all_ok
from ..utils.display import format_company_table, print_error, print_success

def update_company(company_id: int, price: float = None, shares: int = None) -> bool:
    if price is None and shares is None:
        return False
    
    updates = {}
    if price is not None:
        updates["price"] = price
    if shares is not None:
        updates["shares"] = shares
    
    with get_session() as session:
        session.execute(
            update(companies)
            .where(companies.c.id == company_id)
            .values(**updates)
        )
    return True

def get_companies():
    with get_session() as session:
        return session.execute(select(companies)).fetchall()

def main_loop():
    print("\nWelcome to Simulation Game 2 - Team 1 Interface")
    
    while True:
        companies_data = get_companies()
        print("\nCurrent Company Data:")
        print(format_company_table([
            {
                "name": c.name,
                "price": c.price,
                "shares": c.shares
            }
            for c in companies_data
        ]))
        
        print("\nOptions:")
        print("1. Update company price")
        print("2. Update shares offered")
        print("3. Mark data as final")
        print("4. Check if Team 2 is ready")
        print("5. View results")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            company_id = int(input("Enter company ID: "))
            try:
                price = float(input("Enter new price: "))
                if update_company(company_id, price=price):
                    print_success("Price updated successfully!")
                    set_toggle(f"company_{company_id}", "team1", "TBD")
                else:
                    print_error("Failed to update price")
            except ValueError:
                print_error("Invalid price value")
        
        elif choice == "2":
            company_id = int(input("Enter company ID: "))
            try:
                shares = int(input("Enter new shares: "))
                if update_company(company_id, shares=shares):
                    print_success("Shares updated successfully!")
                    set_toggle(f"company_{company_id}", "team1", "TBD")
                else:
                    print_error("Failed to update shares")
            except ValueError:
                print_error("Invalid shares value")
        
        elif choice == "3":
            company_id = int(input("Enter company ID to mark as final: "))
            set_toggle(f"company_{company_id}", "team1", "OK")
            print_success(f"Company {company_id} marked as final")
        
        elif choice == "4":
            if check_all_ok():
                print_success("All data is finalized!")
            else:
                print("Waiting for Team 2 to finalize data...")
        
        elif choice == "5":
            if check_all_ok():
                recalculate_outputs()
                print("\nFinal Results:")
                # TODO: Add results display
            else:
                print_error("Cannot view results until all data is finalized")
        
        elif choice == "6":
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