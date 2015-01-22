from captain.lib.controlled_types import Worker, Tif, Side, UserName

from commontests.test_order_book_sharing_template import BaseOrderBookSharing, BaseStagedOrderBookSharing
from commontests.utils import register_crews, WorkerRelationships

from sgx.tests.utils import (mf_config, mf_option_config, mf_multi_leg_config,
                             futures_filter, fspread_filter, option_filter, ostrategy_filter,
                             change_ob_share_mods, hold_reject_mods, replace_ob_share_mods,
                             ob_share_replace_arej_mods, replace_reject_mods, submit_reject_mods)

# Global Variables

admin_relations = WorkerRelationships(del_shares=[Worker.TT_ADMIN_WITH_DIRECT_ACCT,
                                                  Worker.TT_ADMIN_WITH_PROXY_DIRECT_ACCT])

__all__ = ['TestOrderBookSharing_Futures', 'TestOrderBookSharing_Spreads',
           'TestOrderBookSharing_Options', 'TestOBSharing_TTADM']

obs_exclude = ['inq_rej_t1_del_t1',
               'inq_rej_t1_del_t2',
               'inq_rej_t2_del_t1',
               'inq_rej_t2_del_t2',
               'inq_t1_NO_CBK_t2_del_t1_NO_CBK_t2',
               'inq_t1_del_t1',
               'inq_t2_del_t1']

admin_test = ['hold_rej_t2_del_t2',
              'sub_rej_t2_after_hold_t1_del_t2',]

class TestOrderBookSharing_Futures(BaseOrderBookSharing):
    def __init__(self):
        register_crews(Worker.PROXY_DIRECT)
        super(TestOrderBookSharing_Futures,self).__init__()
        
        self.tifs=[Tif.GTD, Tif.GTC, Tif.GTDATE]
        self.sides=[Side.BUY,Side.SELL]
        self.mf_config=mf_config
        self.preds=[futures_filter]
#        self.change_reject_actions = ob_share_change_reject_mods
        self.change_actions = change_ob_share_mods
        self.replace_actions = replace_ob_share_mods
        self.hold_reject_actions = hold_reject_mods
        self.replace_reject_actions = replace_reject_mods
        self.replace_arej_actions = ob_share_replace_arej_mods
        self.resubmit_reject_actions = submit_reject_mods
        
        self.scen_list = obs_exclude
        
class TestOrderBookSharing_Spreads(BaseOrderBookSharing):
    def __init__(self):
        register_crews(Worker.PROXY_DIRECT)
        super(TestOrderBookSharing_Spreads,self).__init__()
        
        self.tifs=[Tif.GTD, Tif.GTC, Tif.GTDATE]
        self.sides=[Side.BUY,Side.SELL]
        self.mf_config=mf_multi_leg_config
        self.preds=[fspread_filter]
#        self.change_reject_actions = ob_share_change_reject_mods
        self.change_actions = change_ob_share_mods
        self.replace_actions = replace_ob_share_mods
        self.hold_reject_actions = hold_reject_mods
        self.replace_reject_actions = replace_reject_mods
        self.replace_arej_actions = ob_share_replace_arej_mods
        self.resubmit_reject_actions = submit_reject_mods
        
        self.scen_list = obs_exclude
        
class TestOrderBookSharing_Options(BaseOrderBookSharing):
    def __init__(self):
        register_crews(Worker.PROXY_DIRECT)
        super(TestOrderBookSharing_Options,self).__init__()
        
        self.tifs=[Tif.GTD, Tif.GTC, Tif.GTDATE]
        self.sides=[Side.BUY,Side.SELL]
        self.mf_config=mf_option_config
        self.preds=[option_filter]
#        self.change_reject_actions = ob_share_change_reject_mods
        self.change_actions = change_ob_share_mods
        self.replace_actions = replace_ob_share_mods
        self.hold_reject_actions = hold_reject_mods
        self.replace_reject_actions = replace_reject_mods
        self.replace_arej_actions = ob_share_replace_arej_mods
        self.resubmit_reject_actions = submit_reject_mods
        
        self.scen_list = obs_exclude
        
class TestOBSharing_TTADM(BaseOrderBookSharing):
    def __init__(self):
        register_crews(Worker.DIRECT,admin_relations)
        super(TestOBSharing_TTADM,self).__init__()
        
        self.tifs=[Tif.GTD]
        self.sides=[Side.BUY,Side.SELL]
        self.mf_config=mf_config
        self.preds=[futures_filter]
        self.is_exclude_scens = False
        
        self.scen_list = admin_test