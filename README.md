# SonarQube Projects Manager

This repository manages SonarQube projects using the SonarCloud API. It provides a centralized way to configure and synchronize SonarQube projects across your organization.

## 📋 Overview

The repository contains:
- **Configuration file**: `sonarqube-projects.yaml` - Defines project settings and visibility
- **Sync script**: `scripts/sync-sonarqube-projects.py` - Python script to create/update projects via SonarCloud API

## ✨ Features

- **Centralized Configuration**: Manage all SonarQube projects in a single YAML file
- **Automated Project Creation**: Script automatically creates projects that don't exist
- **Visibility Management**: Configure public/private project visibility
- **Main Branch Setup**: Automatically sets the main branch to 'main' for new projects
- **Organization Integration**: Works with SonarCloud organization `unir-tfm-devops`

## Project Structure

```
sonarqube-projects/
├── README.md                    # This file
├── sonarqube-projects.yaml      # Project configuration
├── scripts/
│   └── sync-sonarqube-projects.py  # Sync script
└── .github/
    └── workflows/
        └── sync-sonarqube-projects.yml  # GitHub Action workflow
```

## 🔧 Prerequisites

- Python 3.x
- SonarCloud account with API access
- SonarCloud API token

## ⚙️ Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sonarqube-projects
   ```

2. **Set up your SonarCloud API token**:
   ```bash
   export SONAR_TOKEN='your-sonarcloud-api-token'
   ```
   
   You can get your API token from:
   - SonarCloud → Account → Security → Generate Tokens

3. **Install Python dependencies**:
   ```bash
   pip install requests pyyaml
   ```

## ⚙️ Configuration

Edit `sonarqube-projects.yaml` to define your projects:

```yaml
projects:
  - key: "spring-boot-template"
    visibility: "public"

  - key: "products-search-api"
    visibility: "public"
```

### Configuration Options

- **key**: The project identifier (will be prefixed with `unir-tfm-devops_`)
- **visibility**: Project visibility (`public` or `private`)

## 🚀 Usage

### Manual Execution

Run the sync script to create/update projects:

```bash
python scripts/sync-sonarqube-projects.py
```

### Automated Execution via GitHub Actions

The repository includes a GitHub Action workflow that automatically runs the sync script whenever changes are made to the `main` branch that affect the `sonarqube-projects.yaml` file.

**When it triggers:**
- Push to `main` branch with changes to `sonarqube-projects.yaml`
- Manual workflow dispatch

**What it does:**
1. Checks out the repository
2. Installs Python dependencies
3. Runs the sync script with the configured `SONAR_TOKEN` secret

### What the script does:
1. Read the project configuration from `sonarqube-projects.yaml`
2. Check if each project exists in SonarCloud
3. Create new projects that don't exist
4. Set the main branch to 'main' for newly created projects
5. Skip projects that already exist

## 🔌 API Integration

The script uses the following SonarCloud API endpoints:
- `GET /api/projects/search` - Check if project exists
- `POST /api/projects/create` - Create new project
- `POST /api/project_branches/rename` - Set main branch

## 🤝 Contributing

1. Add new projects to `sonarqube-projects.yaml`
2. Run the sync script to create them
3. Commit both the configuration and any script improvements

## 🔧 Troubleshooting

**Error: SONAR_TOKEN environment variable is not set**
- Make sure you've exported your SonarCloud API token

**API request failed**
- Verify your API token has the necessary permissions
- Check your network connection to SonarCloud

**Failed to create project**
- Ensure the project key is unique within your organization
- Verify you have admin permissions in the SonarCloud organization
