'''
Created on Sep 2, 2013

@author: johncaine
'''
import extractstats, computestats


#insert_game_data('20121216', '20130317')
#print "Done adding data for these dates!"
gameid = '323142429'
computestats.update_all_null_possessions(extractstats.db)
