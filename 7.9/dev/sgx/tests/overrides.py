#Python Imports
import logging
import time

# Pyrate Imports
from ttapi import aenums, cppclient
from ttapi.client import pythonify
from captain import implements, scope, interface, Action, Context, OrderContext, create_context
from captain.lib import Override, PriceQuantityChange, SetExpectedNonTradeDataFromFills,\
                        WaitForLastPricesOnTradeDataUpdateNoDuplicateCallbackCheck,\
                        WaitForOrderStatus, WaitForDirectTradeDataIgnoreOtherCallbacks,\
                        SetCurrentLastPrices
from pyrate.manager import Manager

# CommonTests Imports
from commontests import Small_Price_Qty_Chg_Predicate

log = logging.getLogger(__name__)

SPQCOverride = [Override(PriceQuantityChange, Small_Price_Qty_Chg_Predicate())]

SGXOverrides = []
SGXTradestateOverrides = []

### predicate ####
class IsSpreadChange(object):
    def __call__(self, action_type, arg_spec, test):
        if arg_spec['order_action'] == aenums.TT_ORDER_ACTION_CHANGE:
            # Trace thru the test to see if we are dealing with
            # a spread or strategy contract
            contract_types = 'TT_PROD_FSPREAD, TT_PROD_OSTRATEGY'
            for action in reversed(test.actions):
                at = type(action)
                if at.base_id == 'TickRel' and \
                  filter(lambda v: v in action.signature, contract_types):

                    return True

        return False
    def __hash__(self):
        return hash(hash_value(self.__class__.__name__).hexdigest())

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__class__.__name__

    __repr__ = __str__

    @property
    def signature(self):
        return str(self)




#//----------------------------------------#
# --- Action override for fills

#@implements(WaitForFill)
#class SGXWaitForFill(WaitForFill):
#
#    def setup(self, qty=None, fill_type=None, rel_qty=None, op='add', price=None, timeout=20):
#        super(SGXWaitForFill, self).setup(qty, fill_type, rel_qty, op, price, timeout)
#        self.leg_feeds = ('order', 'fill')
#
##Override WaitForFill with SGXWaitForFill
#SGXOverrides.add_override(WaitForFill,
#                 SGXWaitForFill,
#                 sgx_predicate)


### override ####
@implements(WaitForOrderStatus)
class WaitForReplaceStatusFromSpreadChange(WaitForOrderStatus):

    def run(self, ctx):

        if ctx.pending.limit_prc != 0:

            return WaitForOrderStatus(self.order_action, self.order_status,
                                      self.order_action_orig,
                                      timeout=self.timeout).run(ctx)

        ctx = WaitForOrderStatus(order_action=aenums.TT_ORDER_ACTION_DELETE,
                                 order_status=self.order_status,
                                 order_action_orig=aenums.TT_ORDER_ACTION_REPLACE,
                                 timeout=self.timeout).run(ctx)

        ctx = WaitForOrderStatus(order_action=aenums.TT_ORDER_ACTION_ADD,
                                 order_status=self.order_status,
                                 order_action_orig=aenums.TT_ORDER_ACTION_REPLACE,
                                 timeout=self.timeout).run(ctx)

        return ctx

### override ####
@implements(WaitForOrderStatus)
class WaitForAddStatusFromMOO(WaitForOrderStatus):

    def run(self, ctx):

        if ctx.pending.order_restrict == aenums.TT_MARKET_ON_OPEN_RES:

            return WaitForOrderStatus(self.order_action, self.order_status,
                                      self.order_action_orig,
                                      timeout=self.timeout).run(ctx)

        ctx = WaitForOrderStatus(order_action=aenums.TT_ORDER_ACTION_ADD,
                                 order_status=aenums.TT_ORDER_STATUS_REJECTED,
                                 order_action_orig=aenums.TT_ORDER_ACTION_ADD,
                                 timeout=self.timeout).run(ctx)

        return ctx

#SGXOverrides.append(Override(WaitForReplaceStatusFromSpreadChange, IsSpreadChange()))

#Predicate for Small Price Quantity Change
#pqc = Override(PriceQuantityChange,
#               Small_Price_Qty_Chg_Predicate())

