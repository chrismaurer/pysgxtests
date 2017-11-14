# Python Imports
from operator import eq, gt
#import os
import re
import datetime
import logging
from copy import deepcopy
from datetime import timedelta
#from ConfigParser import SafeConfigParser

# Pyrate Imports
from ttapi import aenums#,cppclient
from pyrate.ttapi.trader import TTAPITrader

#from pyrate.manager import Manager
from pyrate.marketfinder import MarketFinderConfigData

from captain import bind
from captain.lib import Override, PriceQuantityChange, SetOrderAttrs, TickRel
from captain.lib.controlled_types import (Messages, ProductType, ProductGroup, ContractFilter, AConfigKey,
                                          Worker, ExchangeClearingAccount, ExchangeSubAccount, FreeText, Tif,
                                          UserName, Broker, Company, OperatorID, SubUserId, FileNames)
# Captain imports
from captain.lib.strategy_definitions import Strategy
from captain.controlled import (controlled_name_type, ControlledName)
from captain.lib.strategy import StrategyLeg, strike_equal_value_minus_diff
from pyrate.ttapi.predicates import ProductComparison, ContractComparison
from ttutil import PositiveIntegerBounds, in_, not_in_

#CommonTests Imports
from commontests.utils import Small_Price_Qty_Chg_Predicate

pcq = [Override(PriceQuantityChange, Small_Price_Qty_Chg_Predicate)]

# Global Variables
log = logging.getLogger(__name__)

################
#Aconfig path
################
PFX_enabled = AConfigKey.PRICE_SERVER_PFXENABLED
NumDepthLevels = AConfigKey.MARKET_DEPTH_NUMDEPTHLEVELS
EchoCount = AConfigKey.PRICE_SERVER_PDD_ECHOCOUNT
accumulate_ltq = AConfigKey.GAL_LAST_TRADED_QUANTITY
TTQAP_enabled = AConfigKey.TTQAP_ENABLED
MarketDepth_Coalescing = AConfigKey.MARKET_DEPTH_INTERVAL_MSECS
PDD_Type = AConfigKey.PRICE_SERVER_PDD_TYPE

#########################
#bounds for MarketParams
#########################
bounds_1_1 = PositiveIntegerBounds(1,1)
bounds_1_5 = PositiveIntegerBounds(1,5)
bounds_1_10 = PositiveIntegerBounds(1,10)
bounds_1_15 = PositiveIntegerBounds(1,15)
bounds_1_20 = PositiveIntegerBounds(1,20)
bounds_1_35 = PositiveIntegerBounds(1,35)
bounds_5_7 = PositiveIntegerBounds(5,7)
bounds_5_10 = PositiveIntegerBounds(5,10)
bounds_6_10 = PositiveIntegerBounds(6,10)
bounds_20_50 = PositiveIntegerBounds(20,50)
#####################################################################################

mf_config = MarketFinderConfigData()
mf_config.timeout = 500
mf_config.depth = 20
mf_config.maxTriesPerProduct = 12
mf_config.useDefaultBestPriceFirst = True
mf_config.defaultBestPrice = 2.00
mf_config.useCache = True
mf_config.fixLotQty = True
mf_config.failPatterns = [re.compile('.*Illegal transaction at this time.*'),
                         re.compile('.*The transaction is not valid for this instrument type.*'),
                         re.compile('.*Given time validity is not allowed.*'),
                         re.compile('.*Given premium is not allowed.*'),
                          re.compile('.*The series first trading time is in the future.*'),
                          re.compile('.*The series \(or its underlying\) is stopped.*'),
                          re.compile('.*Pre-trade server could not find series.*'),
                          re.compile('.*User is not allowed to act in this instrument type.*'),
                          re.compile('.*A required limit has not been set.*')]
mf_config.acceptable_reject_messages = ['No qty filled or placed in order book; EX: omniapi_tx_ex() returned 0 with txstat 1',
                                        'EX: transaction aborted (Order-book volume was too low to fill order.)',
                                        'EX: transaction aborted (Allowed Order Quantity limit exceeded)',
                                        'EX: transaction aborted (Market orders are not allowed for this instrument)',
                                        'EX: transaction aborted (The trigger order trigger time validity is not valid.)']

