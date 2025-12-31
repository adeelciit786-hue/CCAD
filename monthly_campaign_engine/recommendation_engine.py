"""
Recommendation Engine
Generates strategic recommendations from analysis results.
"""

import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime


class RecommendationEngine:
    """Generate strategic recommendations from analysis."""
    
    def __init__(self, 
                 metrics_df: pd.DataFrame,
                 trends: Dict | List[Dict],
                 losses: List[Dict],
                 business_context: Dict):
        """Initialize with analysis results."""
        self.df = metrics_df
        self.trends = trends
        self.losses = losses
        self.business_context = business_context
        self.total_monthly_budget = metrics_df.groupby('Month')['cost'].sum().mean()
    
    def generate_budget_recommendations(self) -> List[Dict]:
        """Generate budget allocation recommendations."""
        recommendations = []
        
        service_coverage = self.business_context.get('service_coverage', {})
        
        # Recommend budget shifts based on ROI
        for service, metrics in service_coverage.items():
            if metrics.get('status') == 'UNDERFUNDED' and metrics.get('roi', 0) > 1.5:
                recommendations.append({
                    'type': 'BUDGET_INCREASE',
                    'target': service,
                    'current_spend': metrics['total_spend'],
                    'recommended_spend': round(metrics['total_spend'] * 1.2, 2),
                    'increase_amount': round(metrics['total_spend'] * 0.2, 2),
                    'reason': f"{service} has ROI of {metrics['roi']:.2f}x with underfunded allocation",
                    'expected_impact': f"Increase revenue by ~{int(metrics['roi'] * 0.2 * metrics['total_spend'])} AED",
                    'confidence': 0.85,
                    'priority': 'HIGH'
                })
            elif metrics.get('status') == 'OVERFUNDED' and metrics.get('roi', 0) < 1.0:
                recommendations.append({
                    'type': 'BUDGET_DECREASE',
                    'target': service,
                    'current_spend': metrics['total_spend'],
                    'recommended_spend': round(metrics['total_spend'] * 0.8, 2),
                    'decrease_amount': round(metrics['total_spend'] * 0.2, 2),
                    'reason': f"{service} has negative ROI of {metrics['roi']:.2f}x",
                    'expected_impact': f"Save ~{int(metrics['total_spend'] * 0.2)} AED with minimal impact",
                    'confidence': 0.80,
                    'priority': 'MEDIUM'
                })
        
        return recommendations
    
    def generate_loss_remediation(self) -> List[Dict]:
        """Generate recommendations to address detected losses."""
        recommendations = []
        
        # Group losses by type
        loss_types = {}
        for loss in self.losses:
            issue_type = loss.get('issue_type', 'UNKNOWN')
            if issue_type not in loss_types:
                loss_types[issue_type] = []
            loss_types[issue_type].append(loss)
        
        # Generate recommendations per loss type
        for loss_type, loss_list in loss_types.items():
            if loss_type == 'SPEND_UP_CONVERSIONS_DOWN':
                for loss in loss_list:
                    recommendations.append({
                        'type': 'PAUSE_INVESTIGATE',
                        'target': loss['campaign_name'],
                        'reason': loss['description'],
                        'action': f"Pause {loss['campaign_name']} to audit targeting, keywords, and ad copy",
                        'root_cause_hypothesis': 'Audience shift, keyword mismatch, or ad fatigue',
                        'expected_impact': 'Reduce wasted spend and restore efficiency',
                        'confidence': 0.75,
                        'priority': 'HIGH'
                    })
            
            elif loss_type == 'DECLINING_EFFICIENCY':
                for loss in loss_list:
                    recommendations.append({
                        'type': 'OPTIMIZE_TARGETING',
                        'target': loss['campaign_name'],
                        'reason': f"CPA increased {loss['cpa_increase_pct']:.1f}%",
                        'action': f"Review and tighten targeting parameters, test new bid strategies",
                        'root_cause_hypothesis': 'Audience expansion dilution or competitive pressure',
                        'expected_impact': f"Restore CPA to ~{loss['initial_cpa']:.2f} AED",
                        'confidence': 0.70,
                        'priority': 'MEDIUM'
                    })
            
            elif loss_type == 'CTR_SUDDEN_DROP':
                for loss in loss_list:
                    recommendations.append({
                        'type': 'REFRESH_CREATIVES',
                        'target': loss['campaign_name'],
                        'reason': f"CTR dropped {loss['ctr_drop_pct']:.1f}%",
                        'action': f"Create new ad variations, test different headlines and copy",
                        'root_cause_hypothesis': 'Ad fatigue or seasonal relevance loss',
                        'expected_impact': f"Recover CTR toward {loss['previous_ctr']:.2f}%",
                        'confidence': 0.80,
                        'priority': 'MEDIUM'
                    })
            
            elif loss_type == 'CVR_SUDDEN_DROP':
                for loss in loss_list:
                    recommendations.append({
                        'type': 'LANDING_PAGE_AUDIT',
                        'target': loss['campaign_name'],
                        'reason': f"CVR dropped {loss['cvr_drop_pct']:.1f}%",
                        'action': f"Audit landing pages for loading issues, mobile optimization, form problems",
                        'root_cause_hypothesis': 'Landing page degradation or UX issues',
                        'expected_impact': f"Recover CVR toward {loss['previous_cvr']:.2f}%",
                        'confidence': 0.78,
                        'priority': 'HIGH'
                    })
            
            elif loss_type == 'HIGH_SPEND_LOW_ROAS':
                for loss in loss_list:
                    recommendations.append({
                        'type': 'PAUSE_OR_RESTRUCTURE',
                        'target': loss['campaign_name'],
                        'reason': f"Negative ROI: spending {loss['spend']} AED with {loss['roas']:.2f}x ROAS",
                        'action': f"Either pause campaign or restructure with tighter targeting and lower bid strategy",
                        'root_cause_hypothesis': 'Irrelevant traffic or high-intent audience missing',
                        'expected_impact': f"Stop losing {loss['spend'] * (1 - loss['roas']):.2f} AED/month",
                        'confidence': 0.85,
                        'priority': 'CRITICAL'
                    })
        
        return recommendations
    
    def generate_growth_opportunities(self) -> List[Dict]:
        """Identify campaigns to scale."""
        recommendations = []
        
        # Find high-performing campaigns
        monthly_summary = self.df.groupby('campaign_name').agg({
            'conversions': 'sum',
            'cost': 'sum',
            'cpa': 'mean',
            'roas': 'mean',
            'ctr': 'mean'
        }).reset_index()
        
        # Campaigns with strong ROAS
        strong_performers = monthly_summary[monthly_summary['roas'] > 2.0]
        
        for _, campaign in strong_performers.iterrows():
            current_spend = campaign['cost']
            monthly_avg_spend = current_spend / len(self.df[self.df['campaign_name'] == campaign['campaign_name']].drop_duplicates('Month'))
            
            recommendations.append({
                'type': 'SCALE_CAMPAIGN',
                'target': campaign['campaign_name'],
                'current_monthly_spend': round(monthly_avg_spend, 2),
                'recommended_monthly_spend': round(monthly_avg_spend * 1.3, 2),
                'increase_amount': round(monthly_avg_spend * 0.3, 2),
                'current_roas': round(campaign['roas'], 2),
                'reason': f"{campaign['campaign_name']} has strong ROAS of {campaign['roas']:.2f}x",
                'action': f"Increase daily budget by 30% and test new keywords/audiences",
                'expected_impact': f"Generate {int(campaign['conversions'] * 0.3 / len(monthly_summary))} additional monthly conversions",
                'confidence': 0.90,
                'priority': 'HIGH'
            })
        
        return recommendations
    
    def generate_strategic_initiatives(self) -> List[Dict]:
        """Generate broader strategic initiatives."""
        recommendations = []
        
        platform_align = self.business_context.get('platform_alignment', {})
        service_gaps = self.business_context.get('service_gaps', [])
        
        # Platform rebalancing
        misaligned = [p for p, m in platform_align.items() if m.get('status') == 'MISALIGNED']
        if misaligned:
            recommendations.append({
                'type': 'REBALANCE_PLATFORMS',
                'targets': misaligned,
                'reason': 'Platform budget allocation doesn\'t match strategic targets',
                'action': 'Gradually shift budget toward underrepresented platforms (5% per month)',
                'expected_impact': 'Better platform diversification and risk reduction',
                'confidence': 0.75,
                'priority': 'MEDIUM'
            })
        
        # Service expansion
        if service_gaps:
            recommendations.append({
                'type': 'EXPAND_SERVICE_COVERAGE',
                'targets': [g.get('service') for g in service_gaps],
                'reason': f"{len(service_gaps)} services are underrepresented or missing",
                'action': 'Launch new campaign clusters for unrepresented services',
                'expected_impact': 'Capture untapped demand and increase overall revenue',
                'confidence': 0.70,
                'priority': 'MEDIUM'
            })
        
        return recommendations
    
    def generate_all_recommendations(self) -> Dict:
        """Generate comprehensive recommendations."""
        return {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_recommendations': 0,
                'critical_count': 0,
                'high_priority_count': 0,
                'medium_priority_count': 0
            },
            'budget_recommendations': self.generate_budget_recommendations(),
            'loss_remediation': self.generate_loss_remediation(),
            'growth_opportunities': self.generate_growth_opportunities(),
            'strategic_initiatives': self.generate_strategic_initiatives()
        }
    
    def get_executive_summary(self) -> Dict:
        """Get executive summary of key recommendations."""
        all_recs = self.generate_all_recommendations()
        
        # Count by priority
        critical = [r for r in all_recs['loss_remediation'] if r.get('priority') == 'CRITICAL']
        high = [r for r in all_recs.get('budget_recommendations', []) + 
                    all_recs.get('loss_remediation', []) + 
                    all_recs.get('growth_opportunities', [])
                if r.get('priority') == 'HIGH']
        
        return {
            'total_issues_detected': len(self.losses),
            'critical_actions': len(critical),
            'high_priority_actions': len(high),
            'total_recommendations': (
                len(all_recs['budget_recommendations']) +
                len(all_recs['loss_remediation']) +
                len(all_recs['growth_opportunities']) +
                len(all_recs['strategic_initiatives'])
            ),
            'top_critical_actions': critical[:3],
            'estimated_monthly_impact': self._estimate_financial_impact(all_recs)
        }
    
    def _estimate_financial_impact(self, recommendations: Dict) -> Dict:
        """Estimate financial impact of recommendations."""
        estimated_savings = 0
        estimated_revenue_increase = 0
        
        for rec in recommendations.get('loss_remediation', []):
            if 'decrease_amount' in rec:
                estimated_savings += rec['decrease_amount']
        
        for rec in recommendations.get('growth_opportunities', []):
            if 'expected_impact' in rec:
                # Extract numerical value from impact string
                try:
                    impact = int(''.join(filter(str.isdigit, rec['expected_impact'].split()[1])))
                    estimated_revenue_increase += impact
                except:
                    pass
        
        return {
            'estimated_savings': round(estimated_savings, 2),
            'estimated_revenue_increase': estimated_revenue_increase,
            'net_impact': round(estimated_revenue_increase - estimated_savings, 2)
        }
