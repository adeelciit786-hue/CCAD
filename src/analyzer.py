"""
Performance Analyzer Module
Calculates key performance metrics and detects trends/risks.
"""

import pandas as pd
from typing import Dict


class PerformanceAnalyzer:
    """Analyze Google Ads campaign performance metrics."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with data.
        
        Args:
            df: DataFrame with campaign data
        """
        self.df = df.copy()
        self.campaign_metrics = {}
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate key metrics for each campaign."""
        grouped = self.df.groupby('campaign_name')
        
        for campaign_name, group in grouped:
            total_impressions = group['impressions'].sum()
            total_clicks = group['clicks'].sum()
            total_cost = group['cost'].sum()
            total_conversions = group['conversions'].sum()
            total_revenue = group['revenue'].sum() if 'revenue' in group.columns else 0
            
            # Calculate metrics
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            cpa = (total_cost / total_conversions) if total_conversions > 0 else float('inf')
            roas = (total_revenue / total_cost) if total_cost > 0 and total_revenue > 0 else 0
            avg_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
            
            self.campaign_metrics[campaign_name] = {
                'campaign_type': group['campaign_type'].iloc[0] if 'campaign_type' in group.columns else 'Unknown',
                'platform': group['platform'].iloc[0] if 'platform' in group.columns else 'Unknown',
                'impressions': int(total_impressions),
                'clicks': int(total_clicks),
                'cost': round(total_cost, 2),
                'conversions': int(total_conversions),
                'revenue': round(total_revenue, 2),
                'ctr': round(ctr, 2),  # %
                'conversion_rate': round(conversion_rate, 2),  # %
                'cpa': round(cpa, 2),
                'cpc': round(avg_cpc, 2),
                'roas': round(roas, 2)
            }
    
    def get_campaign_metrics(self, campaign_name: str | None = None) -> dict[str, dict[str, int | float | str]]:
        """
        Get metrics for a specific campaign or all campaigns.
        
        Args:
            campaign_name: Campaign to analyze, or None for all
            
        Returns:
            Dictionary of metrics
        """
        if campaign_name:
            return self.campaign_metrics.get(campaign_name, {})
        return self.campaign_metrics
    
    def compare_campaigns(self) -> dict[str, tuple[str, float] | None]:
        """
        Compare all campaigns side-by-side.
        
        Returns:
            Dictionary with comparisons and rankings
        """
        if not self.campaign_metrics:
            return {}
        
        # Sort by different metrics
        by_cpa = sorted(
            self.campaign_metrics.items(),
            key=lambda x: x[1]['cpa'] if x[1]['cpa'] != float('inf') else float('inf')
        )
        
        by_roas = sorted(
            self.campaign_metrics.items(),
            key=lambda x: x[1]['roas'],
            reverse=True
        )
        
        by_ctr = sorted(
            self.campaign_metrics.items(),
            key=lambda x: x[1]['ctr'],
            reverse=True
        )
        
        by_conversion_rate = sorted(
            self.campaign_metrics.items(),
            key=lambda x: x[1]['conversion_rate'],
            reverse=True
        )
        
        return {
            'best_cpa': (by_cpa[0][0], by_cpa[0][1]['cpa']) if by_cpa else None,
            'worst_cpa': (by_cpa[-1][0], by_cpa[-1][1]['cpa']) if by_cpa else None,
            'best_roas': (by_roas[0][0], by_roas[0][1]['roas']) if by_roas else None,
            'worst_roas': (by_roas[-1][0], by_roas[-1][1]['roas']) if by_roas else None,
            'best_ctr': (by_ctr[0][0], by_ctr[0][1]['ctr']) if by_ctr else None,
            'worst_ctr': (by_ctr[-1][0], by_ctr[-1][1]['ctr']) if by_ctr else None,
            'best_conversion_rate': (by_conversion_rate[0][0], by_conversion_rate[0][1]['conversion_rate']) if by_conversion_rate else None,
            'worst_conversion_rate': (by_conversion_rate[-1][0], by_conversion_rate[-1][1]['conversion_rate']) if by_conversion_rate else None,
        }
    
    def detect_trends_and_risks(self) -> list[dict[str, str | int | float]]:
        """
        Detect trends and potential issues in campaign performance.
        
        Returns:
            List of detected issues with details
        """
        issues = []
        
        for campaign_name, metrics in self.campaign_metrics.items():
            # High CPA detection
            if metrics['conversions'] > 0:
                avg_cpa = metrics['cpa']
                if avg_cpa > 500:  # Threshold for high CPA
                    issues.append({
                        'campaign': campaign_name,
                        'issue_type': 'HIGH_CPA',
                        'severity': 'High' if avg_cpa > 1000 else 'Medium',
                        'value': avg_cpa,
                        'description': f"High cost per acquisition (CPA): AED {avg_cpa}"
                    })
            
            # Low CTR detection
            if metrics['ctr'] < 1.0 and metrics['impressions'] > 100:
                issues.append({
                    'campaign': campaign_name,
                    'issue_type': 'LOW_CTR',
                    'severity': 'Medium',
                    'value': metrics['ctr'],
                    'description': f"Low click-through rate (CTR): {metrics['ctr']}%"
                })
            
            # Low conversion rate detection
            if metrics['clicks'] > 50 and metrics['conversion_rate'] < 1.0:
                issues.append({
                    'campaign': campaign_name,
                    'issue_type': 'LOW_CONVERSION_RATE',
                    'severity': 'High',
                    'value': metrics['conversion_rate'],
                    'description': f"Low conversion rate: {metrics['conversion_rate']}%"
                })
            
            # Low ROAS detection
            if metrics['roas'] > 0 and metrics['roas'] < 1.5 and metrics['cost'] > 100:
                issues.append({
                    'campaign': campaign_name,
                    'issue_type': 'LOW_ROAS',
                    'severity': 'Medium',
                    'value': metrics['roas'],
                    'description': f"Low return on ad spend (ROAS): {metrics['roas']}"
                })
            
            # High spend with low return
            if metrics['cost'] > 5000 and metrics['conversions'] < 10:
                issues.append({
                    'campaign': campaign_name,
                    'issue_type': 'HIGH_SPEND_LOW_RETURN',
                    'severity': 'High',
                    'value': metrics['cost'],
                    'description': f"High spend (AED {metrics['cost']}) with minimal conversions"
                })
        
        return sorted(issues, key=lambda x: {'High': 0, 'Medium': 1, 'Low': 2}.get(str(x.get('severity', 'Low')), 3))
    
    def analyze_by_platform(self) -> Dict:
        """
        Analyze aggregate metrics by platform (Search, Display, App).
        
        Returns:
            Dictionary with platform-level metrics
        """
        if 'platform' not in self.df.columns:
            return {}
        
        platform_data = {}
        grouped = self.df.groupby('platform')
        
        for platform, group in grouped:
            total_impressions = group['impressions'].sum()
            total_clicks = group['clicks'].sum()
            total_cost = group['cost'].sum()
            total_conversions = group['conversions'].sum()
            total_revenue = group['revenue'].sum() if 'revenue' in group.columns else 0
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            cpa = (total_cost / total_conversions) if total_conversions > 0 else float('inf')
            roas = (total_revenue / total_cost) if total_cost > 0 and total_revenue > 0 else 0
            
            platform_data[platform] = {
                'impressions': int(total_impressions),
                'clicks': int(total_clicks),
                'cost': round(total_cost, 2),
                'conversions': int(total_conversions),
                'revenue': round(total_revenue, 2),
                'ctr': round(ctr, 2),
                'conversion_rate': round(conversion_rate, 2),
                'cpa': round(cpa, 2),
                'roas': round(roas, 2),
                'percentage_of_budget': round((total_cost / self.df['cost'].sum() * 100), 2)
            }
        
        return platform_data
    
    def analyze_by_device_os(self) -> Dict:
        """
        Analyze aggregate metrics by device OS (iOS, Android, Web).
        
        Returns:
            Dictionary with device OS-level metrics
        """
        if 'device_os' not in self.df.columns:
            return {}
        
        device_data = {}
        grouped = self.df.groupby('device_os')
        
        for device_os, group in grouped:
            total_impressions = group['impressions'].sum()
            total_clicks = group['clicks'].sum()
            total_cost = group['cost'].sum()
            total_conversions = group['conversions'].sum()
            total_revenue = group['revenue'].sum() if 'revenue' in group.columns else 0
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            cpa = (total_cost / total_conversions) if total_conversions > 0 else float('inf')
            roas = (total_revenue / total_cost) if total_cost > 0 and total_revenue > 0 else 0
            
            device_data[device_os] = {
                'impressions': int(total_impressions),
                'clicks': int(total_clicks),
                'cost': round(total_cost, 2),
                'conversions': int(total_conversions),
                'revenue': round(total_revenue, 2),
                'ctr': round(ctr, 2),
                'conversion_rate': round(conversion_rate, 2),
                'cpa': round(cpa, 2),
                'roas': round(roas, 2),
                'percentage_of_budget': round((total_cost / self.df['cost'].sum() * 100), 2)
            }
        
        return device_data
