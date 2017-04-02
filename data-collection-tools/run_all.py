import code_contributors
import other_contributors
from utils.init import authenticator, config

g = authenticator.get_github()
config.init(g)
# config.init_2()

code_contributors.run(g=g, config=config)
other_contributors.run(g=g, config=config)
