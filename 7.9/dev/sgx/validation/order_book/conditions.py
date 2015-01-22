import logging

log = logging.getLogger(__name__)

def is_exchange_reject(action, before, after):
    return (after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED and
            not is_gateway_reject(action, before, after))


def is_gateway_reject(action, before, after):
    return False

def is_order_sent_to_exchange(action, before, after):
    return True
