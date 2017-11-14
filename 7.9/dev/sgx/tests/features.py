# python imports
import copy

# captain imports
from captain.lib.controlled_types import (Worker, OrderType, OrderRes, OrderMod,
                                          Tif, Side, ProductType)
from commontests.features import (OrderServerFlags, OrderServerFeatureSpec, SUPPORTED,
                                  UNSUPPORTED)

# commontests imports
from commontests.utils import OrderInfo

from sgx.tests.overrides import SGXOverrides

gateway = OrderServerFeatureSpec()

##############################################################################
# OrderType Support
##############################################################################
gateway[OrderType.LIMIT] = SUPPORTED
gateway[OrderType.MARKET] = SUPPORTED
gateway[OrderType.MTL] = SUPPORTED

gateway[OrderType.BATCH] = UNSUPPORTED
gateway[OrderType.CROSS] = UNSUPPORTED
gateway[OrderType.OCO] = UNSUPPORTED
gateway[OrderType.BEST_LIMIT] = UNSUPPORTED

##############################################################################
# OrderRes Support
##############################################################################
gateway[OrderRes.FOK] = SUPPORTED
gateway[OrderRes.IOC] = SUPPORTED
gateway[OrderRes.NONE] = SUPPORTED
gateway[OrderRes.LOC] = SUPPORTED
gateway[OrderRes.LOO] = SUPPORTED
gateway[OrderRes.MOC] = SUPPORTED
gateway[OrderRes.MOO] = SUPPORTED

gateway[OrderRes.BLOCK] = UNSUPPORTED
gateway[OrderRes.ICEBERG] = UNSUPPORTED
gateway[OrderRes.LIMIT_TO_MARKET_ON_LIMIT] = UNSUPPORTED
gateway[OrderRes.LSM] = UNSUPPORTED
gateway[OrderRes.MARKET_TO_LIMIT_ON_LEFTOVER] = UNSUPPORTED
gateway[OrderRes.MINVOL] = UNSUPPORTED
gateway[OrderRes.VOLA] = UNSUPPORTED

##############################################################################
# OrderMod Support
##############################################################################
gateway[OrderMod.NONE] = SUPPORTED
gateway[OrderMod.STOP] = SUPPORTED
gateway[OrderMod.IF_TOUCHED] = SUPPORTED
gateway[OrderMod.PASSIVE] = SUPPORTED

gateway[OrderMod.BEST_ONLY] = UNSUPPORTED
gateway[OrderMod.AUTO_AGRESS] = UNSUPPORTED
gateway[OrderMod.LMTL] = UNSUPPORTED
gateway[OrderMod.PASSIVE_AUTO_AGRESS] = UNSUPPORTED
gateway[OrderMod.PASSIVE_BEST_ONLY] = UNSUPPORTED

##############################################################################
# Tif Support
##############################################################################
gateway[Tif.GTD] = SUPPORTED
gateway[Tif.GTC] = SUPPORTED
gateway[Tif.GTDATE] = UNSUPPORTED

gateway[Tif.GIS] = UNSUPPORTED

##############################################################################
# Product Support
##############################################################################
gateway[ProductType.FSPREAD] = SUPPORTED
gateway[ProductType.FUTURE] = SUPPORTED
gateway[ProductType.OPTION] = SUPPORTED

gateway[ProductType.ENERGY] = UNSUPPORTED
gateway[ProductType.OSTRATEGY] = UNSUPPORTED
gateway[ProductType.STOCK] = UNSUPPORTED

#gateway.unsupported_accepts_hold.insert_combo(OrderType.LIMIT, OrderRes.ICEBERG, OrderMod.STOP)
#gateway.unsupported_accepts_hold.insert_combo(OrderMod.STOP, OrderRes.IOC)
#gateway.unsupported_accepts_hold.insert_combo(OrderMod.STOP, OrderRes.FOK)
#gateway.unsupported_accepts_hold.insert_combo(OrderMod.STOP, ProductType.OPTION)
#gateway.unsupported_accepts_hold.insert_combo(OrderMod.STOP, ProductType.OSTRATEGY)

