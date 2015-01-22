from basis_validation import basis_log_files_rules
#import basis_validation.login.rules as basis_login_rules

import rules as tocom_rules

def setup_login(table):
    login_table = table.get_rule('login')
##    login_table.add_rule(basis_log_files_rules.capability_enum_TT_SUPPORTS_ORDER_QUANTITY_AT_DEPTH_is_True, cond='False')
#    login_table.add_rule(tocom_rules.capability_enum_TT_SUPPORTS_ORDER_QUANTITY_AT_DEPTH_is_False, cond='False')
#    login_table.optout_rule(basis_log_files_rules.capability_enum_TT_SUPPORTS_ORDER_QUANTITY_AT_DEPTH_is_True,
#                            tocom_rules.capability_enum_TT_SUPPORTS_ORDER_QUANTITY_AT_DEPTH_is_False,
#                            'is_action_WaitForOnServerCapabilities',
#                            note='TOCOM does not support Order Qty at Depth')