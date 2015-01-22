from captain.lib.controlled_types import Worker

from commontests.test_fill_server_template import BaseTestNonRolloverFillServer
from commontests.utils import register_crews

from sgx.tests.utils import (mf_config, mf_option_config, mf_multi_leg_config,
                             futures_filter, fspread_filter, option_filter, ostrategy_filter)

__all__ = ['TestFillServerNonRolloverFutures',
           'TestFillServerNonRolloverSpreads',
           'TestFillServerNonRolloverOptions',
           'TestFillServerNonRolloverStrategies']

class TestFillServerNonRolloverFutures(BaseTestNonRolloverFillServer):
    def __init__(self):
        register_crews(Worker.DIRECT)
        super(TestFillServerNonRolloverFutures, self).__init__(mf_config, futures_filter)

        self.prod_types = futures_filter

class TestFillServerNonRolloverSpreads(BaseTestNonRolloverFillServer):
    def __init__(self):
        register_crews(Worker.DIRECT)
        super(TestFillServerNonRolloverSpreads, self).__init__(mf_multi_leg_config, fspread_filter)

        self.prod_types = fspread_filter

class TestFillServerNonRolloverOptions(BaseTestNonRolloverFillServer):
    def __init__(self):
        register_crews(Worker.DIRECT)
        super(TestFillServerNonRolloverOptions, self).__init__(mf_option_config, option_filter)

        self.prod_types = option_filter

class TestFillServerNonRolloverStrategies(BaseTestNonRolloverFillServer):
    def __init__(self):
        register_crews(Worker.DIRECT)
        super(TestFillServerNonRolloverStrategies, self).__init__(mf_multi_leg_config, ostrategy_filter)

        self.prod_types = ostrategy_filter