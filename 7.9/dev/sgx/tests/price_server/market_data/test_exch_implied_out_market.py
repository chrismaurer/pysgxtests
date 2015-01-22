from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_implied_out_market_template import BaseTestImpliedOutPrices
from commontests.utils import register_crews

from sgx.tests.utils import (mf_multi_leg_config, bounds_1_20, bounds_5_10, bounds_1_10,
                             fspread_filter, NumDepthLevels, PFX_enabled, EchoCount)

__all__ = ['TestImpliedOutPricesTwoLegged', 'TestImpliedOutPricesThreeLegged']

class TestImpliedOutPricesTwoLegged(BaseTestImpliedOutPrices):

    def __init__(self):

        super(TestImpliedOutPricesTwoLegged, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_multi_leg_config, [fspread_filter])]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'false', NumDepthLevels : '5', EchoCount : '0'}),
                                                    (1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds=bounds_1_20
        self.orders_per_price_level_bounds=bounds_5_10
        self.order_round_lot_multiplier_bounds=bounds_1_10
        self.legs_for_implied_out=[0, 1]
        self.wait_timeout = 360

class TestImpliedOutPricesThreeLegged(BaseTestImpliedOutPrices):

    def __init__(self):

        super(TestImpliedOutPricesThreeLegged, self).__init__()

        self.market_config_and_filters = [(mf_multi_leg_config, spread_prod_type_implied_three_legged)]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'false', NumDepthLevels : '5', EchoCount : '0'}),
                                                    (1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds=bounds_1_20
        self.orders_per_price_level_bounds=bounds_5_10
        self.order_round_lot_multiplier_bounds=bounds_1_10
        self.legs_for_implied_out=[(0, 1), (1, 2), (0, 2)]
        self.wait_timeout = 360
