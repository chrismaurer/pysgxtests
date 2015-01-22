import operator

# Pyrate Imports
from ttapi import aenums, cppclient

#Commontests imports
from basis_validation.order_book.utils import *
from basis_validation.utils import compare

###########################################
# Order Action Rules
###########################################

def exchange_credentials_is_populated_non_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_non_held_orders(before),
                'after.book[sok].exchange_credentials', "''", op=operator.ne) 
