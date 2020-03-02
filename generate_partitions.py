import pickle


''' 
Partitions are saved in two forms: 
PARTITIIONS - by sum of values
PARTITIONS_IND - by number of summands, and sum of values

To build the recursion table, it's important to generate values in order of the number of summands in the partitions.
For the other purposes, such as validating the recursion table or running a random large number search, it doesn't matter. 

'''
PARTITIONS = [[] for i in range(60)]
PARTITIONS_IND = [[[] for t in range(60)] for i in range(60)]


def partitions(n, m = None):
  '''
  Partition n with a maximum part size of m. Yield non-increasing
  lists in decreasing lexicographic order. The default for m is
  effectively n, so the second argument is not needed to create the
  generator unless you do want to limit part sizes.
  '''
  if m is None or m >= n: yield [n]
  for f in range(n-1 if (m is None or m >= n) else m, 0, -1):
    for p in partitions(n-f, f): yield [f] + p


for i in range(60):
	for part in partitions(i):
		PARTITIONS_IND[len(part)][i].append(tuple(part))
		PARTITIONS[i].append(tuple(part))


handle = open("PARTITIONS", "wb+")
pickle.dump([PARTITIONS,PARTITIONS_IND], handle)