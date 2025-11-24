# main.py
from expense_manager import ExpenseManager
from data_analyzer import DataAnalyzer
import os

# This Provides the interface the user sees


def clear_screen():
       #Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def dis_men():
    """Display the main menu"""
    print("\n" + "="*50)
    print("      SMART EXPENSE TRACKER")
    print("="*50)
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. View Expenses by Month")
    print("5. Expense Summary by Category")
    print("6. Expense Summary by Month")
    print("7. View Category Pie Chart")
    print("8. View Monthly Trend Chart")
    print("9. Compare Two Months")
    print("10. Save Expenses")
    print("11. Exit")
    print("="*50)

def valid_input(prompt, input_type=str):
       #Get validated user input
    while True:
        try:
            user_input = input(prompt)
            if input_type == float:
                return float(user_input)
            elif input_type == int:
                return int(user_input)
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please try again.")

def main():
    
    manager = ExpenseManager()
    analyzer = DataAnalyzer()
    filename = "expenses.csv"
    
    
    success, message = manager.load_from_file(filename)
    print(message)
    
    while True:
        dis_men()
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            clear_screen()
            print("--- Add New Expense ---")
            date = input("Enter date (YYYY-MM-DD): ").strip()
            amount = valid_input("Enter amount: $", float)
            category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
            description = input("Enter description: ").strip()
            
            success, message = manager.add_exp(date, amount, category, description)
            print(message)
            
        elif choice == '2':
            clear_screen()
            print("--- All Expenses ---")
            manager.view_exp()
            
        elif choice == '3':
            clear_screen()
            category = input("Enter category to filter: ").strip()
            print(f"--- Expenses for {category} ---")
            manager.view_exp(filter_category=category)
            
        elif choice == '4':
            clear_screen()
            month = input("Enter month to filter (YYYY-MM): ").strip()
            print(f"--- Expenses for {month} ---")
            manager.view_exp(filter_month=month)
            
        elif choice == '5':
            clear_screen()
            month_filter = input("Enter month to summarize (YYYY-MM) or press Enter for all time: ").strip()
            month_filter = month_filter if month_filter else None
            summary = manager.get_summary_cat(month_filter)
            print(summary)
            
        elif choice == '6':
            clear_screen()
            summary = manager.get_summary_month()
            print(summary)
            
        elif choice == '7':
            clear_screen()
            month_filter = input("Enter month for pie chart (YYYY-MM) or press Enter for all time: ").strip()
            month_filter = month_filter if month_filter else None
            analyzer.plt_cat_piechart(manager, month_filter)
            
        elif choice == '8':
            clear_screen()
            analyzer.plt_monthlytrend(manager)
            
        elif choice == '9':
            clear_screen()
            print("--- Compare Two Months ---")
            month1 = input("Enter first month (YYYY-MM): ").strip()
            month2 = input("Enter second month (YYYY-MM): ").strip()
            analyzer.plt_cat_comparison(manager, month1, month2)
            
        elif choice == '10':
            success, message = manager.save_file(filename)
            print(message)
            
        elif choice == '11':
        
            success, message = manager.save_file(filename)
            print(message)
            print("Thank you for using Smart Expense Tracker! Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1-11.")
        
        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    main()