# Basis validation Imports
from basis_validation.rfq import roundtrip as base_rfq_rules

def setup_rfq_table(table):
    rfq_table = table.get_rule('rfq')

    if 'price_action_is_action_sent' in dir(base_rfq_rules):
        # 7.9 COMMONTESTS
        prefix = 'price_'
    else:
        # pre 7.9 COMMONTESTS
        prefix = ''