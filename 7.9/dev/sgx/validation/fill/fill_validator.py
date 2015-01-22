# CommonTests Imports
from basis_validation import *
from basis_validation.utils import compare
from basis_validation.fill.utils import *
from basis_validation.fill.fill_validator import srvr_vrmf

# SGX Imports
from .conditions import *
from .roundtrip_rules import *

__all__ = ['setup_fill']


# Steps to view all rules available.
# Start a python intrepreter (python -i) with your PYTHONPATH set as if you're running automation.
# type:  from basis_validation import fill
# type:  from pprint import pprint
# To see fill rules type:  pprint( dir( fill.roundtrip ) )

def setup_fill(fill_table):

    ##################
    # ## Conditions ##
    ##################

    ##################
    # ## Core Enums ##
    ##################
    core_enums_table = fill_table.get_rule('roundtrip').get_rule('core_enums')

    core_enums_table.override_rule('open_close_is_open_close_book_order', 'True',
                                   -1, note= 'investigating as of 6-2-2010')

    if srvr_vrmf.version == 7 and srvr_vrmf.release < 17:
        core_enums_table.add_rule(fill_srs_comb_code_is_default, cond='False')
        core_enums_table.override_rule('fill_cmb_code_is_fill_srs_comb_code', 'True', 202961,
                                       'fill_srs_comb_code_is_default',
                                       'Leg fills Fill.srs.comb_code is incorrect (OS Rule 4.26.3)')

    #####################
    ### Date and Time ###
    #####################
    date_and_time_table = fill_table.get_rule('roundtrip').get_rule('date_and_time')


    ###########
    # ## IDs ##
    ###########
    ids_table = fill_table.get_rule('roundtrip').get_rule('ids')

    # exchange_order_id
    ids_table.add_rule(basis_fill_roundtrip.exchange_order_id_is_empty, cond='False')

    # transaction_no
    ids_table.optout_rule('legs_transaction_identifier_is_empty', 'True', None, note='Running order_feed_and_fill_feed_transaction_no instead')
    ids_table.optout_rule('non_legs_transaction_identifier_is_not_empty', 'True', None, note='Running order_feed_and_fill_feed_transaction_no instead')
    ids_table.optout_rule('transaction_identifier_is_not_empty', 'True', None, note='Temp Optout')

    ##############
    # ## Misc ##
    ##############
    misc_table = fill_table.get_rule('roundtrip').get_rule('misc')

    # exchange_credentials
    misc_table.replace_rule('exchange_credentials_is_populated', exchange_credentials_is_populated)

    ##############
    # ## Prices ##
    ##############
    prices_table = fill_table.get_rule('roundtrip').get_rule('price')

    ##################
    # ## Quantities ##
    ##################
    quantities_table = fill_table.get_rule('roundtrip').get_rule('quantities')

    quantities_table.override_rule( 'wrk_qty_is_aggregate', 'True', 139782, note="This should be TT_INVALID_QTY for the legs of a strategy/ spread" )

    ###################
    # ## Series Info ##
    ###################
    series_info_table = fill_table.get_rule('roundtrip').get_rule('series_info')


    ###################
    # ## Trader Info ##
    ###################
    trader_info_table = fill_table.get_rule('roundtrip').get_rule('trader_info')

    trader_info_table.optout_rule( 'giveup_mbr_is_clearing_mbr_book_order', 'True', None, note="SGX will optout permanently" )

    trader_info_table.optout_rule('cntr_party_is_empty', 'True', None, note ='Permanently opt out counter party - according to pcr 52156')