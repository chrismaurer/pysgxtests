from basis_validation.log_files.utils import *
from basis_validation import *
#from basis_validation.utils import compare
#from captain.plugins.log_file_validator import *


def sgx_fill_server_start_msg_is_logged(action, before, after, action_indices):
    search_for_log_file_messages(action, before, after, action_indices,
                                 file_name = "FillServer_{0.year}-{0.month:02}-{0.day:02}.log".format(remote_machine_time(action, before)),
                                 regex_str = ".*[10000355] \| Starting up Fill Server.*for exchange.*")

def sgx_fill_server_stop_msg_is_logged(action, before, after, action_indices):
    search_for_log_file_messages(action, before, after, action_indices,
                                 file_name = "FillServer_{0.year}-{0.month:02}-{0.day:02}.log".format(remote_machine_time(action, before)),
                                 regex_str = ".*[10000356] \| Shutting down Fill Server.*for exchange.*")
