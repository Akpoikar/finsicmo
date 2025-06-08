# Simulation Game 2

A Python CLI application for running a two-team investment simulation game.

## Setup

1. Create a PostgreSQL database named `simulation_game`

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
DB_URL=postgresql://username:password@localhost:5432/simulation_game
```

## Usage

Run Team 1 interface:
```bash
python main.py --team 1
```

Run Team 2 interface:
```bash
python main.py --team 2
```

## Game Rules

### Team 1 (Companies)
- Set price and shares for 3 companies
- Mark data as final when ready
- View results when both teams are ready

### Team 2 (Investors)
- Input share bids for 3 investors across companies
- Mark bids as final when ready
- View results when both teams are ready

## Output Calculations
- Total shares bid = sum of investor bids
- Capital raised = price × min(shares_bid, shares_offered)
- Subscription status = "Over" if shares_bid > shares_offered, else "Under"

## Development Notes

- Uses SQLAlchemy for database operations
- Concurrent access via separate CLI instances
- Status tracking via toggle flags
- Pretty-printed tables using tabulate 