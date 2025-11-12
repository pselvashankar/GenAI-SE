import sys

def get_friends():
    """
    Prompts the user to enter the names of all friends.
    Returns a list of friend names.
    """
    friends = []
    print("--- Welcome to Splitwise CLI ---")
    print("First, let's add the friends in your group.")
    
    while True:
        try:
            name = input("Enter a friend's name (or press Enter to finish): ").strip()
            if not name:
                if len(friends) < 2:
                    print("You need at least two friends to split expenses.")
                    continue
                else:
                    break
            if name in friends:
                print(f"'{name}' is already in the group.")
            else:
                friends.append(name)
                print(f"Added '{name}'. Current group: {', '.join(friends)}")
        except EOFError:
            sys.exit("Exiting.")
        except KeyboardInterrupt:
            sys.exit("\nExiting.")
            
    print("\nGreat! Your group is set:")
    for i, friend in enumerate(friends, 1):
        print(f"{i}. {friend}")
    return friends

def record_expenses(friends):
    """
    Loops to record multiple expenses from the user.
    Calculates and returns the final balance for each friend.
    """
    # Initialize balances dictionary, e.g., {'Alice': 0, 'Bob': 0}
    balances = {friend: 0.0 for friend in friends}
    num_friends = len(friends)
    
    print("\n--- Record Expenses ---")
    
    while True:
        try:
            # 1. Get expense description
            expense_description = input("\nEnter expense description (or press Enter to finish): ").strip()
            if not expense_description:
                break
                
            # 2. Get total amount
            total_amount = 0.0
            while True:
                amount_str = input(f"Enter total amount for '{expense_description}': $").strip()
                try:
                    total_amount = float(amount_str)
                    if total_amount <= 0:
                        print("Amount must be greater than 0.")
                    else:
                        break
                except ValueError:
                    print("Invalid amount. Please enter a number (e.g., 25.50)")

            # 3. Get who paid
            payer = ""
            while True:
                print("Who paid for this?")
                for i, friend in enumerate(friends, 1):
                    print(f"  {i}. {friend}")
                
                payer_choice = input("Enter the number or name of the payer: ").strip()
                
                if payer_choice.isdigit() and 1 <= int(payer_choice) <= num_friends:
                    payer = friends[int(payer_choice) - 1]
                    break
                elif payer_choice in friends:
                    payer = payer_choice
                    break
                else:
                    print(f"Invalid choice. Please enter a number from 1-{num_friends} or a valid name.")
            
            # 4. For this simple version, we'll split equally among ALL friends
            # You could expand this to ask *who* to split between
            print(f"Splitting ${total_amount:.2f} for '{expense_description}' equally among all {num_friends} friends.")
            share_per_person = total_amount / num_friends
            
            # 5. Update balances
            # The payer is "owed" the full amount they paid
            balances[payer] += total_amount
            
            # Everyone "owes" their share of the expense
            for friend in friends:
                balances[friend] -= share_per_person
                
            print(f"Success: Added expense. {payer} paid ${total_amount:.2f}.")
            print("Current balances (positive means owed, negative means owes):")
            for friend, balance in balances.items():
                print(f"  {friend}: ${balance:+.2f}")

        except EOFError:
            break
        except KeyboardInterrupt:
            break
            
    print("\n--- Finished Recording Expenses ---")
    return balances

def calculate_settlements(balances):
    """
    Calculates the simplest set of transactions to settle all debts.
    Prints the settlement plan.
    """
    print("\n--- Calculating Settlements ---")
    
    # Create two lists:
    # creditors: {'name': 'Alice', 'amount': 75.0} (who are owed money)
    # debtors: {'name': 'Bob', 'amount': 25.0} (who owe money)
    creditors = []
    debtors = []
    
    for friend, balance in balances.items():
        if balance > 0.01: # Use a small tolerance for floating point errors
            creditors.append({'name': friend, 'amount': balance})
        elif balance < -0.01:
            # Store the amount owed as a positive number
            debtors.append({'name': friend, 'amount': -balance}) 

    if not creditors and not debtors:
        print("Everyone is settled up. No payments needed!")
        return

    # List to store transaction strings
    transactions = []

    # This algorithm matches the person who owes the most with the
    # person who is owed the most, minimizing total transactions.
    while debtors and creditors:
        # Sort by amount to optimize (optional, but cleaner)
        debtors.sort(key=lambda x: x['amount'], reverse=True)
        creditors.sort(key=lambda x: x['amount'], reverse=True)
        
        debtor = debtors[0]
        creditor = creditors[0]
        
        # How much can be paid? The minimum of the two amounts.
        payment_amount = min(debtor['amount'], creditor['amount'])
        
        # Record the transaction
        transactions.append(
            f"{debtor['name']} pays {creditor['name']} ${payment_amount:.2f}"
        )
        
        # Update the amounts
        debtor['amount'] -= payment_amount
        creditor['amount'] -= payment_amount
        
        # Remove if they are settled up
        if debtor['amount'] < 0.01:
            debtors.pop(0)
        if creditor['amount'] < 0.01:
            creditors.pop(0)

    print("\n--- Settlement Plan ---")
    if not transactions:
        print("Everyone is already settled up!")
    else:
        for trx in transactions:
            print(f"  - {trx}")

def main():
    """
    Main function to run the application.
    """
    try:
        friends = get_friends()
        if not friends:
            print("No friends were added. Exiting.")
            return
            
        balances = record_expenses(friends)
        
        print("\n--- Final Balances ---")
        for friend, balance in balances.items():
            if balance > 0:
                print(f"{friend} is owed ${balance:.2f}")
            elif balance < 0:
                print(f"{friend} owes ${-balance:.2f}")
            else:
                print(f"{friend} is settled")
                
        calculate_settlements(balances)
        
        print("\n--- All Done! ---")
        
    except (EOFError, KeyboardInterrupt):
        print("\n\nCaught exit signal. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()