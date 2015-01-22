import logging

from ttapi import cppclient, aenums
from pyrate.manager import Manager
from captain.lib.controlled_types import Worker, Tif

from commontests.fill_server import *
from commontests.test_fill_server_template import BaseTestFillServerRollover
from commontests.utils import register_crews

from sgx.tests.utils import (mf_config, mf_option_config, mf_multi_leg_config,
                             futures_filter, fspread_filter, option_filter, ostrategy_filter)
from sgx.tests.overrides import SGXOverrides

class FSNonRollOverFutures(BaseTestFillServerRollover):
    def create_test(self):
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        #SetSessions()
        self.run_fill_server_non_rollover_no_share_map(preds=futures_filter,
                                                       mf_cfg=mf_config,
                                                       override_list=SGXOverrides)
        self.run_fill_server_non_rollover_share_map(preds=futures_filter,
                                                    mf_cfg=mf_config,
                                                    override_list=SGXOverrides)

class FSNonRollOverSpreads(BaseTestFillServerRollover):
    def create_test(self):
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        #SetSessions()
        self.run_fill_server_non_rollover_no_share_map(preds=fspread_filter,
                                                       mf_cfg=mf_multi_leg_config,
                                                       override_list=SGXOverrides)
        self.run_fill_server_non_rollover_share_map(preds=fspread_filter,
                                                    mf_cfg=mf_multi_leg_config,
                                                    override_list=SGXOverrides)

class FSNonRollOverOptions(BaseTestFillServerRollover):
    def create_test(self):
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        #SetSessions()
        self.run_fill_server_non_rollover_no_share_map(preds=option_filter,
                                                       mf_cfg=mf_option_config,
                                                       override_list=SGXOverrides)
        self.run_fill_server_non_rollover_share_map(preds=option_filter,
                                                    mf_cfg=mf_option_config,
                                                    override_list=SGXOverrides)

###############################################################
###### Use following driver command to run these tests ########
####start python -i %TT_DEV_HOME%\gwautomation\captain\7.7\dev\captain\driver.py -m -t 172.24.10.104 -u tkyadmin -p 12345678 eurexets.tests.fill_server.test_rollover:TestRolloverDownWithAutoSODTrue eurexets.tests.fill_server.test_rollover:TestRolloverDownWithAutoSODFalse eurexets.tests.fill_server.test_rollover:TestFillRolloverDownFillRolloverDown eurexets.tests.fill_server.test_rollover:TestFillRolloverDownFlatRolloverDown eurexets.tests.fill_server.test_rollover:TestTrimFlatPositions eurexets.tests.fill_server.test_rollover:TestTrimTestNoFills eurexets.tests.fill_server.test_rollover:TestTrimTestDontTrimFills eurexets.tests.fill_server.test_rollover:TestTrimTestTrimFills eurexets.tests.fill_server.test_rollover:TestTrimFills eurexets.tests.fill_server.test_rollover:TestRolloverDownMultipleContracts eurexets.tests.fill_server.test_rollover:TestFillChangeTimeFill eurexets.tests.fill_server.test_rollover:TestLoadOldBofVerifyPositions eurexets.tests.fill_server.test_rollover:TestRolloverDownWithAutoSODTrue_ttord eurexets.tests.fill_server.test_rollover:TestRolloverDownWithAutoSODFalse_ttord eurexets.tests.fill_server.test_rollover:TestFillRolloverDownFillRolloverDown_ttord eurexets.tests.fill_server.test_rollover:TestFillRolloverDownFlatRolloverDown_ttord eurexets.tests.fill_server.test_rollover:TestTrimFlatPositions_ttord eurexets.tests.fill_server.test_rollover:TestTrimTestNoFills_ttord eurexets.tests.fill_server.test_rollover:TestTrimTestDontTrimFills_ttord eurexets.tests.fill_server.test_rollover:TestTrimTestTrimFills eurexets.tests.fill_server.test_rollover:TestTrimFills_ttord eurexets.tests.fill_server.test_rollover:TestRolloverDownMultipleContracts_ttord eurexets.tests.fill_server.test_rollover:TestFillChangeTimeFill_ttord eurexets.tests.fill_server.test_rollover:TestLoadOldBofVerifyPositions_ttord


