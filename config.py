"""
Configuration and Constants Module
Define thresholds, settings, and constants for the bot.
"""

# ============================================================================
# BUSINESS CONFIGURATION
# ============================================================================

BUSINESS_NAME = "Champion Cleaners UAE"
CURRENCY = "AED"
MONTHLY_BUDGET = 25000  # AED

# Campaign types
CAMPAIGN_TYPES = {
    'Search': 'Search',
    'PMax': 'Performance Max',
    'Android App': 'Android App Install',
    'iOS App': 'iOS App Install'
}

# Platform types
PLATFORMS = {
    'Search': 'Search Network',
    'Display': 'Display Network',
    'App': 'App Campaigns'
}

# Device OS types
DEVICE_OS_TYPES = {
    'iOS': 'Apple iOS',
    'Android': 'Google Android',
    'Web': 'Desktop/Mobile Web'
}

# ============================================================================
# PERFORMANCE THRESHOLDS
# ============================================================================

# CPA (Cost Per Acquisition) thresholds
CPA_THRESHOLDS = {
    'high': 500,      # AED - Flag as high CPA
    'warning': 300,   # AED - Warning level
}

# CTR (Click-Through Rate) thresholds
CTR_THRESHOLDS = {
    'low': 1.0,       # % - Flag as low CTR
    'warning': 1.5,   # % - Warning level
}

# Conversion Rate thresholds
CONVERSION_RATE_THRESHOLDS = {
    'low': 1.0,       # % - Flag as low conversion rate
    'warning': 2.0,   # % - Warning level
}

# ROAS (Return on Ad Spend) thresholds
ROAS_THRESHOLDS = {
    'low': 1.5,       # x - Flag as low ROAS
    'warning': 2.0,   # x - Warning level
}

# Budget thresholds
BUDGET_THRESHOLDS = {
    'high_spend': 5000,       # AED - High spend warning
    'low_return': 10,         # conversions - Low return threshold
    'low_volume': 100,        # impressions - Low volume warning
}

# ============================================================================
# EFFICIENCY SCORING
# ============================================================================

# Weights for efficiency scoring (used in budget allocation)
EFFICIENCY_WEIGHTS = {
    'roas': 0.6,              # 60% weight for ROAS
    'conversion_rate': 0.4,   # 40% weight for conversion rate
}

# ============================================================================
# CONFIDENCE LEVELS
# ============================================================================

CONFIDENCE_LEVELS = {
    'High': 'Strong data support, clear recommendation',
    'Medium': 'Moderate data support, investigate further',
    'Low': 'Limited data, inconclusive pattern'
}

# ============================================================================
# ISSUE SEVERITY MAPPING
# ============================================================================

ISSUE_SEVERITY = {
    'HIGH_CPA': 'Medium',
    'LOW_CTR': 'Medium',
    'LOW_CONVERSION_RATE': 'High',
    'LOW_ROAS': 'Medium',
    'HIGH_SPEND_LOW_RETURN': 'High'
}

# ============================================================================
# BUDGET ALLOCATION
# ============================================================================

# Minimum budget allocation percentage per campaign (prevents over-cutting)
MIN_BUDGET_ALLOCATION = 0.05  # 5%

# Maximum budget allocation percentage per campaign (prevents over-concentration)
MAX_BUDGET_ALLOCATION = 0.50  # 50%

# Suggested budget adjustment increments
BUDGET_ADJUSTMENT_STEP = 5  # % (round to nearest 5%)

# ============================================================================
# RECOMMENDATION ACTIONS
# ============================================================================

