from utils.init import authenticator
from utils.init import config

g = authenticator.get_githubs()
config.init(g)