gateway.unsupported.insert_combo(OrderType.MARKET, Tif.GTC)
gateway.unsupported.insert_combo(OrderRes.IOC, Tif.GTC)
gateway.unsupported.insert_combo(OrderRes.FOK, Tif.GTC)
gateway.unsupported.insert_combo(OrderRes.LOO, OrderMod.IF_TOUCHED)
gateway.unsupported.insert_combo(OrderRes.LOC, OrderMod.IF_TOUCHED)
gateway.unsupported.insert_combo(OrderRes.MOO, OrderMod.IF_TOUCHED)
gateway.unsupported.insert_combo(OrderRes.MOC, OrderMod.IF_TOUCHED)
gateway.unsupported.insert_combo(OrderRes.LOO, OrderMod.STOP)
gateway.unsupported.insert_combo(OrderRes.LOC, OrderMod.STOP)
gateway.unsupported.insert_combo(OrderRes.MOO, OrderMod.STOP)
gateway.unsupported.insert_combo(OrderRes.MOC, OrderMod.STOP)
gateway.unsupported.insert_combo(OrderRes.LOO, ProductType.FSPREAD)
gateway.unsupported.insert_combo(OrderRes.LOC, ProductType.FSPREAD)
gateway.unsupported.insert_combo(OrderRes.MOO, ProductType.FSPREAD)
gateway.unsupported.insert_combo(OrderRes.MOC, ProductType.FSPREAD)
#gateway.unsupported.insert_combo(OrderRes.LOO, Tif.GTDATE)
#gateway.unsupported.insert_combo(OrderRes.LOC, Tif.GTDATE)
#gateway.unsupported.insert_combo(OrderRes.MOO, Tif.GTDATE)
#gateway.unsupported.insert_combo(OrderRes.MOC, Tif.GTDATE)

gateway_flags = OrderServerFlags()
gateway_flags.across_prices = OrderServerFlags.SUPPORTED
gateway_flags.across_prices_with_opposing_market = OrderServerFlags.EXPECT_ADD_DEL
gateway_flags.alter_stop_price = OrderServerFlags.SUPPORTED
gateway_flags.chg_udel = OrderServerFlags.UNSUPPORTED
gateway_flags.dchg = OrderServerFlags.SUPPORTED
gateway_flags.drej = OrderServerFlags.SUPPORTED
gateway_flags.detailed_depth = OrderServerFlags.SUPPORTED
gateway_flags.exchange_cancelled = OrderServerFlags.EXPECT_REJECT
gateway_flags.lone_cancel = OrderServerFlags.UNSUPPORTED
gateway_flags.inquire = OrderServerFlags.EXPECT_REJECT
gateway_flags.ipfill = OrderServerFlags.EXPECT_ADD_DEL
gateway_flags.itrig = OrderServerFlags.EXPECT_ADD
gateway_flags.mtl_type_persists = True
gateway_flags.pfill_hold = OrderServerFlags.SUPPORTED
gateway_flags.sub_rej = OrderServerFlags.SUPPORTED
gateway_flags.os_restart = OrderServerFlags.UNCHANGED
gateway_flags.only_admin_gets_incomplete_order = False
gateway_flags.rfq = OrderServerFlags.EXPECT_ACCEPT

gateway_flags.incomplete_orders = True
gateway_flags.incomplete_order_order_no_persist = True
gateway_flags.only_admin_gets_incomplete_order = True

def get_order_info_flags(order_info):
    retval = copy.copy(gateway_flags)
#    if order_info.res is OrderRes.MOO:
#        retval.needs_opposite_market = True
#    if order_info.otype is OrderType.MARKET and order_info.res is OrderRes.NONE:
#        retval.exchange_cancelled = OrderServerFlags.EXPECT_REJECT
#        if order_info.prod_type is [ProductType.OPTION, ProductType.OSTRATEGY]:
#            retval.across_prices = OrderServerFlags.UNSUPPORTED
#    if order_info.tif == Tif.GTD:
#        retval.os_restart = OrderServerFlags.UNCHANGED
    if order_info.res is [OrderRes.MOC, OrderRes.MOO]:
        retval.add_del = OrderServerFlags.EXPECT_REJECT
        retval.chg_hold_del = OrderServerFlags.EXPECT_REJECT
        retval.hold_chg_del = OrderServerFlags.EXPECT_REJECT
        retval.rep_del = OrderServerFlags.EXPECT_REJECT
        retval.sub_after_onhold_del = OrderServerFlags.EXPECT_REJECT
        retval.needs_opposite_market = True

        print 'FUCK! '*6
        print dir(retval)
        print 'FUCK! '*6

    return retval

