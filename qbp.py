from random import *
import copy
import sys
import time
import resource

def calc( n, mat, sol ):
	value = 0
	for i in xrange( n ):
		for j in xrange( n ):
			value += ( mat[i][j] * sol[i] * sol[j] )

	return value

def generateAttempt( n, s ):
	seed( s )
	result = []
	for i in xrange( n ):
		result.append( randint( 0, 1 ) )

	return result

def invValue( v ):
	if v == 0:
		return 1
	else:
		return 0

def getVariable( n ):
	return randint( 1, n )

def randrange_float(start, stop, step):
	return randint(0, int((stop - start) / step)) * step + start

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

param = sys.argv[1:]

filename = param[0]
f = filename.split( "/" )[1]
nfile = f.replace( ".sparse", '' )
crit = int( param[1] )

file = open( filename, 'r' )

finish = False
read = False
m = 0
n = 0

while not finish:
    line = file.readline()

    if not line:
        finish = True

    else:
        line = line.split()
        
        if len( line ) > 0:
            if len( line ) == 2:
                n = int( line[0] )
                m = int( line[1] )
                q = [[0 for x in xrange( n + 1 )] for y in xrange( n + 1 )]
                #print n, m, q
                read = True                

            elif read:
            	i = int( line[0] )
            	j = int( line[1] )
            	k = int( line[2] )

            	q[i][j] = k
            	q[j][i] = k

file.close()

pattern = "{:5s}{:14s}{:4s}{:8s}{:12s}{:10s}"
p2 = "{:<5.2f}{:14s}{:<4d}{:<8.2f}{:<12d}{:<10d}"
file = open( "q5.txt", 'a' )
file.write( pattern.format( "alg", "instance", "rep", 'time', 'iterations', 'value' ) + '\n' )
file.close()
print pattern.format( "alg", "instance", "rep", 'time', 'iterations', 'value' )
prob = float( param[2] )
rg = float( param[3] )

ti = []
iterations = []
values = []

for z in xrange( 5 ):
	s = time.time()
	solution = generateAttempt( n + 1, s )
	#solution = [1 for x in xrange( n + 1 )]
	#print solution
	bvalue = calc( n + 1, q, solution )
	start = time.time()
	ts = time.time()
	drt = 0
	it = 0

	while time.time() - start < crit:
		acp = False
		while not acp:
			p = getVariable( n )
			t = copy.deepcopy( solution )
			t[p] = invValue( t[p] )
			fitness = calc( n + 1, q, t )
			u = randrange_float( 0.0, 1.0, rg )
			if u <= prob:
				acp = True
		it += 1

		if fitness < bvalue:
			bvalue = fitness
			solution = copy.deepcopy( t )
			drt = time.time() - ts
			#print bvalue

	file = open( "q5.txt", 'a' )
	print p2.format( prob, nfile, z+1, drt, it, bvalue )
	file.write( p2.format( prob, nfile, z+1, drt, it, bvalue ) + '\n' )
	file.close()
	ti.append( drt )
	iterations.append( it )
	values.append( bvalue )

print str( prob ) + " " + nfile + " " + str( '{0:,.2f}'.format( mean( ti ) ) ), str( '{0:,.2f}'.format( pstdev( ti ) ) )
print str( prob ) + " " + nfile + " " + str( '{0:,.2f}'.format( mean( iterations ) ) ), str( '{0:,.2f}'.format( pstdev( iterations ) ) )
print str( prob ) + " " + nfile + " " + str( '{0:,.2f}'.format( mean( values ) ) ), str( '{0:,.2f}'.format( pstdev( values ) ) )

'''for z in xrange( 5 ):
	s = time.time()
	solution = generateAttempt( n + 1, s )
	#solution = [1 for x in xrange( n + 1 )]
	#print solution
	bvalue = calc( n + 1, q, solution )
	start = time.time()
	ts = time.time()
	drt = 0
	it = 0

	while time.time() - start < crit:
		cur = 100000000
		curT = []
		ii = 2**3
		for j in xrange( ii ):
			p = getVariable( n )

			t = copy.deepcopy( solution )
			#print 'p',p, t, solution
			t[p] = invValue( t[p] )
			fitness = calc( n + 1, q, t )
			#print fitness
			if fitness < cur:
				cur = fitness
				curT = copy.deepcopy( t )

		it += 1

		if cur < bvalue:
			bvalue = cur
			solution = copy.deepcopy( curT )
			drt = time.time() - ts
			#print bvalue

	file = open( "q4.txt", 'a' )
	print p2.format( "MM", nfile, z+1, drt, it, bvalue )
	file.write( p2.format( "MM", nfile, z+1, drt, it, bvalue ) + '\n' )
	file.close()'''

'''for z in xrange( 15 ):
	s = time.time()
	solution = generateAttempt( n + 1, s )
	#solution = [1 for x in xrange( n + 1 )]
	#print solution
	bvalue = calc( n + 1, q, solution )
	start = time.time()
	ts = time.time()
	drt = 0
	it = 0

	while time.time() - start < crit:
		p = getVariable( n )
		t = copy.deepcopy( solution )
		t[p] = invValue( t[p] )
		fitness = calc( n + 1, q, t )
		it += 1

		if fitness < bvalue:
			bvalue = fitness
			solution = copy.deepcopy( t )
			drt = time.time() - ts
			#print bvalue

	file = open( "q4.txt", 'a' )
	print p2.format( "PM", nfile, z+1, drt, it, bvalue )
	file.write( p2.format( "PM", nfile, z+1, drt, it, bvalue ) + '\n' )
	file.close()'''
	#print drt, bvalue