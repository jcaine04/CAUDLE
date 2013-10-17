'''
Created on Oct 13, 2013

@author: johncaine
'''

from math import exp

class CalcStats(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def twoPtPercentage(self, twopm, twopa):
        return twopm / twopa
    
    def threePtPercentage(self, threepm, threepa):
        return threepm / threepa
    
    def astPercentage(self, ast, mp, tmmp, tmfgm, fgm):
        return ast / (((mp / (tmmp / 5.0)) * tmfgm) - fgm)
    
    def blkPercentage(self, blk, tmmp, mp, oppfga, opp3pa):
        return (blk * (tmmp/5.0)) / (mp * (oppfga - opp3pa))
    
    def drebPercentage(self, dreb, tmmp, mp, tmdreb, opporeb):
        return (dreb * (tmmp / 5.0)) / (mp * (tmdreb + opporeb))
    
    def efgPercentage(self, fgm, threepm, fga):
        return (fgm + .5 * threepm) / fga
    
    def fgPercentage(self, fgm, fga):
        return fgm / fga
    
    def ftPercentage(self, ftm, fta):
        return ftm / fta
    
    def gmsc(self, pts, fgm, fga, fta, ftm, oreb, dreb, stl, ast, blk, pf, tos):
        return pts + 0.4 * fgm - 0.7 * fga - 0.4 * (fta - ftm) + 0.7 * oreb + 0.3 * \
            dreb + stl + 0.7 * ast + 0.7 * blk - 0.4 * pf - tos
            
    def mov(self, pts, opppts): 
        return pts - opppts
    
    def orebpercentage(self, oreb, tmmp, mp, tmoreb, oppdreb):
        return (oreb * (tmmp / 5.0)) / (mp * (tmoreb + oppdreb))
    
    def pace(self, tmposs, oppposs, tmmp):
        return 40.0 * ((tmposs + oppposs) / (2.0 * (tmmp / 5)))
        
    def poss(self, tmfga, tmfta, tmoreb, oppdreb, tmfga, tmfgm, tmtos, oppfga, oppfta, opporeb, tmdreb, oppfga, oppfgm, opptos):
        return 0.5 * ((tmfga + 0.4 * tmfta - 1.07 * (tmoreb / (tmoreb + oppdreb)) * (tmfga - tmfgm) + tmtos) \
                      + (oppfga + 0.4 * oppfta - 1.07 * (opporeb / (opporeb + tmdreb)) * (oppfga - oppfgm) + opptos))
    
    def stlPercentage(self, stl, tmmp, mp, oppposs):
        return (stl * (tmmp / 5)) / (mp * oppposs)
    
    def toPercentage(self, tos, fga, fta):
        return tos / (fga + 0.44 * fta + tos)
    
    def tsPercentage(self, pts, fga, fta):
        return pts / (2.0 * (fga + 0.44 * fta))

    def usgPercentage(self, fga, fta, tos, tmmp, mp, tmfga, tmfta, tmtos):
        return ((fga + 0.44 * fta + tos) * (tmmp / 5)) / (mp * (tmfga + 0.44 * tmfta + tmtos))
        
    def wPyth(self, g, ortg, drtg):
        oweighted = exp(ortg, 10.25)
        dweighted = exp(drtg, 10.25)
        return oweighted / (oweighted + dweighted)
        
        
        