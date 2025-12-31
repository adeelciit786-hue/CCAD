"""
Keyword Loader Module
Loads and validates keyword-level data from CSV files.
"""

import pandas as pd
from typing import Tuple, Dict, List
import os


class KeywordLoader:
    """Load and validate keyword-level Google Ads data."""
    
    REQUIRED_COLUMNS = [
        'campaign_name',
        'ad_group_name',
        'keyword',
        'match_type',
        'impressions',
        'clicks',
        'cost',
        'conversions'
    ]
    
    OPTIONAL_COLUMNS = ['revenue', 'search_term', 'quality_score', 'ctr_percent', 'conversion_rate_percent']
    
    def __init__(self, filepath: str):
        """Initialize keyword loader with CSV file path."""
        self.filepath = filepath
        self.df: pd.DataFrame | None = None
        self.validation_warnings = []
        self.validation_errors = []
    
    def load(self) -> pd.DataFrame:
        """Load and validate CSV file."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        try:
            # Try standard CSV first
            self.df = pd.read_csv(self.filepath)
        except Exception as e:
            # Try Google Ads format (skip first 2 rows)
            try:
                self.df = pd.read_csv(self.filepath, skiprows=2)
            except Exception as e2:
                raise ValueError(f"Failed to load CSV: {str(e)}")
        
        # Convert Google Ads format if needed
        self._convert_google_ads_format()
        
        print(f"[OK] Loaded {len(self.df)} keywords from {self.filepath}")
        
        self._validate_columns()
        self._clean_data()
        
        return self.df
    
    def _convert_google_ads_format(self) -> None:
        """Convert Google Ads keyword report format to required format."""
        assert self.df is not None, "DataFrame not initialized"
        # Check if this is a Google Ads export (has 'Keyword' column instead of 'keyword')
        if 'Keyword' in self.df.columns and 'keyword' not in self.df.columns:
            # Google Ads export - convert columns
            column_mapping = {
                'Keyword': 'keyword',
                'Match type': 'match_type',
                'Clicks': 'clicks',
                'Impr.': 'impressions',
                'Avg. CPC': 'avg_cpc',
                'Cost': 'cost',
                'Conversions': 'conversions',
                'Conv. rate': 'conversion_rate',
                'CTR': 'ctr'
            }
            
            # Rename existing columns
            for old_col, new_col in column_mapping.items():
                if old_col in self.df.columns:
                    self.df.rename(columns={old_col: new_col}, inplace=True)
            
            # Add missing required columns
            if 'campaign_name' not in self.df.columns:
                self.df['campaign_name'] = 'Website Traffic'
            if 'ad_group_name' not in self.df.columns:
                self.df['ad_group_name'] = 'Keywords'
            
            # Clean keyword values (remove extra quotes from Google Ads)
            if 'keyword' in self.df.columns:
                self.df['keyword'] = self.df['keyword'].astype(str).str.replace('"""', '"').str.strip()
            
            # Remove empty keywords
            self.df = self.df[self.df['keyword'].str.strip() != '']
    
    def _validate_columns(self) -> None:
        """Validate required columns exist."""
        assert self.df is not None, "DataFrame not initialized"
        missing = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        print(f"[OK] All required columns present")
    
    def _clean_data(self) -> None:
        """Clean and normalize data."""
        assert self.df is not None, "DataFrame not initialized"
        # Remove total rows (Google Ads summary rows)
        if 'match_type' in self.df.columns:
            self.df = self.df[~self.df['match_type'].astype(str).str.lower().str.contains('total:', regex=False)]
        
        # Clean keyword values (remove extra quotes from Google Ads)
        if 'keyword' in self.df.columns:
            self.df['keyword'] = self.df['keyword'].astype(str).str.replace('"""', '"', regex=False).str.strip()
            self.df['keyword'] = self.df['keyword'].astype(str).str.replace('^"+|"+$', '', regex=True).str.strip()
        
        # Convert numeric columns
        numeric_cols = ['impressions', 'clicks', 'cost', 'conversions', 'revenue', 'quality_score', 'ctr_percent', 'conversion_rate_percent']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Fill NaN values with 0 for numeric columns
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(0)
        
        # Standardize match_type
        if 'match_type' in self.df.columns:
            self.df['match_type'] = self.df['match_type'].astype(str).str.lower().str.strip()
            # Remove " match" suffix from Google Ads format (e.g., "phrase match" -> "phrase")
            self.df['match_type'] = self.df['match_type'].str.replace(' match$', '', regex=True)
        
        print(f"[OK] Data cleaned and normalized")
    
    def validate_data_quality(self) -> Tuple[bool, List[str], List[str]]:
        """Perform comprehensive data quality checks."""
        self.validation_warnings = []
        self.validation_errors = []
        assert self.df is not None, "DataFrame not initialized"
        
        # Check for missing values
        for col in self.REQUIRED_COLUMNS:
            if self.df[col].isna().sum() > 0:
                self.validation_warnings.append(f"Missing values in {col}: {self.df[col].isna().sum()}")
        
        # Check for invalid match types
        valid_match_types = ['exact', 'phrase', 'broad', 'modified broad']
        invalid_matches = self.df[~self.df['match_type'].isin(valid_match_types)]
        if len(invalid_matches) > 0:
            self.validation_warnings.append(f"Invalid match types found: {len(invalid_matches)}")
        
        # Check for negative values
        for col in ['cost', 'conversions', 'impressions', 'clicks']:
            if (self.df[col] < 0).any():
                self.validation_errors.append(f"Negative values found in {col}")
        
        # Check for zero impressions
        zero_impressions = (self.df['impressions'] == 0).sum()
        if zero_impressions > 0:
            self.validation_warnings.append(f"Keywords with zero impressions: {zero_impressions}")
        
        is_valid = len(self.validation_errors) == 0
        return is_valid, self.validation_warnings, self.validation_errors
    
    def get_summary(self) -> Dict:
        """Get summary of loaded keyword data."""
        assert self.df is not None, "DataFrame not initialized"
        return {
            'total_keywords': len(self.df),
            'campaigns': self.df['campaign_name'].nunique(),
            'ad_groups': self.df['ad_group_name'].nunique(),
            'match_types': self.df['match_type'].unique().tolist(),
            'total_impressions': int(self.df['impressions'].sum()),
            'total_cost': float(self.df['cost'].sum()),
            'total_conversions': int(self.df['conversions'].sum()),
            'total_revenue': float(self.df['revenue'].sum()) if 'revenue' in self.df.columns else 0
        }
