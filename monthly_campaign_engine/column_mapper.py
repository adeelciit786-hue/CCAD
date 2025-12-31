"""
Column Mapper
Maps Google Ads export columns to standard performance metrics.
Handles variations in column naming across exports.
"""

import pandas as pd
from typing import Dict, List, Tuple


class ColumnMapper:
    """Map and normalize Google Ads export columns."""
    
    # Standard column mappings with possible aliases
    COLUMN_MAPPINGS = {
        'campaign_name': ['Campaign', 'campaign', 'Campaign name'],
        'campaign_type': ['Campaign type', 'campaign_type', 'Type'],
        'impressions': ['Impr.', 'Impressions', 'Impr', 'impressions'],
        'clicks': ['Interactions', 'Clicks', 'clicks', 'Clks'],
        'cost': ['Cost', 'cost', 'Spend', 'Ad spend'],
        'conversions': ['Conversions', 'conversions', 'Conv.', 'Conv'],
        'conv_value': ['Conv. value', 'Conversion value', 'conv_value', 'Revenue'],
        'conv_rate': ['Conv. rate', 'Conversion rate', 'conv_rate'],
        'interaction_rate': ['Interaction rate', 'CTR', 'Click rate', 'interaction_rate'],
        'avg_cpc': ['Avg. cost', 'CPC', 'avg_cost', 'Avg. CPC'],
        'campaign_status': ['Campaign status', 'Status'],
        'optimization_score': ['Optimization score', 'Opt. score'],
        'bid_strategy': ['Bid strategy type', 'Bid strategy'],
    }
    
    def __init__(self, df: pd.DataFrame):
        """Initialize mapper with dataframe."""
        self.df = df.copy()
        self.original_columns = df.columns.tolist()
        self.mapping_report = {}
    
    def find_column(self, target_key: str) -> str | None:
        """Find the actual column name for a target key."""
        possible_names = self.COLUMN_MAPPINGS.get(target_key, [])
        
        for col in possible_names:
            if col in self.df.columns:
                return col
        
        return None
    
    def normalize_columns(self) -> pd.DataFrame:
        """Map and normalize all columns."""
        normalized = pd.DataFrame()
        
        for standard_name, possible_names in self.COLUMN_MAPPINGS.items():
            for col_name in possible_names:
                if col_name in self.df.columns:
                    normalized[standard_name] = self.df[col_name]
                    self.mapping_report[standard_name] = col_name
                    break
        
        # Preserve month columns if they exist
        if 'Month' in self.df.columns:
            normalized['Month'] = self.df['Month']
        if 'Month_Num' in self.df.columns:
            normalized['Month_Num'] = self.df['Month_Num']
        
        return normalized
    
    def clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean numeric columns (remove commas, convert to float)."""
        numeric_cols = [
            'impressions', 'clicks', 'cost', 'conversions', 'conv_value',
            'interaction_rate', 'avg_cpc', 'optimization_score'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                # Remove commas and convert to numeric
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(',', ''),
                    errors='coerce'
                )
        
        # Clean percentage columns
        pct_cols = ['conv_rate', 'interaction_rate']
        for col in pct_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace('%', ''),
                    errors='coerce'
                )
        
        return df
    
    def map_and_clean(self) -> Tuple[pd.DataFrame, Dict]:
        """Execute full mapping and cleaning pipeline."""
        print("Normalizing column names...")
        df = self.normalize_columns()
        
        print("Cleaning numeric values...")
        df = self.clean_numeric_columns(df)
        
        # Fill NaN with 0 for numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        print(f"Column mapping successful. {len(self.mapping_report)} columns mapped.")
        
        return df, self.mapping_report