mf_option_config = deepcopy(mf_config)
mf_option_config.maxTriesPerProduct = 120
mf_option_config.useDefaultBestPriceFirst = True
mf_option_config.defaultBestPrice = 5.00

mf_multi_leg_config = deepcopy(mf_config)
mf_multi_leg_config.maxTriesPerProduct = 80
mf_multi_leg_config.useDefaultBestPriceFirst = True
mf_multi_leg_config.defaultBestPrice = 1.000
mf_multi_leg_config.ignoreLegs = True

pred = ProductComparison((('prod_chr', not_in_, ['1MF', '3MF', '4CF', '5CF', 'ACF', 'CCF', 'CFF', 'CIF', 'CVF', 'FEF', 
                                                 'GOF', 'HRF', 'HVF', 'KRF', 'NJF', 'PECF', 'PESF', 'PPCF', 'PPSF', 
                                                 'PVF', 'PXF', 'RGF', 'SVF', 'VCF']),))
ProductGroup.SPECIFIC.register(pred)

ProductGroup.ENERGY.register(['EF',])

ProductGroup.FUTURE.register(['MEGF', 'SMCF'])#'NCH', 'NMD', 'NID'])#, 'SY', 'LPF'])

#ProductGroup.FSPREAD.register(['IDR', 'MYR', 'MYS', 'PHP'])

#ProductGroup.OPTION.register(['SWF', ])

futures_filter = [ProductType.FUTURE, ContractFilter.TRADABLE, ProductGroup.FUTURE]
fspread_filter = [ProductType.FSPREAD, ContractFilter.TRADABLE]#, ProductGroup.FSPREAD]
option_filter = [ProductType.OPTION, ContractFilter.TRADABLE]#, ProductGroup.OPTION]
ostrategy_filter = [ProductType.OSTRATEGY, ContractFilter.TRADABLE]
energies_filter = [ProductType.ENERGY, ContractFilter.TRADABLE, ProductGroup.ENERGY]
outrights = [ProductType.OUTRIGHT, ContractFilter.TRADABLE]
intra_prod_mleg = [ProductType.INTRA_PROD_MULTI_LEG, ContractFilter.TRADABLE]
inter_prod_mleg = [ProductType.INTER_PROD_MULTI_LEG, ContractFilter.TRADABLE]
spread_prod_type_implied_two_legged = [ProductType.FSPREAD, ContractFilter.TRADABLE]
spread_prod_type_implied_three_legged = [ProductType.OSTRATEGY, ContractFilter.TRADABLE,
                                         ContractFilter.BUTTERFLY]
futures_market_filter = [ProductType.FUTURE, ContractFilter.TRADABLE, ProductGroup.MARKET]
spreads_market_filter = [ProductType.FSPREAD, ContractFilter.TRADABLE, ProductGroup.MARKET]
options_market_filter = [ProductType.OPTION, ContractFilter.TRADABLE, ProductGroup.MARKET]
strategy_market_filter = [ProductType.OSTRATEGY, ContractFilter.TRADABLE, ProductGroup.MARKET]
sso_futures_filter = [ProductType.FUTURE, ContractFilter.TRADABLE, ProductGroup.SSO]
sso_fspread_filter = [ProductType.FSPREAD, ContractFilter.TRADABLE, ProductGroup.SSO]
sso_option_filter = [ProductType.OPTION, ContractFilter.TRADABLE, ProductGroup.SSO]
sso_strategy_filter = [ProductType.OSTRATEGY, ContractFilter.TRADABLE, ProductGroup.SSO]
strategy_filter_GTD_GTC = [ProductType.OSTRATEGY, ContractFilter.TRADABLE, ProductGroup.GTD]

#####################################################################################

#######################
## CONTROLLED NAMES  ##
#######################
ExchangeClearingAccount.NUMERIC.register('123456789012')
ExchangeClearingAccount.INVALID.register('1234567890123')

