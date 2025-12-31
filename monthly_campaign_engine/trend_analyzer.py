"""
Trend Analyzer
Detects trends and seasonal patterns across months.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class TrendAnalyzer:
    """Analyze trends and patterns across multiple months."""
    
    def __init__(self, metrics_df: pd.DataFrame):
        """Initialize with metrics dataframe."""
        self.df = metrics_df.copy()
        self.trends = []
    
    def calculate_month_over_month_change(self, metric: str) -> Dict:
        """Calculate month-over-month change for a metric."""
        if 'Month' not in self.df.columns or metric not in self.df.columns:
            return {}
        
        changes = {}
        months = sorted(self.df['Month'].unique())
        
        for i in range(1, len(months)):
            prev_month = months[i - 1]
            curr_month = months[i]
            
            prev_value = self.df[self.df['Month'] == prev_month][metric].sum()
            curr_value = self.df[self.df['Month'] == curr_month][metric].sum()
            
            if prev_value > 0:
                pct_change = ((curr_value - prev_value) / prev_value) * 100
            else:
                pct_change = 0 if curr_value == 0 else 100
            
            changes[f"{prev_month} → {curr_month}"] = {
                'previous_value': round(prev_value, 2),
                'current_value': round(curr_value, 2),
                'change_pct': round(pct_change, 2),
                'direction': 'UP' if pct_change > 0 else 'DOWN' if pct_change < 0 else 'FLAT'
            }
        
        return changes
    
    def detect_growth_trends(self) -> List[Dict]:
        """Detect campaigns with growth or decline trends."""
        trends = []
        
        if 'Month' not in self.df.columns:
            return trends
        
        campaigns = self.df['campaign_name'].unique()
        
        for campaign in campaigns:
            campaign_data = self.df[self.df['campaign_name'] == campaign].sort_values('Month_Num')
            
            if len(campaign_data) < 2:
                continue
            
            # Analyze conversion trend
            conversions = campaign_data['conversions'].values
            costs = campaign_data['cost'].values
            cpas = campaign_data['cpa'].values
            
            conv_trend = 'GROWING' if conversions[-1] > conversions[0] else 'DECLINING' if conversions[-1] < conversions[0] else 'FLAT'
            cpa_trend = 'IMPROVING' if cpas[-1] < cpas[0] else 'DETERIORATING' if cpas[-1] > cpas[0] else 'STABLE'
            
            # Calculate trend strength
            if len(conversions) > 1:
                first_half_conv = conversions[:len(conversions)//2].mean()
                second_half_conv = conversions[len(conversions)//2:].mean()
                trend_strength = 'Strong' if abs(second_half_conv - first_half_conv) > first_half_conv * 0.3 else 'Moderate' if abs(second_half_conv - first_half_conv) > 0 else 'Flat'
            else:
                trend_strength = 'Insufficient data'
            
            trends.append({
                'campaign_name': campaign,
                'campaign_type': campaign_data['campaign_type'].iloc[0],
                'conversion_trend': conv_trend,
                'cpa_trend': cpa_trend,
                'trend_strength': trend_strength,
                'first_month_conversions': int(conversions[0]),
                'last_month_conversions': int(conversions[-1]),
                'first_month_cpa': round(cpas[0], 2),
                'last_month_cpa': round(cpas[-1], 2),
                'total_months': len(campaign_data)
            })
        
        return trends
    
    def detect_seasonal_patterns(self) -> Dict:
        """Detect seasonal demand variations."""
        if 'Month' not in self.df.columns:
            return {}
        
        monthly_performance = {}
        
        for month in sorted(self.df['Month'].unique()):
            month_data = self.df[self.df['Month'] == month]
            monthly_performance[month] = {
                'total_conversions': int(month_data['conversions'].sum()),
                'total_spend': round(month_data['cost'].sum(), 2),
                'avg_cpa': round(month_data['cpa'].mean(), 2),
                'num_campaigns': len(month_data)
            }
        
        # Find peak and low months
        conversions_by_month = [v['total_conversions'] for v in monthly_performance.values()]
        if conversions_by_month:
            peak_month = max(monthly_performance.items(), key=lambda x: x[1]['total_conversions'])[0]
            low_month = min(monthly_performance.items(), key=lambda x: x[1]['total_conversions'])[0]
            avg_conversions = np.mean(conversions_by_month)
            
            return {
                'monthly_breakdown': monthly_performance,
                'peak_month': peak_month,
                'peak_conversions': int(monthly_performance[peak_month]['total_conversions']),
                'low_month': low_month,
                'low_conversions': int(monthly_performance[low_month]['total_conversions']),
                'average_conversions': round(avg_conversions, 2),
                'seasonality_ratio': round(
                    monthly_performance[peak_month]['total_conversions'] / 
                    max(monthly_performance[low_month]['total_conversions'], 1),
                    2
                )
            }
        
        return {}
    
    def detect_volatility(self) -> Dict:
        """Detect campaign volatility and stability."""
        volatility = {}
        
        if 'Month' not in self.df.columns:
            return volatility
        
        campaigns = self.df['campaign_name'].unique()
        
        for campaign in campaigns:
            campaign_data = self.df[self.df['campaign_name'] == campaign].sort_values('Month_Num')
            
            if len(campaign_data) < 2:
                continue
            
            cpa_values = campaign_data['cpa'].values
            cvr_values = campaign_data['cvr'].values
            
            # Calculate volatility as coefficient of variation
            cpa_volatility = (np.std(cpa_values) / np.mean(cpa_values) * 100) if np.mean(cpa_values) > 0 else 0
            cvr_volatility = (np.std(cvr_values) / np.mean(cvr_values) * 100) if np.mean(cvr_values) > 0 else 0
            
            stability = 'UNSTABLE' if cpa_volatility > 50 else 'MODERATE' if cpa_volatility > 25 else 'STABLE'
            
            volatility[campaign] = {
                'cpa_volatility': round(cpa_volatility, 2),
                'cvr_volatility': round(cvr_volatility, 2),
                'stability_rating': stability,
                'num_months': len(campaign_data)
            }
        
        return volatility
