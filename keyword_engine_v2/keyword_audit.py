"""
Keyword Audit Module
Deep audit of keyword health and performance issues.
"""

import pandas as pd
from typing import List, Dict


class KeywordAuditor:
    """Audit keyword performance and detect issues."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize auditor with keyword data."""
        self.df = df.copy()
        self.issues = []
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate key metrics for each keyword."""
        self.df['ctr'] = (self.df['clicks'] / self.df['impressions'] * 100).fillna(0)
        self.df['conversion_rate'] = (self.df['conversions'] / self.df['clicks'] * 100).fillna(0)
        self.df['cpa'] = (self.df['cost'] / self.df['conversions']).fillna(float('inf'))
        self.df['cpc'] = (self.df['cost'] / self.df['clicks']).fillna(0)
        
        if 'revenue' in self.df.columns:
            self.df['roas'] = (self.df['revenue'] / self.df['cost']).fillna(0)
            self.df['roas'] = self.df['roas'].replace([float('inf'), -float('inf')], 0)
    
    def audit_keyword_health(self) -> List[Dict]:
        """Perform comprehensive audit and detect issues."""
        issues = []
        
        for idx, row in self.df.iterrows():
            keyword_issues = self._audit_keyword(row)
            issues.extend(keyword_issues)
        
        return sorted(issues, key=lambda x: {'High': 0, 'Medium': 1, 'Low': 2}.get(x['severity'], 3))
    
    def _audit_keyword(self, row) -> List[Dict]:
        """Audit a single keyword row."""
        issues = []
        keyword = row['keyword']
        
        # Issue 1: Impressions but no clicks
        if row['impressions'] > 50 and row['clicks'] == 0:
            issues.append({
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'issue_type': 'NO_CLICKS',
                'severity': 'High',
                'description': f"High impressions ({int(row['impressions'])}) but zero clicks (CTR: 0%)",
                'value': int(row['impressions'])
            })
        
        # Issue 2: Clicks but no conversions
        if row['clicks'] > 10 and row['conversions'] == 0:
            issues.append({
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'issue_type': 'NO_CONVERSIONS',
                'severity': 'High',
                'description': f"Traffic ({int(row['clicks'])} clicks) but zero conversions (CVR: 0%)",
                'value': int(row['clicks'])
            })
        
        # Issue 3: Low CTR
        if row['impressions'] > 100 and row['ctr'] < 1.0:
            issues.append({
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'issue_type': 'LOW_CTR',
                'severity': 'Medium',
                'description': f"Low click-through rate: {row['ctr']:.2f}%",
                'value': row['ctr']
            })
        
        # Issue 4: High CPA
        if row['conversions'] > 0 and row['cpa'] > 300:
            issues.append({
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'issue_type': 'HIGH_CPA',
                'severity': 'Medium',
                'description': f"High cost per acquisition: AED {row['cpa']:.2f}",
                'value': row['cpa']
            })
        
        # Issue 5: Low ROAS
        if 'revenue' in self.df.columns and row['revenue'] > 0 and row['roas'] > 0 and row['roas'] < 1.5:
            issues.append({
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'issue_type': 'LOW_ROAS',
                'severity': 'Medium',
                'description': f"Low return on ad spend: {row['roas']:.2f}x",
                'value': row['roas']
            })
        
        # Issue 6: High spend low return
        if row['cost'] > 500 and row['conversions'] < 2:
            issues.append({
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'issue_type': 'HIGH_SPEND_LOW_RETURN',
                'severity': 'High',
                'description': f"High spend (AED {row['cost']:.2f}) with minimal conversions ({int(row['conversions'])})",
                'value': row['cost']
            })
        
        return issues
    
    def get_keyword_metrics(self, keyword: str | None = None) -> Dict:
        """Get metrics for specific keyword or all."""
        if keyword:
            keyword_data = self.df[self.df['keyword'] == keyword]
            if len(keyword_data) == 0:
                return {}
            row = keyword_data.iloc[0]
            return {
                'keyword': keyword,
                'campaign': row['campaign_name'],
                'ad_group': row['ad_group_name'],
                'match_type': row['match_type'],
                'impressions': int(row['impressions']),
                'clicks': int(row['clicks']),
                'ctr': round(row['ctr'], 2),
                'cost': round(row['cost'], 2),
                'conversions': int(row['conversions']),
                'conversion_rate': round(row['conversion_rate'], 2),
                'cpa': round(row['cpa'], 2),
                'cpc': round(row['cpc'], 2),
                'revenue': round(row['revenue'], 2) if 'revenue' in self.df.columns else 0,
                'roas': round(row['roas'], 2) if 'roas' in self.df.columns else 0,
                'quality_score': int(row['quality_score']) if 'quality_score' in self.df.columns and row['quality_score'] > 0 else 'N/A'
            }
        
        result = {}
        for keyword in self.df['keyword'].unique():
            result[keyword] = self.get_keyword_metrics(keyword)
        return result
    
    def get_worst_performers(self, metric: str = 'cpa', limit: int = 10) -> List[Dict]:
        """Get worst performing keywords by metric."""
        if metric == 'cpa':
            sorted_df = self.df.sort_values('cpa', ascending=False)
        elif metric == 'ctr':
            sorted_df = self.df.sort_values('ctr', ascending=True)
        elif metric == 'cost':
            sorted_df = self.df.sort_values('cost', ascending=False)
        else:
            sorted_df = self.df
        
        result = []
        for idx, row in sorted_df.head(limit).iterrows():
            result.append({
                'keyword': row['keyword'],
                'campaign': row['campaign_name'],
                'metric': metric,
                'value': round(row[metric], 2) if metric in row else 'N/A'
            })
        
        return result
