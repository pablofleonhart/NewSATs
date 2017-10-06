from operator import itemgetter
from random import *
import sys
import time
import resource

class GSat:
	m = 0	# variables
	n = 0	# clauses
	clauses = set()	# set of clauses
	dicClauses = {}
	attempt = []
	bestImproves = []
	unsatisfiedClauses = set()

	def __init__( self, filename ):
		file = open( filename, "r" )
		finish = False
		read = False
		
		clause = []

		while not finish:
		    line = file.readline()

		    if not line:
		        finish = True

		    else:
		        line = line.split()
		        
		        if len( line ) > 0:
		            if line[0] == 'p':
		                self.n = int( line[2] )
		                self.m = int( line[3] )
		                read = True

		            elif read:
		            	for i in xrange( len( line ) ):
		            		if line[i] == '0':
		            			self.clauses.add( tuple( clause ) )
		            			clause = []
		            		else:
		            			clause.append( line[i] )

		if len( self.clauses ) < self.m:
			self.clauses.add( tuple( clause ) )

		file.close()

		for clause in self.clauses:
			for literal in clause:
				literal = abs( int( literal ) )
				if literal not in self.dicClauses:
					self.dicClauses[literal] = set()
				self.dicClauses[literal].add( tuple( clause ) )

	def run( self, tries ):
		maxFlips = 3 * self.n 	# number of search's restarts
		maxTries = tries		# amount of time to spend looking for an assignment
		seed = time.time()
		it = 0

		for i in xrange( 3 ):
			print 'Try', i + 1
			variable = None
			seed += 10000
			# generates randomly truth assignment
			self.attempt = self.generateAttempt( self.n + 1, seed )

			for j in xrange( 2 ):
				it += 1
				if self.satisfies( variable ):
					return ( self.attempt, j, it )

				start = time.time()
				variable = self.getVariable( variable )			
				print "time", time.time() - start
				self.attempt[variable] = self.invValue( self.attempt[variable] )

		return ( 'Insatisfied' )

	def generateAttempt( self, n, s ):		
		seed( s )
		result = []
		for i in xrange( n ):
			result.append( randint( 0, 1 ) )

		return result

	def invValue( self, v ):
		if v == 0:
			return 1
		else:
			return 0

	def getVariable( self, v ):
		if v is None:
			self.bestImproves.append( -1 )
		#print self.attempt
			clausesChanged = 0
			for variable in xrange( 1, self.n + 1 ):
				clausesToEvaluate = self.dicClauses[variable]
				#print len( clausesToEvaluate )
				brokenClauses = self.countUnsatisfiedClauses( clausesToEvaluate )
				self.attempt[variable] = self.invValue( self.attempt[variable] )
				brokenClausesFlipped = self.countUnsatisfiedClauses( clausesToEvaluate )
				self.attempt[variable] = self.invValue( self.attempt[variable] )
				noBroken = brokenClauses - brokenClausesFlipped

				self.bestImproves.append( noBroken )
				#print variable, noBroken
				if noBroken >= clausesChanged:
					clausesChanged = noBroken
					bestVariable = variable

		else:
			clausesChanged = 0
			for clause in self.dicClauses[v]:
				for variable in clause:
					variable = abs( int( variable ) )
					clausesToEvaluate = self.dicClauses[variable]
					#print len( clausesToEvaluate )
					brokenClauses = self.countUnsatisfiedClauses( clausesToEvaluate )
					self.attempt[variable] = self.invValue( self.attempt[variable] )
					brokenClausesFlipped = self.countUnsatisfiedClauses( clausesToEvaluate )
					self.attempt[variable] = self.invValue( self.attempt[variable] )
					noBroken = brokenClauses - brokenClausesFlipped

					self.bestImproves[variable] = noBroken
					#print variable, noBroken
					if noBroken >= clausesChanged:
						clausesChanged = noBroken
						bestVariable = variable

		print self.bestImproves
		#print bestVariable
		return bestVariable

		'''mx = 0
		px = []
		#print vec
		#idxs, srd = zip( *sorted( enumerate( vec ), key=itemgetter( 1 ), reverse=True ) )		
		#tam = int( len( vec )*0.02 )
		#print srd[:tam], idxs[:tam]
		#change = self.reservoir_sampling( list( srd[:tam] ), list( idxs[:tam] ), 1 )
		#print self.qsort( vec )
		for i in xrange( 1, len( vec ) ):
			if vec[i] > mx:
				mx = vec[i]
				px = []
				px.append( i )
			elif vec[i] == mx:
				px.append( i )

		#print self.reservoir_sampling( px, 5 )
		if len( px ) == 1:
			return px[0]
		else:
			return choice( px )'''
		#return change[0]

	def countUnsatisfiedClauses( self, clauses ):
		count = 0
		for clause in clauses:
			if not self.isSatisfiedClause( clause ):
				count += 1

		return count

	def isSatisfiedClause( self, clause ):
		clauseValue = 0
		for variable in clause:
			ab = abs( int( variable ) )
			if int( variable ) < 0:
				value = self.invValue( self.attempt[ab] )
			else:
				value = self.attempt[ab]

			clauseValue += value

		return clauseValue > 0

	def satisfies( self, variable ):
		if variable:
			if variable in self.dicClauses:
				for clause in self.dicClauses[variable]:
					if self.isSatisfiedClause( clause ):
						if clause in self.unsatisfiedClauses:
							self.unsatisfiedClauses.remove( clause )
					else:
						if clause not in self.unsatisfiedClauses:
							self.unsatisfiedClauses.add( clause )
		else:
			self.unsatisfiedClauses.clear()
			for clause in self.clauses:
				if not self.isSatisfiedClause( clause ):
					self.unsatisfiedClauses.add( clause )

		return len( self.unsatisfiedClauses ) == 0