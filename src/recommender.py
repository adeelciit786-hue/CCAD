"""
Recommendation Engine Module
Generates intelligent, data-driven recommendations based on performance analysis.
"""

from typing import Dict, List, Any
import json


class RecommendationEngine:
    """Generate actionable recommendations based on campaign performance."""
    
    def __init__(self, campaign_metrics: Dict[str, Any], issues: List[Dict[str, Any]], comparisons: Dict[str, Any]):
        """
        Initialize recommendation engine.
        
        Args:
            campaign_metrics: Dictionary of campaign metrics from analyzer
            issues: List of detected issues from analyzer
            comparisons: Comparison data from analyzer
        """
        self.campaign_metrics = campaign_metrics
        self.issues = issues
        self.comparisons = comparisons
        self.recommendations: List[Dict[str, Any]] = []
    
    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate comprehensive recommendations for all campaigns.
        
        Returns:
            List of recommendation objects
        """
        self.recommendations = []
        
        for campaign_name, metrics in self.campaign_metrics.items():
            recommendation = self._generate_for_campaign(campaign_name, metrics)
            if recommendation:
                self.recommendations.append(recommendation)
        
        return self.recommendations
    
    def _generate_for_campaign(self, campaign_name: str, metrics: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        Generate recommendation for a single campaign.
        
        Args:
            campaign_name: Name of the campaign
            metrics: Campaign metrics
            
        Returns:
            Recommendation dictionary
        """
        issues_for_campaign = [i for i in self.issues if i['campaign'] == campaign_name]
        
        # Determine primary issue
        primary_issue = None
        confidence = "Medium"
        
        if not issues_for_campaign:
            # Good performer
            return self._recommend_for_good_performer(campaign_name, metrics)
        
        primary_issue = issues_for_campaign[0]
        issue_type = primary_issue['issue_type']
        
        if issue_type == 'HIGH_CPA':
            return self._recommend_for_high_cpa(campaign_name, metrics, primary_issue)
        
        elif issue_type == 'LOW_CTR':
            return self._recommend_for_low_ctr(campaign_name, metrics, primary_issue)
        
        elif issue_type == 'LOW_CONVERSION_RATE':
            return self._recommend_for_low_conversion_rate(campaign_name, metrics, primary_issue)
        
        elif issue_type == 'LOW_ROAS':
            return self._recommend_for_low_roas(campaign_name, metrics, primary_issue)
        
        elif issue_type == 'HIGH_SPEND_LOW_RETURN':
            return self._recommend_for_high_spend_low_return(campaign_name, metrics, primary_issue)
        
        return None
    
    def _recommend_for_high_cpa(self, campaign_name: str, metrics: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend actions for high CPA campaigns."""
        
        cpa = metrics['cpa']
        conversion_rate = metrics['conversion_rate']
        ctr = metrics['ctr']
        
        recommendations = []
        
        if conversion_rate < 2:
            recommendations.append("Tighten targeting and audience segmentation to improve conversion rate")
        
        if ctr < 1:
            recommendations.append("Refresh ad copy and creative assets - CTR indicates poor ad relevance")
        
        if metrics['cost'] > 5000:
            recommendations.append("Consider reallocating 20-30% of budget to better-performing campaigns")
        
        if not recommendations:
            recommendations.append("Review landing page experience and improve conversion funnel")
        
        return {
            'campaign_name': campaign_name,
            'campaign_type': metrics['campaign_type'],
            'issue_detected': f"High Cost Per Acquisition: AED {cpa}",
            'recommendation': " | ".join(recommendations),
            'confidence_level': 'High',
            'metrics_snapshot': {
                'cpa': cpa,
                'conversion_rate': conversion_rate,
                'ctr': ctr,
                'cost': metrics['cost']
            }
        }
    
    def _recommend_for_low_ctr(self, campaign_name: str, metrics: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend actions for low CTR campaigns."""
        
        return {
            'campaign_name': campaign_name,
            'campaign_type': metrics['campaign_type'],
            'issue_detected': f"Low Click-Through Rate: {metrics['ctr']}%",
            'recommendation': "Improve ad copy relevance with clearer messaging, stronger CTAs, and highlight unique value propositions | Test different ad formats and headlines | Ensure keywords match search intent tightly",
            'confidence_level': 'High',
            'metrics_snapshot': {
                'ctr': metrics['ctr'],
                'impressions': metrics['impressions'],
                'clicks': metrics['clicks']
            }
        }
    
    def _recommend_for_low_conversion_rate(self, campaign_name: str, metrics: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend actions for low conversion rate campaigns."""
        
        cpa = metrics['cpa']
        ctr = metrics['ctr']
        
        recommendations = []
        
        recommendations.append("Audit landing page for UX/design issues and slow load times")
        
        if ctr < 1:
            recommendations.append("First improve CTR by optimizing ad copy - quality matters before volume")
        
        recommendations.append("Test different booking form layouts and reduce friction (fewer fields)")
        
        recommendations.append("Add trust signals: reviews, certifications, money-back guarantees")
        
        return {
            'campaign_name': campaign_name,
            'campaign_type': metrics['campaign_type'],
            'issue_detected': f"Low Conversion Rate: {metrics['conversion_rate']}%",
            'recommendation': " | ".join(recommendations),
            'confidence_level': 'High',
            'metrics_snapshot': {
                'conversion_rate': metrics['conversion_rate'],
                'ctr': ctr,
                'cpa': cpa,
                'clicks': metrics['clicks']
            }
        }
    
    def _recommend_for_low_roas(self, campaign_name: str, metrics: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend actions for low ROAS campaigns."""
        
        roas = metrics['roas']
        cpa = metrics['cpa']
        
        if roas == 0:
            action = "Verify revenue tracking is working correctly | Review conversion tracking setup"
        else:
            action = "Improve conversion rate first | Review service pricing - may be too high relative to market"
        
        return {
            'campaign_name': campaign_name,
            'campaign_type': metrics['campaign_type'],
            'issue_detected': f"Low Return on Ad Spend: {roas}" if roas > 0 else "No revenue tracked",
            'recommendation': action,
            'confidence_level': 'Medium',
            'metrics_snapshot': {
                'roas': roas,
                'cpa': cpa,
                'revenue': metrics['revenue'],
                'cost': metrics['cost']
            }
        }
    
    def _recommend_for_high_spend_low_return(self, campaign_name: str, metrics: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend actions for high spend with low return campaigns."""
        
        cost = metrics['cost']
        conversions = metrics['conversions']
        
        return {
            'campaign_name': campaign_name,
            'campaign_type': metrics['campaign_type'],
            'issue_detected': f"High Spend (AED {cost}) with Minimal Conversions ({conversions})",
            'recommendation': "Pause underperforming ad groups and shift to high-performing variants | Conduct audience and keyword analysis to identify low-quality traffic | Consider restructuring as a retargeting campaign | Re-evaluate landing page or service offering",
            'confidence_level': 'High',
            'metrics_snapshot': {
                'cost': cost,
                'conversions': conversions,
                'cpa': metrics['cpa'],
                'conversion_rate': metrics['conversion_rate']
            }
        }
    
    def _recommend_for_good_performer(self, campaign_name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend actions for well-performing campaigns."""
        
        cost = metrics['cost']
        roas = metrics['roas']
        conversion_rate = metrics['conversion_rate']
        
        action = "Scale budget by 15-25% to expand reach while maintaining quality"
        
        if cost < 2000:
            action = f"Increase budget allocation - currently underfunded at AED {cost}/month"
        elif roas > 2:
            action = "Excellent ROAS - prioritize scaling this campaign for maximum return"
        
        return {
            'campaign_name': campaign_name,
            'campaign_type': metrics['campaign_type'],
            'issue_detected': "Strong performance detected",
            'recommendation': action,
            'confidence_level': 'High',
            'metrics_snapshot': {
                'roas': roas,
                'conversion_rate': conversion_rate,
                'cpa': metrics['cpa'],
                'cost': cost
            }
        }
    
    def generate_budget_allocation_recommendation(self) -> Dict:
        """
        Generate overall budget allocation recommendation across all campaigns.
        
        Returns:
            Dictionary with budget allocation suggestions
        """
        total_cost = sum(m['cost'] for m in self.campaign_metrics.values())
        
        allocations = {}
        
        for campaign_name, metrics in self.campaign_metrics.items():
            current_pct = (metrics['cost'] / total_cost * 100) if total_cost > 0 else 0
            
            # Calculate recommended allocation based on performance
            roas = metrics['roas'] if metrics['roas'] > 0 else 0.5
            conversion_rate = metrics['conversion_rate'] if metrics['conversion_rate'] > 0 else 0.5
            efficiency_score = (roas * conversion_rate)
            
            allocations[campaign_name] = {
                'current_budget': metrics['cost'],
                'current_percentage': round(current_pct, 1),
                'efficiency_score': round(efficiency_score, 2),
                'metrics': {
                    'roas': metrics['roas'],
                    'conversion_rate': metrics['conversion_rate'],
                    'cpa': metrics['cpa']
                }
            }
        
        # Normalize efficiency scores for allocation
        total_score = sum(a['efficiency_score'] for a in allocations.values())
        
        if total_score > 0:
            for campaign in allocations:
                allocations[campaign]['recommended_percentage'] = round(
                    (allocations[campaign]['efficiency_score'] / total_score * 100), 1
                )
                allocations[campaign]['budget_adjustment'] = round(
                    allocations[campaign]['recommended_percentage'] - allocations[campaign]['current_percentage'], 1
                )
        
        return {
            'total_monthly_budget': round(total_cost, 2),
            'allocations': allocations,
            'notes': 'Allocations based on ROAS and conversion rate efficiency'
        }
    
    def _convert_to_serializable(self, obj):
        """Convert numpy/pandas types to Python native types for JSON serialization."""
        if isinstance(obj, dict):
            return {key: self._convert_to_serializable(val) for key, val in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (int, float)):
            return float(obj) if isinstance(obj, float) else int(obj)
        elif obj is None or isinstance(obj, (str, bool)):
            return obj
        else:
            return str(obj)
    
    def export_recommendations_json(self, filepath: str | None = None) -> str:
        """
        Export recommendations as JSON.
        
        Args:
            filepath: Optional file path to save JSON
            
        Returns:
            JSON string of recommendations
        """
        output = {
            'summary': {
                'total_campaigns': len(self.recommendations),
                'high_priority_issues': len([r for r in self.recommendations if r['confidence_level'] == 'High']),
                'medium_priority_issues': len([r for r in self.recommendations if r['confidence_level'] == 'Medium'])
            },
            'recommendations': self.recommendations,
            'budget_allocation': self.generate_budget_allocation_recommendation()
        }
        
        # Convert to serializable format
        output = self._convert_to_serializable(output)
        
        json_str = json.dumps(output, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
            print(f"[OK] Recommendations exported to {filepath}")
        
        return json_str
