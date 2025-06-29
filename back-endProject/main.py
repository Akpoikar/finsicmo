import sys
import argparse
from sqlalchemy.orm import Session
from db.schema import init_db, Company, Investor, SessionLocal
from cli.team1_cli import main_loop as team1_loop
from cli.team2_cli import main_loop as team2_loop
from config import Config
from utils.display import print_info, print_error, print_success

class SimulationGame:
    def __init__(self):
        self.config = Config
    
    def initialize_database(self):
        print_info("Initializing database...")
        try:
            init_db()
            print_success("Database initialized successfully!")
        except Exception as e:
            print_error(f"Failed to initialize database: {str(e)}")
            sys.exit(1)
    
    def seed_sample_data(self):
        print_info("Seeding sample data...")
        try:
            with SessionLocal() as db:
                if self._has_data(db):
                    print_info("Sample data already exists, skipping...")
                    return
                
                self._create_sample_companies(db)
                self._create_sample_investors(db)
                print_success("Sample data created successfully!")
        except Exception as e:
            print_error(f"Failed to seed sample data: {str(e)}")
            sys.exit(1)
    
    def _has_data(self, db: Session) -> bool:
        company_count = db.query(Company).count()
        investor_count = db.query(Investor).count()
        return company_count > 0 or investor_count > 0
    
    def _create_sample_companies(self, db: Session):
        for company_data in self.config.sample_companies:
            company = Company(
                name=company_data["name"],
                price=company_data["price"],
                shares=company_data["shares"]
            )
            db.add(company)
        db.commit()
    
    def _create_sample_investors(self, db: Session):
        for investor_data in self.config.sample_investors:
            investor = Investor(name=investor_data["name"])
            db.add(investor)
        db.commit()
    
    def run_team_interface(self, team_number: int):
        print_info(f"Starting Team {team_number} interface...")
        try:
            if team_number == 1:
                team1_loop()
            else:
                team2_loop()
        except KeyboardInterrupt:
            print_info("\nInterface stopped by user.")
        except Exception as e:
            print_error(f"Error in team interface: {str(e)}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Simulation Game - Multi-team Investment Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --team 1    # Start Team 1 interface
  python main.py --team 2    # Start Team 2 interface
  python main.py --init      # Initialize database only
        """
    )
    
    parser.add_argument(
        "--team",
        type=int,
        choices=[1, 2],
        help="Team number to run (1 or 2)"
    )
    
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize database and seed sample data only"
    )
    
    args = parser.parse_args()
    
    if not args.team and not args.init:
        parser.error("Either --team or --init must be specified")
    
    game = SimulationGame()
    
    try:
        game.initialize_database()
        game.seed_sample_data()
        
        if args.init:
            print_success("Database initialization complete!")
            return
        
        if args.team:
            game.run_team_interface(args.team)
            
    except KeyboardInterrupt:
        print_info("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 