import os

def get_rule_metadata(cloud_provider: str = 'aws'):
    current_path = os.path.dirname(os.path.abspath(__file__))
    rules_metadata_path = os.path.join(current_path, f'{cloud_provider}/{cloud_provider}_rules_metadata.yaml')
    return rules_metadata_path
