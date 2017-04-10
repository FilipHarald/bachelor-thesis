import code_contributors
import other_contributors
from utils.init import authenticator, config

gs = authenticator.get_githubs()
config.init_2(config.repos, gs[1])

code_contributors.run(g=gs[0], config=config)
other_contributors.run(g=gs[0], config=config)