@implements(SetExpectedNonTradeDataFromFills)
class OMAPISetExpectedNonTradeDataFromFills(SetExpectedNonTradeDataFromFills):
    '''
    In OMAPI, OPEN, HIGH and LOW prices are always sent from the exchange in each
    NTD update regardless of whether the values have changed. In some cases, these
    price updates are sent multiple times across multiple callbacks.
    Rather than filtering out this redundant data, Price Server passes it along
    to CoreAPI (ENH 156786: When sending Non Trade Data updates to the client,
    extract from the exchange update messages only the values that changed.).
    In order to support this behaviour, this override appends OPEN, HIGH and LOW
    prices from ctx.price_dict into ctx.price_changes. All modified override
    code below is commented with a "# for override..." comment.

    '''
    def setup(self,
              resting_side,
              accum_ltq,
              one_sec_trade_delay=True):
        """
        :param resting_side: the side of the first order sent
                             before the fill
        :type resting_side : AEnum_BuySellCodes
        :param accum_ltq: whether the last traded qty is accumulated
        :type accum_ltq: Boolean
        :param one_sec_trade_delay: if it's set to 'True,' the trade was
                                    made after one second sleep.
                                    (Only the first trade of every second
                                    puts a timestamp on the wire --PCR 172189)
        :type one_sec_trade_delay: Boolean
        """

        self.resting_side = resting_side
        self.accum_ltq = accum_ltq
        self.one_sec_trade_delay = one_sec_trade_delay

    def run(self, ctx):

        def get_last_price_value(price_id, ctx):
            if price_id in ctx.price_changes:
                return ctx.price_changes[price_id][-1]
            else:
                return ctx.price_dict[price_id]

        def update_ctx_prices(ctx, key, value):
            ctx.price_changes[key].append(value)
            ctx.price_dict[key] = value

        fill_cbk_count = 0
        for cbk in ctx.fill_callbacks['OnRealTimeFill']:
            if (cbk.fill.srs.prod.srs_exch_id == ctx.contract.prod.srs_exch_id and\
                cbk.fill.srs.seriesKey == ctx.contract.seriesKey):
                fill_cbk_count += 1

                # get new Last Traded Price and Last Traded Qty
                new_ltq = max(cbk.fill.long_qty, cbk.fill.short_qty)
                new_ltp = cbk.fill.match_prc

                # get Last Traded Price
                ltp = get_last_price_value(aenums.TT_LAST_TRD_PRC, ctx)

                # get Last Traded Qty
                ltq = get_last_price_value(aenums.TT_LAST_TRD_QTY, ctx)

                #set Last Traded Qty
                if self.accum_ltq and new_ltp == ltp:
                    update_ctx_prices(ctx, aenums.TT_LAST_TRD_QTY, (new_ltq + ltq))
                else:
                    update_ctx_prices(ctx, aenums.TT_LAST_TRD_QTY, new_ltq)

                #set Last Traded Price
                if new_ltp != ltp:
                    update_ctx_prices(ctx, aenums.TT_LAST_TRD_PRC, new_ltp)

                #get Total traded qty
                ttq = get_last_price_value(aenums.TT_TOTL_TRD_QTY, ctx)
                if ttq == cppclient.TT_INVALID_QTY:
                    ttq = 0
                #set Total traded qty
                update_ctx_prices(ctx, aenums.TT_TOTL_TRD_QTY, (ttq + new_ltq))

                # get Trade Direction
                trade_dir = get_last_price_value('TradeDirection', ctx)
                # set Trade Direction
                if ltp == cppclient.TT_INVALID_PRICE:
                    new_trade_dir = aenums.eDirectionUnknown
                else:
                    if ltp > new_ltp:
                        new_trade_dir = aenums.eDirectionDown
                    elif ltp < new_ltp:
                        new_trade_dir = aenums.eDirectionUp
                    elif ltp == new_ltp:
                        new_trade_dir = aenums.eDirectionFlat
                if new_trade_dir != trade_dir:
                    update_ctx_prices(ctx, 'TradeDirection', new_trade_dir)

                # get Trade state
                ts = get_last_price_value(aenums.TT_TRADE_STATE, ctx)
                # set Trade state
                if ts == 0:
                    new_ts = 0
                else:
                    new_ts = (aenums.TT_PRICE_STATE_ASK if self.resting_side == aenums.TT_BUY else
                               aenums.TT_PRICE_STATE_BID)
                if new_ts != ts:
                    update_ctx_prices(ctx, aenums.TT_TRADE_STATE, new_ts)

                # get high_price
                high_prc = get_last_price_value(aenums.TT_HIGH_PRC, ctx)
                # set high_price
                if (high_prc == cppclient.TT_INVALID_PRICE) or (high_prc < new_ltp):
                    ctx.price_changes[aenums.TT_HIGH_PRC].append(new_ltp)

                # get low price
                low_prc = get_last_price_value(aenums.TT_LOW_PRC, ctx)
                # set low price
                if (low_prc == cppclient.TT_INVALID_PRICE) or (low_prc > new_ltp):
                    ctx.price_changes[aenums.TT_LOW_PRC].append(new_ltp)

                # set open if it does not exist
                if aenums.TT_OPEN_PRC not in ctx.price_dict:
                    update_ctx_prices(ctx, aenums.TT_OPEN_PRC, new_ltp)

                # set exch time stamp
                # note: because the exact value of the exch time stamp
                # needs to be obtained from the messages sent from the
                # exchange, the validation of value will be done by
                # simulator tests
                if self.one_sec_trade_delay and \
                   ctx.price_session.consumer.ServerCapabilities.\
                   Get(aenums.TT_SUPPORTS_EXCHANGE_TIMESTAMPS):
                    ctx.price_changes[aenums.TT_EXCH_TIMESTAMP]
        if fill_cbk_count == 0:
            raise AssertionError('Failed to set Expected NTD because no'
                                 ' fill callback found for prod.srs_exch_id: {0};'
                                 ' sereiesKey:{1}'\
                                 .format(ctx.contract.prod.srs_exch_id,
                                         ctx.contract.seriesKey))

        ctx.price_changes[aenums.TT_NTD_SEQNO] = ['greater than 0']
        for idx, contract_ctx in enumerate(ctx.leg_contexts):
            ctx.leg_contexts[idx] = self.run(contract_ctx)

        return ctx

