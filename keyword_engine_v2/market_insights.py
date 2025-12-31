"""
Market Insights Module
Infers market trends and identifies keyword opportunities.
"""

import pandas as pd
from typing import List, Dict, Set


class MarketInsights:
    """Generate market insights and opportunity identification."""
    
    # Service themes for Champion Cleaners
    SERVICE_THEMES = {
        'laundry': ['laundry', 'dry cleaning', 'wash', 'ironing', 'garment'],
        'express': ['express', 'same-day', 'urgent', 'rush', 'quick', '24 hour'],
        'location': ['dubai', 'uae', 'near me', 'nearby', 'service'],
        'premium': ['premium', 'luxury', 'high-end', 'professional'],
        'sofa': ['sofa', 'couch', 'furniture', 'upholstery'],
        'carpet': ['carpet', 'rug', 'floor', 'cleaning'],
        'curtain': ['curtain', 'drape', 'blind', 'window'],
        'pickup': ['pickup', 'delivery', 'free delivery', 'door-to-door'],
        'corporate': ['corporate', 'business', 'office', 'company']
    }
    
    def __init__(self, df: pd.DataFrame):
        """Initialize market insights analyzer."""
        self.df = df.copy()
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate metrics."""
        self.df['ctr'] = (self.df['clicks'] / self.df['impressions'] * 100).fillna(0)
        self.df['conversion_rate'] = (self.df['conversions'] / self.df['clicks'] * 100).fillna(0)
        self.df['cpa'] = (self.df['cost'] / self.df['conversions']).fillna(float('inf'))
    
    def identify_trending_themes(self) -> List[Dict]:
        """Identify trending keyword themes."""
        trends = []
        
        for theme_name, theme_keywords in self.SERVICE_THEMES.items():
            # Find keywords matching this theme
            matching_keywords = self.df[
                self.df['keyword'].str.lower().str.contains('|'.join(theme_keywords), case=False, na=False)
            ]
            
            if len(matching_keywords) > 0:
                total_impressions = matching_keywords['impressions'].sum()
                total_clicks = matching_keywords['clicks'].sum()
                total_conversions = matching_keywords['conversions'].sum()
                
                ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
                
                # Determine trend direction (simplified)
                if total_conversions > 5:
                    trend_strength = 'strong'
                elif total_conversions > 0:
                    trend_strength = 'moderate'
                else:
                    trend_strength = 'weak'
                
                trends.append({
                    'theme': theme_name,
                    'keyword_count': len(matching_keywords),
                    'total_impressions': int(total_impressions),
                    'total_clicks': int(total_clicks),
                    'ctr': round(ctr, 2),
                    'total_conversions': int(total_conversions),
                    'conversion_rate': round(cvr, 2),
                    'trend_strength': trend_strength,
                    'opportunity_level': 'High' if total_impressions > 500 and cvr > 2 else 'Medium' if total_impressions > 100 else 'Low'
                })
        
        return sorted(trends, key=lambda x: x['total_conversions'], reverse=True)
    
    def identify_new_keyword_opportunities(self) -> List[Dict]:
        """Identify potential new keyword opportunities."""
        opportunities = []
        
        # Analyze existing themes to suggest extensions
        existing_keywords = set(self.df['keyword'].str.lower().unique())
        
        # Generate new keyword combinations
        new_combinations = [
            ('express laundry', 'High-intent same-day laundry searches'),
            ('same-day dry cleaning', 'Urgent laundry needs'),
            ('premium curtain cleaning', 'High-value service upsell'),
            ('sofa cleaning near me', 'Local furniture cleaning'),
            ('corporate laundry service', 'B2B laundry opportunities'),
            ('carpet cleaning dubai', 'Location-specific service'),
            ('laundry pickup delivery', 'Convenience-focused searches'),
            ('eco-friendly dry cleaning', 'Sustainability angle'),
            ('white shirt laundry', 'Premium garment care'),
            ('wedding dress cleaning', 'Special occasion services')
        ]
        
        for keyword, intent in new_combinations:
            if keyword.lower() not in existing_keywords:
                opportunities.append({
                    'suggested_keyword': keyword,
                    'intent_type': intent,
                    'recommended_match_type': 'exact',
                    'estimated_monthly_searches': 50,
                    'priority': 'High' if any(theme in keyword.lower() for theme in ['express', 'same-day', 'pickup', 'delivery']) else 'Medium',
                    'reason': f"Aligns with Champion Cleaners services and high-intent searches",
                    'action': f"Add '{keyword}' as exact match"
                })
        
        return opportunities
    
    def analyze_location_opportunity(self) -> List[Dict]:
        """Analyze location-specific opportunities."""
        opportunities = []
        
        # Check if location keywords exist
        location_keywords = self.df[
            self.df['keyword'].str.lower().str.contains('dubai|sharjah|abu dhabi|uae|near me', case=False, na=False)
        ]
        
        if len(location_keywords) > 0:
            total_impressions = location_keywords['impressions'].sum()
            total_conversions = location_keywords['conversions'].sum()
            
            opportunities.append({
                'location_focus': 'Current location keywords',
                'total_impressions': int(total_impressions),
                'total_conversions': int(total_conversions),
                'status': 'Active',
                'recommendation': 'Increase bids for high-performing location keywords'
            })
        else:
            opportunities.append({
                'location_focus': 'Location-specific keywords missing',
                'status': 'Gap identified',
                'recommendation': 'Add location keywords: Dubai, Sharjah, Abu Dhabi specific terms',
                'suggested_keywords': [
                    'dry cleaning dubai',
                    'laundry service sharjah',
                    'carpet cleaning abu dhabi',
                    'cleaning service near me',
                    'laundry pickup dubai'
                ]
            })
        
        return opportunities
    
    def identify_service_gaps(self) -> List[Dict]:
        """Identify services not well represented in keywords."""
        gaps = []
        
        services = ['sofa cleaning', 'carpet cleaning', 'curtain cleaning', 'corporate laundry']
        
        for service in services:
            service_keywords = self.df[
                self.df['keyword'].str.lower().str.contains(service, case=False, na=False)
            ]
            
            if len(service_keywords) == 0:
                gaps.append({
                    'service': service,
                    'gap_type': 'MISSING_SERVICE_KEYWORDS',
                    'severity': 'High',
                    'recommendation': f"Add keywords targeting '{service}'",
                    'suggested_keywords': [
                        f"{service} dubai",
                        f"best {service}",
                        f"{service} near me",
                        f"professional {service}"
                    ]
                })
            else:
                keyword_count = len(service_keywords)
                if keyword_count < 3:
                    gaps.append({
                        'service': service,
                        'gap_type': 'INSUFFICIENT_COVERAGE',
                        'severity': 'Medium',
                        'current_keywords': keyword_count,
                        'recommendation': f"Expand {service} keyword coverage",
                        'suggested_additions': f"Add {3 - keyword_count} more keyword variants"
                    })
        
        return gaps
