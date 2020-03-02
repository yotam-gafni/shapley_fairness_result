import itertools
import math
from copy import copy
import time

'''
Three increasingly efficient implementations of Shapley value calculation by straight-forward runthrough on the permutations. 
Different levels of deduping and reusing of temporary values. 
For small-scale calculations that don't require a generation of the full recursion table ultimate_calc_avg_shapley_sr seems 
faster than the generating function approach.
The input is given in the form of all token sizes, where the significant player to calculate for is given last as a string. 
To convert from the paper (A,m,T) format, you can write (A + [1] * (m-1) + ["1"],T) as in the test below. 
'''


def calc_avg_shapley_sr(val_list, thresh):
	counter = 0
	running_count = 0
	for perm in itertools.permutations(val_list):
		thresh_checker = 0
		for elem in perm:
			if type(elem) == type(''):
				if thresh_checker + int(elem) >= thresh:
					counter += 1
			else:
				thresh_checker += elem
			if thresh_checker >= thresh:
				break 
	return counter / math.factorial(len(val_list))

def alternative_calc_avg_shapley_sr(val_list, thresh):
	count_prob = 0
	pools = {}
	working_str = []
	for i in set(val_list[:-1]):
		pools[i] = val_list.count(i)
	
	if int(val_list[-1]) >= thresh:
		count_prob += math.factorial(len(val_list) - 1)


	for i in set(val_list[:-1]):
		temp_pools = copy(pools)
		combis = temp_pools[i]
		temp_pools[i] -= 1
		if temp_pools[i] == 0:
			temp_pools.pop(i)
		if i < thresh:
			working_str.append([[i], temp_pools, combis])

	while working_str:
		new_working_str = []
		for sub_str in working_str:
			if sum(sub_str[0]) + int(val_list[-1]) >= thresh:
				count_prob += sub_str[2] * math.factorial(sum(sub_str[1].values()))
			for pool in sub_str[1].items():
				i = pool[0]
				temp_pools = copy(sub_str[1])
				combis = temp_pools[i]
				temp_pools[i] -= 1
				if temp_pools[i] == 0:
					temp_pools.pop(i)
				if sum(sub_str[0] + [i]) < thresh:
					new_working_str.append([copy(sub_str[0]) + [i], temp_pools, sub_str[2]*combis])
		working_str = new_working_str

	return count_prob / math.factorial(len(val_list))

def ultimate_calc_avg_shapley_sr(val_list, thresh, timeout = 10):
	s1 = time.time()
	count_prob = 0
	pools = {}
	working_str = []
	for i in set(val_list[:-1]):
		pools[i] = val_list.count(i)
	
	if int(val_list[-1]) >= thresh:
		count_prob += math.factorial(len(val_list) - 1)


	for i in set(val_list[:-1]):
		temp_pools = copy(pools)
		combis = temp_pools[i]
		temp_pools[i] -= 1
		if temp_pools[i] == 0:
			temp_pools.pop(i)
		if i < thresh:
			working_str.append([[i], temp_pools, combis])


	while working_str:

		new_working_str = []
		i = 0
		for sub_str in working_str:
			i = i + 1
			if i % 100 == 0:
				e1 = time.time()
				if e1 - s1 > timeout:
					return None

			if sum(sub_str[0]) + int(val_list[-1]) >= thresh:
				count_prob += sub_str[2] * math.factorial(sum(sub_str[1].values()))
			for pool in sub_str[1].items():
				i = pool[0]
				temp_pools = copy(sub_str[1])
				combis = temp_pools[i]
				temp_pools[i] -= 1
				if temp_pools[i] == 0:
					temp_pools.pop(i)
				if sum(sub_str[0] + [i]) < thresh:
					new_working_str.append([copy(sub_str[0]) + [i], temp_pools, sub_str[2]*combis])

		dedup_str = []
		i = 0
		for nws in new_working_str:
			i = i + 1
			if i % 100 == 0:
				e1 = time.time()
				if e1 - s1 > timeout:
					return None
			nws[0].sort()
			if nws in dedup_str:
				ind = dedup_str.index(nws)
				dedup_str[ind][2] += nws[2]
			else:
				dedup_str.append(nws)

		working_str = dedup_str

	return count_prob / math.factorial(len(val_list))


if __name__ == "__main__":
	val1 = ultimate_calc_avg_shapley_sr([2,5,7,3] + [1,1,1,1] + ["1"],13)
	val2 = alternative_calc_avg_shapley_sr([2,5,7,3] + [1,1,1,1] + ["1"],13)
	val3 = calc_avg_shapley_sr([2,5,7,3] + [1,1,1,1] + ["1"],13)
	print(val1 == val2 == val3)