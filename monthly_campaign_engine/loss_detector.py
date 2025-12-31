"""
Loss Detector
Identifies lost opportunities, customer loss signals, and performance leaks.
"""

import pandas as pd
import numpy as np
from typing import List, Dict


class LossDetector:
    """Detect lost opportunities and performance deterioration."""
    
    def __init__(self, metrics_df: pd.DataFrame):
        """Initialize with metrics dataframe."""
        self.df = metrics_df.copy()
        self.losses = []
    
    def detect_spend_conversion_mismatch(self) -> List[Dict]:
        """Detect months where spend increased but conversions dropped."""
        issues = []
        
        if 'Month' not in self.df.columns:
            return issues
        
        campaigns = self.df['campaign_name'].unique()
        
        for campaign in campaigns:
            campaign_data = self.df[self.df['campaign_name'] == campaign].sort_values('Month_Num')
            
            if len(campaign_data) < 2:
                continue
            
            for i in range(len(campaign_data) - 1):
                prev_row = campaign_data.iloc[i]
                curr_row = campaign_data.iloc[i + 1]
                
                spend_increase = curr_row['cost'] - prev_row['cost']
                conv_change = curr_row['conversions'] - prev_row['conversions']
                
                # Flag: Spend up, conversions down
                if spend_increase > 0 and conv_change < 0:
                    issues.append({
                        'campaign_name': campaign,
                        'campaign_type': campaign_data.iloc[i]['campaign_type'],
                        'issue_type': 'SPEND_UP_CONVERSIONS_DOWN',
                        'from_month': prev_row['Month'],
                        'to_month': curr_row['Month'],
                        'spend_change': round(spend_increase, 2),
                        'spend_change_pct': round((spend_increase / max(prev_row['cost'], 1)) * 100, 2),
                        'conversion_loss': int(abs(conv_change)),
                        'prev_cpa': round(prev_row['cpa'], 2),
                        'curr_cpa': round(curr_row['cpa'], 2),
                        'severity': 'HIGH',
                        'description': f"Spend increased by AED {spend_increase:.2f} but lost {int(abs(conv_change))} conversions"
                    })
        
        return issues
    
    def detect_efficiency_decline(self) -> List[Dict]:
        """Detect campaigns with declining efficiency (rising CPA)."""
        issues = []
        
        if 'Month' not in self.df.columns:
            return issues
        
        campaigns = self.df['campaign_name'].unique()
        
        for campaign in campaigns:
            campaign_data = self.df[self.df['campaign_name'] == campaign].sort_values('Month_Num')
            
            if len(campaign_data) < 2:
                continue
            
            first_cpa = campaign_data.iloc[0]['cpa']
            last_cpa = campaign_data.iloc[-1]['cpa']
            
            # Flag: CPA deteriorated significantly
            if first_cpa > 0 and last_cpa > first_cpa * 1.3:  # 30% increase
                issues.append({
                    'campaign_name': campaign,
                    'campaign_type': campaign_data.iloc[0]['campaign_type'],
                    'issue_type': 'DECLINING_EFFICIENCY',
                    'first_month': campaign_data.iloc[0]['Month'],
                    'last_month': campaign_data.iloc[-1]['Month'],
                    'initial_cpa': round(first_cpa, 2),
                    'final_cpa': round(last_cpa, 2),
                    'cpa_increase': round(last_cpa - first_cpa, 2),
                    'cpa_increase_pct': round(((last_cpa - first_cpa) / first_cpa) * 100, 2),
                    'severity': 'MEDIUM' if last_cpa < first_cpa * 1.5 else 'HIGH',
                    'description': f"CPA deteriorated from AED {first_cpa:.2f} to AED {last_cpa:.2f}"
                })
        
        return issues
    
    def detect_sudden_drops(self) -> List[Dict]:
        """Detect sudden drops in CTR or conversion rate."""
        issues = []
        
        if 'Month' not in self.df.columns:
            return issues
        
        campaigns = self.df['campaign_name'].unique()
        threshold = 0.5  # 50% drop
        
        for campaign in campaigns:
            campaign_data = self.df[self.df['campaign_name'] == campaign].sort_values('Month_Num')
            
            if len(campaign_data) < 2:
                continue
            
            for i in range(len(campaign_data) - 1):
                prev_row = campaign_data.iloc[i]
                curr_row = campaign_data.iloc[i + 1]
                
                # Check CTR drop
                if prev_row['ctr'] > 0:
                    ctr_change = (curr_row['ctr'] - prev_row['ctr']) / prev_row['ctr']
                    if ctr_change < -threshold:
                        issues.append({
                            'campaign_name': campaign,
                            'campaign_type': campaign_data.iloc[i]['campaign_type'],
                            'issue_type': 'CTR_SUDDEN_DROP',
                            'from_month': prev_row['Month'],
                            'to_month': curr_row['Month'],
                            'previous_ctr': round(prev_row['ctr'], 2),
                            'current_ctr': round(curr_row['ctr'], 2),
                            'ctr_drop_pct': round(ctr_change * 100, 2),
                            'severity': 'HIGH',
                            'description': f"CTR dropped from {prev_row['ctr']:.2f}% to {curr_row['ctr']:.2f}%"
                        })
                
                # Check CVR drop
                if prev_row['cvr'] > 0:
                    cvr_change = (curr_row['cvr'] - prev_row['cvr']) / prev_row['cvr']
                    if cvr_change < -threshold:
                        issues.append({
                            'campaign_name': campaign,
                            'campaign_type': campaign_data.iloc[i]['campaign_type'],
                            'issue_type': 'CVR_SUDDEN_DROP',
                            'from_month': prev_row['Month'],
                            'to_month': curr_row['Month'],
                            'previous_cvr': round(prev_row['cvr'], 2),
                            'current_cvr': round(curr_row['cvr'], 2),
                            'cvr_drop_pct': round(cvr_change * 100, 2),
                            'severity': 'HIGH',
                            'description': f"CVR dropped from {prev_row['cvr']:.2f}% to {curr_row['cvr']:.2f}%"
                        })
        
        return issues
    
    def detect_high_spend_low_roi(self) -> List[Dict]:
        """Detect high-spend campaigns with poor ROI."""
        issues = []
        
        if 'Month' not in self.df.columns:
            return issues
        
        # Find campaigns above median spend
        median_monthly_spend = self.df.groupby('Month')['cost'].median().mean()
        threshold = median_monthly_spend * 1.5  # 150% of median
        
        for _, row in self.df[self.df['cost'] > threshold].iterrows():
            # Flag if ROAS < 1.0 (not profitable)
            if row['roas'] < 1.0 and row['cost'] > 100:
                issues.append({
                    'campaign_name': row['campaign_name'],
                    'campaign_type': row['campaign_type'],
                    'issue_type': 'HIGH_SPEND_LOW_ROAS',
                    'month': row['Month'],
                    'spend': round(row['cost'], 2),
                    'conversions': int(row['conversions']),
                    'revenue': round(row['conv_value'], 2),
                    'roas': round(row['roas'], 2),
                    'severity': 'MEDIUM' if row['roas'] > 0.7 else 'HIGH',
                    'description': f"Spending AED {row['cost']:.2f} with ROAS of {row['roas']:.2f}x (unprofitable)"
                })
        
        return issues
    
    def detect_inactive_campaigns(self) -> List[Dict]:
        """Detect campaigns with zero activity."""
        issues = []
        
        inactive = self.df[
            (self.df['impressions'] == 0) | 
            ((self.df['clicks'] == 0) & (self.df['conversions'] == 0))
        ]
        
        for _, row in inactive.iterrows():
            issues.append({
                'campaign_name': row['campaign_name'],
                'campaign_type': row['campaign_type'],
                'issue_type': 'INACTIVE',
                'month': row['Month'] if 'Month' in row else 'Unknown',
                'impressions': int(row['impressions']),
                'clicks': int(row['clicks']),
                'conversions': int(row['conversions']),
                'spend': round(row['cost'], 2),
                'severity': 'MEDIUM',
                'description': 'Campaign showing zero or minimal activity (potential budget waste)'
            })
        
        return issues
    
    def get_all_losses(self) -> List[Dict]:
        """Get all detected losses."""
        all_losses = []
        all_losses.extend(self.detect_spend_conversion_mismatch())
        all_losses.extend(self.detect_efficiency_decline())
        all_losses.extend(self.detect_sudden_drops())
        all_losses.extend(self.detect_high_spend_low_roi())
        all_losses.extend(self.detect_inactive_campaigns())
        
        # Sort by severity
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        all_losses = sorted(
            all_losses,
            key=lambda x: severity_order.get(x.get('severity', 'LOW'), 3)
        )
        
        return all_losses
