"""
Business Context
Maps campaigns to Champion Cleaners services and analyzes service-spend alignment.
"""

import pandas as pd
from typing import Dict, List


class BusinessContextAnalyzer:
    """Analyze campaigns in context of Champion Cleaners business."""
    
    # Champion Cleaners main services
    SERVICE_KEYWORDS = {
        'home_cleaning': ['home', 'house', 'residential', 'villa', 'apartment', 'domestic'],
        'office_cleaning': ['office', 'commercial', 'corporate', 'workplace', 'business'],
        'carpet_cleaning': ['carpet', 'rug', 'upholstery', 'sofa'],
        'deep_cleaning': ['deep', 'sanitize', 'disinfect', 'thorough', 'post-construction'],
        'window_cleaning': ['window', 'glass', 'facade', 'blind', 'exterior'],
        'moving_cleaning': ['moving', 'post-move', 'relocation', 'end-of-lease', 'move-out']
    }
    
    # Campaign type mapping to services
    CAMPAIGN_SERVICE_MAPPING = {
        'Search': ['home_cleaning', 'office_cleaning', 'carpet_cleaning'],
        'Performance Max': ['home_cleaning', 'office_cleaning'],
        'Android App': ['home_cleaning', 'office_cleaning'],
        'iOS App': ['home_cleaning', 'office_cleaning']
    }
    
    PLATFORM_BUDGET_TARGET = {
        'Search': 0.40,  # 40% of budget
        'Performance Max': 0.30,  # 30% of budget
        'Android App': 0.15,  # 15% of budget
        'iOS App': 0.15  # 15% of budget
    }
    
    SERVICE_REVENUE_IMPORTANCE = {
        'home_cleaning': 0.35,
        'office_cleaning': 0.25,
        'carpet_cleaning': 0.15,
        'deep_cleaning': 0.12,
        'window_cleaning': 0.08,
        'moving_cleaning': 0.05
    }
    
    def __init__(self, monthly_data: pd.DataFrame):
        """Initialize with monthly campaign data."""
        self.df = monthly_data.copy()
    
    def _map_campaign_to_service(self, campaign_name: str) -> List[str]:
        """Map a campaign name to likely services."""
        campaign_lower = campaign_name.lower()
        matched_services = []
        
        for service, keywords in self.SERVICE_KEYWORDS.items():
            if any(kw in campaign_lower for kw in keywords):
                matched_services.append(service)
        
        return matched_services if matched_services else ['general']
    
    def get_service_coverage_analysis(self) -> dict[str, dict[str, float | int]]:
        """Analyze which services get budget and which don't."""
        service_budget = {svc: 0 for svc in self.SERVICE_KEYWORDS.keys()}
        service_budget['other'] = 0
        
        service_conversions = {svc: 0 for svc in self.SERVICE_KEYWORDS.keys()}
        service_conversions['other'] = 0
        
        service_revenue = {svc: 0 for svc in self.SERVICE_KEYWORDS.keys()}
        service_revenue['other'] = 0
        
        campaign_mapping = {}
        
        for _, row in self.df.iterrows():
            campaign_name = row['campaign_name']
            
            if campaign_name not in campaign_mapping:
                campaign_mapping[campaign_name] = self._map_campaign_to_service(campaign_name)
            
            services = campaign_mapping[campaign_name]
            
            if not services or services == ['general']:
                service_budget['other'] += row['cost']
                service_conversions['other'] += row['conversions']
                service_revenue['other'] += row['conv_value']
            else:
                # Distribute spend across mapped services
                spend_per_service = row['cost'] / len(services)
                conv_per_service = row['conversions'] / len(services)
                rev_per_service = row['conv_value'] / len(services)
                
                for svc in services:
                    service_budget[svc] += spend_per_service
                    service_conversions[svc] += conv_per_service
                    service_revenue[svc] += rev_per_service
        
        # Calculate metrics per service
        total_budget = self.df['cost'].sum()
        analysis = {}
        
        for service in self.SERVICE_KEYWORDS.keys():
            budget = service_budget[service]
            conversions = service_conversions[service]
            revenue = service_revenue[service]
            expected_importance = self.SERVICE_REVENUE_IMPORTANCE.get(service, 0.05)
            actual_share = budget / total_budget if total_budget > 0 else 0
            
            analysis[service] = {
                'total_spend': round(budget, 2),
                'spend_pct': round(actual_share * 100, 2),
                'expected_importance_pct': round(expected_importance * 100, 2),
                'conversions': int(conversions),
                'revenue': round(revenue, 2),
                'roi': round(revenue / budget, 2) if budget > 0 else 0,
                'alignment': self._calculate_alignment(actual_share, expected_importance),
                'status': self._service_status(actual_share, expected_importance)
            }
        
        return analysis
    
    def _calculate_alignment(self, actual: float, expected: float) -> float:
        """Calculate alignment score (0-1) between actual and expected spend."""
        if expected == 0:
            return 0 if actual > 0 else 1
        
        ratio = actual / expected
        # Score based on how close to expected (1.0 is perfect)
        if 0.8 <= ratio <= 1.2:
            return 1.0
        elif 0.5 <= ratio <= 1.5:
            return 0.8
        elif 0.3 <= ratio <= 2.0:
            return 0.5
        else:
            return 0.2
    
    def _service_status(self, actual: float, expected: float) -> str:
        """Determine service status."""
        if actual == 0:
            return 'UNREPRESENTED'
        
        ratio = actual / expected if expected > 0 else 2
        
        if 0.8 <= ratio <= 1.2:
            return 'BALANCED'
        elif ratio < 0.8:
            return 'UNDERFUNDED'
        else:
            return 'OVERFUNDED'
    
    def get_platform_budget_alignment(self) -> dict[str, dict[str, float | str]]:
        """Analyze platform budget allocation."""
        total_monthly_spend = self.df['cost'].sum()
        platform_spend = self.df.groupby('campaign_type')['cost'].sum()
        
        analysis = {}
        
        for platform, target_pct in self.PLATFORM_BUDGET_TARGET.items():
            actual_spend = platform_spend.get(platform, 0)
            actual_pct = (actual_spend / total_monthly_spend * 100) if total_monthly_spend > 0 else 0
            
            analysis[platform] = {
                'actual_spend': round(actual_spend, 2),
                'actual_pct': round(actual_pct, 2),
                'target_pct': round(target_pct * 100, 2),
                'variance_pct': round(actual_pct - (target_pct * 100), 2),
                'status': 'ALIGNED' if abs(actual_pct - (target_pct * 100)) < 5 else 'MISALIGNED'
            }
        
        return analysis
    
    def get_high_performing_services(self, top_n: int = 3) -> list[dict[str, str | float | int]]:
        """Identify top-performing services by ROI."""
        service_analysis = self.get_service_coverage_analysis()
        
        ranked = []
        for service, metrics in service_analysis.items():
            total_spend: float | int = metrics['total_spend']
            if total_spend > 0:
                ranked.append({
                    'service': service,
                    'roi': metrics['roi'],
                    'conversions': metrics['conversions'],
                    'spend': metrics['total_spend']
                })
        
        ranked = sorted(ranked, key=lambda x: x['roi'], reverse=True)
        return ranked[:top_n]
    
    def get_service_gaps(self) -> list[dict[str, str | float]]:
        """Identify underrepresented services."""
        service_analysis = self.get_service_coverage_analysis()
        gaps = []
        
        for service, metrics in service_analysis.items():
            if metrics['status'] == 'UNREPRESENTED':
                gaps.append({
                    'service': service,
                    'importance': round(self.SERVICE_REVENUE_IMPORTANCE.get(service, 0) * 100, 2),
                    'recommendation': f"No campaigns found for {service}. Consider creating targeted campaigns."
                })
            elif metrics['status'] == 'UNDERFUNDED':
                expected_importance_pct: float | int = metrics['expected_importance_pct']
                total_spend: float | int = metrics['total_spend']
                gaps.append({
                    'service': service,
                    'current_spend': total_spend,
                    'expected_spend': round(expected_importance_pct / 100 * self.df['cost'].sum(), 2),
                    'gap': round(expected_importance_pct / 100 * self.df['cost'].sum() - total_spend, 2),
                    'recommendation': f"Increase budget for {service} (currently {metrics['spend_pct']}% vs expected {metrics['expected_importance_pct']}%)"
                })
        
        return gaps
    
    def get_context_summary(self) -> dict[str, dict[str, dict[str, float | int]] | dict[str, dict[str, float | str]] | list[dict[str, str | float | int]] | list[dict[str, str | float]]]:
        """Get full business context summary."""
        return {
            'service_coverage': self.get_service_coverage_analysis(),
            'platform_alignment': self.get_platform_budget_alignment(),
            'top_services': self.get_high_performing_services(),
            'service_gaps': self.get_service_gaps()
        }
