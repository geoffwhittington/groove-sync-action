#!/usr/bin/env python3

import os
import sys
import yaml
import requests
import glob
from pathlib import Path
from typing import Dict, Any, Optional

class GrooveSync:
    def __init__(self):
        self.api_url = os.environ['GROOVE_API_URL'].rstrip('/')
        self.context_id = os.environ['USER_CONTEXT_ID']
        self.grooves_path = os.environ.get('GROOVES_PATH', '.grooves')
        self.file_pattern = os.environ.get('FILE_PATTERN', '**/*.{yml,yaml}')
        
    def load_yaml(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load and parse a YAML file."""
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"::error file={file_path}::Error parsing YAML: {e}")
            return None
        except Exception as e:
            print(f"::error file={file_path}::Error reading file: {e}")
            return None

    def sync_groove(self, groove_data: Dict[str, Any], file_path: str) -> bool:
        """Sync a single groove with the API."""
        try:
            # Extract tool name from file path or use specified one
            tool_name = groove_data.get('toolName') or Path(file_path).stem
            
            # Prepare the request data
            request_data = {
                'name': groove_data.get('name', tool_name),
                'description': groove_data.get('description', ''),
                'toolName': tool_name,
                'inputSchema': groove_data.get('inputSchema', {
                    'type': 'object',
                    'required': ['text'],
                    'properties': {
                        'text': {
                            'type': 'string',
                            'description': 'The text to expand using this groove'
                        }
                    }
                }),
                'beats': groove_data.get('beats', [])
            }
            
            # Try to update first
            put_response = requests.put(
                f"{self.api_url}/api/tools/{self.context_id}",
                json=request_data
            )
            
            # If groove doesn't exist, create it
            if put_response.status_code == 404:
                post_response = requests.post(
                    f"{self.api_url}/api/tools/{self.context_id}",
                    json=request_data
                )
                
                if post_response.status_code != 200:
                    print(f"::error file={file_path}::Error creating groove: {post_response.text}")
                    return False
                    
                print(f"::notice file={file_path}::Created new groove")
                return True
                
            elif put_response.status_code != 200:
                print(f"::error file={file_path}::Error updating groove: {put_response.text}")
                return False
                
            print(f"::notice file={file_path}::Updated existing groove")
            return True
            
        except Exception as e:
            print(f"::error file={file_path}::Error syncing groove: {str(e)}")
            return False

    def run(self) -> bool:
        """Run the groove synchronization process."""
        success = True
        
        # Expand the file pattern to handle multiple extensions
        pattern = self.file_pattern.replace('{yml,yaml}', 'yml') + ',' + self.file_pattern.replace('{yml,yaml}', 'yaml')
        yaml_files = []
        
        # Handle multiple patterns
        for p in pattern.split(','):
            yaml_files.extend(glob.glob(os.path.join(self.grooves_path, p.strip()), recursive=True))
        
        if not yaml_files:
            print("::warning::No groove YAML files found")
            return True
            
        print(f"Found {len(yaml_files)} groove files to process")
        
        for file_path in yaml_files:
            print(f"::group::Processing {file_path}")
            groove_data = self.load_yaml(file_path)
            
            if groove_data is None:
                success = False
                print("::endgroup::")
                continue
                
            if not self.sync_groove(groove_data, file_path):
                success = False
            print("::endgroup::")
                
        return success

def main():
    syncer = GrooveSync()
    if not syncer.run():
        sys.exit(1)

if __name__ == '__main__':
    main() 