def get_reject_order_info(field):
    limit = OrderInfo(Worker.DIRECT, OrderType.LIMIT, OrderRes.NONE, OrderMod.NONE,
                      Tif.GTD, Side.BUY, ProductType.FUTURE)
    return limit.clone(field)

def get_market_finder_config(order_info):
    import re
    from copy import deepcopy
    from pyrate.marketfinder import MarketFinderConfigData

    mf_config = MarketFinderConfigData()
    mf_config.timeout = 500
    mf_config.depth = 20
    mf_config.maxTriesPerProduct = 12
    mf_config.useCache = True
    mf_config.fixLotQty = False
    mf_config.failPatterns = (re.compile('.*Illegal transaction at this time.*'),
                             re.compile('.*The transaction is not valid for this instrument type.*'),
                             re.compile('.*Given time validity is not allowed.*'),
                             re.compile('.*Given premium is not allowed.*'),
                             re.compile('.*The series first trading time is in the future.*'),
                             re.compile('.*The series \(or its underlying\) is stopped.*'),
                             re.compile('.*Pre-trade server could not find series.*'),
                             re.compile('.*User is not allowed to act in this instrument type.*'),
                             re.compile('.*A required limit has not been set.*'))
    mf_config.acceptable_reject_messages = ['No qty filled or placed in order book; EX: omniapi_tx_ex() returned 0 with txstat 1',
                                            'EX: transaction aborted (Order-book volume was too low to fill order.)',
                                            'EX: transaction aborted (Allowed Order Quantity limit exceeded)',
                                            'EX: transaction aborted (Market orders are not allowed for this instrument)',
                                            'EX: transaction aborted (The trigger order trigger time validity is not valid.)']

    if order_info.prod_type == ProductType.OPTION:
        mf_config.maxTriesPerProduct = 120
        mf_config.useDefaultBestPriceFirst = True
        mf_config.defaultBestPrice = 5.00
        return mf_config
    if order_info.prod_type == ProductType.FSPREAD or \
    order_info.prod_type == ProductType.OSTRATEGY or \
    order_info.prod_type == ProductType.MULTI_LEG:
        mf_config.maxTriesPerProduct = 80
        mf_config.useDefaultBestPriceFirst = True
        mf_config.defaultBestPrice = 1.00
        mf_config.ignoreLegs = True
        return mf_config
    if order_info.mod == OrderMod.STOP:
        mf_config.name = 'STOP orders'
        mf_config.depth = 0
        mf_config.stopTicks = 1
        mf_config.limitTicks = 6
        return mf_config
    if order_info.mod == OrderMod.IF_TOUCHED:
        mf_config.name = 'IF TOUCHED orders'
        mf_config.depth = 0
        mf_config.stopTicks = 1
        mf_config.limitTicks = 6
        return mf_config
    else:
        return mf_config

def get_market_finder_order_info(order_info):
    limit = OrderInfo(Worker.DIRECT, OrderType.LIMIT, OrderRes.NONE, OrderMod.NONE,
                      Tif.GTD, Side.BUY, ProductType.FUTURE)
    market = OrderInfo(Worker.DIRECT, OrderType.MARKET, OrderRes.NONE, OrderMod.NONE,
                       Tif.GTD, Side.BUY, ProductType.FUTURE)
    if order_info.mod == OrderMod.STOP:
        if order_info.otype == OrderType.MARKET:
            return market.clone(order_info.primary_worker, order_info.mod, order_info.prod_type)
        if order_info.otype == OrderType.LIMIT:
            return limit.clone(order_info.primary_worker, order_info.mod, order_info.prod_type)
    if order_info.mod == OrderMod.IF_TOUCHED:
        if order_info.otype == OrderType.MARKET:
            return market.clone(order_info.primary_worker, order_info.mod, order_info.prod_type)
        if order_info.otype == OrderType.LIMIT:
            return limit.clone(order_info.primary_worker, order_info.mod, order_info.prod_type)
    if order_info.otype == OrderType.MARKET:
        return market.clone(order_info.primary_worker, order_info.prod_type)
    return limit.clone(order_info.primary_worker, order_info.prod_type)

