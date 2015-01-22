from ttapi import aenums

# GW and Commontests Imports
from commontests.price_server.templates.test_exch_contracts_template import BaseTestContracts

__all__ = ['TestContracts']

class TestContracts(BaseTestContracts):
    def __init__(self):

        super(TestContracts, self).__init__()

        self.prod_types=[aenums.TT_PROD_FUTURE,
                         aenums.TT_PROD_FSPREAD,
                         aenums.TT_PROD_OPTION,
                         aenums.TT_PROD_OSTRATEGY,
                         aenums.TT_PROD_ENERGY]
