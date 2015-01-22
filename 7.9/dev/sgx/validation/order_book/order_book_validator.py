# CommonTests Imports
from basis_validation import *
from basis_validation.utils import compare
from basis_validation.order.order_validator import delete_not_reject
from basis_validation.order import roundtrip

# SGX Imports
from .conditions import *
from .roundtrip_rules import * 

__all__ = ['setup_order_book']

def setup_order_book(order_book_table):
    order_book_table.optout_rule('order_no_old_is_order_no_old_book_all_orders', 'is_book_order_onhold',
                                 new_rule=None, note = 'Held orders have a new order_no_old')
    order_book_table.optout_rule('order_no_is_order_no_book_all_orders', 'is_book_order_onhold',
                                 new_rule=None, note = 'Held orders have a new order_no')
    order_book_table.optout_rule('exchange_order_id_is_exchange_order_id_book_all_orders', 'is_book_order_onhold',
                                 new_rule=None, note = 'Held orders have a new exchange_order_id')

    ###################
    # Misc
    ###################
    # exchange_credentials
    order_book_table.replace_rule('exchange_credentials_is_populated_non_held_orders', exchange_credentials_is_populated_non_held_orders) 

    order_book_table.add_rule(basis_order_book_rules.round_trip_id_is_round_trip_id_book_all_orders, cond='False')
    order_book_table.optout_rule('round_trip_id_is_zero_all_orders', 'is_action_DownloadOrderBook',
                                       'round_trip_id_is_round_trip_id_book_all_orders')