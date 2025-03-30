import os
import sys
import argparse
from github import Github
import subprocess
import requests


def main(gitlab_repo, github_repo, gitlab_url, github_org, gitlab_token, github_token, gitlab_group_id):
    try:
        # Check if tokens are set
        if not github_token or not gitlab_token:
            raise ValueError("GitHub or GitLab token is missing!")

    #GitHub Actions Importer
    migrate_command = f"""
    gh actions-importer migrate gitlab --target-url https://github.com/{github_org}/{github_repo} --output-dir tmp/migrate --namespace bachelor-vizrt --project unit-testing-class-2023-java --github-access-token {github_token} --gitlab-access-token {gitlab_token}
    """
    subprocess.run(migrate_command, shell=True, check=True)
    print("GitHub Actins Importer completed.")

    
    except subprocess.CalledProcessError as e:
        print(f"Error during migration: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate GitLab repository to GitHub.")
    parser.add_argument("--gitlab-repo", required=True, help="GitLab repository name (e.g. group/project)")
    parser.add_argument("--github-repo", required=True, help="GitHub repository name")
    parser.add_argument("--gitlab-url", required=True, help="GitLab URL")
    parser.add_argument("--github-org", required=True, help="GitHub organization")
    parser.add_argument("--gitlab-token", required=True, help="GitLab token")
    parser.add_argument("--github-token", required=True, help="GitHub token")
    parser.add_argument("--gitlab-group-id", required=True, help="GitLab Group ID")
    args = parser.parse_args()
    
    main(args.gitlab_repo, args.github_repo, args.gitlab_url, args.github_org, args.gitlab_token, args.github_token, args.gitlab_group_id)
