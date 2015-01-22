from captain.lib.controlled_types import Worker

from commontests.test_logging_template import BaseTestLogFiles
from commontests.utils import register_crews

from sgx.tests.utils import mf_config, futures_filter
from sgx.tests.features import gateway

# Global Variables
__all__ = ['TestSGXLogFiles']

class TestSGXLogFiles(BaseTestLogFiles):
    def __init__(self, mf_config=mf_config, prod_types=[futures_filter],rfq_fields_to_validate=['']):
               
        super(TestSGXLogFiles, self).__init__(mf_config, prod_types, rfq_fields_to_validate) 
        register_crews(Worker.DIRECT)       

        self.timeout = 700
        self.delay_time = 20