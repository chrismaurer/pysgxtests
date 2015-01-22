from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_vap_template import BaseTestVap
from commontests.utils import register_crews

from sgx.tests.utils import (mf_config, mf_option_config, mf_multi_leg_config,
                             futures_filter, fspread_filter, option_filter, ostrategy_filter,
                             PFX_enabled, accumulate_ltq, EchoCount)

from sgx.tests.overrides import SGXOverrides

__all__ = ['TestVAPAllProducts', 'TestVAPOptions', 'TestVAPMultilegs']

class TestVAPFutures(BaseTestVap):

    def __init__(self):

        super(TestVAPFutures, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_config, [futures_filter])]

        self.accumulate_ltq_and_Aconfig_settings = [(False, {PFX_enabled : 'true', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'true', accumulate_ltq : '0', EchoCount : '0'}),
                                                    (False, {PFX_enabled : 'false', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'false', accumulate_ltq : '0', EchoCount : '0'})]

        self.overrides = SGXOverrides
        self.wait_timeout = 360
        self.restart_timeout = 500

class TestVAPOptions(BaseTestVap):

    def __init__(self):

        super(TestVAPOptions, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_option_config, [option_filter])]

        self.accumulate_ltq_and_Aconfig_settings = [(False, {PFX_enabled : 'true', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'true', accumulate_ltq : '0', EchoCount : '0'}),
                                                    (False, {PFX_enabled : 'false', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'false', accumulate_ltq : '0', EchoCount : '0'})]
        self.wait_timeout = 360

        self.overrides = SGXOverrides

class TestVAPMultilegs(BaseTestVap):

    def __init__(self):

        super(TestVAPMultilegs, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_multi_leg_config, [fspread_filter, ostrategy_filter])]

        self.accumulate_ltq_and_Aconfig_settings = [(False, {PFX_enabled : 'true', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'true', accumulate_ltq : '0', EchoCount : '0'}),
                                                    (False, {PFX_enabled : 'false', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'false', accumulate_ltq : '0', EchoCount : '0'})]
        self.wait_timeout = 360

        self.overrides = SGXOverrides