@implements(SetCurrentLastPrices)
class OMAPISetCurrentLastPrices(Action):
    def run(self, ctx):

        prices = ctx.price_session.getPrices(ctx.contract)
        for price_id, price_value in prices.items():
            ctx.price_dict[price_id] = price_value.value
        #GetTradeData is only needed for contracts in PFX mode
        #because TTQ is correct from getPrices and
        #contracts in TTAPI mode do not have updates for
        #TradeDirection
        prc_tbl_rec_handle = ctx.price_session.getStrike(ctx.contract)
        if ctx.price_session.consumer.IsPFX_Series(prc_tbl_rec_handle):
            # sleeping here for new EMDI behavior (we can do a wait for non-trade data update instead)
            time.sleep(10)
            if ctx.price_session.consumer.GetTradeData(ctx.contract) is not None:
                last_prices = \
                ctx.price_session.consumer.GetTradeData(ctx.contract).LastPrices()
                ctx.price_dict['TradeDirection'] = last_prices.GetLastTradeDirection()
                ctx.price_dict[aenums.TT_LAST_TRD_PRC] = last_prices.GetLastTradedPrice()
                ctx.price_dict[aenums.TT_LAST_TRD_QTY] = last_prices.GetLastTradedQty()
                ctx.price_dict[aenums.TT_TRADE_STATE] = last_prices.GetTradeState()
                ctx.price_dict[aenums.TT_TOTL_TRD_QTY] = last_prices.GetTotalTradedQty()

         #removing recursion for new EMDI behavior -- left in commented out old code per Shailesh's request
#        for idx, contract_ctx in enumerate(ctx.leg_contexts):
#            ctx.leg_contexts[idx] = self.run(contract_ctx)

        return ctx

#SGXOverrides.append(Override(OMAPISetExpectedNonTradeDataFromFills))
#SGXOverrides.append(Override(OMAPISetCurrentLastPrices))
#SGXOverrides.append(Override(WaitForAddStatusFromMOO))
SGXOverrides.append(Override(WaitForLastPricesOnTradeDataUpdateNoDuplicateCallbackCheck))
SGXOverrides.append(Override(WaitForDirectTradeDataIgnoreOtherCallbacks))
SGXTradestateOverrides.extend(SGXOverrides)
SGXTradestateOverrides.append(Override(OMAPISetExpectedNonTradeDataFromFills))
