import time
from typing import Optional
from ..services.investor_service import InvestorService
from ..services.company_service import CompanyService
from ..logic.calculator import recalculate_outputs
from ..logic.toggle_handler import check_all_ok, get_pending_approvals
from ..utils.display import (
    format_company_table, format_investor_table, format_results_table, 
    format_approval_status, print_error, print_success, print_warning, print_info
)
from config import Config

class Team2CLI:
    def __init__(self):
        self.investor_service = InvestorService()
        self.company_service = CompanyService()
        self.config = Config.display
    
    def run(self):
        print_info("\n=== Simulation Game - Team 2 Interface ===")
        print_info("You are responsible for managing investor bids and approvals.")
        
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
        investors = self.investor_service.get_all_investors_with_bids()
        
        print("\n" + "="*60)
        print("CURRENT COMPANY DATA:")
        print("="*60)
        print(format_company_table(companies))
        
        print("\n" + "="*60)
        print("CURRENT INVESTOR BIDS:")
        print("="*60)
        print(format_investor_table(investors))
        
        approvals = get_pending_approvals()
        if approvals:
            print("\nAPPROVAL STATUS:")
            print("="*60)
            print(format_approval_status(approvals))
    
    def _display_menu(self):
        print("\n" + "="*60)
        print("TEAM 2 OPTIONS:")
        print("="*60)
        print("1. Update investor bid")
        print("2. Mark bid as final")
        print("3. Check approval status")
        print("4. View simulation results")
        print("5. Add new investor")
        print("6. View bid details")
        print("7. Exit")
    
    def _handle_choice(self, choice: str):
        if choice == "1":
            self._update_investor_bid()
        elif choice == "2":
            self._mark_bid_final()
        elif choice == "3":
            self._check_approval_status()
        elif choice == "4":
            self._view_results()
        elif choice == "5":
            self._add_new_investor()
        elif choice == "6":
            self._view_bid_details()
        elif choice == "7":
            print_success("Goodbye!")
            exit(0)
        else:
            print_error("Invalid choice. Please enter a number between 1-7.")
    
    def _update_investor_bid(self):
        try:
            investor_id = int(input("Enter investor ID: "))
            company_id = int(input("Enter company ID: "))
            shares = int(input("Enter shares to bid: "))
            
            if self.investor_service.update_bid(investor_id, company_id, shares):
                print_success("Bid updated successfully!")
                print_warning("Bid status reset to TBD.")
            else:
                print_error("Failed to update bid. Check investor ID, company ID, and shares.")
        except ValueError:
            print_error("Invalid input. Please enter valid numbers.")
    
    def _mark_bid_final(self):
        try:
            investor_id = int(input("Enter investor ID: "))
            company_id = int(input("Enter company ID: "))
            
            investor = self.investor_service.get_investor_by_id(investor_id)
            company = self.company_service.get_company_by_id(company_id)
            
            if not investor or not company:
                print_error("Investor or company not found.")
                return
            
            if self.investor_service.approve_bid(investor_id, company_id):
                print_success(f"Bid for '{investor['name']}' on '{company['name']}' marked as final.")
            else:
                print_error("Failed to mark bid as final.")
        except ValueError:
            print_error("Invalid investor ID or company ID.")
    
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
    
    def _add_new_investor(self):
        try:
            name = input("Enter investor name: ").strip()
            
            investor_id = self.investor_service.create_investor(name)
            if investor_id:
                print_success(f"Investor '{name}' created successfully with ID: {investor_id}")
            else:
                print_error("Failed to create investor. Check input data.")
        except Exception as e:
            print_error(f"Error creating investor: {str(e)}")
    
    def _view_bid_details(self):
        try:
            investor_id = int(input("Enter investor ID: "))
            company_id = int(input("Enter company ID: "))
            
            investor = self.investor_service.get_investor_by_id(investor_id)
            company = self.company_service.get_company_by_id(company_id)
            
            if not investor or not company:
                print_error("Investor or company not found.")
                return
            
            bid_amount = investor['bids'].get(company['name'], 0)
            status = self.investor_service.get_bid_status(investor_id, company_id)
            
            print("\n" + "="*50)
            print("BID DETAILS:")
            print("="*50)
            print(f"Investor: {investor['name']}")
            print(f"Company: {company['name']}")
            print(f"Bid Amount: {bid_amount:,} shares")
            print(f"Status: {status}")
            print(f"Company Price: ${company['price']:.2f}")
            print(f"Company Shares: {company['shares']:,}")
            
            if bid_amount > 0:
                total_value = bid_amount * company['price']
                print(f"Total Bid Value: ${total_value:,.2f}")
        except ValueError:
            print_error("Invalid investor ID or company ID.")

def main_loop():
    cli = Team2CLI()
    cli.run()

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nExiting...") 