import time
from typing import Optional
from ..services.company_service import CompanyService
from ..logic.calculator import recalculate_outputs
from ..logic.toggle_handler import check_all_ok, get_pending_approvals
from ..utils.display import (
    format_company_table, format_results_table, format_approval_status,
    print_error, print_success, print_warning, print_info
)
from config import Config

class Team1CLI:
    def __init__(self):
        self.company_service = CompanyService()
        self.config = Config.display
    
    def run(self):
        print_info("\n=== Simulation Game - Team 1 Interface ===")
        print_info("You are responsible for managing company data and pricing.")
        
        while True:
            self._display_current_state()
            self._display_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                self._handle_choice(choice)
            except KeyboardInterrupt:
                print_info("\nExiting...")
                break
            except Exception as e:
                print_error(f"An error occurred: {str(e)}")
            
            time.sleep(self.config.refresh_interval)
    
    def _display_current_state(self):
        companies = self.company_service.get_all_companies()
        print("\n" + "="*60)
        print("CURRENT COMPANY DATA:")
        print("="*60)
        print(format_company_table(companies))
        
        approvals = get_pending_approvals()
        if approvals:
            print("\nAPPROVAL STATUS:")
            print("="*60)
            print(format_approval_status(approvals))
    
    def _display_menu(self):
        print("\n" + "="*60)
        print("TEAM 1 OPTIONS:")
        print("="*60)
        print("1. Update company price")
        print("2. Update shares offered")
        print("3. Mark company data as final")
        print("4. Check approval status")
        print("5. View simulation results")
        print("6. Add new company")
        print("7. Exit")
    
    def _handle_choice(self, choice: str):
        if choice == "1":
            self._update_company_price()
        elif choice == "2":
            self._update_company_shares()
        elif choice == "3":
            self._mark_company_final()
        elif choice == "4":
            self._check_approval_status()
        elif choice == "5":
            self._view_results()
        elif choice == "6":
            self._add_new_company()
        elif choice == "7":
            print_success("Goodbye!")
            exit(0)
        else:
            print_error("Invalid choice. Please enter a number between 1-7.")
    
    def _update_company_price(self):
        try:
            company_id = int(input("Enter company ID: "))
            price = float(input(f"Enter new price (${Config.game.min_price}-${Config.game.max_price}): "))
            
            if self.company_service.update_company(company_id, price=price):
                print_success("Price updated successfully!")
                print_warning("Team 2 approvals have been reset to TBD.")
            else:
                print_error("Failed to update price. Check company ID and price range.")
        except ValueError:
            print_error("Invalid input. Please enter valid numbers.")
    
    def _update_company_shares(self):
        try:
            company_id = int(input("Enter company ID: "))
            shares = int(input(f"Enter new shares (1-{Config.game.max_shares}): "))
            
            if self.company_service.update_company(company_id, shares=shares):
                print_success("Shares updated successfully!")
                print_warning("Team 2 approvals have been reset to TBD.")
            else:
                print_error("Failed to update shares. Check company ID and shares range.")
        except ValueError:
            print_error("Invalid input. Please enter valid numbers.")
    
    def _mark_company_final(self):
        try:
            company_id = int(input("Enter company ID to mark as final: "))
            company = self.company_service.get_company_by_id(company_id)
            
            if not company:
                print_error("Company not found.")
                return
            
            from ..logic.toggle_handler import set_toggle
            if set_toggle(f"company_{company_id}", "team1", "OK"):
                print_success(f"Company '{company['name']}' marked as final.")
            else:
                print_error("Failed to mark company as final.")
        except ValueError:
            print_error("Invalid company ID.")
    
    def _check_approval_status(self):
        if check_all_ok():
            print_success("All data is finalized! Simulation can proceed.")
        else:
            print_warning("Waiting for all approvals to be finalized...")
            approvals = get_pending_approvals()
            print(format_approval_status(approvals))
    
    def _view_results(self):
        if check_all_ok():
            results = recalculate_outputs()
            print("\n" + "="*80)
            print("SIMULATION RESULTS:")
            print("="*80)
            print(format_results_table(results))
        else:
            print_error("Cannot view results until all data is finalized.")
            print_warning("Please ensure all companies and bids are approved by both teams.")
    
    def _add_new_company(self):
        try:
            name = input("Enter company name: ").strip()
            price = float(input(f"Enter price (${Config.game.min_price}-${Config.game.max_price}): "))
            shares = int(input(f"Enter shares (1-{Config.game.max_shares}): "))
            
            company_id = self.company_service.create_company(name, price, shares)
            if company_id:
                print_success(f"Company '{name}' created successfully with ID: {company_id}")
            else:
                print_error("Failed to create company. Check input data.")
        except ValueError:
            print_error("Invalid input. Please enter valid data.")

def main_loop():
    cli = Team1CLI()
    cli.run()

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nExiting...") 