class TestRolloverDownWithAutoSODTrue(BaseTestFillServerRollover):
    def __init__(self, scenario=rollover_down_with_auto_sod_true, mf_config=mf_config,
                 prod_types=futures_filter, timeout=200):
        super(TestRolloverDownWithAutoSODTrue, self).__init__(scenario, mf_config, prod_types,
                                                              timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestRolloverDownWithAutoSODFalse(BaseTestFillServerRollover):
    def __init__(self, scenario=rollover_down_with_auto_sod_false, mf_config=mf_multi_leg_config,
                 prod_types=fspread_filter, timeout=200):
        super(TestRolloverDownWithAutoSODFalse, self).__init__(scenario, mf_config, prod_types,
                                                              timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestFillRolloverDownFillRolloverDown(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_down_fill_rollover_down, mf_config=mf_option_config,
                 prod_types=option_filter, timeout=200):
        super(TestFillRolloverDownFillRolloverDown, self).__init__(scenario, mf_config, prod_types,
                                                                   timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestTrimFlatPositions(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_flat_positions, mf_config=mf_config,
                 prod_types=futures_filter,
                 delay_time=20, timeout=200):
        super(TestTrimFlatPositions, self).__init__(scenario, mf_config, prod_types,
                                                    delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestTrimTestNoFills(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_test_no_fills, mf_config=mf_config,
                 prod_types=fspread_filter,
                 timeout=200):
        super(TestTrimTestNoFills, self).__init__(scenario, mf_config, prod_types,
                                                  timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestTrimTestDontTrimFills(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_test_dont_trim_fills, mf_config=mf_config,
                 prod_types=option_filter,
                 delay_time=20, timeout=200):
        super(TestTrimTestDontTrimFills, self).__init__(scenario, mf_config, prod_types,
                                                        delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestTrimFills(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_fills, mf_config=mf_config,
                 prod_types=futures_filter,
                 delay_time=20, timeout=200):
        super(TestTrimFills, self).__init__(scenario, mf_config, prod_types,
                                            delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestRolloverDownMultipleContracts(BaseTestFillServerRollover):
    def __init__(self, scenario=rollover_down_with_multiple_contracts,
                 preds=fspread_filter, mf_config=mf_multi_leg_config,
                 delay_time=20, timeout=200):
        super(TestRolloverDownMultipleContracts, self).__init__(scenario, mf_config, preds, preds=preds,
                                                                delay_time=delay_time,
                                                                timeout=timeout)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestFillChangeTimeFill(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_change_time_fill, mf_config=mf_option_config,
                 prod_types=option_filter, delay_time=20, timeout=200):
        super(TestFillChangeTimeFill, self).__init__(scenario, mf_config, prod_types,
                                                     delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverDownNoFillRolloverUp(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_down_no_fill_rollover_up, mf_config=mf_config,
                 prod_types=futures_filter, delay_time=20, timeout=200):
        super(TestFillRolloverDownNoFillRolloverUp, self).__init__(scenario, mf_config, prod_types,
                                                                   delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverUpFillRolloverUp(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_up_fill_rollover_up, mf_config=mf_multi_leg_config,
                 prod_types=fspread_filter, delay_time=20, timeout=200):
        super(TestFillRolloverUpFillRolloverUp, self).__init__(scenario, mf_config, prod_types,
                                                                   delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestFillRolloverUpFlatRolloverUp(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_up_flat_rollover_up, mf_config=mf_option_config,
                 prod_types=option_filter,
                 delay_time=20, timeout=200):
        super(TestFillRolloverUpFlatRolloverUp, self).__init__(scenario, mf_config, prod_types,
                                                                   delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverUpBiasNotEqualToGatewayTimeZone(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_up_bias_not_equal_to_gateway_time_zone,
                 mf_config=mf_multi_leg_config,
                 prod_types=ostrategy_filter,
                 timeout=200):
        super(TestFillRolloverUpBiasNotEqualToGatewayTimeZone, self).__init__(scenario, mf_config,
                                                                               prod_types, timeout=200)

class TestRolloverDownWithAutoSODTrue_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=rollover_down_with_auto_sod_true, mf_config=mf_multi_leg_config,
                 prod_types=ostrategy_filter, timeout=200):
        super(TestRolloverDownWithAutoSODTrue_ttord, self).__init__(scenario, mf_config, prod_types, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestRolloverDownWithAutoSODFalse_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=rollover_down_with_auto_sod_false, mf_config=mf_option_config,
                 prod_types=option_filter, timeout=200):
        super(TestRolloverDownWithAutoSODFalse_ttord, self).__init__(scenario, mf_config, prod_types,
                                                              timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestFillRolloverDownFillRolloverDown_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_down_fill_rollover_down, mf_config=mf_multi_leg_config,
                 prod_types=fspread_filter, timeout=200):
        super(TestFillRolloverDownFillRolloverDown_ttord, self).__init__(scenario, mf_config,
                                                                         prod_types,
                                                                         timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverDownFlatRolloverDown_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_down_flat_rollover_down, mf_config=mf_config,
                 prod_types=futures_filter,
                 delay_time=20, timeout=200):
        super(TestFillRolloverDownFlatRolloverDown_ttord, self).__init__(scenario, mf_config,
                                                                         prod_types,
                                                                         delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestTrimFlatPositions_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_flat_positions, mf_config=mf_multi_leg_config,
                 prod_types=ostrategy_filter,
                 delay_time=20, timeout=200):
        super(TestTrimFlatPositions_ttord, self).__init__(scenario, mf_config, prod_types,
                                                          delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestTrimTestNoFills_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_test_no_fills, mf_config=mf_option_config,
                 prod_types=option_filter,
                 timeout=200):
        super(TestTrimTestNoFills_ttord, self).__init__(scenario, mf_config, prod_types,
                                                        
                                                        timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestTrimTestDontTrimFills_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_test_dont_trim_fills, mf_config=mf_multi_leg_config,
                 prod_types=fspread_filter,
                 delay_time=20, timeout=200):
        super(TestTrimTestDontTrimFills_ttord, self).__init__(scenario, mf_config, prod_types,
                                                              delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestTrimTestTrimFills_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_test_trim_fills, mf_config=mf_config,
                 prod_types=futures_filter,
                 delay_time=20, timeout=200):
        super(TestTrimTestTrimFills_ttord, self).__init__(scenario, mf_config, prod_types,
                                                          delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
class TestTrimFills_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=trim_fills, mf_config=mf_multi_leg_config, prod_types=ostrategy_filter,
                 delay_time=20, timeout=200):
        super(TestTrimFills_ttord, self).__init__(scenario, mf_config, prod_types,
                                                  delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestRolloverDownMultipleContracts_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=rollover_down_with_multiple_contracts,
                 preds=option_filter, mf_config=mf_option_config,
                 delay_time=20, timeout=200):
        super(TestRolloverDownMultipleContracts_ttord, self).__init__(scenario, mf_config, preds,
                                                                      preds=preds,
                                                                      delay_time=delay_time,
                                                                      timeout=timeout)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestFillChangeTimeFill_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_change_time_fill, mf_config=mf_multi_leg_config,
                 prod_types=fspread_filter,
                 delay_time=20, timeout=200):
        super(TestFillChangeTimeFill_ttord, self).__init__(scenario, mf_config, prod_types,
                                                           delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverDownNoFillRolloverUp_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_down_no_fill_rollover_up, mf_config=mf_config,
                 prod_types=futures_filter,
                 delay_time=20, timeout=200):
        super(TestFillRolloverDownNoFillRolloverUp_ttord, self).__init__(scenario, mf_config,
                                                                         prod_types,
                                                                         delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverUpFillRolloverUp_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_up_fill_rollover_up, mf_config=mf_multi_leg_config,
                 prod_types=fspread_filter,
                 delay_time=20, timeout=200):
        super(TestFillRolloverUpFillRolloverUp_ttord, self).__init__(scenario, mf_config, prod_types,
                                                                     delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

        self.tif=Tif.GTC
        self.side=aenums.TT_SELL

class TestFillRolloverUpFlatRolloverUp_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_up_flat_rollover_up, mf_config=mf_option_config,
                 prod_types=option_filter,
                 delay_time=20, timeout=200):
        super(TestFillRolloverUpFlatRolloverUp_ttord, self).__init__(scenario, mf_config, prod_types,
                                                                     delay_time=20, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))

class TestFillRolloverUpBiasNotEqualToGatewayTimeZone_ttord(BaseTestFillServerRollover):
    def __init__(self, scenario=fill_rollover_up_bias_not_equal_to_gateway_time_zone, mf_config=mf_multi_leg_config,
                 prod_types=ostrategy_filter,
                 timeout=200):
        super(TestFillRolloverUpBiasNotEqualToGatewayTimeZone_ttord, self).__init__(scenario,
                                                                                    mf_config,
                                                                                    prod_types, timeout=200)
        register_crews(Worker.DIRECT,
                       WorkerRelationships(direct_no_shares=[Worker.NO_SHARE],
                                           direct_shares=[Worker.NO_SHARE,Worker.SHARE]))
