from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'monthly_campaign_engine'))

from file_loader import MonthlyFileLoader

loader = MonthlyFileLoader('c:\\Users\\adeel\\Google ADS')
df = loader.combine_all_months()
print(f'Combined shape: {df.shape}')
print(f'Campaigns: {df["Campaign"].nunique()}')
print(f'Months: {df["Month"].nunique()}')
print(f'Columns: {df.columns.tolist()[:10]}')
