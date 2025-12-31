"""
Google Ads Report Parser
Handles Google Ads native CSV export format
"""

import pandas as pd
from typing import Optional


class GoogleAdsReportParser:
    """Parse and normalize Google Ads keyword reports."""
    
    @staticmethod
    def parse_google_ads_report(csv_file: str) -> Optional[pd.DataFrame]:
        """
        Parse Google Ads keyword report CSV and convert to standard format.
        
        Args:
            csv_file: Path to Google Ads CSV report
            
        Returns:
            Normalized DataFrame with standard columns
        """
        try:
            # Read the CSV, skipping the title and date rows
            df = pd.read_csv(csv_file, skiprows=2)
            
            # Print original columns for debugging
            print(f"[CSV] Columns found: {list(df.columns)}")
            
            # Map Google Ads columns to our standard format
            column_mapping = {
                'Keyword': 'keyword',
                'Match type': 'match_type',
                'Clicks': 'clicks',
                'Impr.': 'impressions',
                'Cost': 'cost',
                'Conversions': 'conversions',
                'Conv. value': 'revenue',
                'Cost / conv.': 'cpa',
                'Conv. rate': 'conversion_rate',
                'CTR': 'ctr'
            }
            
            # Rename columns
            df_renamed = df.rename(columns=column_mapping)
            
            # Add missing required columns with defaults
            if 'campaign_name' not in df_renamed.columns:
                df_renamed['campaign_name'] = 'Google Ads Search'
            
            if 'ad_group_name' not in df_renamed.columns:
                df_renamed['ad_group_name'] = 'Standard'
            
            # Select required columns
            required_cols = [
                'keyword', 'match_type', 'impressions', 'clicks', 
                'cost', 'conversions', 'campaign_name', 'ad_group_name'
            ]
            
            # Check which columns we have
            available_cols = [col for col in required_cols if col in df_renamed.columns]
            df_final = df_renamed[available_cols].copy()
            
            # Data cleaning
            # Remove quotes from keyword names
            df_final['keyword'] = df_final['keyword'].str.replace('"""', '', regex=False).str.strip()
            
            # Remove quotes from match type
            if 'match_type' in df_final.columns:
                df_final['match_type'] = df_final['match_type'].str.lower().str.strip()
            
            # Convert numeric columns
            numeric_cols = ['impressions', 'clicks', 'cost', 'conversions']
            for col in numeric_cols:
                if col in df_final.columns:
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0)
            
            # Remove any rows with missing keywords
            df_final = df_final.dropna(subset=['keyword'])
            df_final = df_final[df_final['keyword'].str.len() > 0]
            
            print(f"[CSV] Successfully parsed {len(df_final)} keywords")
            print(f"[CSV] Final columns: {list(df_final.columns)}")
            
            return df_final
            
        except Exception as e:
            print(f"[CSV] Error parsing file: {e}")
            return None
