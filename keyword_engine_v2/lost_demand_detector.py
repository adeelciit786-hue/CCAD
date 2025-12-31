"""
Lost Demand Detector Module
Detects lost searches and demand gaps in keyword coverage.
"""

import pandas as pd
from typing import List, Dict


class LostDemandDetector:
    """Detect lost searches and demand gaps."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize detector with keyword data."""
        self.df = df.copy()
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate metrics for analysis."""
        self.df['ctr'] = (self.df['clicks'] / self.df['impressions'] * 100).fillna(0)
        self.df['conversion_rate'] = (self.df['conversions'] / self.df['clicks'] * 100).fillna(0)
    
    def detect_lost_searches(self) -> List[Dict]:
        """Detect potential lost search opportunities."""
        lost_searches = []
        
        # Pattern 1: High impressions but low CTR
        for idx, row in self.df.iterrows():
            if row['impressions'] > 100 and row['ctr'] < 1.0:
                lost_searches.append({
                    'keyword': row['keyword'],
                    'campaign': row['campaign_name'],
                    'match_type': row['match_type'],
                    'lost_type': 'IMPRESSION_NO_ENGAGEMENT',
                    'severity': 'High',
                    'description': f"Getting {int(row['impressions'])} impressions but CTR only {row['ctr']:.2f}% - users not clicking",
                    'potential_searches_lost': int(row['impressions'] * (1 - row['ctr'] / 100)),
                    'recommendation': 'Improve ad copy relevance or consider exact-match conversion'
                })
        
        # Pattern 2: Clicks but no conversions
        for idx, row in self.df.iterrows():
            if row['clicks'] > 10 and row['conversions'] == 0:
                lost_searches.append({
                    'keyword': row['keyword'],
                    'campaign': row['campaign_name'],
                    'match_type': row['match_type'],
                    'lost_type': 'CLICK_NO_CONVERSION',
                    'severity': 'High',
                    'description': f"Getting {int(row['clicks'])} clicks but zero conversions - funnel issue",
                    'potential_searches_lost': int(row['clicks']),
                    'recommendation': 'Check landing page relevance or adjust targeting'
                })
        
        return lost_searches
    
    def detect_match_type_gaps(self) -> List[Dict]:
        """Detect gaps in match type coverage."""
        gaps = []
        
        # Group by keyword to compare match types
        keyword_groups = self.df.groupby('keyword')
        
        for keyword, group in keyword_groups:
            match_types = group['match_type'].unique()
            
            # If broad exists but exact doesn't
            if 'broad' in match_types and 'exact' not in match_types:
                broad_data = group[group['match_type'] == 'broad'].iloc[0]
                if broad_data['clicks'] > 5:
                    gaps.append({
                        'keyword': keyword,
                        'gap_type': 'MISSING_EXACT',
                        'severity': 'High',
                        'current_match_type': 'broad',
                        'clicks_from_broad': int(broad_data['clicks']),
                        'description': f"Broad match getting {int(broad_data['clicks'])} clicks but no Exact variant",
                        'recommendation': f"Add Exact match variant of '{keyword}'"
                    })
            
            # If phrase exists but exact doesn't
            if 'phrase' in match_types and 'exact' not in match_types:
                phrase_data = group[group['match_type'] == 'phrase'].iloc[0]
                if phrase_data['clicks'] > 5:
                    gaps.append({
                        'keyword': keyword,
                        'gap_type': 'MISSING_EXACT_FROM_PHRASE',
                        'severity': 'Medium',
                        'current_match_type': 'phrase',
                        'clicks_from_phrase': int(phrase_data['clicks']),
                        'description': f"Phrase match getting {int(phrase_data['clicks'])} clicks but no Exact variant",
                        'recommendation': f"Add Exact match variant of '{keyword}' for better intent matching"
                    })
        
        return gaps
    
    def detect_search_intent_mismatch(self) -> List[Dict]:
        """Detect potential search intent mismatches."""
        mismatches = []
        
        for idx, row in self.df.iterrows():
            # High CTR but low conversion indicates intent mismatch
            if row['ctr'] > 3.0 and row['conversions'] == 0 and row['clicks'] > 5:
                mismatches.append({
                    'keyword': row['keyword'],
                    'campaign': row['campaign_name'],
                    'mismatch_type': 'HIGH_CTR_NO_CONVERSION',
                    'severity': 'High',
                    'description': f"Users clicking (CTR: {row['ctr']:.2f}%) but not converting - landing page mismatch",
                    'ctr': row['ctr'],
                    'clicks': int(row['clicks']),
                    'recommendation': 'Review landing page relevance or service match'
                })
            
            # Low CTR despite being exact match
            if row['match_type'] == 'exact' and row['ctr'] < 0.5 and row['impressions'] > 50:
                mismatches.append({
                    'keyword': row['keyword'],
                    'campaign': row['campaign_name'],
                    'mismatch_type': 'EXACT_MATCH_LOW_CTR',
                    'severity': 'Medium',
                    'description': f"Exact match keyword with {row['ctr']:.2f}% CTR - ad copy may not match intent",
                    'ctr': row['ctr'],
                    'impressions': int(row['impressions']),
                    'recommendation': 'Improve ad copy to match keyword intent'
                })
        
        return mismatches
    
    def identify_high_intent_gaps(self) -> List[Dict]:
        """Identify high-intent keywords that are underperforming."""
        high_intent_keywords = [
            'dry cleaning', 'laundry service', 'curtain cleaning', 'sofa cleaning',
            'carpet cleaning', 'express laundry', 'same-day cleaning', 'book now',
            'order online', 'premium laundry', 'cleaning service near me'
        ]
        
        gaps = []
        
        for intent_keyword in high_intent_keywords:
            matching_keywords = self.df[self.df['keyword'].str.contains(intent_keyword, case=False, na=False)]
            
            if len(matching_keywords) == 0:
                gaps.append({
                    'intent_theme': intent_keyword,
                    'gap_type': 'UNCOVERED_HIGH_INTENT',
                    'severity': 'High',
                    'description': f"No keywords targeting high-intent '{intent_keyword}' searches",
                    'recommendation': f"Add keywords targeting '{intent_keyword}' as exact match"
                })
            else:
                # Check if coverage is sufficient
                total_impressions = matching_keywords['impressions'].sum()
                if total_impressions < 50:
                    gaps.append({
                        'intent_theme': intent_keyword,
                        'gap_type': 'INSUFFICIENT_COVERAGE',
                        'severity': 'Medium',
                        'current_impressions': int(total_impressions),
                        'description': f"Low impression volume ({int(total_impressions)}) for high-intent '{intent_keyword}'",
                        'recommendation': f"Increase bid or add more variants for '{intent_keyword}'"
                    })
        
        return gaps
