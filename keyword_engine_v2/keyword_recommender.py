"""
Keyword Recommender Module
Generates actionable keyword-level recommendations.
"""

import pandas as pd
from typing import List, Dict


class KeywordRecommender:
    """Generate actionable keyword recommendations with ROI projections."""
    
    def __init__(self, audit_issues: List[Dict], match_recommendations: List[Dict], 
                 lost_searches: List[Dict], opportunities: List[Dict]):
        """Initialize recommender with analysis results."""
        self.audit_issues = audit_issues
        self.match_recommendations = match_recommendations
        self.lost_searches = lost_searches
        self.opportunities = opportunities
        self.recommendations = []
        
        # Default metrics for ROI calculations
        self.avg_cpc = 2.5  # Average cost per click
        self.avg_conversion_rate = 0.05  # 5% baseline conversion rate
        self.avg_order_value = 200  # Average order value in AED
        self.monthly_searches_lost_recovery = 50  # Estimated searches recoverable per lost opportunity
    
    def generate_comprehensive_recommendations(self) -> List[Dict]:
        """Generate prioritized keyword recommendations."""
        self.recommendations = []
        
        # Process audit issues
        for issue in self.audit_issues:
            rec = self._create_recommendation_from_issue(issue)
            if rec:
                self.recommendations.append(rec)
        
        # Process match type recommendations
        for match_rec in self.match_recommendations:
            rec = self._create_recommendation_from_match(match_rec)
            if rec:
                self.recommendations.append(rec)
        
        # Process lost search opportunities
        for lost in self.lost_searches:
            rec = self._create_recommendation_from_lost(lost)
            if rec:
                self.recommendations.append(rec)
        
        # Process new opportunities
        for opp in self.opportunities:
            rec = self._create_recommendation_from_opportunity(opp)
            if rec:
                self.recommendations.append(rec)
        
        # Sort by priority and confidence
        return sorted(
            self.recommendations,
            key=lambda x: (
                {'High': 0, 'Medium': 1, 'Low': 2}.get(x.get('priority', 'Medium'), 3),
                {'High': 0, 'Medium': 1, 'Low': 2}.get(x.get('confidence', 'Medium'), 3)
            )
        )
    
    def _create_recommendation_from_issue(self, issue: Dict) -> Dict | None:
        """Create recommendation from audit issue with ROI projections."""
        if issue['issue_type'] == 'NO_CLICKS':
            # Estimate potential clicks and revenue if CTR is improved
            impressions = issue.get('value', 1000)
            potential_clicks = int(impressions * 0.03)  # 3% CTR improvement target
            potential_conversions = int(potential_clicks * self.avg_conversion_rate)
            potential_revenue = potential_conversions * self.avg_order_value
            
            return {
                'keyword': issue['keyword'],
                'campaign': issue['campaign'],
                'problem': f"High impressions ({issue['value']}) but zero clicks",
                'recommendation': 'Improve ad copy or convert to exact match to increase relevance',
                'action': 'CONVERT_TO_EXACT_OR_PAUSE',
                'priority': 'High',
                'confidence': 'High',
                'expected_impact': 'Increase CTR by 2-3%',
                'estimated_traffic_increase': potential_clicks,
                'estimated_conversions': potential_conversions,
                'estimated_monthly_revenue_impact': f"AED {potential_revenue:,.0f}",
                'estimated_roi': '250-400%'
            }
        
        elif issue['issue_type'] == 'NO_CONVERSIONS':
            clicks = issue.get('value', 50)
            potential_conversions = int(clicks * 0.03)  # 3% baseline conversion
            potential_revenue = potential_conversions * self.avg_order_value
            cost_reduction = clicks * self.avg_cpc * 0.5  # 50% cost reduction if optimized
            
            return {
                'keyword': issue['keyword'],
                'campaign': issue['campaign'],
                'problem': f"Getting {issue['value']} clicks but zero conversions",
                'recommendation': 'Review landing page relevance or add negative keywords',
                'action': 'REVIEW_LANDING_PAGE',
                'priority': 'High',
                'confidence': 'Medium',
                'expected_impact': 'Improve conversion rate',
                'estimated_traffic_increase': clicks,
                'estimated_conversions': potential_conversions,
                'estimated_monthly_revenue_impact': f"AED {potential_revenue:,.0f}",
                'estimated_cost_savings': f"AED {cost_reduction:,.0f}",
                'estimated_roi': '150-300%'
            }
        
        elif issue['issue_type'] == 'HIGH_CPA':
            current_cpa = issue.get('value', 50)
            clicks = 100  # Baseline estimate
            target_cpa = current_cpa * 0.5
            cost_savings = clicks * (current_cpa - target_cpa)
            
            return {
                'keyword': issue['keyword'],
                'campaign': issue['campaign'],
                'problem': f"High cost per acquisition: AED {issue['value']:.2f}",
                'recommendation': 'Tighten targeting or improve landing page relevance',
                'action': 'REDUCE_BID_OR_PAUSE',
                'priority': 'Medium',
                'confidence': 'High',
                'expected_impact': 'Lower CPA by 20-30%',
                'estimated_monthly_cost_savings': f"AED {cost_savings:,.0f}",
                'estimated_roi': '20-30%',
                'sales_impact_note': 'Improves profitability per conversion'
            }
        
        elif issue['issue_type'] == 'LOW_CTR':
            impressions = issue.get('value', 1000)
            current_ctr = 0.005  # 0.5% estimated current
            improved_ctr = 0.015  # 1.5% target
            additional_clicks = int(impressions * (improved_ctr - current_ctr))
            potential_conversions = int(additional_clicks * self.avg_conversion_rate)
            potential_revenue = potential_conversions * self.avg_order_value
            
            return {
                'keyword': issue['keyword'],
                'campaign': issue['campaign'],
                'problem': f"Low click-through rate: {issue['value']:.2f}%",
                'recommendation': 'Improve ad copy to match keyword intent',
                'action': 'IMPROVE_AD_COPY',
                'priority': 'Medium',
                'confidence': 'High',
                'expected_impact': 'Increase CTR by 1-2%',
                'estimated_additional_clicks': additional_clicks,
                'estimated_additional_conversions': potential_conversions,
                'estimated_monthly_revenue_increase': f"AED {potential_revenue:,.0f}",
                'estimated_roi': '100-200%'
            }
        
        return None
    
    def _create_recommendation_from_match(self, match_rec: Dict) -> Dict | None:
        """Create recommendation from match type analysis with ROI projections."""
        # Estimate CPA improvement and cost savings
        estimated_cpa_reduction = 0.20  # 20% CPA reduction with better match type
        monthly_clicks = 100  # Baseline estimate
        current_cpc = self.avg_cpc
        target_cpc = current_cpc * (1 - estimated_cpa_reduction)
        monthly_cost_savings = monthly_clicks * (current_cpc - target_cpc)
        
        # Estimate conversion improvement (better match types = better conversion)
        conversion_improvement = 0.25  # 25% improvement in conversion rate
        estimated_conversions = int(monthly_clicks * self.avg_conversion_rate * (1 + conversion_improvement))
        estimated_new_revenue = estimated_conversions * self.avg_order_value
        
        return {
            'keyword': match_rec['keyword'],
            'campaign': match_rec['campaign'],
            'problem': f"{match_rec['current_match_type'].upper()} match not optimal",
            'recommendation': match_rec['reason'],
            'action': f"CONVERT_{match_rec['current_match_type'].upper()}_TO_{match_rec['recommended_match_type'].upper()}",
            'priority': 'High',
            'confidence': match_rec['confidence'],
            'expected_impact': match_rec['expected_impact'],
            'estimated_monthly_cost_savings': f"AED {monthly_cost_savings:,.0f}",
            'estimated_conversions_improvement': f"+{estimated_conversions} monthly",
            'estimated_monthly_revenue_impact': f"AED {estimated_new_revenue:,.0f}",
            'estimated_roi': '150-250%',
            'sales_impact': f"Higher conversion rate, better ROI per click"
        }
    
    def _create_recommendation_from_lost(self, lost: Dict) -> Dict | None:
        """Create recommendation from lost search detection with revenue impact."""
        searches_lost = lost.get('potential_searches_lost', 50)
        expected_clicks = int(searches_lost * 0.2)  # 20% click-through expectation
        expected_conversions = int(expected_clicks * self.avg_conversion_rate)
        expected_revenue = expected_conversions * self.avg_order_value
        
        return {
            'keyword': lost['keyword'],
            'campaign': lost['campaign'],
            'problem': lost['description'],
            'recommendation': lost['recommendation'],
            'action': 'FIX_COVERAGE_GAP',
            'priority': 'High',
            'confidence': 'High',
            'expected_impact': f"Recover {lost['potential_searches_lost']} searches",
            'estimated_monthly_searches': searches_lost,
            'estimated_clicks': expected_clicks,
            'estimated_conversions': expected_conversions,
            'estimated_monthly_revenue_recovery': f"AED {expected_revenue:,.0f}",
            'estimated_roi': '300-500%',
            'sales_opportunity': f"Unlock {searches_lost} high-intent searches/month"
        }
    
    def _create_recommendation_from_opportunity(self, opp: Dict) -> Dict | None:
        """Create recommendation from opportunity with growth projections."""
        if 'suggested_keyword' in opp:
            monthly_searches = opp.get('monthly_searches', 100)
            expected_clicks = int(monthly_searches * 0.15)  # 15% CTR for new keyword
            expected_conversions = int(expected_clicks * self.avg_conversion_rate * 0.8)  # 80% of baseline (new keyword)
            expected_revenue = expected_conversions * self.avg_order_value
            keyword_cost = expected_clicks * self.avg_cpc
            
            return {
                'keyword': opp['suggested_keyword'],
                'campaign': 'New keyword',
                'problem': 'Missed high-intent searches',
                'recommendation': f"Add '{opp['suggested_keyword']}' to capture {opp['intent_type'].lower()}",
                'action': 'ADD_NEW_KEYWORD',
                'priority': opp['priority'],
                'confidence': 'Medium',
                'expected_impact': 'Increase reach by ~50 monthly searches',
                'estimated_monthly_searches': monthly_searches,
                'estimated_monthly_clicks': expected_clicks,
                'estimated_monthly_conversions': expected_conversions,
                'estimated_monthly_cost': f"AED {keyword_cost:,.0f}",
                'estimated_monthly_revenue': f"AED {expected_revenue:,.0f}",
                'estimated_roi': '80-120%',
                'growth_opportunity': f"Expand reach to {monthly_searches} monthly high-intent searches"
            }
        return None
    
    def get_top_recommendations(self, limit: int = 10) -> List[Dict]:
        """Get top recommendations by priority and confidence."""
        return self.recommendations[:limit]
    
    def get_recommendations_by_action(self, action: str) -> List[Dict]:
        """Filter recommendations by action type."""
        return [r for r in self.recommendations if r.get('action') == action]
    
    def export_recommendations_json(self) -> Dict:
        """Export recommendations as JSON structure."""
        return {
            'summary': {
                'total_recommendations': len(self.recommendations),
                'high_priority': len([r for r in self.recommendations if r.get('priority') == 'High']),
                'medium_priority': len([r for r in self.recommendations if r.get('priority') == 'Medium']),
                'high_confidence': len([r for r in self.recommendations if r.get('confidence') == 'High'])
            },
            'recommendations': self.recommendations
        }
