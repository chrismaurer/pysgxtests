from captain.lib.controlled_types import Worker

from commontests.test_audit_log_template import BaseTestAuditLogFiles
from commontests.utils import register_crews, WorkerRelationships

from sgx.tests.utils import mf_config, futures_filter
from sgx.tests.features import gateway

# Global Variables
__all__ = ['TestTFXAuditLog']

class TestTFXAuditLog(BaseTestAuditLogFiles):
    def __init__(self, mf_config=mf_config, prod_types=[futures_filter], rfq_fields_to_validate=['']):

        super(TestTFXAuditLog, self).__init__(mf_config, prod_types, rfq_fields_to_validate)
        register_crews(Worker.DIRECT, WorkerRelationships(direct_shares=[Worker.SHARE]))