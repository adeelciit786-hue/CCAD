"""
Match Type Optimizer Module
Analyzes and optimizes keyword match type strategy.
"""

import pandas as pd
from typing import List, Dict


class MatchTypeOptimizer:
    """Optimize keyword match type strategy."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize optimizer with keyword data."""
        self.df = df.copy()
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate metrics for analysis."""
        self.df['ctr'] = (self.df['clicks'] / self.df['impressions'] * 100).fillna(0)
        self.df['conversion_rate'] = (self.df['conversions'] / self.df['clicks'] * 100).fillna(0)
        self.df['cpa'] = (self.df['cost'] / self.df['conversions']).fillna(float('inf'))
        self.df['cpc'] = (self.df['cost'] / self.df['clicks']).fillna(0)
    
    def analyze_match_type_performance(self) -> Dict:
        """Analyze performance by match type."""
        performance = {}
        
        for match_type in self.df['match_type'].unique():
            match_data = self.df[self.df['match_type'] == match_type]
            
            total_impressions = match_data['impressions'].sum()
            total_clicks = match_data['clicks'].sum()
            total_cost = match_data['cost'].sum()
            total_conversions = match_data['conversions'].sum()
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            cpa = (total_cost / total_conversions) if total_conversions > 0 else float('inf')
            cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
            
            performance[match_type] = {
                'keywords_count': len(match_data),
                'impressions': int(total_impressions),
                'clicks': int(total_clicks),
                'ctr': round(ctr, 2),
                'cost': round(total_cost, 2),
                'conversions': int(total_conversions),
                'conversion_rate': round(conversion_rate, 2),
                'cpa': round(cpa, 2),
                'cpc': round(cpc, 2)
            }
        
        return performance
    
    def recommend_match_type_changes(self) -> List[Dict]:
        """Recommend match type conversions."""
        recommendations = []
        
        # Convert conversion_rate to numeric if it's a string
        df = self.df.copy()
        if df['conversion_rate'].dtype == 'object':
            df['conversion_rate'] = df['conversion_rate'].astype(str).str.replace('%', '').str.strip()
            df['conversion_rate'] = pd.to_numeric(df['conversion_rate'], errors='coerce').fillna(0)
        
        # Analyze broad match keywords
        broad_keywords = df[df['match_type'] == 'broad']
        for idx, row in broad_keywords.iterrows():
            if row['clicks'] > 5:
                if row['conversion_rate'] > 2.0:
                    # High performer - should be exact
                    recommendations.append({
                        'keyword': row['keyword'],
                        'campaign': row['campaign_name'],
                        'current_match_type': 'broad',
                        'recommended_match_type': 'exact',
                        'reason': f"Broad match converting well (CVR: {row['conversion_rate']:.2f}%) - should be exact for better control",
                        'expected_impact': 'Higher conversion rate, better CPA',
                        'confidence': 'High',
                        'action': 'Convert to Exact match'
                    })
                elif row['ctr'] < 1.0 and row['impressions'] > 100:
                    # Low performer - too broad
                    recommendations.append({
                        'keyword': row['keyword'],
                        'campaign': row['campaign_name'],
                        'current_match_type': 'broad',
                        'recommended_match_type': 'phrase',
                        'reason': f"Broad match getting low CTR ({row['ctr']:.2f}%) - refine to Phrase",
                        'expected_impact': 'Better intent matching, higher CTR',
                        'confidence': 'High',
                        'action': 'Convert to Phrase match'
                    })
        
        # Analyze phrase match keywords
        phrase_keywords = df[df['match_type'] == 'phrase']
        for idx, row in phrase_keywords.iterrows():
            if row['clicks'] > 10 and row['conversion_rate'] > 3.0:
                # High performer - should be exact
                recommendations.append({
                    'keyword': row['keyword'],
                    'campaign': row['campaign_name'],
                    'current_match_type': 'phrase',
                    'recommended_match_type': 'exact',
                    'reason': f"Phrase match converting well (CVR: {row['conversion_rate']:.2f}%) - should be exact",
                    'expected_impact': 'Better ROI, lower CPA',
                    'confidence': 'High',
                    'action': 'Convert to Exact match'
                })
        
        # Analyze exact match keywords
        exact_keywords = self.df[self.df['match_type'] == 'exact']
        for idx, row in exact_keywords.iterrows():
            if row['clicks'] > 0 and row['conversion_rate'] < 0.5 and row['ctr'] > 2.0:
                # Traffic but low conversion - landing page issue
                recommendations.append({
                    'keyword': row['keyword'],
                    'campaign': row['campaign_name'],
                    'current_match_type': 'exact',
                    'recommended_match_type': 'exact',
                    'reason': f"Exact match with good CTR ({row['ctr']:.2f}%) but low CVR - landing page issue",
                    'expected_impact': 'Improved conversion rate',
                    'confidence': 'Medium',
                    'action': 'Check landing page relevance'
                })
        
        return recommendations
    
    def get_best_match_type_keywords(self) -> List[Dict]:
        """Get best performing keywords by match type."""
        best_keywords = []
        
        for match_type in ['exact', 'phrase', 'broad']:
            match_data = self.df[self.df['match_type'] == match_type]
            
            if len(match_data) > 0:
                # Find best by conversion rate
                best_by_cvr = match_data.nlargest(1, 'conversion_rate')
                if len(best_by_cvr) > 0 and best_by_cvr.iloc[0]['conversions'] > 0:
                    row = best_by_cvr.iloc[0]
                    best_keywords.append({
                        'match_type': match_type,
                        'keyword': row['keyword'],
                        'metric': 'conversion_rate',
                        'value': round(row['conversion_rate'], 2),
                        'conversions': int(row['conversions'])
                    })
                
                # Find best by CPA
                best_by_cpa = match_data[match_data['conversions'] > 0].nsmallest(1, 'cpa')
                if len(best_by_cpa) > 0:
                    row = best_by_cpa.iloc[0]
                    best_keywords.append({
                        'match_type': match_type,
                        'keyword': row['keyword'],
                        'metric': 'cpa',
                        'value': round(row['cpa'], 2),
                        'conversions': int(row['conversions'])
                    })
        
        return best_keywords
