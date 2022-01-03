def findRepos(repo_name: str, git_repo: list) -> list:
    repo_name = repo_name.lower()
    all_match = []
    for x in git_repo:
        if x['name'].lower().startswith(repo_name) or x['full_name'].lower().startswith(repo_name):
            all_match.append(x['name'])
    return all_match


def checkGetParams(request, *args):
    OK = False
    for item in request.args:
        if item in [*args]:
            OK = True
        else:
            OK = False
    return OK


def checkTokenScope(token_list, token, scope):
    if token in token_list.keys():
        return scope in token_list[token]['scopes']
    return False


if __name__ == "__main__":
    pass