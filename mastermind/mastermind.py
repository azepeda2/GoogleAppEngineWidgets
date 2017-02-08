# mastermind game, command line edition

import random
def generateSecret(colors):
	secret=[]
	i=0
	while i<4:
		number= random.randint(0,len(colors)-1)
		color = colors[number]
		secret.append(color)
		i=i+1
	return secret


def computeExacts(guess,secretCopy):
	i=0
	match=0
	while (i<4):
		if (guess[i]==secretCopy[i]):
			match=match+1
			# cross out so doesn't match again
			guess[i]='x'
			secretCopy[i]='y'
		i=i+1
	return match

def computePartials(guess,secretCopy):
	i=0
	partial_matches=0
	while (i<4):
		j=0
		while (j<4):
			if (guess[i]==secretCopy[j]):
				partial_matches=partial_matches+1
				# cross out so doesn't match again
				guess[i]='x'
				secretCopy[j]='y'
			j=j+1
		i=i+1
	return partial_matches


	



