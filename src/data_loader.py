"""
Data Loader Module
Handles CSV loading, validation, and data cleaning for Google Ads performance data.
"""

import pandas as pd
from typing import Tuple, Dict, List
import os


class DataLoader:
    """Load and validate Google Ads performance data from CSV files."""
    
    REQUIRED_COLUMNS = [
        'date',
        'campaign_name',
        'campaign_type',
        'impressions',
        'clicks',
        'cost',
        'conversions'
    ]
    
    OPTIONAL_COLUMNS = ['revenue', 'installs', 'platform', 'device_os']
    
    def __init__(self, filepath: str):
        """
        Initialize DataLoader with CSV file path.
        
        Args:
            filepath: Path to the CSV file
        """
        self.filepath = filepath
        self.df: pd.DataFrame | None = None
        self.validation_warnings = []
        self.validation_errors = []
    
    def load(self) -> pd.DataFrame:
        """
        Load CSV file and perform initial validation.
        
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        try:
            self.df = pd.read_csv(self.filepath)
            print(f"[OK] Loaded {len(self.df)} rows from {self.filepath}")
        except Exception as e:
            raise ValueError(f"Failed to load CSV: {str(e)}")
        
        self._validate_columns()
        self._clean_data()
        
        return self.df
    
    def _validate_columns(self) -> None:
        """Validate that required columns exist."""
        assert self.df is not None, "DataFrame not initialized"
        missing = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        print(f"[OK] All required columns present")
    
    def _clean_data(self) -> None:
        """Clean and normalize data."""
        assert self.df is not None, "DataFrame not initialized"
        # Convert date to datetime
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        # Convert numeric columns
        numeric_cols = ['impressions', 'clicks', 'cost', 'conversions', 'revenue', 'installs']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Fill NaN values with 0 for numeric columns
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(0)
        
        print(f"[OK] Data cleaned and normalized")
    
    def validate_data_quality(self) -> Tuple[bool, List[str], List[str]]:
        """
        Perform comprehensive data quality checks.
        
        Returns:
            Tuple of (is_valid, warnings, errors)
        """
        assert self.df is not None, "DataFrame not initialized"
        self.validation_warnings = []
        self.validation_errors = []
        
        # Check for missing values in required columns
        for col in self.REQUIRED_COLUMNS:
            if self.df[col].isna().sum() > 0:
                self.validation_warnings.append(f"Missing values in {col}: {self.df[col].isna().sum()}")
        
        # Check for zero impressions/clicks
        zero_impressions = (self.df['impressions'] == 0).sum()
        if zero_impressions > 0:
            self.validation_warnings.append(f"Records with zero impressions: {zero_impressions}")
        
        zero_clicks = (self.df['clicks'] == 0).sum()
        if zero_clicks > 0:
            self.validation_warnings.append(f"Records with zero clicks: {zero_clicks}")
        
        # Check for negative values
        for col in ['cost', 'conversions', 'impressions', 'clicks']:
            if (self.df[col] < 0).any():
                self.validation_errors.append(f"Negative values found in {col}")
        
        # Check for insufficient data volume per campaign
        campaign_volumes = self.df.groupby('campaign_name')['impressions'].sum()
        low_volume_campaigns = campaign_volumes[campaign_volumes < 100]
        if len(low_volume_campaigns) > 0:
            for campaign, volume in low_volume_campaigns.items():
                self.validation_warnings.append(
                    f"Low data volume for '{campaign}': {int(volume)} impressions"
                )
        
        is_valid = len(self.validation_errors) == 0
        
        return is_valid, self.validation_warnings, self.validation_errors
    
    def get_summary(self) -> Dict:
        """
        Get a summary of loaded data.
        
        Returns:
            Dictionary with data overview
        """
        assert self.df is not None, "DataFrame not initialized"
        return {
            'total_rows': len(self.df),
            'date_range': f"{self.df['date'].min().date()} to {self.df['date'].max().date()}" if 'date' in self.df.columns else 'N/A',
            'campaigns': self.df['campaign_name'].nunique(),
            'campaign_types': self.df['campaign_type'].unique().tolist() if 'campaign_type' in self.df.columns else [],
            'total_impressions': int(self.df['impressions'].sum()),
            'total_cost': float(self.df['cost'].sum()),
            'total_conversions': int(self.df['conversions'].sum())
        }
