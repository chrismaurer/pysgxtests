from ttapi import aenums

from commontests.test_throttled_orders_template import (BaseTestOrderThrottle,
                                                        BaseTestThrottleOrderBook)
from commontests.utils import register_crews, WorkerRelationships

from captain.lib.controlled_types import Worker

from sgx.tests.utils import mf_config, futures_filter

__all__ = ['TestOrderThrottle', 'TestThrottleOrderBook']

rel = WorkerRelationships(proxy_primary_fillers=[Worker.PROXY_NO_SHARE_PRIMARY_SHARE],
                          proxy_secondary_fillers=[Worker.PROXY_NO_SHARE_PRIMARY_SHARE])

class TestOrderThrottle(BaseTestOrderThrottle):
    def __init__(self):
        super(TestOrderThrottle, self).__init__(mf_config, [futures_filter], order_rate=3)
        register_crews(Worker.PROXY_DIRECT, rel)
        self.inquire_order_status = aenums.TT_ORDER_STATUS_REJECTED

class TestThrottleOrderBook(BaseTestThrottleOrderBook):
    def __init__(self):
        super(TestThrottleOrderBook, self).__init__(mf_config, futures_filter, order_rate=3)
        register_crews(Worker.PROXY_DIRECT, rel)
        self.inquire_order_status = aenums.TT_ORDER_STATUS_REJECTED