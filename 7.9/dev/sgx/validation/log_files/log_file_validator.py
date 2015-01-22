from basis_validation import log_files
from basis_validation.validator import FullValidator, LogValidator
# SGX Imports
from .conditions import *
from .rules import *


#Pyrate Imports
from captain.plugins.log_file_validator import IndicesDecisionTable, LockedDecisionTable
from captain.plugins.validator import LockedDecisionTable

#Commontests Imports
from basis_validation import conditions as base_conditions
from basis_validation.log_files import rules
from basis_validation.log_files import conditions





def setup_file(table):
    log_file_table = table.get_rule('log_message')
    log_file_table.add_rule(sgx_fill_server_start_msg_is_logged, 'sgx_fill_server_start_msg_is_logged', cond='False')    
    log_file_table.add_rule(sgx_fill_server_stop_msg_is_logged, 'sgx_fill_server_stop_msg_is_logged', cond='False')
    
    
     
    log_file_table.override_rule('order_server_state_changed_msg_is_logged', 'True', 157204, note="PCR for Order Server")
    
    log_file_table.optout_rule('fill_server_stop_msg_is_logged', 'is_action_StopGatewayServer and is_server_FillServer', new_rule='sgx_fill_server_stop_msg_is_logged', note="Fill Server keeps changing this message" )
    log_file_table.optout_rule('fill_server_start_msg_is_logged', 'is_action_StartGatewayServer and is_server_FillServer', new_rule='sgx_fill_server_start_msg_is_logged', note="Fill Server keeps changing this message" )
    log_file_table.optout_rule('order_server_contract_download_msg_is_logged', 'True', new_rule=None, note="SGX does not use this rule")
    log_file_table.optout_rule('price_server_contract_download_msg_is_logged', 'True', new_rule=None, note="SGX does not use this rule" )

class SGXLogFileValidator(LogValidator):
    """
    If you only want file validation, you can use this plugin class instead
    of the top level one.
    
    """
    def __init__(self, log_results=False, throw_results=True):
        super(SGXLogFileValidator, self).__init__(log_results, throw_results)
        
        setup_file(self.root_table)
        
