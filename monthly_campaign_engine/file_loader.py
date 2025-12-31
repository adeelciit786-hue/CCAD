"""
Multi-Month Campaign File Loader
Loads and normalizes monthly campaign CSV files from Google Ads exports.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import re


class MonthlyFileLoader:
    """Load and parse multiple monthly campaign CSV files."""
    
    def __init__(self, directory: str = "."):
        """Initialize loader with directory containing monthly CSVs."""
        self.directory = Path(directory)
        self.raw_dataframes = {}  # {month_key: dataframe}
        self.months_found = []
    
    def find_monthly_files(self) -> List[Path]:
        """Find all monthly CSV files (e.g., 'Mar 2025.csv')."""
        pattern = re.compile(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\.csv$', re.IGNORECASE)
        files = [f for f in self.directory.glob("*.csv") if pattern.match(f.name)]
        return sorted(files)
    
    def _extract_month_year(self, filename: str) -> Tuple[str, int, str]:
        """Extract month name, year, and month key from filename."""
        match = re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})\.csv$', filename, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid filename format: {filename}")
        
        month_name = match.group(1).capitalize()
        year = int(match.group(2))
        month_key = f"{month_name} {year}"
        
        return month_name, year, month_key
    
    def load_monthly_files(self) -> Dict[str, pd.DataFrame]:
        """Load all monthly CSV files."""
        files = self.find_monthly_files()
        
        if not files:
            print("WARNING: No monthly CSV files found (pattern: 'Mon YYYY.csv')")
            return {}
        
        for csv_file in files:
            try:
                month_name, year, month_key = self._extract_month_year(csv_file.name)
                self.months_found.append(month_key)
                
                # Skip header rows and load the actual campaign data
                df = pd.read_csv(csv_file, skiprows=2)
                
                # Filter to campaign rows (exclude "Total:" rows which are in Campaign status column)
                df = df[~df['Campaign status'].fillna('').str.contains('Total:', na=False, regex=False)].copy()
                
                # Also exclude rows where Campaign is NaN or empty
                df = df[df['Campaign'].notna()].copy()
                df = df[df['Campaign'].str.strip() != ''].copy()
                
                # Add month identifier
                df['Month'] = month_key
                df['Month_Num'] = (year - 2024) * 12 + ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month_name) + 1
                
                self.raw_dataframes[month_key] = df
                
            except Exception as e:
                print(f"  [ERROR] {csv_file.name}: {str(e)}")
        
        return self.raw_dataframes
    
    def get_dataframe(self, month_key: str) -> pd.DataFrame | None:
        """Get a specific month's dataframe."""
        return self.raw_dataframes.get(month_key, None)
    
    def get_all_months(self) -> List[str]:
        """Get list of all months loaded in order."""
        return sorted(self.months_found)
    
    def combine_all_months(self) -> pd.DataFrame:
        """Combine all monthly dataframes into single time-series."""
        # Ensure files are loaded first
        if not self.raw_dataframes:
            self.load_monthly_files()
        
        if not self.raw_dataframes:
            return pd.DataFrame()
        
        dfs = list(self.raw_dataframes.values())
        combined = pd.concat(dfs, ignore_index=True)
        
        # Sort by month
        month_order = self.get_all_months()
        if 'Month' in combined.columns and month_order:
            combined['Month'] = pd.Categorical(combined['Month'], categories=month_order, ordered=True)
            combined = combined.sort_values(['Month', 'Campaign']).reset_index(drop=True)
        
        return combined
        return combined
