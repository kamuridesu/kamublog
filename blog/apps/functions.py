def findRepos(repo_name: str, git_repo: list) -> list:
    repo_name = repo_name.lower()
    all_match = []
    for x in git_repo:
        if x['name'].lower().startswith(repo_name) or x['full_name'].lower().startswith(repo_name):
            all_match.append(x['name'])
    return all_match


if __name__ == "__main__":
    pass