RECOMMENDATIONS = {
    'HIGH_CPA': {
        'title': 'High Cost Per Acquisition',
        'primary_actions': [
            'Tighten targeting and audience segmentation',
            'Review and improve landing page',
            'Reduce form friction (fewer fields)',
            'Test different ad copy and messaging'
        ],
        'secondary_actions': [
            'Consider reallocating budget to better performers',
            'Add trust signals and social proof',
            'Review pricing strategy'
        ]
    },
    'LOW_CTR': {
        'title': 'Low Click-Through Rate',
        'primary_actions': [
            'Improve ad copy relevance',
            'Strengthen call-to-action',
            'Test different headlines and variations',
            'Ensure keywords match search intent'
        ],
        'secondary_actions': [
            'Improve ad extensions',
            'Test different ad formats',
            'Review bidding strategy'
        ]
    },
    'LOW_CONVERSION_RATE': {
        'title': 'Low Conversion Rate',
        'primary_actions': [
            'Audit landing page for UX issues',
            'Reduce booking form friction',
            'Check page load speed',
            'Add trust signals and reviews'
        ],
        'secondary_actions': [
            'Test different page layouts',
            'Improve call-to-action clarity',
            'Review conversion tracking'
        ]
    },
    'LOW_ROAS': {
        'title': 'Low Return on Ad Spend',
        'primary_actions': [
            'Verify revenue tracking setup',
            'Review service pricing',
            'Improve conversion funnel',
            'Adjust bidding strategy'
        ],
        'secondary_actions': [
            'Analyze customer lifetime value',
            'Consider retargeting campaigns',
            'Test different audience segments'
        ]
    },
    'HIGH_SPEND_LOW_RETURN': {
        'title': 'High Spend with Low Return',
        'primary_actions': [
            'Pause underperforming ad groups',
            'Conduct keyword analysis',
            'Identify low-quality traffic sources',
            'Restructure campaign'
        ],
        'secondary_actions': [
            'Consider retargeting approach',
            'Review audience selection',
            'Test different messaging'
        ]
    }
}

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Console output formatting
OUTPUT_FORMATTING = {
    'section_width': 80,
    'indent': 2,
    'metric_decimal_places': 2,
    'currency_symbol': 'AED',
}

# JSON export settings
JSON_SETTINGS = {
    'indent': 2,
    'sort_keys': False,
    'default_filename': 'recommendations.json'
}

# ============================================================================
# DATA VALIDATION SETTINGS
# ============================================================================

VALIDATION_RULES = {
    'min_impressions': 100,     # Minimum impressions for valid campaign
    'max_missing_values': 0.1,  # Max % of missing values allowed
    'date_format': '%Y-%m-%d',  # Expected date format
}

# ============================================================================
# REPORTING SETTINGS
# ============================================================================

REPORTING = {
    'include_platform_analysis': True,
    'include_device_analysis': True,
    'include_budget_recommendations': True,
    'min_recommendations': 1,
    'max_recommendations': 10,
}

# ============================================================================
# CUSTOM THRESHOLDS BY CAMPAIGN TYPE
# ============================================================================

CAMPAIGN_TYPE_THRESHOLDS = {
    'Search': {
        'expected_ctr': 3.0,
        'expected_conversion_rate': 3.0,
        'expected_cpa': 100,
    },
    'PMax': {
        'expected_ctr': 2.0,
        'expected_conversion_rate': 2.0,
        'expected_cpa': 200,
    },
    'Android App': {
        'expected_ctr': 4.0,
        'expected_conversion_rate': 3.0,
        'expected_cpa': 150,
    },
    'iOS App': {
        'expected_ctr': 5.0,
        'expected_conversion_rate': 5.0,
        'expected_cpa': 100,
    }
}

# ============================================================================
# API & INTEGRATION SETTINGS (Future Use)
# ============================================================================

# Google Ads API
GOOGLE_ADS_CONFIG = {
    'enabled': False,  # Set to True when API integration is ready
    'version': 'v17',
    'refresh_interval_hours': 24,
}

# Streamlit Dashboard
STREAMLIT_CONFIG = {
    'enabled': False,  # Set to True when dashboard is ready
    'port': 8501,
    'theme': 'light',
}

# Webhook/Alert Settings
ALERTS_CONFIG = {
    'enabled': False,
    'slack_webhook': None,
    'email_recipients': [],
    'alert_on_high_severity': True,
}
