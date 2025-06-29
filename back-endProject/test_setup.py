#!/usr/bin/env python3
"""
Simple test script to verify the backend setup and basic functionality.
Run this after setting up the database to ensure everything works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.schema import init_db, Company, Investor, SessionLocal
from config import Config, ApprovalStatus
from utils.display import print_info, print_success, print_error
from logic.game_coordinator import GameCoordinator
from logic.validation_engine import ValidationEngine
from logic.calculation_engine import CalculationEngine

def test_database_connection():
    """Test database connection and basic operations."""
    print_info("Testing database connection...")
    
    try:
        init_db()
        print_success("Database connection successful!")
        return True
    except Exception as e:
        print_error(f"Database connection failed: {str(e)}")
        return False

def test_sample_data():
    """Test sample data creation and retrieval."""
    print_info("Testing sample data...")
    
    try:
        with SessionLocal() as db:
            companies = db.query(Company).all()
            investors = db.query(Investor).all()
            
            print_success(f"Found {len(companies)} companies and {len(investors)} investors")
            
            if companies:
                print_info("Sample companies:")
                for company in companies:
                    print(f"  - {company.name}: ${company.price:.2f}, {company.shares} shares")
            
            if investors:
                print_info("Sample investors:")
                for investor in investors:
                    print(f"  - {investor.name}")
            
            return True
    except Exception as e:
        print_error(f"Sample data test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration loading."""
    print_info("Testing configuration...")
    
    try:
        print(f"Database URL: {Config.db.url}")
        print(f"Max companies: {Config.game.max_companies}")
        print(f"Max investors: {Config.game.max_investors}")
        print(f"Price range: ${Config.game.min_price} - ${Config.game.max_price}")
        print(f"Share range: 1 - {Config.game.max_shares}")
        print(f"ApprovalStatus.TBD = {ApprovalStatus.TBD}")
        print(f"ApprovalStatus.OK = {ApprovalStatus.OK}")
        print_success("Configuration loaded successfully!")
        return True
    except Exception as e:
        print_error(f"Configuration test failed: {str(e)}")
        return False

def test_logic_modules():
    """Test the new modular logic structure."""
    print_info("Testing logic modules...")
    
    try:
        coordinator = GameCoordinator()
        validation_engine = ValidationEngine()
        calculation_engine = CalculationEngine()
        
        print_success("All logic modules initialized successfully!")
        
        # Test validation
        is_valid, message = validation_engine.validate_company_data("TestCo", 10.0, 1000)
        print_info(f"Validation test: {message}")
        
        # Test game status
        game_status = coordinator.get_game_status()
        print_info(f"Game status: {len(game_status)} components loaded")
        
        return True
    except Exception as e:
        print_error(f"Logic modules test failed: {str(e)}")
        return False

def test_status_conversion():
    """Test status conversion between numeric and string values."""
    print_info("Testing status conversion...")
    
    try:
        from logic.status_manager import StatusManager
        status_manager = StatusManager()
        
        # Test numeric to string
        assert status_manager.status_to_string(ApprovalStatus.TBD) == "TBD"
        assert status_manager.status_to_string(ApprovalStatus.OK) == "OK"
        
        # Test string to numeric
        assert status_manager.string_to_status("TBD") == ApprovalStatus.TBD
        assert status_manager.string_to_status("OK") == ApprovalStatus.OK
        
        print_success("Status conversion working correctly!")
        return True
    except Exception as e:
        print_error(f"Status conversion test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print_info("=" * 50)
    print_info("BACKEND SETUP TEST - MODULAR VERSION")
    print_info("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Database Connection", test_database_connection),
        ("Sample Data", test_sample_data),
        ("Logic Modules", test_logic_modules),
        ("Status Conversion", test_status_conversion),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        if test_func():
            passed += 1
        else:
            print_error(f"{test_name} test failed!")
    
    print_info("\n" + "=" * 50)
    print_info(f"TEST RESULTS: {passed}/{total} tests passed")
    print_info("=" * 50)
    
    if passed == total:
        print_success("All tests passed! Backend is ready to use.")
        print_info("\nYou can now run:")
        print_info("  python main.py --team 1  # Start Team 1 interface")
        print_info("  python main.py --team 2  # Start Team 2 interface")
    else:
        print_error("Some tests failed. Please check the setup.")
        sys.exit(1)

if __name__ == "__main__":
    main() 