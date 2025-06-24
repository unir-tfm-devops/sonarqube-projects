import os
import requests
import yaml

SONAR_URL = "https://sonarcloud.io"
TOKEN = os.environ['SONAR_TOKEN']
HEADERS = {
    'Authorization': f'Basic {TOKEN}:',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def project_exists(key):
    resp = requests.get(f"{SONAR_URL}/api/projects/search", params={"projects": key}, headers=HEADERS)
    return any(p["key"] == key for p in resp.json().get("components", []))

def create_project(key, visibility="public"):
    data = {
        "project": "unir-tfm-devops_" + key,
        "organization": "unir-tfm-devops",
        "name": key,
        "visibility": visibility
    }
    resp = requests.post(f"{SONAR_URL}/api/projects/create", headers=HEADERS, data=data)
    if resp.status_code != 200:
        print(f"Failed to create {key}: {resp.status_code} {resp.text}")
    else:
        print(f"Created project: {key}")

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
