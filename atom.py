from string import *
AtomSymbol = [ 'x','h','he','li','be','b','c','n','o','f','ne', \
     'na','mg','al','si','p','s','cl','ar','k','ca','sc','ti', \
     'v','cr','mn','fe','co','ni','cu','zn','ga','ge','as','se', \
     'br','kr','rb','sr','y','zr','nb','mo','tc','ru','rh','pd', \
     'ag','cd','in','sn','sb','te','i','xe','cs','ba','la','ce', \
     'pr','nd','pm','sm','eu','gd','tb','dy','ho','er','tm','yb', \
     'lu','hf','ta','w ','re','os','ir','pt','au','hg','tl','pb', \
     'bi','po','at','fr','rn','ra','ac','th','pa','u','np','pu', \
     'am','cm','bk','cf','es','fm','md','no','lr' ]

class Atom:
    def __init__(self, symbol, x=0.0,y=0.0,z=0.0):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.z = z
        self.setAtomNo()
        
    def setAtomNo(self):
        self.atomno = AtomSymbol.index(lower(self.symbol))

    def __str__(self):
        line = ('%s\t%16.12f\t%16.12f\t%16.12f') \
               % (self.symbol, self.x, self.y, self.z)
        return line

