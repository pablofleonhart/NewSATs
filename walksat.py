from operator import itemgetter
from random import *
import sys
import time
import resource

class WalkSat:
	prob = 0.5
	n = 0	# variables
	m = 0	# clauses
	clauses = set()	# set of clauses
	dicClauses = {}
	attempt = []
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
		maxFlips = 3 * self.n	# number of search's restarts
		maxTries = tries		# amount of time to spend looking for an assignment
		seed = time.time()
		it = 0
		start = time.time()
		i = 0
		while time.time() - start < tries:
		#for i in xrange( maxTries ):
			i += 1
			variable = None
			#print 'Try', i, len( self.unsatisfiedClauses )
			seed += 10000
			# generates randomly truth assignment
			self.attempt = self.generateAttempt( self.n + 1, seed )

			for j in xrange( maxFlips ):
				it += 1
				if self.satisfies( variable ):
					return ( self.attempt, j, it )

				t = time.time()
				b, bestVariable = self.getVariable()
				print time.time() - t

				if b > 0 and random() < self.prob:
					randomVar = randint( 1, self.n )
					self.attempt[randomVar] = self.invValue( self.attempt[randomVar] )
					variable = randomVar
				else:
					self.attempt[bestVariable] = self.invValue( self.attempt[bestVariable] )
					variable = bestVariable

		return ( 'Insatisfied', 0, it )

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

	def getVariable( self ):
		bestVariable = None
		b = len( self.clauses ) + 1
		unsatisfiedClause = sample( self.unsatisfiedClauses, 1 )[0]

		for variable in unsatisfiedClause:
			variable = abs( int( variable ) )
			clausesToEvaluate = self.dicClauses[variable]
			brokenClauses = self.countUnsatisfiedClauses( clausesToEvaluate )
			self.attempt[variable] = self.invValue( self.attempt[variable] )
			brokenClausesFlipped = self.countUnsatisfiedClauses( clausesToEvaluate )
			self.attempt[variable] = self.invValue( self.attempt[variable] )
			broken = brokenClausesFlipped - brokenClauses

			if broken < b:
				b = broken
				bestVariable = variable

		return b, bestVariable

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