UserName.PRIMARY.register('sgx_un')
UserName.NON_PRIMARY.register('sgx_nonp_un')
OperatorID.PRIMARY.register('sgx_oid')
OperatorID.NON_PRIMARY.register('sgx_nonp_oid')
SubUserId.VALID_PRIMARY.register('sgx_suid')
ExchangeClearingAccount.VALID_PRIMARY.register('fmod_accta')
ExchangeClearingAccount.VALID_NON_PRIMARY.register('fmod_acctb')
ExchangeSubAccount.VALID_PRIMARY.register('fmod_saccta')
ExchangeSubAccount.VALID_NON_PRIMARY.register('fmod_sacctb')
FreeText.VALID_PRIMARY.register('fmod_ffta')
FreeText.VALID_NON_PRIMARY_ONE.register('fmod_fftb')

Tif.GTDATE.register(timedelta(10))
Tif.GTDATE_FAR_FUTURE.register(timedelta(20))
Tif.GTDATE_FAR_PAST.register(timedelta(-10))
tomorrow = datetime.datetime.now() + timedelta(1)
Tif.ROLLOVER.register(datetime.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day,
                                        hour=11, minute=35, second=00))

## Strategy Creation ##
call_filter = ContractComparison([('callput', eq, aenums.TT_CALL)])
put_filter = ContractComparison([('callput', eq, aenums.TT_PUT)])
option_call_preds = [ProductType.OPTION, ContractFilter.TRADABLE, call_filter]
option_put_preds = [ProductType.OPTION, ContractFilter.TRADABLE, put_filter]
Strategy.NSC_TWO_LEGS.register({'legs':[StrategyLeg(base_preds=option_call_preds,
                                                    leg_preds=None,
                                                    qty_ratio=1,
                                                    buy_sell=aenums.TT_BUY),
                                        StrategyLeg(base_preds=option_put_preds,
                                                    leg_preds=[('contr_exp', eq, 1),
                                                               ('strike', eq, 1)],
                                                    qty_ratio=1,
                                                    buy_sell=aenums.TT_SELL)],
                                'exch_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID,
                                'tt_prod_type':aenums.TT_PROD_OSTRATEGY,
                                'tt_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID})
Strategy.NSC_THREE_LEGS.register({'legs':[StrategyLeg(base_preds=option_call_preds,
                                                      leg_preds=None,
                                                      qty_ratio=1,
                                                      buy_sell=aenums.TT_BUY),
                                          StrategyLeg(base_preds=option_put_preds,
                                                      leg_preds=[('contr_exp', eq, 1),
                                                                 ('strike', eq, 1)],
                                                      qty_ratio=1,
                                                      buy_sell=aenums.TT_BUY),
                                          StrategyLeg(base_preds=option_call_preds,
                                                      leg_preds=[('contr_exp', eq, 1),
                                                                 ('strike', gt, 1)],
                                                      qty_ratio=1,
                                                      buy_sell=aenums.TT_SELL)],
                                  'exch_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID,
                                  'tt_prod_type':aenums.TT_PROD_OSTRATEGY,
                                  'tt_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID})
Strategy.NSC_FOUR_LEGS.register({'legs':[StrategyLeg(base_preds=option_put_preds,
                                                     leg_preds=None,
                                                     qty_ratio=1,
                                                     buy_sell=aenums.TT_BUY),
                                         StrategyLeg(base_preds=option_put_preds,
                                                     leg_preds=[('contr_exp', eq, 1),
                                                                ('strike', gt, 1)],
                                                     qty_ratio=1,
                                                     buy_sell=aenums.TT_SELL),
                                         StrategyLeg(base_preds=option_put_preds,
                                                     leg_preds=[('contr_exp', eq, 1),
                                                                ('strike', gt, 2)],
                                                     qty_ratio=1,
                                                     buy_sell=aenums.TT_BUY),
                                         StrategyLeg(base_preds=option_put_preds,
                                                     leg_preds=[('contr_exp', eq, 1),
                                                                ('strike', gt, 3)],
                                                     qty_ratio=1,
                                                     buy_sell=aenums.TT_SELL)],
                                 'exch_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID,
                                 'tt_prod_type':aenums.TT_PROD_OSTRATEGY,
                                 'tt_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID})
Strategy.COVERED.register({'legs':[StrategyLeg(base_preds=option_put_preds,
                                               leg_preds=None,
                                               buy_sell=aenums.TT_BUY,
                                               qty_ratio=1),
                                   StrategyLeg(base_preds=futures_filter,
                                               leg_preds=None,
                                               buy_sell=aenums.TT_SELL,
                                               qty_ratio=1)],
                           'exch_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID,
                           'tt_prod_type':aenums.TT_PROD_OSTRATEGY,
                           'tt_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID})
Strategy.COVERED_TWO_FUT_LEGS.register({'legs':[StrategyLeg(base_preds=option_call_preds,
                                                            leg_preds=None,
                                                            buy_sell=aenums.TT_BUY,
                                                            qty_ratio=1),
                                                StrategyLeg(base_preds=option_put_preds,
                                                            leg_preds=[('contr_exp', eq, 1),
                                                                       ('strike', eq, 1)],
                                                            buy_sell=aenums.TT_SELL,
                                                            qty_ratio=1),
                                                StrategyLeg(base_preds=futures_filter,
                                                            leg_preds=None,
                                                            buy_sell=aenums.TT_SELL,
                                                            qty_ratio=1),
                                                StrategyLeg(base_preds=futures_filter,
                                                            leg_preds=[('contr_exp', gt, 3), ],
                                                            qty_ratio=1,
                                                            buy_sell=aenums.TT_BUY)],
                                        'exch_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID,
                                        'tt_prod_type':aenums.TT_PROD_OSTRATEGY,
                                        'tt_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID})
Strategy.INVALID.register({'legs':[StrategyLeg(base_preds=option_call_preds,
                                               leg_preds=None,
                                               qty_ratio=2,
                                               buy_sell=aenums.TT_BUY),
                                   StrategyLeg(base_preds=option_put_preds,
                                               leg_preds=[('contr_exp', eq, 1),
                                                          ('strike', eq, 1)],
                                               qty_ratio=2,
                                               buy_sell=aenums.TT_BUY)],
                           'exch_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID,
                           'tt_prod_type':aenums.TT_PROD_OSTRATEGY,
                           'tt_strategy_code':aenums.TT_TAILOR_MADE_COMB_ID})
Messages.SERIES_CREATE_SUCCESS.register('Spread/Strategy created successfully')
Messages.SERIES_CREATE_REJECT.register('DC3, EX: transaction aborted \(Illegal ratio between the legs\.\)')
Messages.SERIES_CREATE_INVERT_REJECT.register('You made a poopy strategy!')

###################################
## ORDER BOOK SHARING SCENARIOS  ##
###################################
change_hold_reject_mods = [
                      bind(SetOrderAttrs, {'exchange_clearing_account':ExchangeClearingAccount.INVALID}),
                      bind(SetOrderAttrs, {'tif':Tif.GTD}),
                      bind( SetOrderAttrs, {'acct_type':aenums.TT_ACCT_NONE} ),
                      bind(SetOrderAttrs,{'order_qty':-9999})
                      ]

change_ob_share_mods = [bind(TickRel, 2),
               bind(TickRel, -1),
               bind(SetOrderAttrs, {'chg_qty':1}),
               bind(SetOrderAttrs, {'chg_qty':-2}),
               bind(SetOrderAttrs, {'exchange_clearing_account':ExchangeClearingAccount.NUMERIC})
              ]

hold_reject_mods= [bind(SetOrderAttrs,{'order_qty': -9999 })]

replace_ob_share_mods = [bind(TickRel, 2),
                bind(TickRel, -1),
                bind(SetOrderAttrs, {'chg_qty':1}),
                bind(SetOrderAttrs, {'chg_qty':-2}),
                bind(SetOrderAttrs, {'exchange_clearing_account':ExchangeClearingAccount.NUMERIC})
                ]

ob_share_replace_arej_mods = [bind(SetOrderAttrs, {'tif':Tif.GTD})]

replace_reject_mods= [bind(SetOrderAttrs,{'site_order_key':'111111'}),]

submit_reject_mods = [bind(SetOrderAttrs, {'tif':Tif.GTDATE_FAR_PAST})]

replace_reject_mods= [bind(SetOrderAttrs,{'site_order_key':'111111'}),]

submit_reject_mods = [bind(SetOrderAttrs, {'tif':Tif.GTDATE_FAR_PAST})]

