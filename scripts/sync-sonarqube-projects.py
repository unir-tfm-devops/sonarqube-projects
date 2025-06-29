import os
import requests
import yaml

SONAR_URL = "https://sonarcloud.io"

# Check if SONAR_TOKEN is set
if 'SONAR_TOKEN' not in os.environ:
    print("Error: SONAR_TOKEN environment variable is not set")
    print("Please set it with: export SONAR_TOKEN='your-token-here'")
    exit(1)

TOKEN = os.environ['SONAR_TOKEN']
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def project_exists(key):
    try:
        url = f"{SONAR_URL}/api/projects/search"
        params = {"projects": "unir-tfm-devops_" + key, "organization": "unir-tfm-devops"}
        
        print(f"Checking if project exists: {key}")
        resp = requests.get(url, params=params, headers=HEADERS)
        
        # Check if the request was successful
        if resp.status_code != 200:
            print(f"API request failed for {key}: {resp.status_code} {resp.text}")
            return False
            
        # Try to parse JSON response
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response for {key}: {resp.text}")
            print(f"Response status: {resp.status_code}")
            return False
            
        return any(p["key"] == "unir-tfm-devops_" + key for p in data.get("components", []))
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {key}: {e}")
        return False

def set_main_branch(key):
    """Set the main branch for a SonarQube project"""
    try:
        data = {
            "project": "unir-tfm-devops_" + key,
            "name": "main"
        }
        resp = requests.post(f"{SONAR_URL}/api/project_branches/rename", headers=HEADERS, data=data)
        
        if resp.status_code in [200, 204]:
            print(f"Set main branch to 'main' for project: {key}")
        else:
            print(f"Failed to set main branch for {key}: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed while setting main branch for {key}: {e}")


def create_project(key, visibility="public"):
    try:
        data = {
            "project": "unir-tfm-devops_" + key,
            "organization": "unir-tfm-devops",
            "name": key,
            "visibility": visibility,
            "newCodeDefinitionType": "previous_version",
            "newCodeDefinitionValue": "previous_version"
        }
        resp = requests.post(f"{SONAR_URL}/api/projects/create", headers=HEADERS, data=data)
        
        if resp.status_code == 200:
            print(f"Created project: {key}")
            # Set the main branch to 'main' after project creation
            set_main_branch(key)
        else:
            print(f"Failed to create {key}: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed while creating {key}: {e}")

def main():
    with open("sonarqube-projects.yaml", 'r') as f:
        projects = yaml.safe_load(f)['projects']

    for proj in projects:
        key = proj['key']
        visibility = proj.get('visibility', 'public')

        if not project_exists(key):
            create_project(key, visibility)
        else:
            print(f"Project already exists: {key}")

if __name__ == "__main__":
    main()
