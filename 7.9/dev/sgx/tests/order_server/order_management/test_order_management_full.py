import os
import re
import sys

from pyrate.ttapi.predicates import ProductComparison
from captain.lib.controlled_types import Worker, ProductGroup, ProductType
from ttutil import in_

from commontests.order_server.order_management.suites import OrderManagementSuiteGenerator

from sgx.tests.order_alterations import *
from sgx.tests.features import gateway

acceptance_suite_gen = OrderManagementSuiteGenerator(gateway, group_scenario_percentage=1)
acceptance_suite_gen(sys.modules[__name__])
