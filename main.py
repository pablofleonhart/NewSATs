import os
import sys
import time
from gsat import GSat
from walksat import WalkSat

def mean( data ):
    n = len( data )
    if n < 1:
        return 0.00

    return sum( data ) / n

def _ss( data ):
    c = mean( data )
    ss = sum( ( x - c ) ** 2 for x in data )
    return ss

def pstdev( data ):
    n = len( data )
    if n < 2:
        return 0.00
    ss = _ss( data )
    pvar = ss / n
    return pvar ** 0.5

if ( len(sys.argv) != 3 ):
	print "Use:", sys.argv[0], "<sat_problem.cnf> <MaxTime(seconds)>"
	sys.exit(1)

pattern = "{:9s}{:14s}{:7s}{:7s}{:4s}{:10s}"
file = open( "gsatresults.txt", 'a' )
file.write( pattern.format( "alg", "instance", "rep", 't', 'p', 'i' ) + '\n' )
file.close()

ti = []
period = []
iteration = []
wti = []
wperiod = []
witeration = []

param = sys.argv[1:]
filename = param[0]
tries = int( param[1] )

gsat = GSat( filename )
wsat = WalkSat( filename )

for i in xrange( 1, 2 ):		
	start = time.time()
	res = gsat.run( tries )
	end = time.time()
	drt = end - start

	f = filename.split( "/" )[1]
	nfile = f.replace( ".cnf", '' )

	if res == 'Insatisfied':
		pattern = "{:9s}{:14s}{:<7d}{:<7.2f}{:<4s}{:<10s}"
		file = open( "gsatresults.txt", 'a' )
		file.write( pattern.format( "gsat", nfile, i, drt, "NA", "NA" ) + '\n' )
		file.close()
		ti.append( drt )
		period.append( 0 )
		iteration.append( res[2] )

	else:
		pattern = "{:9s}{:14s}{:<7d}{:<7.2f}{:<4d}{:<10d}"
		file = open( "gsatresults.txt", 'a' )
		file.write( pattern.format( "gsat", nfile, i, drt, res[1], res[2] ) + '\n' )
		file.close()
		ti.append( drt )
		period.append( res[1] )
		iteration.append( res[2] )

	'''start = time.time()
	res = wsat.run( tries )
	end = time.time()
	drt = end - start

	f = filename.split( "/" )[1]
	nfile = f.replace( ".cnf", '' )

	if res == 'Insatisfied':
		pattern = "{:9s}{:14s}{:<7d}{:<7.2f}{:<4s}{:<10s}"
		file = open( "walkresults.txt", 'a' )
		file.write( pattern.format( "walksat", nfile, i, drt, "NA", "NA" ) + '\n' )
		file.close()
		wti.append( drt )
		wperiod.append( 0 )
		witeration.append( res[2] )

	else:
		pattern = "{:9s}{:14s}{:<7d}{:<7.2f}{:<4d}{:<10d}"
		file = open( "walkresults.txt", 'a' )
		file.write( pattern.format( "walksat", nfile, i, drt, res[1], res[2] ) + '\n' )
		file.close()
		wti.append( drt )
		wperiod.append( res[1] )
		witeration.append( res[2] )'''

	print "gsat", i, drt

print "gsat " + nfile + " " + str( '{0:,.2f}'.format( mean( ti ) ) ), str( '{0:,.2f}'.format( pstdev( ti ) ) )
print "gsat " + nfile + " " + str( '{0:,.2f}'.format( mean( period ) ) ), str( '{0:,.2f}'.format( pstdev( period ) ) )
print "gsat " + nfile + " " + str( '{0:,.2f}'.format( mean( iteration ) ) ), str( '{0:,.2f}'.format( pstdev( iteration ) ) )
#print "walksat " + nfile + " " + str( '{0:,.2f}'.format( mean( wti ) ) ), str( '{0:,.2f}'.format( pstdev( wti ) ) )
#print "walksat " + nfile + " " + str( '{0:,.2f}'.format( mean( wperiod ) ) ), str( '{0:,.2f}'.format( pstdev( wperiod ) ) )
#print "walksat " + nfile + " " + str( '{0:,.2f}'.format( mean( witeration ) ) ), str( '{0:,.2f}'.format( pstdev( witeration ) ) )