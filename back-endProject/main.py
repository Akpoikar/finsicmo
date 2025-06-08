import sys
import argparse
from sqlalchemy import insert
from db.schema import init_db, companies, investors
from db.session import get_session
from cli.team1_cli import main_loop as team1_loop
from cli.team2_cli import main_loop as team2_loop

def init_sample_data():
    with get_session() as session:
        if session.execute("SELECT COUNT(*) FROM companies").scalar() > 0:
            return
        
        session.execute(
            insert(companies).values([
                {"name": "TechCorp", "price": 10.0, "shares": 1000},
                {"name": "BioMed", "price": 15.0, "shares": 750},
                {"name": "GreenEnergy", "price": 12.5, "shares": 500},
            ])
        )
        
        session.execute(
            insert(investors).values([
                {"name": "Angel Fund"},
                {"name": "Growth Capital"},
                {"name": "Tech Ventures"},
            ])
        )

def main():
    parser = argparse.ArgumentParser(description="Simulation Game 2")
    parser.add_argument(
        "--team",
        type=int,
        choices=[1, 2],
        required=True,
        help="Team number (1 or 2)"
    )
    
    args = parser.parse_args()
    
    try:
        print("Initializing database...")
        init_db()
        init_sample_data()
        
        if args.team == 1:
            team1_loop()
        else:
            team2_loop()
            
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 