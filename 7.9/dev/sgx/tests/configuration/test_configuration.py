import sys

from pyrate.fileutils import INIConfig

from commontests.test_configuration_template import BaseTestConfiguration
from commontests import (hostinfo_order_server_active, hostinfo_price_server_active,
                         hostinfo_order_server_down, hostinfo_price_server_down,
                         hostinfo_order_server_feed_down, hostinfo_price_server_feed_down,
                         hostinfo_order_server_initializing, hostinfo_price_server_initializing,
                         hostinfo_order_server_active_with_valid_trader,
                         hostinfo_order_server_active_with_invalid_trader,
                         hostinfo_order_server_active_order_rejected)

this_mod = sys.modules[__name__]

INI_CONFIG_NAMES = ['host_info_order_active_omnibus', 'host_info_order_active_unsupported_config',
                    'host_info_order_active_invalid_order_delete_timer', 'host_info_order_active_invalid_log_level',
                    'host_info_order_active_unsupported_api_config', 'host_info_order_active_invalid_heartbeat_interval',
                    'host_info_order_active_made_up_section', 'host_info_price_down_TTP_IP_missing',
                    'hostinfo_order_server_active_order_rejected_Member1_TTF_IP_missing',
                    'host_info_order_down_duplicate_Member', 'host_info_order_active_invalid_max_connection_attempts',
                    'host_info_order_down_duplicate_TTF_ID', 'host_info_order_down_duplicate_TTO_ID',
                    'host_info_order_down_reused_TTF_ID', 'host_info_order_down_reused_TTO_ID',
                    'host_info_order_down_duplicate_Membership', 'host_info_order_active_invalid_EnableSendRecvLog']

for name in INI_CONFIG_NAMES:
    setattr(this_mod, name, INIConfig(name))
    
host_info_order_active_omnibus.set_data('GLOBAL', 'AccountHandling', 'Omnibus')
host_info_order_active_unsupported_config.set_data('GLOBAL', 'UnsupportedConfig', '1')
host_info_order_active_invalid_order_delete_timer.set_data('GLOBAL', 'OrderDeleteTimer', '300')
host_info_order_active_invalid_log_level.set_data('GLOBAL', 'LogLevel', 'LotsAndLotsOfLogging')
host_info_order_active_unsupported_api_config.set_data('GLOBAL', 'APIConfig', 'A:\\om_api_config.cfg')
host_info_order_active_invalid_heartbeat_interval.set_data('GLOBAL', 'HeartbeatInterval', 'OnceEveryTenSeconds')
host_info_order_active_made_up_section.set_data('MADE_UP_SECTION', 'FakeParameter', 'True')
host_info_order_active_invalid_EnableSendRecvLog.set_data('MEMBER_1', 'EnableSendRecvLog', 'Will_you_enable_this_please?')
host_info_order_active_invalid_max_connection_attempts.set_data('MEMBER_1', 'MaxConnectionAttempts', 'Five')

host_info_price_down_TTP_IP_missing.set_data('TTP', 'AccessIP', '')

host_info_order_down_duplicate_Member.set_data('MEMBER_2', 'Member', 'GWSQE1')
host_info_order_down_duplicate_TTF_ID.set_data('MEMBER_2_TTF', 'UserId', 'T_TT835A17')
host_info_order_down_duplicate_TTO_ID.set_data('MEMBER_2_TTO_1', 'UserId', 'T_TT835A56')
host_info_order_down_reused_TTF_ID.set_data('MEMBER_1_TTO_1', 'UserId', 'T_TT835A17')
host_info_order_down_reused_TTO_ID.set_data('MEMBER_1_TTO_2', 'UserId', 'T_TT835A56')
host_info_order_down_duplicate_Membership.set_data('MEMBER_1', 'Member', 'GWSQE3')

hostinfo_order_server_active_order_rejected_Member1_TTF_IP_missing.set_data('MEMBER_1_TTF', 'AccessIP', '')

class TestConfiguration(BaseTestConfiguration):
    def __init__(self):
        super(TestConfiguration, self).__init__()
        self.host_info_order_active=[host_info_order_active_omnibus]
        self.host_info_order_active=[host_info_order_active_unsupported_config]
        self.host_info_order_active=[host_info_order_active_invalid_order_delete_timer]
        self.host_info_order_active=[host_info_order_active_invalid_log_level]
        self.host_info_order_active=[host_info_order_active_unsupported_api_config]
        self.host_info_order_active=[host_info_order_active_invalid_heartbeat_interval]
        self.host_info_order_active=[host_info_order_active_made_up_section]
        self.host_info_order_active=[host_info_order_active_invalid_EnableSendRecvLog]
        self.host_info_order_active=[host_info_order_active_invalid_max_connection_attempts]

        self.host_info_price_down=[host_info_price_down_TTP_IP_missing]

        self.host_info_order_down=[host_info_order_down_duplicate_Member]
        self.host_info_order_down=[host_info_order_down_duplicate_TTF_ID]
        self.host_info_order_down=[host_info_order_down_duplicate_TTO_ID]
        self.host_info_order_down=[host_info_order_down_reused_TTF_ID]
        self.host_info_order_down=[host_info_order_down_reused_TTO_ID]
        self.host_info_order_down=[host_info_order_down_duplicate_Membership]

        self.hostinfo_order_server_active_order_rejected=[hostinfo_order_server_active_order_rejected_Member1_TTF_IP_missing]

        self.excluded_scen=[hostinfo_price_server_active, hostinfo_order_server_feed_down,
                            hostinfo_price_server_feed_down, hostinfo_order_server_initializing,
                            hostinfo_price_server_initializing, hostinfo_order_server_active_with_invalid_trader,
                            hostinfo_order_server_active_with_valid_trader]
        self.timeout=180