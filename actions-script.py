import os
import sys
import argparse
import subprocess

def run_actions_importer(github_org, github_repo, github_token, gitlab_token):
    # GitHub Actions Importer
    migrate_command = f"""
    gh actions-importer migrate gitlab --target-url https://github.com/{github_org}/{github_repo} --output-dir tmp/migrate --namespace bachelor-vizrt --project unit-testing-class-2023-java --github-access-token {github_token} --gitlab-access-token {gitlab_token}
    """
    subprocess.run(migrate_command, shell=True, check=True)
    print("GitHub Actions Importer completed.")

def main(gitlab_repo, github_repo, gitlab_token, github_token, github_org):
    try:
        # Check if tokens are set
        if not github_token or not gitlab_token:
            raise ValueError("GitHub or GitLab token is missing!")

        run_actions_importer(github_org, github_repo, github_token, gitlab_token)

        print("Actions Importer completed")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate GitLab repository to GitHub.")
    parser.add_argument("--gitlab-repo", required=True, help="GitLab repository name (e.g. group/project)")
    parser.add_argument("--github-repo", required=True, help="GitHub repository name")
    parser.add_argument("--gitlab-token", required=True, help="GitLab token")
    parser.add_argument("--github-token", required=True, help="GitHub token")

    args = parser.parse_args()
    
    main(args.gitlab_repo, args.github_repo, args.gitlab_token, args.github_token)