def get_valid_ob_scope_combos(combo, order_info):
#    for ob_scope in combo:
#        if 'udel' in ob_scope and order_info.res not in (OrderRes.IOC, OrderRes.FOK):
#            return False
#        elif 'trig' in ob_scope or 'sub' in ob_scope or 'hold' in ob_scope or 'pfill' in ob_scope:
#            return False
#        elif 'rep' in ob_scope:
#            return False

    return True

def get_product_group_for_order_info(order_info):
    from sgx.tests.utils import ProductGroup

    if order_info.otype == OrderType.MARKET or order_info.tif == Tif.GTC \
            or order_info.res == OrderRes.LOC or order_info.res == OrderRes.LOO \
            or order_info.res == OrderRes.MOC or order_info.res == OrderRes.MOO:
        return order_info.clone(ProductGroup.SPECIFIC)
    else:
     return order_info

def get_operator_id(entity, exch_mgt):
    from pyrate import Manager

    ttus = Manager.getTTUserSetup()
    sub_user_id = entity.sub_user_id
    user = entity.user_name
    gw = Manager.getGateway().name
    ## try to access operator id in TTUS:
    ## first catch exception for OnBehalfOf orders
    ## then catch other exception and assume no operator id
    try:
        operator_id = ttus.user_mgt_data[user][entity.trader.mgt][gw].uxg_operator_id
    except:
        try:
            operator_id = ttus.user_mgt_data[user][exch_mgt.mgt][gw].uxg_operator_id
        except:
            operator_id = ''

    if sub_user_id:
        return sub_user_id
    if operator_id:
        return operator_id
    if user:
        return user
    else:
        return exch_mgt.trader

