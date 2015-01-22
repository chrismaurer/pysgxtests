import re
import sys

from commontests.order_server.order_book.suites import *
from sgx.tests.features import gateway
from sgx.tests.order_alterations import *

ss_suite_gen = ServiceShutdownSuiteGenerator(gateway,
                                             group_include_patterns=[re.compile('recovery_reliability')],
                                             suite_exclude_patterns=[re.compile('StartOrderserverSuccessfulWhenPriceServerDown'),
                                                                     re.compile('NetworkDisconnect'),
                                                                     re.compile('StopTtmWithoutDownload')],
                                             qty=5)

ss_suite_gen(sys.modules[__name__])
