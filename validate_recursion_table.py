import time
import pickle
import itertools

handle = open("PARTITIONS","rb")
PARTITIONS, PARTITIONS_IND = pickle.load(handle)

handle2 = open("recursion_table", "rb")
recursion_table = pickle.load(handle2)


count_pairs = 0
max_ratio = 1
min_ratio = 1
for m in range(1,25):
	for total_sum in range(1,25):
		print("m={}, total_sum={}".format(m,total_sum))
		for strategic_players in PARTITIONS[total_sum]:
			subpar = []
			for sp in strategic_players:
				subpar.append(PARTITIONS[sp])
			all_subperm_sep = [l for l in itertools.product(*subpar)]
			all_subperm = []
			for i in all_subperm_sep:
				all_subperm.append(tuple(sorted([item for sl in i for item in sl], reverse=True)))
			subsets = list(set(all_subperm))
			for subset in subsets:
				for T in range(1, m + total_sum + 1):
					valA = 1 - m * recursion_table[tuple([m,T,strategic_players])]
					valB = 1 - m * recursion_table[tuple([m,T,subset])]
					ratio = valA / valB
					max_ratio = max(max_ratio, ratio)
					min_ratio = min(min_ratio, ratio)
					count_pairs += 1

print("Pairs tested: {}".format(count_pairs))
print("Max ratio: {}".format(max_ratio))

# to get the "reverse ratio" in the article, apply 1/min_ratio
print("Min ratio: {}".format(min_ratio))
