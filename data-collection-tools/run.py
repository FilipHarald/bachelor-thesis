from code_contributors import *
from utils.init import authenticator, config

g = authenticator.get_github()
config.init(g)

results = []
for repo in config.repos:
    contributors = get_repo_contributors(repo, g)
    results.append(analyze_users(repo, contributors))
plt.ylabel('users (%)')
plt.xlabel('commits (%)')
plt.legend()
plt.show()

for res in results:
    print(res)
