from ttapi import aenums
from captain import TTAPICaptainTest, OrderContext, bind
from captain.lib import *
from captain.lib.controlled_types import (OrderType, OrderRes, OrderMod, Side, 
                                          Worker, Tif, ExchangeClearingAccount)
from commontests import *

from pyrate.manager import Manager

from sgx.tests.utils import mf_config, futures_filter, option_filter, fspread_filter
from sgx.tests.overrides import SPQCOverride, SGXOverrides

#Parameters:
futures = futures_filter
options = option_filter
spreads = fspread_filter
smoke_chg = [bind(TickRel, 1),
             bind(SetOrderAttrs, {'chg_qty':-1})]
smoke_rep=smoke_chg
smoke_market_price_change = [bind(SetOrderAttrs, {'chg_qty':1})]

smoke_direct = Worker.DIRECT.value
smoke_ttord = Worker.PROXY_DIRECT.value
smoke_fill = Worker.FILL

__all__ = ['TestOrderAcceptance']

class TestOrderAcceptance(TTAPICaptainTest):
    def __init__(self):
        super(TestOrderAcceptance,self).__init__()
        register_crews(Worker.DIRECT)

    def context(self):
        return OrderContext()

    def create_test(self):

        for trader_map in (smoke_direct, smoke_ttord):
            SetSessions()
            SetTraderAndCustomer()

            for nodes in OrderGenerator(order_types=[OrderType.LIMIT],
                                        restrictions=[OrderRes.NONE],
                                        modifications=[OrderMod.NONE],
                                        tifs=[Tif.GTD],
                                        sides=[Side.BUY]):
                for nodes in ContractsWithPrices(mf_config, [options, spreads]):
                    for nodes in OverrideSets([[Override()]], [SPQCOverride]):

                        add_del()
                        chg_del(change_actions=smoke_chg)
                        rep_del(replace_actions=smoke_rep)
                        sub_after_hold_del()
                        sub_after_onhold_del()
                        pfill_del()
                        fill()
                        ifill()
                        upd_del()

                        chg_pfill_chg_del(change1_actions=smoke_chg, change2_actions=smoke_chg)
                        chg_fill(change_actions=smoke_chg)
                        chg_hold_chg_del(change1_actions=smoke_chg, change2_actions=smoke_chg)
                        chg_hold_sub_chg_del(change1_actions=smoke_chg, change2_actions=smoke_chg)

                        rep_pfill_rep_del(replace1_actions=smoke_rep, replace2_actions=smoke_rep)
                        rep_fill(replace_actions=smoke_rep)
                        rep_hold_rep_del(replace1_actions=smoke_rep, replace2_actions=smoke_rep)
                        rep_hold_sub_rep_del(replace1_actions=smoke_rep, replace2_actions=smoke_rep)

            for nodes in OrderGenerator(order_types=[OrderType.MARKET],
                                        restrictions=[OrderRes.NONE,
                                                      OrderRes.IOC,
                                                      OrderRes.FOK],
                                        modifications=[OrderMod.NONE],
                                        tifs=[Tif.GTD],
                                        sides=[Side.SELL]):
                for nodes in ContractsWithPrices(mf_config, [futures, options]):
                    for nodes in OverrideSets([[Override()]], [SPQCOverride]):
                        ifill()
                        add_rej()
                        onhold_chg_del(change_actions=smoke_chg)
                        onhold_rep_del(replace_actions=smoke_rep)
                        sub_after_onhold_ifill()
            
            for nodes in OrderGenerator(order_types=[OrderType.LIMIT],
                                        restrictions=[OrderRes.NONE],
                                        modifications=[OrderMod.STOP,
                                                       OrderMod.IF_TOUCHED],
                                        tifs=[Tif.GTD],
                                        sides=[Side.BUY]):
                for nodes in ContractsWithPrices(mf_config, [futures, options]):
                    for nodes in OverrideSets([[Override()]], [SPQCOverride]):
                        add_del()
                        add_trig_fill()
                        add_trig_del()
                        chg_del(change_actions=smoke_chg)
                        rep_del(replace_actions=smoke_rep)
                        sub_after_hold_del()
                        sub_after_onhold_del()
                        upd_del()

            for nodes in OrderGenerator(order_types=[OrderType.MARKET],
                                        restrictions=[OrderRes.NONE],
                                        modifications=[OrderMod.STOP,
                                                       OrderMod.IF_TOUCHED],
                                        tifs=[Tif.GTD],
                                        sides=[Side.SELL]):
                for nodes in ContractsWithPrices(mf_config, [options, spreads]):
                    for nodes in OverrideSets([[Override()]], [SPQCOverride]):

                        add_del()
                        add_trig_udel()
                        ifill_after_itrig()
                        chg_del(change_actions=smoke_chg)
                        rep_del(replace_actions=smoke_rep)
                        sub_after_hold_del()
                        sub_after_onhold_del()
                        upd_del()

            for nodes in OrderGenerator(order_types=[OrderType.LIMIT],
                                        restrictions=[OrderRes.NONE],
                                        modifications=[OrderMod.NONE],
                                        tifs=[Tif.GTD],
                                        sides=[Side.BUY, Side.SELL]):
                for nodes in ContractsWithPrices(mf_config, [futures, spreads]):
                    SetOrderAttrs({'hints':aenums.HINT_POSITION_RESERVE})
                    addonhold_del()
                    onhold_chg_del(change_actions=smoke_chg)
                    onhold_rep_del(replace_actions=smoke_rep)
