# expense_manager.py
import csv
import os
from datetime import datetime
import pandas as pd
from models import Expense

# Manages all expense related operations including CRUD operations and data persistence based on what the user inputs in the interface 

class ExpenseManager:
        
    def __init__(self):
        self.expenses = []
        self.next_id = 1

    def add_exp(self, date, amount, category, description):
           #Add a new expense to the tracker
        try:
            
            datetime.strptime(date, '%Y-%m-%d')
            
            # Create and add expense
            expense = Expense(self.next_id, date, float(amount), category, description)
            self.expenses.append(expense)
            self.next_id += 1
            return True, "Expense added successfully!"
            
        except ValueError as e:
            return False, f"Error: Invalid input - {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def view_exp(self, filter_category=None, filter_month=None):
           #View all expenses, with optional filtering
        if not self.expenses:
            print("No expenses found.")
            return []

        filtered_expenses = self.expenses
        
        if filter_category:
            filtered_expenses = [e for e in filtered_expenses if e.category.lower() == filter_category.lower()]
        
        if filter_month:
            filtered_expenses = [e for e in filtered_expenses if e.date.startswith(filter_month)]
        
        if not filtered_expenses:
            print("No expenses match the filter criteria.")
            return []

        
        print("\n" + "="*80)
        print(f"{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("="*80)
        
        total = 0
        for expense in filtered_expenses:
            print(f"{expense.id:<4} {expense.date:<12} {expense.category:<15} ${expense.amount:<9.2f} {expense.description}")
            total += expense.amount
        
        print("="*80)
        print(f"Total: ${total:.2f}")
        print("="*80)
        
        return filtered_expenses

    def get_summary_cat(self, month=None):
           #Get summary of expenses grouped by category
        if not self.expenses:
            return "No expenses to summarize."

        
        data = [expense.to_dict() for expense in self.expenses]
        df = pd.DataFrame(data)
        
        
        if month:
            df = df[df['date'].str.startswith(month)]
            if df.empty:
                return f"No expenses found for {month}"

        summary = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        
        result = "\n--- Expense Summary by Category ---\n"
        total = 0
        for category, amount in summary.items():
            result += f"{category:<15}: ${amount:>8.2f}\n"
            total += amount
        
        result += "-" * 40 + f"\n{'Total':<15}: ${total:>8.2f}"
        return result

    def get_summary_month(self):
           #Get summary of expenses grouped by month
        if not self.expenses:
            return "No expenses to summarize."

        data = [expense.to_dict() for expense in self.expenses]
        df = pd.DataFrame(data)
        
        # Extract year-month from date
        df['year_month'] = df['date'].str[:7]  
        summary = df.groupby('year_month')['amount'].sum().sort_index()
        
        result = "\n--- Expense Summary by Month ---\n"
        total = 0
        for month, amount in summary.items():
            result += f"{month:<10}: ${amount:>8.2f}\n"
            total += amount
        
        result += "-" * 35 + f"\n{'Total':<10}: ${total:>8.2f}"
        return result

    def save_file(self, filename="expenses.csv"):
           #Save the expenses to CSV file
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                if self.expenses:
                    writer = csv.DictWriter(file, fieldnames=['id', 'date', 'amount', 'category', 'description'])
                    writer.writeheader()
                    for expense in self.expenses:
                        writer.writerow(expense.to_dict())
            return True, f"Expenses saved to {filename}"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"

    def load_from_file(self, filename="expenses.csv"):
           #Load the expenses from CSV file
        try:
            if not os.path.exists(filename):
                return True, "No existing data file found. Starting fresh."
            
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.expenses = []
                for row in reader:
                    expense = Expense.from_dict(row)
                    self.expenses.append(expense)
                    self.next_id = max(self.next_id, expense.id + 1)
            
            return True, f"Loaded {len(self.expenses)} expenses from {filename}"
        except Exception as e:
            return False, f"Error loading file: {str(e)}"

    def get_exp_analysis(self):
           #Get the expenses as DataFrame for analysis
        if not self.expenses:
            return None
        data = [expense.to_dict() for expense in self.expenses]
        return pd.DataFrame(data)