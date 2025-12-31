"""
Script to convert Google Ads keyword report to compatible format
"""

import pandas as pd
from pathlib import Path

def convert_google_ads_keywords(input_file, output_file):
    """
    Convert Google Ads keyword report to required format.
    
    The input file has:
    - 2 header rows (title, date range)
    - Column headers in row 3
    - Data starting from row 4
    """
    
    try:
        # Read the file skipping the first 2 rows (metadata)
        df = pd.read_csv(input_file, skiprows=2)
        
        print(f"Loaded {len(df)} keywords from {input_file}")
        print(f"\nOriginal columns: {df.columns.tolist()}")
        
        # Define mapping from Google Ads columns to required columns
        column_mapping = {
            'Keyword': 'keyword',
            'Match type': 'match_type',
            'Clicks': 'clicks',
            'Impr.': 'impressions',
            'Avg. CPC': 'avg_cpc',
            'Cost': 'cost',
            'Conversions': 'conversions',
            'Conv. rate': 'conversion_rate',
            'CTR': 'ctr'
        }
        
        # Create required columns
        # Extract campaign and ad group from available data
        df['campaign_name'] = 'Website Traffic'  # Default campaign name
        df['ad_group_name'] = 'Keywords'  # Default ad group name
        
        # Rename columns to match requirements
        df_converted = pd.DataFrame()
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df_converted[new_col] = df[old_col]
            else:
                # If column not found, create empty column
                df_converted[new_col] = 0
        
        # Add mandatory columns
        df_converted['campaign_name'] = df['campaign_name']
        df_converted['ad_group_name'] = df['ad_group_name']
        
        # Ensure keyword column exists
        if 'keyword' not in df_converted.columns:
            df_converted['keyword'] = df['Keyword'] if 'Keyword' in df.columns else ''
        
        # Clean up percentage signs and convert to numeric
        for col in ['conversion_rate', 'ctr']:
            if col in df_converted.columns:
                df_converted[col] = df_converted[col].astype(str).str.replace('%', '').str.strip()
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
        
        # Convert numeric columns
        numeric_cols = ['clicks', 'impressions', 'cost', 'conversions', 'avg_cpc']
        for col in numeric_cols:
            if col in df_converted.columns:
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce').fillna(0)
        
        # Remove rows with missing keywords
        df_converted = df_converted.dropna(subset=['keyword'])
        df_converted = df_converted[df_converted['keyword'].str.strip() != '']
        
        # Clean keyword values (remove extra quotes)
        df_converted['keyword'] = df_converted['keyword'].astype(str).str.replace('"""', '"').str.strip()
        
        # Select and order columns
        final_columns = ['campaign_name', 'ad_group_name', 'keyword', 'match_type', 
                        'impressions', 'clicks', 'cost', 'conversions']
        
        df_final = df_converted[final_columns].copy()
        
        # Save to new CSV
        df_final.to_csv(output_file, index=False)
        
        print(f"\nConverted {len(df_final)} keywords successfully!")
        print(f"Saved to: {output_file}")
        print(f"\nNew columns: {df_final.columns.tolist()}")
        print(f"\nFirst 3 rows:")
        print(df_final.head(3))
        
        return True
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    input_file = 'website traffic 2 keywords.csv'
    output_file = 'website_traffic_2_keywords_converted.csv'
    
    if Path(input_file).exists():
        convert_google_ads_keywords(input_file, output_file)
    else:
        print(f"Input file not found: {input_file}")
