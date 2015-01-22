# commontests imports
from basis_validation import *
from basis_validation.validator import FullValidator

# Pyrate Imports
from captain.plugins.validator import ValidatorPlugin
from captain.plugins.log_file_validator import LogFileValidator, Indices
from basis_validation.fill_server.fill_server_validator import setup_fill_server

# SGX Imports
from order.order_validator import setup_order
from fill.fill_validator import setup_fill
from order_book.order_book_validator import setup_order_book
from price.price_validator import setup_price_table
from login.login_validator import setup_login
from log_files.log_file_validator import setup_file
from rfq.rfq_validator import setup_rfq_table

__all__ = ['SGXValidator', 'SGXFillServerValidator', 'SGXLogFileValidator',
           'SGXLoginValidator', 'SGXPriceValidator', 'SGXRFQValidator']

class SGXValidator(FullValidator):
    def __init__(self, log_results=False, throw_results=True):
        #### Order validation flags #####
        self.transient_order_info_in_single_msg = 'None'
        self.exch_supports_native_holds = False
        self.minvol_rest_removed_on_market_entry = False
        self.immediate_or_bulk_transfer_of_hidden_qty_for_iceberg = 'bulk'
        self.separate_fill_and_order_feeds = True
        self.exch_provides_exec_qty_on_non_delete = False
        self.exch_provides_date_time = False
        self.hold_causes_new_order_number_or_autosubmit = 'None'
        self.risk_account_mapped_field = 'exchange_clearing_account'
        #### Fill validation flags #####
        self.exch_provides_trade_identifier = 'Summary'
        self.gw_sets_FILL_TRANSACTION_IDENTIFIER_AS_INTEGER = False
        #### Order Book Download validation flags #####
        self.exec_qty_updated_on_download = False

        # Setup basis validation as per gw rules
        super(SGXValidator, self).__init__(log_results, throw_results)

        # Setup SGX specific validation
        setup_order(self.root_table.get_rule('order'))
        setup_fill(self.root_table.get_rule('fill'))
        setup_order_book(self.root_table.get_rule('order_book'))

class SGXFillServerValidator(ValidatorPlugin):
    def __init__(self, log_results=True, throw_results=True):
        self.risk_account_mapped_field = 'exchange_clearing_account'
        super(SGXFillServerValidator, self).__init__(log_results, throw_results)
        setup_fill_server(self)

class SGXLogFileValidator(LogValidator):
    def __init__(self, log_results=False, throw_results=True):
        super(SGXLogFileValidator, self).__init__(log_results, throw_results)
        setup_file(self.root_table)

class SGXLoginValidator(LoginValidator):
    def __init__(self, log_results=True, throw_results=True):
        super(SGXLoginValidator, self).__init__(log_results, throw_results)
        setup_login(self.root_table)

class SGXPriceValidator(PriceValidator):
    def __init__(self, log_results=True, throw_results=True):
        super(SGXPriceValidator, self).__init__(log_results, throw_results)
        setup_price_table(self.root_table)

class SGXRFQValidator(RFQValidator):
    def __init__(self, log_results=True, throw_results=True):
        super(SGXRFQValidator, self).__init__(log_results, throw_results)
        setup_rfq_table(self.root_table)