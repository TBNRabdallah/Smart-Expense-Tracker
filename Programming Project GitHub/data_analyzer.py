# data_analyzer.py
import matplotlib.pyplot as plt
import pandas as pd

# Analyzes Data and creates charts based on what the user inputs in the interface

class DataAnalyzer:
          
    def __init__(self):
        plt.style.use('seaborn-v0_8') 

    def plt_cat_piechart(self, expense_manager, month=None):
        #Generate a pie chart of expenses by category
        df = expense_manager.get_exp_analysis()
        if df is None or df.empty:
            print("No data available for visualization.")
            return

        
        if month:
            df = df[df['date'].str.startswith(month)]
            if df.empty:
                print(f"No expenses found for {month}")
                return

        
        category_totals = df.groupby('category')['amount'].sum()
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(category_totals)))
        
        wedges, texts, autotexts = plt.pie(
            category_totals.values, 
            labels= category_totals.index,
            autopct='%1.1f%%',
            colors= colors,
            startangle= 90,
            shadow= True
        )
        
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.title(f'Expense Distribution by Category\n({month if month else "All Time"})', fontsize=14, fontweight='bold')
        plt.axis('equal')  
        plt.tight_layout()
        plt.show()

    def plt_monthlytrend(self, expense_manager):
        #    Generate a bar chart of monthly expenses
        df = expense_manager.get_exp_analysis()
        if df is None or df.empty:
            print("No data available for visualization.")
            return

        
        df['year_month'] = df['date'].str[:7]
        monthly_totals = df.groupby('year_month')['amount'].sum().sort_index()
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(monthly_totals.index, monthly_totals.values, color='skyblue', edgecolor='navy', alpha=0.7)
        
        
        for bar, value in zip(bars, monthly_totals.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(monthly_totals.values)*0.01, 
                    f'${value:.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Monthly Expense Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plt_cat_comparison(self, expense_manager, month1, month2):
        #Compare expense categories between two months
        df = expense_manager.get_exp_analysis()
        if df is None or df.empty:
            print("No data available for visualization.")
            return

        # Filter data for both months
        df['year_month'] = df['date'].str[:7]
        df1 = df[df['year_month'] == month1]
        df2 = df[df['year_month'] == month2]
        
        if df1.empty or df2.empty:
            print("Not enough data for comparison.")
            return

        
        cat1 = df1.groupby('category')['amount'].sum()
        cat2 = df2.groupby('category')['amount'].sum()
        
        
        all_categories = set(cat1.index) | set(cat2.index)
        
    
        amounts1 = [cat1.get(cat, 0) for cat in all_categories]
        amounts2 = [cat2.get(cat, 0) for cat in all_categories]
        
        # comparison chart
        x = range(len(all_categories))
        width = 0.35
        
        plt.figure(figsize=(12, 6))
        plt.bar([i - width/2 for i in x], amounts1, width, label=month1, alpha=0.7)
        plt.bar([i + width/2 for i in x], amounts2, width, label=month2, alpha=0.7)
        
        plt.xlabel('Categories')
        plt.ylabel('Amount ($)')
        plt.title(f'Expense Comparison: {month1} vs {month2}')
        plt.xticks(x, all_categories, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()