"""
Example configuration file for Google Sheets POD Automation

This file demonstrates different ways to configure the POD automation tool.
Copy and modify these examples to suit your specific needs.
"""

from config.settings import Config

# Example 1: Basic configuration
# The minimum required configuration to get started
basic_config = Config({
    'google_account': 'your-email@gmail.com',
    'credentials_file': 'sheetsAPI.json'
})

# Example 2: Custom configuration with all options
# Full configuration with custom templates and settings
custom_config = Config({
    # Required settings
    'google_account': 'your-business-email@company.com',
    'credentials_file': '../credentials/google-sheets-api.json',
    
    # Optional settings with custom values
    'pod_lists_sheet': 'MyCustomPOD-Lists',
    'standard_description': 'Amazing {broad_niche} design. Perfect gift for anyone who loves {broad_niche}!',
    'default_language': 'EN',
    'default_type': 'unisex adult',
    'default_color': 'navy',
    'default_tags': 'CUSTOM_TAG, POD_DESIGN'
})

# Example 3: Environment-based configuration
# Configuration that changes based on environment (development vs production)
import os

def get_environment_config():
    """
    Returns configuration based on environment variables
    Useful for CI/CD pipelines and different deployment environments
    """
    
    # Check if we're in development mode
    is_development = os.getenv('ENVIRONMENT', 'production') == 'development'
    
    if is_development:
        return Config({
            'google_account': 'dev-test@example.com',
            'credentials_file': 'dev-credentials.json',
            'pod_lists_sheet': 'DEV-POD-lists'
        })
    else:
        return Config({
            'google_account': os.getenv('GOOGLE_ACCOUNT'),
            'credentials_file': os.getenv('GOOGLE_CREDENTIALS_FILE', 'prod-credentials.json'),
            'pod_lists_sheet': 'PROD-POD-lists'
        })

# Example 4: Niche-specific configurations
# Different configurations for different product niches

cat_lover_config = Config({
    'google_account': 'cat-products@example.com',
    'credentials_file': 'cat-sheets-api.json',
    'standard_description': 'Purrfect {broad_niche} shirt for cat lovers. Great gift for cat moms and dads!',
    'default_color': 'black',
    'default_tags': 'CAT_LOVER, PET_OWNER'
})

fitness_config = Config({
    'google_account': 'fitness-products@example.com', 
    'credentials_file': 'fitness-sheets-api.json',
    'standard_description': 'Motivational {broad_niche} gear for fitness enthusiasts. Perfect for gym sessions!',
    'default_color': 'navy',
    'default_type': 'athletic fit',
    'default_tags': 'FITNESS, MOTIVATION, GYM'
})

# Usage examples:
if __name__ == "__main__":
    # Example of how to use these configurations
    from src.main import PODAutomation
    
    # Use basic config
    automation = PODAutomation(basic_config)
    
    # Or use custom config
    # automation = PODAutomation(custom_config)
    
    # Or use environment-based config
    # automation = PODAutomation(get_environment_config())
    
    print("Configuration examples loaded successfully!")
    print(f"Google account: {automation.config.google_account}")
    print(f"Credentials file: {automation.config.credentials_file}")
