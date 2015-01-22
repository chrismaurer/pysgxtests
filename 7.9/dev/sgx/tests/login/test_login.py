# Pyrate Imports
from captain.lib.controlled_types import Trader, Worker

# CommonTests Imports
from commontests.test_login_template import BaseTestLogin
from commontests.utils import register_crews

class TestLogin(BaseTestLogin):
    def __init__(self):
        register_crews(Worker.DIRECT)
        super(TestLogin, self).__init__()
        self.valid_traders = [Trader.DIRECT,
                              Trader.PROXY_DIRECT]
