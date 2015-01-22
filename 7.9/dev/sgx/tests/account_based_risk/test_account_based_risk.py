# captain imports
from captain.lib.controlled_types import Worker, Side
from captain import bind

# CommonTests Imports
from commontests.test_account_based_risk_template import BaseTestAccountBasedRiskOutright, BaseTestAccountBasedRiskMleg
from commontests.utils import register_crews
from commontests.account_based_risk import *

# Utils Imports
from sgx.tests.utils import mf_config, mf_multi_leg_config, futures_filter, fspread_filter
from sgx.tests.features import gateway

__all__ = ['TestRiskOutright', 'TestRiskMleg']

class TestRiskOutright(BaseTestAccountBasedRiskOutright):
   def __init__(self,mf_config=mf_config, mf_pred=[futures_filter]):
       
       super(TestRiskOutright, self).__init__(mf_config, mf_pred)
       register_crews(Worker.DIRECT)

       self.scen_list = [avoid_orders_that_cross_reject_new,
                         avoid_orders_that_cross_none,
                         allow_trading_flag_outright_product_limit,
                         allow_trading_flag_outright_contract_limit,
                         max_order_size_outright_product_limit,
                         max_order_size_outright_product_limit_rej,
                         max_order_size_outright_contract_limit,
                         max_order_size_outright_contract_limit_rej,
                         bind(max_position_outright_product_limit_rej, [1, 2, 3], [Side.BUY]),
                         bind(max_position_outright_product_limit_rej, [1], [Side.SELL]),
                         max_position_product_product_limit_rej,
                         bind(max_long_short_product_limit_rej, [1, 2, 3], [Side.BUY]),
                         bind(max_long_short_product_limit_rej, [1], [Side.SELL]),
                         bind(max_position_outright_contract_limit_rej, [1, 2, 3], [Side.BUY]),
                         bind(max_position_outright_contract_limit_rej, [1], [Side.SELL]),
                         price_reasonability_outright_product_limit,
                         price_reasonability_outright_product_limit_rej,
                         price_reasonability_outright_contract_limit,
                         price_reasonability_outright_contract_limit_rej,
                         price_reasonability_outright_apply_into_mkt_product_limit,
                         price_reasonability_outright_apply_into_mkt_product_limit_rej,
                         price_reasonability_outright_apply_into_mkt_contract_limit,
                         price_reasonability_outright_apply_into_mkt_contract_limit_rej,
                         user_account_permission_off_no_account,
                         user_account_permission_on_no_account_rej,
                         user_account_permission_off_with_account,
                         user_account_permission_on_with_account,
                         user_account_permission_on_with_account_rej,
                         user_account_permission_alter_order_os_restart_rej]

class TestRiskMleg(BaseTestAccountBasedRiskMleg):
   def __init__(self,mf_config=mf_multi_leg_config, mf_pred=[fspread_filter]):
       
       super(TestRiskMleg, self).__init__(mf_config, mf_pred)
       register_crews(Worker.DIRECT)
