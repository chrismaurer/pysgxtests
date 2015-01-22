from commontests.price_server.templates.test_exch_implied_in_market_template import BaseTestImpliedInPrices
from sgx.tests.utils import (mf_config, spread_prod_type_implied_two_legged,
                             spread_prod_type_implied_three_legged, PFX_enabled,
                             NumDepthLevels, EchoCount, bounds_1_20, bounds_5_10, bounds_1_10)

class TestImpliedInPricesTwoLegged(BaseTestImpliedInPrices):

    def __init__(self):

        super(TestImpliedInPricesTwoLegged, self).__init__()

        self.market_config_and_filters = [(mf_config, spread_prod_type_implied_two_legged)]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'false', NumDepthLevels : '5', EchoCount : '0'}),
                                                    (1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds=bounds_1_20
        self.orders_per_price_level_bounds=bounds_5_10
        self.order_round_lot_multiplier_bounds=bounds_1_10
        self.wait_timeout = 360


class TestImpliedInPricesThreeLegged(BaseTestImpliedInPrices):

    def __init__(self):

        super(TestImpliedInPricesThreeLegged, self).__init__()

        self.market_config_and_filters = [(mf_config, spread_prod_type_implied_three_legged)]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'false', NumDepthLevels : '5', EchoCount : '0'}),
                                                    (1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds=bounds_1_20
        self.orders_per_price_level_bounds=bounds_5_10
        self.order_round_lot_multiplier_bounds=bounds_1_10
        self.wait_timeout = 360
