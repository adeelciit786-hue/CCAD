"""
Metrics Engine
Calculates standard performance metrics from normalized campaign data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class MetricsEngine:
    """Calculate performance metrics from campaign data."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with normalized dataframe."""
        self.df = df.copy()
        self.metrics = pd.DataFrame()
    
    def calculate_ctr(self) -> pd.Series:
        """Calculate Click-Through Rate (%)."""
        self.df['ctr'] = 0.0
        mask = self.df['impressions'] > 0
        self.df.loc[mask, 'ctr'] = (self.df.loc[mask, 'clicks'] / self.df.loc[mask, 'impressions']) * 100
        return self.df['ctr']
    
    def calculate_conversion_rate(self) -> pd.Series:
        """Calculate Conversion Rate (%)."""
        self.df['cvr'] = 0.0
        mask = self.df['clicks'] > 0
        self.df.loc[mask, 'cvr'] = (self.df.loc[mask, 'conversions'] / self.df.loc[mask, 'clicks']) * 100
        return self.df['cvr']
    
    def calculate_cpc(self) -> pd.Series:
        """Calculate Cost Per Click (AED)."""
        self.df['cpc'] = 0.0
        mask = self.df['clicks'] > 0
        self.df.loc[mask, 'cpc'] = self.df.loc[mask, 'cost'] / self.df.loc[mask, 'clicks']
        return self.df['cpc']
    
    def calculate_cpa(self) -> pd.Series:
        """Calculate Cost Per Acquisition (AED)."""
        self.df['cpa'] = 0.0
        mask = self.df['conversions'] > 0
        self.df.loc[mask, 'cpa'] = self.df.loc[mask, 'cost'] / self.df.loc[mask, 'conversions']
        return self.df['cpa']
    
    def calculate_roas(self) -> pd.Series:
        """Calculate Return on Ad Spend (multiplier)."""
        self.df['roas'] = 0.0
        mask = self.df['cost'] > 0
        self.df.loc[mask, 'roas'] = self.df.loc[mask, 'conv_value'] / self.df.loc[mask, 'cost']
        return self.df['roas']
    
    def calculate_spend_share(self) -> pd.Series:
        """Calculate % of total monthly spend."""
        self.df['spend_share'] = 0.0
        
        if 'Month' in self.df.columns:
            for month in self.df['Month'].unique():
                mask = self.df['Month'] == month
                total_spend = float(self.df.loc[mask, 'cost'].sum())  # type: ignore
                if total_spend > 0:
                    self.df.loc[mask, 'spend_share'] = (self.df.loc[mask, 'cost'] / total_spend) * 100  # type: ignore
        else:
            total_spend = float(self.df['cost'].sum())  # type: ignore
            if total_spend > 0:
                self.df['spend_share'] = (self.df['cost'] / total_spend) * 100  # type: ignore
        
        return self.df['spend_share']
    
    def calculate_all_metrics(self) -> pd.DataFrame:
        """Calculate all metrics."""
        print("Calculating CTR...")
        self.calculate_ctr()
        
        print("Calculating Conversion Rate...")
        self.calculate_conversion_rate()
        
        print("Calculating CPC...")
        self.calculate_cpc()
        
        print("Calculating CPA...")
        self.calculate_cpa()
        
        print("Calculating ROAS...")
        self.calculate_roas()
        
        print("Calculating Spend Share...")
        self.calculate_spend_share()
        
        # Handle NaN and inf values (but exclude categorical columns)
        self.df = self.df.replace([np.inf, -np.inf], 0)
        
        # Only fillna for numeric columns
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(0)
        
        return self.df
    
    def get_summary_by_month(self) -> Dict:
        """Get monthly summary metrics."""
        if 'Month' not in self.df.columns:
            return {}
        
        summary = {}
        
        for month in sorted(self.df['Month'].unique()):
            month_data = self.df[self.df['Month'] == month]
            
            summary[month] = {
                'total_impressions': int(month_data['impressions'].sum()),
                'total_clicks': int(month_data['clicks'].sum()),
                'total_cost': round(month_data['cost'].sum(), 2),
                'total_conversions': int(month_data['conversions'].sum()),
                'total_revenue': round(month_data['conv_value'].sum(), 2),
                'avg_ctr': round(month_data['ctr'].mean(), 2),
                'avg_cvr': round(month_data['cvr'].mean(), 2),
                'avg_cpc': round(month_data['cpc'].mean(), 2),
                'avg_cpa': round(month_data['cpa'].mean(), 2),
                'avg_roas': round(month_data['roas'].mean(), 2),
                'num_campaigns': len(month_data)
            }
        
        return summary
    
    def get_campaign_metrics_by_month(self) -> pd.DataFrame:
        """Get detailed metrics for each campaign-month combination."""
        return self.df[[
            'campaign_name', 'campaign_type', 'Month', 'Month_Num',
            'impressions', 'clicks', 'cost', 'conversions', 'conv_value',
            'ctr', 'cvr', 'cpc', 'cpa', 'roas', 'spend_share'
        ]].copy()
