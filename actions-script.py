import os
import sys
import argparse
import subprocess

def check_docker_installed():
    try:
        subprocess.run(['docker', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def run_actions_importer(github_org, github_repo, github_token, gitlab_token):
    if not check_docker_installed():
        print("Error: Docker is not installed or not in PATH.")
        sys.exit(1)

    # GitHub Actions Importer
    migrate_command = f"""
    gh actions-importer migrate gitlab --target-url https://github.com/{github_org}/{github_repo} --output-dir tmp/migrate --namespace bachelor-vizrt --project unit-testing-class-2023-java --github-access-token {github_token} --gitlab-access-token {gitlab_token}
    """
    try:
        subprocess.run(migrate_command, shell=True, check=True)
        print("GitHub Actions Importer completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing gh actions-importer: {e}")
        sys.exit(1)

def main(gitlab_repo, github_repo, gitlab_token, github_token, github_org):
    try:
        # Check if tokens are set
        if not github_token or not gitlab_token:
            raise ValueError("GitHub or GitLab token is missing!")

        print(f"Starting migration from GitLab: {gitlab_repo} to GitHub: {github_org}/{github_repo}")

        run_actions_importer(github_org, github_repo, github_token, gitlab_token)

        print("Actions Importer completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate GitLab repository to GitHub.")
    parser.add_argument("--gitlab-repo", required=True, help="GitLab repository name (e.g. group/project)")
    parser.add_argument("--github-repo", required=True, help="GitHub repository name")
    parser.add_argument("--github-org", required=True, help="GitHub organization name")
    parser.add_argument("--gitlab-token", required=True, help="GitLab token")
    parser.add_argument("--github-token", required=True, help="GitHub token")

    args = parser.parse_args()

    main(args.gitlab_repo, args.github_repo, args.gitlab_token, args.github_token, args.github_org)
