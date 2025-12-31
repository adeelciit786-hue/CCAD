"""
Website Relevance Checker
Aligns keywords with actual services offered on website.
"""

import pandas as pd
from typing import Dict, List


class WebsiteRelevanceChecker:
    """Check alignment of keywords with website services."""
    
    def __init__(self):
        """Initialize with Champion Cleaners service mapping."""
        self.services = self._initialize_service_mapping()
        self.alignment_results = []
    
    def _initialize_service_mapping(self) -> Dict[str, Dict]:
        """Initialize service mapping from Champion Cleaners website."""
        return {
            'dry_cleaning': {
                'name': 'Dry Cleaning Services',
                'url': '/services/dry-cleaning',
                'keywords': ['dry cleaning', 'dry clean', 'professional dry cleaning', 'premium dry cleaning'],
                'related_keywords': ['laundry', 'garment care', 'clothing service']
            },
            'laundry': {
                'name': 'Laundry Services',
                'url': '/services/laundry',
                'keywords': ['laundry', 'laundry service', 'wash', 'ironing', 'pressing'],
                'related_keywords': ['express laundry', 'same-day laundry', 'quick laundry']
            },
            'curtain_cleaning': {
                'name': 'Curtain & Blind Cleaning',
                'url': '/services/curtains',
                'keywords': ['curtain cleaning', 'curtains', 'blind cleaning', 'window treatment cleaning'],
                'related_keywords': ['drapes', 'drapery cleaning', 'blind cleaning', 'sheer cleaning']
            },
            'sofa_cleaning': {
                'name': 'Sofa & Upholstery Cleaning',
                'url': '/services/sofa',
                'keywords': ['sofa cleaning', 'upholstery cleaning', 'furniture cleaning', 'couch cleaning'],
                'related_keywords': ['armchair cleaning', 'mattress cleaning', 'fabric cleaning']
            },
            'carpet_cleaning': {
                'name': 'Carpet & Rug Cleaning',
                'url': '/services/carpet',
                'keywords': ['carpet cleaning', 'rug cleaning', 'floor cleaning', 'carpet care'],
                'related_keywords': ['deep cleaning carpet', 'stain removal', 'steam cleaning']
            },
            'corporate_laundry': {
                'name': 'Corporate & Business Laundry',
                'url': '/services/corporate',
                'keywords': ['corporate laundry', 'business laundry', 'office laundry', 'uniform cleaning'],
                'related_keywords': ['company laundry', 'workplace cleaning', 'hotel laundry']
            }
        }
    
    def check_keyword_alignment(self, keywords_df: pd.DataFrame) -> List[Dict]:
        """Check how well keywords align with actual services."""
        alignment_results = []
        
        for _, row in keywords_df.iterrows():
            keyword = row['keyword'].lower()
            campaign = row.get('campaign', 'Unknown')
            
            aligned_service = self._find_aligned_service(keyword)
            
            if aligned_service:
                alignment = {
                    'keyword': row['keyword'],
                    'campaign': campaign,
                    'aligned_service': aligned_service['name'],
                    'alignment_strength': self._calculate_alignment_strength(keyword, aligned_service),
                    'status': 'ALIGNED',
                    'issue': None
                }
            else:
                alignment = {
                    'keyword': row['keyword'],
                    'campaign': campaign,
                    'aligned_service': None,
                    'alignment_strength': 0.0,
                    'status': 'MISALIGNED',
                    'issue': 'Keyword not clearly mapped to service offerings'
                }
            
            alignment_results.append(alignment)
        
        self.alignment_results = alignment_results
        return alignment_results
    
    def _find_aligned_service(self, keyword: str) -> Dict | None:
        """Find which service a keyword aligns with."""
        keyword_lower = keyword.lower()
        
        # Direct match in service keywords
        for service_id, service_info in self.services.items():
            for kw in service_info['keywords']:
                if kw.lower() in keyword_lower or keyword_lower in kw.lower():
                    return service_info
            
            # Check related keywords
            for related_kw in service_info['related_keywords']:
                if related_kw.lower() in keyword_lower or keyword_lower in related_kw.lower():
                    return service_info
        
        return None
    
    def _calculate_alignment_strength(self, keyword: str, service: Dict) -> float:
        """Calculate how well keyword aligns with service (0.0-1.0)."""
        keyword_lower = keyword.lower()
        
        # Exact match = 1.0
        for kw in service['keywords']:
            if kw.lower() == keyword_lower:
                return 1.0
        
        # Partial match in keywords = 0.8
        for kw in service['keywords']:
            if kw.lower() in keyword_lower or keyword_lower in kw.lower():
                return 0.8
        
        # Related keyword match = 0.6
        for related_kw in service['related_keywords']:
            if related_kw.lower() in keyword_lower or keyword_lower in related_kw.lower():
                return 0.6
        
        return 0.0
    
    def identify_misaligned_keywords(self) -> List[Dict]:
        """Identify keywords that don't align with services."""
        return [
            r for r in self.alignment_results
            if r['status'] == 'MISALIGNED'
        ]
    
    def identify_weak_alignments(self, threshold: float = 0.7) -> List[Dict]:
        """Identify keywords with weak alignment strength."""
        return [
            r for r in self.alignment_results
            if r['alignment_strength'] < threshold and r['alignment_strength'] > 0.0
        ]
    
    def get_service_coverage(self) -> Dict[str, int]:
        """Get keyword coverage per service."""
        coverage = {}
        
        for service_id, service_info in self.services.items():
            count = len([
                r for r in self.alignment_results
                if r['aligned_service'] == service_info['name']
            ])
            coverage[service_info['name']] = count
        
        # Add misaligned
        coverage['Unaligned Keywords'] = len([
            r for r in self.alignment_results
            if r['status'] == 'MISALIGNED'
        ])
        
        return coverage
    
    def identify_uncovered_services(self) -> List[Dict]:
        """Identify services with no or low keyword coverage."""
        coverage = self.get_service_coverage()
        uncovered = []
        
        for service_id, service_info in self.services.items():
            service_name = service_info['name']
            keyword_count = coverage.get(service_name, 0)
            
            if keyword_count == 0:
                uncovered.append({
                    'service': service_name,
                    'issue': 'NO_KEYWORDS',
                    'description': f"Service '{service_name}' has no keywords in portfolio",
                    'suggested_keywords': service_info['keywords'],
                    'recommended_action': f"Add {len(service_info['keywords'])} primary keywords"
                })
            elif keyword_count < 3:
                uncovered.append({
                    'service': service_name,
                    'issue': 'LOW_COVERAGE',
                    'description': f"Service '{service_name}' has only {keyword_count} keywords",
                    'suggested_keywords': service_info['related_keywords'],
                    'recommended_action': f"Add {3 - keyword_count} related keywords"
                })
        
        return uncovered
    
    def get_landing_page_recommendations(self, keywords_df: pd.DataFrame) -> List[Dict]:
        """Generate landing page recommendations based on keyword alignment."""
        recommendations = []
        
        # High-cost misaligned keywords
        if 'cost' in keywords_df.columns:
            misaligned = self.identify_misaligned_keywords()
            
            for mis_kw in misaligned:
                matching_row = keywords_df[
                    keywords_df['keyword'] == mis_kw['keyword']
                ].iloc[0]
                
                cost = matching_row.get('cost', 0)
                if cost > 100:  # Significant spend on misaligned keyword
                    recommendations.append({
                        'keyword': mis_kw['keyword'],
                        'campaign': mis_kw['campaign'],
                        'issue': 'HIGH_SPEND_ON_MISALIGNED',
                        'cost': cost,
                        'recommendation': f"Keyword '{mis_kw['keyword']}' (AED {cost:.0f} spent) doesn't clearly map to any service. Review landing page or pause keyword.",
                        'action': 'REVIEW_LANDING_PAGE'
                    })
        
        return recommendations
    
    def export_alignment_report(self) -> Dict:
        """Export alignment analysis as dictionary."""
        return {
            'total_keywords_reviewed': len(self.alignment_results),
            'aligned_keywords': len([r for r in self.alignment_results if r['status'] == 'ALIGNED']),
            'misaligned_keywords': len([r for r in self.alignment_results if r['status'] == 'MISALIGNED']),
            'service_coverage': self.get_service_coverage(),
            'uncovered_services': self.identify_uncovered_services(),
            'weak_alignments': self.identify_weak_alignments(),
            'alignment_details': self.alignment_results
        }
