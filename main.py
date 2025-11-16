# main.py for testing turn logic

from turn import TurnSystem

def main():
    """Test the turn system"""
    try:
        game = TurnSystem()
        
        print("=" * 60)
        print("SmartCents - Turn System Test")
        print("=" * 60)
        print(f"Starting Money: ${game.player.getMoney()}")
        print(f"Starting Happiness: {game.player.getHappiness()}")
        print()
        
        # Run 10 turns
        for turn in range(1, 7):
            print(f"\n--- TURN {turn} ---")
            result = game.oneTurn()
            
            # Check if bankrupt
            if result.get("status") == "Bankrupt":
                print(" GAME OVER - BANKRUPT!")
                print(f"Year: {result['year']}")
                print(f"Checking: ${result['checking']:.2f}")
                print(f"Savings: ${result['savings']:.2f}")
                print(f"Net Worth: ${result['networth']:.2f}")
                break
            
            # Print turn results
            print(f"Year: {result['year']}")
            print(f"Income: ${result['income']:.2f}")
            print(f"Interest Earned: ${result['interestEarned']:.2f}")
            print(f"Checking: ${result['checking']:.2f}")
            print(f"Savings: ${result['savings']:.2f}")
            print(f"Net Worth: ${result['networth']:.2f}")
            print(f"Happiness: {result['happiness']}")
            
            # Test deposit on turn 3
            if turn == 3:
                print("\n→ Testing deposit...")
                deposit_result = game.deposit_to_savings(100)
                print(f"  Deposited $100: {deposit_result}")
                print(f"  Checking: ${game.player.getMoney():.2f}")
                print(f"  Savings: ${game.player.bank.getSavings():.2f}")
            
            # Test withdraw on turn 6
            if turn == 6:
                print("\n Testing withdrawal...")
                withdraw_result = game.withdraw_from_savings(50)
                print(f"  Withdrew $50: {withdraw_result}")
                print(f"  Checking: ${game.player.getMoney():.2f}")
                print(f"  Savings: ${game.player.bank.getSavings():.2f}")
        
        print("\n" + "=" * 60)
        print("Test Complete")
        print("=" * 60)
    
    except Exception as e:
        print(f"ERROR: {type(e).__name__}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()