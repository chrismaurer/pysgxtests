import os
import re
import sys

from pyrate.ttapi.predicates import ProductComparison
from captain.lib.controlled_types import Worker, ProductGroup, ProductType
from ttutil import in_

from commontests.order_server.order_management.suites import OrderManagementAcceptanceSuiteGenerator

from sgx.tests.order_alterations import *
from sgx.tests.features import gateway

acceptance_suite_gen = OrderManagementAcceptanceSuiteGenerator(gateway, group_scenario_percentage=50,
                                                               primary_workers=[Worker.PROXY_DIRECT],
                                                               suite_include_patterns=[re.compile('Future')])
acceptance_suite_gen(sys.modules[__name__])
