import os
import requests
import subprocess
import threading


def get_repositories_from_github(org_name, token):

    repo_list_url = f"https://api.github.com/orgs/{org_name}/repos?per_page=100"
    headers = {"Authorization": f"token {token}"}

    all_repos = []
    while repo_list_url:
        response = requests.get(repo_list_url, headers=headers)
        repos = response.json()

        for repo in repos:
            project_name = repo["name"]
            clone_url = repo["clone_url"]
            all_repos.append((project_name, clone_url))

        link_header = response.headers.get("Link", "")
        next_page_url = None
        if link_header:
            links = link_header.split(", ")
            for link in links:
                url, rel = link.split("; ")
                if rel == 'rel="next"':
                    next_page_url = url.strip("<>")
        repo_list_url = next_page_url

    return all_repos


def clone_repository(project_name, repo_url, t_folder):
    target_path = os.path.join(t_folder, project_name)
    command = ["git", "clone", repo_url, target_path]
    subprocess.run(command)


def clone_repositories_to_local(t_folder, repo_list):
    threads = []

    for project_name, repo_url in repo_list:
        t = threading.Thread(target=clone_repository, args=(project_name, repo_url, t_folder))
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()


if __name__ == '__main__':

    t_folder = ""  # save path name
    os.makedirs(t_folder, exist_ok=True)

    username = ""  # git hub mail not nickname
    access_token = ""  # access token
    organization_name = ""  # organization_name

    repositories = get_repositories_from_github(organization_name, access_token)
    clone_repositories_to_local(t_folder, repositories)

    print("fin")
