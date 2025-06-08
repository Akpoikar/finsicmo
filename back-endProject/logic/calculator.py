from typing import Dict, List
from sqlalchemy import select
from ..db.schema import companies, bids, calculated_outputs
from ..db.session import get_session

def recalculate_outputs():
    with get_session() as session:
        company_data = session.execute(select(companies)).fetchall()
        
        # Note: tried doing this in one query but this is clearer
        bid_data = {}
        for company in company_data:
            company_bids = session.execute(
                select(bids).where(bids.c.company_id == company.id)
            ).fetchall()
            bid_data[company.id] = sum(b.shares_bid for b in company_bids)

        # Calculate outputs for each company
        for company in company_data:
            total_bid = bid_data.get(company.id, 0)
            capital = company.price * min(total_bid, company.shares)
            
            sub_status = "Over" if total_bid > company.shares else "Under"
            
            session.execute(
                calculated_outputs.delete().where(
                    calculated_outputs.c.company_id == company.id
                )
            )
            session.execute(
                calculated_outputs.insert().values(
                    company_id=company.id,
                    total_bid=total_bid,
                    capital_raised=capital,
                    subscription_status=sub_status
                )
            )
    
    return True 

# For debugging
def _print_calcs(): 
    with get_session() as session:
        results = session.execute(select(calculated_outputs)).fetchall()
        for r in results:
            print(f"Company {r.company_id}: {r.total_bid} shares, ${r.capital_raised:,.2f}") 