def get_auditlog_values(entity, fields, get_operator_id, gateway):
    from ttapi import client
    from pyrate import Manager
    from pyrate.ttapi.order import TTAPIOrder

    contract = entity.srs
    if entity.trader.member.startswith('TTORD'):
        ttus = Manager.getTTUserSetup()
        exch_mgt = ttus.ttord_mappings[entity.trader.mgt][gateway.name]
    else:
        exch_mgt = entity.trader

    if type(entity) == client.rfqc.RFQC:
        rfqc = entity
        auditlog_values_all = {}
        auditlog_values_all['DisplayName'] = 'needs implementation'
        auditlog_values_all['ProdType'] = cppclient.Enum2AuxStr(contract.prod.prod_type)
        auditlog_values_all['GW Specific'] = ''
        auditlog_values_all['TxtMsg'] = ''
        auditlog_values_all['Srvr'] = gateway.orderServer.ip
        auditlog_values_all['ExchTime'] = ''
        auditlog_values_all['ClrMember'] = ''
        auditlog_values_all['FFT3'] = ''
        auditlog_values_all['FFT2'] = ''
        auditlog_values_all['FFT1'] = ''
        auditlog_values_all['Account'] = ''
        auditlog_values_all['Trader'] = rfqc.trader.trader
        auditlog_values_all['Group'] = rfqc.trader.group
        auditlog_values_all['Member'] = rfqc.trader.member
        auditlog_values_all['User ID'] = rfqc.trader.user
        auditlog_values_all['ExchTrader'] = exch_mgt.trader
        auditlog_values_all['ExchGroup'] = exch_mgt.group
        auditlog_values_all['ExchMember'] = exch_mgt.member
        auditlog_values_all['OrderRes'] = ''
        auditlog_values_all['OrderType'] = cppclient.Enum2AuxStr(rfqc.quote_type)
        auditlog_values_all['Strike'] = contract.strike
        auditlog_values_all['StopPrc'] = ''
        auditlog_values_all['LimitPrc'] = 0
        auditlog_values_all['C/P'] = cppclient.Enum2AuxStr(contract.callput)
        auditlog_values_all['O/C'] = ''
        auditlog_values_all['Expiry'] = contract.contr_exp
        auditlog_values_all['Prod'] = contract.prod.prod_chr
        auditlog_values_all['ExcQty'] = ''
        auditlog_values_all['WrkQty'] = ''
        auditlog_values_all['OrdQty'] = rfqc.qty
        auditlog_values_all['B/S'] = cppclient.Enum2AuxStr(rfqc.action)
        auditlog_values_all['Action'] = 'RFQ'
        auditlog_values_all['ExchOrderId'] = ''
        auditlog_values_all['OrderNo'] = 'needs implementation'
        auditlog_values_all['Status'] = 'Void'
        auditlog_values_all['Source'] = 'needs implementation'
        auditlog_values_all['SrsKey'] = contract.seriesKey
        auditlog_values_all['Exch'] = gateway.name
        auditlog_values_all['Date/Time'] = 'needs implementation'
        auditlog_values_all['RecordNo'] = 0

        # in Remaining Fields
        auditlog_values_all['OperatorID'] = get_operator_id(rfqc, exch_mgt)
        auditlog_values_all['senderSubID'] = rfqc.sub_user_id
        auditlog_values_all['CompanyIdentifier'] = 'needs implementation'
        auditlog_values_all['BrokerIdentifier'] = 'needs implementation'
        auditlog_values_all['OrderSourceAutomated'] = 'needs implementation'
        auditlog_values_all['RegionCode'] = rfqc.senderLocationData.senderRegionCode \
                            if hasattr(rfqc, 'senderLocationData') else ''
        auditlog_values_all['CountryCode'] = rfqc.senderLocationData.senderCountryCode \
                             if hasattr(rfqc, 'senderLocationData') else ''
        auditlog_values_all['Contract'] = contract.seriesName

    elif type(entity) == TTAPIOrder:
        order = entity
        contract = order.srs
        auditlog_values_all = {}
        auditlog_values_all['DisplayName'] = 'needs implementation'
        auditlog_values_all['ProdType'] = cppclient.Enum2AuxStr(contract.prod.prod_type)

        auditlog_values_all['GW Specific'] = ''
        auditlog_values_all['TxtMsg'] = ''
        auditlog_values_all['Srvr'] = gateway.orderServer.ip
        auditlog_values_all['ExchTime'] = 'needs implementation'
        auditlog_values_all['ClrMember'] = order.customer.clearing_member
        auditlog_values_all['FFT3'] = order.customer.free_text
        auditlog_values_all['FFT2'] = order.customer.exchange_sub_account
        auditlog_values_all['FFT1'] = order.customer.exchange_clearing_account
        auditlog_values_all['Account'] = order.customer.acct_type
        auditlog_values_all['Trader'] = order.trader.trader
        auditlog_values_all['Group'] = order.trader.group
        auditlog_values_all['Member'] = order.trader.member
        auditlog_values_all['User ID'] = order.user_name
        # find exchange mgt when trader is TTORD

        auditlog_values_all['ExchTrader'] = exch_mgt.trader
        auditlog_values_all['ExchGroup'] = exch_mgt.group
        auditlog_values_all['ExchMember'] = exch_mgt.member
        auditlog_values_all['OrderRes'] = order.tif
        auditlog_values_all['OrderType'] = cppclient.Enum2AuxStr(order.order_type)
        auditlog_values_all['Strike'] = contract.strike
        auditlog_values_all['StopPrc'] = order.stop_prc
        auditlog_values_all['LimitPrc'] = order.limit_prc
        auditlog_values_all['C/P'] = cppclient.Enum2AuxStr(contract.callput)
        auditlog_values_all['O/C'] = cppclient.Enum2AuxStr(order.open_close)
        auditlog_values_all['Expiry'] = contract.contr_exp
        auditlog_values_all['Prod'] = contract.prod.prod_chr
        auditlog_values_all['ExcQty'] = order.exec_qty
        auditlog_values_all['WrkQty'] = order.wrk_qty
        auditlog_values_all['OrdQty'] = order.order_qty
        auditlog_values_all['B/S'] = cppclient.Enum2AuxStr(order.buy_sell)
        auditlog_values_all['Action'] = order.order_action
        auditlog_values_all['ExchOrderId'] = order.exchange_order_id
        auditlog_values_all['OrderNo'] = order.order_no
        auditlog_values_all['Status'] = order.order_status
        auditlog_values_all['Source'] = 'needs implementation'
        auditlog_values_all['SrsKey'] = contract.seriesKey
        auditlog_values_all['Exch'] = gateway.name
        auditlog_values_all['Date/Time'] = 'needs implementation'
        auditlog_values_all['RecordNo'] = 0

        # in Remaining Fields
        auditlog_values_all['MsgOrg'] = ''  ##needs implementation
        auditlog_values_all['OperatorID'] = get_operator_id(order, exch_mgt)
        auditlog_values_all['senderSubID'] = order.sub_user_id
        auditlog_values_all['ExchangeCredential'] = order.exchange_credentials
        auditlog_values_all['OrderSourceAutomated'] = order.is_automated
        auditlog_values_all['RegionCode'] = order.senderLocationData.senderRegionCode \
                            if hasattr(order, 'senderLocationData') else ''
        auditlog_values_all['CountryCode'] = order.senderLocationData.senderCountryCode \
                             if hasattr(order, 'senderLocationData') else ''
        auditlog_values_all['Origin'] = order.origin
        auditlog_values_all['CTI'] = order.cti_code
        auditlog_values_all['Contract'] = contract.seriesName
        auditlog_values_all['MinQty'] = order.min_qty
        auditlog_values_all['OrdFlgs'] = order.order_flags
        auditlog_values_all['OrdActOrig'] = order.order_action_orig
        auditlog_values_all['OrdKey'] = order.order_key
        auditlog_values_all['OrderSourceHistory'] = order.order_source_history
        auditlog_values_all['LastOrderSrc'] = order.last_applied_order_source
        auditlog_values_all['FirstOrderSrc'] = order.first_applied_order_source
        auditlog_values_all['OrdNoOld'] = order.order_no_old
        auditlog_values_all['ExchTransNo'] = order.exch_trans_no
        auditlog_values_all['ExchOrdId'] = order.exchange_order_id
        auditlog_values_all['DisclQty'] = order.disclosed_qty
        auditlog_values_all['Sndr'] = order.sender
        auditlog_values_all['SOK'] = order.site_order_key
        auditlog_values_all['StopTrigQty'] = order.stop_trigger_qty

    else:
        raise ValueError('Unknown entity type {0}'.format(type(entity)))

    auditlog_values = {}
    for field in fields:
        auditlog_values[field] = auditlog_values_all[field]

    return auditlog_values

def overrides(suite_type_mro, order_info, suffix):
    from captain.lib import (Override, OverrideSet, OverrideSets, PriceQuantityChange,
                             ChangeAsCancelReplace)
    from commontests.utils import Small_Price_Qty_Chg_Predicate, AcctChg_Predicate
    spqc = Override(PriceQuantityChange, Small_Price_Qty_Chg_Predicate())

    suite_type_mro_names = [c.__name__ for c in suite_type_mro]
    if 'OrderManagementSuite' in suite_type_mro_names:
        return OverrideSets([SGXOverrides, [spqc]])
    else:
        return OverrideSet([Override()])

gateway.get_order_info_flags = get_order_info_flags
gateway.get_reject_order_info = get_reject_order_info
gateway.get_market_finder_config = get_market_finder_config
gateway.get_market_finder_order_info = get_market_finder_order_info
gateway.get_product_group_for_order_info = get_product_group_for_order_info
gateway.get_valid_ob_scope_combos = get_valid_ob_scope_combos
gateway.get_operator_id = get_operator_id
gateway.get_auditlog_values = get_auditlog_values
gateway.get_overrides = overrides
gateway.default_flags = gateway_flags