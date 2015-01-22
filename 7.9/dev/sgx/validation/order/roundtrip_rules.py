import operator, sys
from ConfigParser import SafeConfigParser

from ttapi import aenums, cppclient
from ttutil import in_

from basis_validation.utils import compare

__all__ = []  # populated at the bottom of this module

###################
# Core Enum Rules
###################

###################
# ID Rules
###################
def exchange_order_id_has_changed(action, before, after):
    compare(before.pending.exchange_order_id, after.pending.exchange_order_id, op=operator.ne)

def exchange_order_id_is_same(action, before, after):
    compare(before.pending.exchange_order_id, after.pending.exchange_order_id)

def site_order_key_is_same(action, before, after):
    compare(before.pending.site_order_key, after.pending.site_order_key)

###################
# Quantity Rules
###################
def fill_qty_is_not_checked(action, before, after):
    pass

###################
# Price Rules
###################
def limit_prc_for_mtl_is_not_ttinvalid(action, before, after):
    compare(after.pending.limit_prc, cppclient.TT_INVALID_PRICE, op=operator.ne)

###################
# Date & Time Rules
###################
def time_exch_is_zero(action, before, after):

    time_exch_after = after.pending.time_exch

    compare(time_exch_after.hr, 0)
    compare(time_exch_after.min, 0)
    compare(time_exch_after.sec, 0)
    compare(time_exch_after.ms, 0)


def date_exch_is_zero(action, before, after):

    date_exch_after = after.pending.date_exch

    compare(date_exch_after.day, 0)
    compare(date_exch_after.mth, 0)
    compare(date_exch_after.day, 0)

#def passive_aggressive_flag_is_set(action, before, after):
#    compare(after.pending.order_flags, aenums.TT_PASSIVE_MOD_CODE, op=operator.eq)

def time_processed_is_not_zero(action, before, after):

    time_processed_after = after.pending.time_processed
    total_time = 0

    total_time += time_processed_after.hr
    total_time += time_processed_after.min
    total_time += time_processed_after.sec
    total_time += time_processed_after.ms

    compare(total_time, 0, op=operator.ne )

def date_processed_is_not_zero(action, before, after):

    date_processed_after = after.pending.date_processed
    compare(date_processed_after.day, 0, op=operator.ne)

def sgx_time_sent_is_current_time(action, before, after):
    time_sent_is_current_time(action, before, after, time_threshold=6)

###################
# Trader Info Rules
###################

###################
# Series Info Rules
###################

###################
# Misc
###################

_hostinfo_member_user_id = None
def get_hostinfo_member_user_id():
    global _hostinfo_member_user_id
    if not _hostinfo_member_user_id:
        from pyrate import Manager
        filename = "{0}\{1}hostinfo.cfg".format(Manager.getOrderServer().mappedConfigDir,
                                                Manager.getGateway().name)
        parser = SafeConfigParser()
        parser.read([filename])

        for section in parser.sections():
            if section.startswith('MEMBER_1_TTF'):
                _hostinfo_member_user_id = "{0}".format(parser.get(section, 'UserId'))
    return _hostinfo_member_user_id

###################
# Misc
###################
def exchange_credentials_is_populated(action, before, after):
    compare(after.pending.exchange_credentials, get_hostinfo_member_user_id(), operator.eq)

#############################################
## Populate __all__ module level attribute ##
#############################################
this_mod = sys.modules[__name__]
for attr in dir(this_mod):
    attr_val = getattr(this_mod, attr)
    if not attr.startswith('_') and \
      (hasattr(attr_val, '__module__') and attr_val.__module__ == __name__):
        __all__.append(attr)