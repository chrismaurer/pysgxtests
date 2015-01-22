from ttapi import aenums

from captain.lib.controlled_types import Trader, Worker
from captain.lib.strategy_definitions import Strategy

from commontests.test_uds_template import BaseTestStrategyCreation
from commontests.utils import register_crews

from sgx.tests.utils import mf_option_config, mf_multi_leg_config

class TestTailorMadeCombinations(BaseTestStrategyCreation):
    def __init__(self):
        register_crews(Worker.DIRECT)
        super(TestTailorMadeCombinations, self).__init__()
        self.valid_traders = [Trader.DIRECT,
                              Trader.PROXY_DIRECT]
        mf_option_config.depth = 0
        self.supported_intra_prod_strategies = (Strategy.NSC_TWO_LEGS,
                                                Strategy.NSC_THREE_LEGS,
                                                Strategy.NSC_FOUR_LEGS,
                                                Strategy.COVERED,
                                                Strategy.COVERED_TWO_FUT_LEGS)
        self.supported_inter_prod_strategies = (Strategy.NSC_TWO_LEGS,
                                                Strategy.NSC_THREE_LEGS,
                                                Strategy.NSC_FOUR_LEGS,
                                                Strategy.COVERED,
                                                Strategy.COVERED_TWO_FUT_LEGS)
        self.leg_mf_config = mf_option_config
        self.strat_creation_mf_config = mf_multi_leg_config
        self.post_creation_pause = 20
#        self.intra_prod_product_names = (('ED', 'EL', 'EY', 'IN', 'NK', 'SG', 'TW'))
        self.intra_prod_product_names = (('ED', 'IN', 'NK', 'SG', 'TW'))
        self.inter_prod_product_names = (('EL', 'EY',),)
        self.exclude_scenarios = ['create_inverted_strategy_exch_reject']