import code_contributors
from utils.init import authenticator, config

g = authenticator.get_github()
config.init(g)

code_contributors.run(g=g, config=config)
