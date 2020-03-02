import math
import time
from copy import copy
import pickle


handle = open("PARTITIONS","rb")
PARTITIONS, PARTITIONS_IND = pickle.load(handle)

recursion_table = {}

for m in range(1,25):
	print(m)
	for t in range(1,25):
		for total_sum in range(25):
			for strategic_players in PARTITIONS_IND[t][total_sum]:
				for T in range(1, m + total_sum + 1):
					if T == total_sum + m:
						recursion_table[tuple([m,T,strategic_players])] = 1/(m+t)
					else:
						tot = 0
						for i in range(len(strategic_players)):
							temp_sp = strategic_players[:i] + strategic_players[i+1:]
							if m + sum(temp_sp) >= T:
								if len(temp_sp) == 0:
									tot += 1/(m+t) * 1/m
								else:
									tot += 1/(m+t) * recursion_table[tuple([m,T,temp_sp])]

						if m - 1 + total_sum >= T and m > 1:
							tot += (m-1)/(m+t) * recursion_table[tuple([m-1,T,strategic_players])]

						recursion_table[tuple([m,T,strategic_players])] = tot


handle2 = open("recursion_table", "wb+")
pickle.dump(recursion_table, handle2)



