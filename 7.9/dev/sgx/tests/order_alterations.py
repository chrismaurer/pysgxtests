# python imports
from collections import defaultdict

# pycppclient imports
from ttapi import cppclient

# captain imports
from captain import bind
from captain.lib import SetOrderAttrs, TickRel, SetCustomer, ChangeSide
from captain.lib.controlled_types import Tif, Customer, OrderType, OrderRes, ExchangeClearingAccount as ECA

__all__ = ['causes_del_rej', 'causes_hold_rej', 'causes_sub_rej', 'chg_for_itrig', 'chg_into_del', 'chg_into_ifill',
           'chg_into_udel', 'held_chg', 'held_chg_rej', 'held_rep', 'held_rep_rej', 'rep_for_itrig', 'rep_into_ifill',
           'resting_chg', 'resting_chg_rej', 'resting_rep', 'resting_rep_arej', 'resting_rep_drej',
           'resting_rep_rej', 'post_trig_chg', 'post_trig_rep', 'stop_chg', 'stop_rep',
           'oco_chg', 'oco_rep', 'ob_scope_chg', 'ob_scope_rep', 'lsm_chg', 'lsm_rep', 'chg_for_itrig', 'rep_for_itrig']

#########################
#CONTROLLED NAMES
#########################
ECA.VALID_PRIMARY.register('NewAccount')
ECA.VALID_NON_PRIMARY.register('xyx')
ECA.NUMERIC.register('1234134')
ECA.INVALID.register('BADTXT')

resting_chg = [#bind(TickRel, 2),
               #bind(TickRel, -1),
               bind(SetOrderAttrs, {'chg_qty':1}),
               bind(SetOrderAttrs, {'chg_qty':-1})]

resting_rep = [bind(TickRel, 2),
               bind(TickRel, -1),
               bind(SetOrderAttrs, {'chg_qty':1}),
               bind(SetOrderAttrs, {'chg_qty':-1}),
               bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY}),
               bind(SetCustomer, Customer.PROXY_DIRECT_SHARE)]

chg_for_itrig = []

chg_into_del = [bind(SetOrderAttrs, {'chg_qty': cppclient.TT_INVALID_QTY}),
                bind(SetOrderAttrs, {'chg_qty':-999})]

chg_into_udel = [bind(SetOrderAttrs, {'order_restrict':OrderRes.IOC})]

chg_into_ifill = [bind(TickRel, 2),
                  bind(SetOrderAttrs, {'chg_qty':1}),
                  bind(SetOrderAttrs, {'chg_qty':-1}),
                  bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY})]

resting_chg_rej = [bind(SetOrderAttrs, {'tif': Tif.GTC})]

resting_rep_rej = [bind(SetOrderAttrs, {'site_order_key':''})]

resting_rep_drej = resting_rep_rej

resting_rep_arej = [bind(SetOrderAttrs, {'tif': Tif.GTC})]

causes_del_rej = [ChangeSide,
                  bind(SetOrderAttrs, {'site_order_key':''})]

causes_hold_rej = [bind(SetOrderAttrs, {'site_order_key':''})]

causes_sub_rej = [bind(SetOrderAttrs, {'tif': Tif.GTC})]

held_chg = [bind(TickRel, 2),
            bind(TickRel, -1),
            bind(SetOrderAttrs, {'chg_qty':1}),
            bind(SetOrderAttrs, {'chg_qty':-1}),
            bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY})]

held_chg_rej = [bind(SetOrderAttrs, {'order_qty':0})]

held_rep = [bind(TickRel, 2),
            bind(TickRel, -1),
            bind(SetOrderAttrs, {'chg_qty':1}),
            bind(SetOrderAttrs, {'chg_qty':-1}),
            bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY}),
            bind(SetCustomer, Customer.PROXY_DIRECT_SHARE)]

held_rep_rej = [bind(SetOrderAttrs, {'limit_prc':cppclient.TT_INVALID_PRICE})]

rep_for_itrig = []

rep_into_ifill  = [bind(TickRel, 2),
                   bind(SetOrderAttrs, {'chg_qty':1}),
                   bind(SetOrderAttrs, {'chg_qty':-1}),
                   bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY}),
                   bind(SetCustomer, Customer.PROXY_DIRECT_SHARE)]

post_trig_chg = [None]

post_trig_rep = [None]

stop_chg = [None]

stop_rep = [None]

oco_chg = []

oco_rep = []

chg_for_itrig = []
rep_for_itrig = []
lsm_chg = []
lsm_rep = []

###########################
# OrderBook scenario sets #
###########################
ob_scope_chg = defaultdict(list)

for ob_scope in ['chg_to_book',
                 'pfill_chg_to_book']:
    ob_scope_chg[ob_scope] = [bind(SetOrderAttrs, {'chg_qty':-1}),]

for ob_scope in ['chg_to_mid_book',
                 'chg_as_held_to_mid_book']:
    ob_scope_chg[ob_scope] = [bind(SetOrderAttrs, {'chg_qty':7})]

ob_scope_rep = defaultdict(list)
ob_scope_rep['rep_to_book'] = [bind(TickRel, 1)]
