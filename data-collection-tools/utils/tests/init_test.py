from utils.init import authenticator
from utils.init import config

g = authenticator.get_github()
config.init(g)
