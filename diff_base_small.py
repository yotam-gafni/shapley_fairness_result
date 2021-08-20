import time
import pickle
import itertools

from legacy_shapley_calc import ultimate_calc_avg_shapley_sr

handle = open("PARTITIONS","rb")
PARTITIONS, PARTITIONS_IND = pickle.load(handle)

count_vals = 0
for s in range(2,12):
	max_ratio = 1
	min_ratio = 1
	histograms = {}
	count = 0
	for m in range(s,25):
		for strategic_players in PARTITIONS[m]:
			strategic_players = list(strategic_players)
			skip_this = False
			for sp in strategic_players:
				if sp < s or sp > 2*s-1:
					skip_this = True
					break
			if skip_this:
				continue
			for total_sum in range(2*s, m):
				for big_players in PARTITIONS[total_sum]:
					big_players = list(big_players)
					skip_this = False
					for bp in big_players:
						if bp < 2*s:
							skip_this = True
							break
					if skip_this:
						continue
					for T in range(1, m+total_sum + 1):
						count += 1
						if count % 1000 == 0:
							print(count)
						already_checked = {}
						vals = {}
						for val in range(s, 2*s):
							already_checked[val] = 0
							vals[val] = 0
						for i in range(len(strategic_players)):
							if already_checked[strategic_players[i]] == 0:
								vals[strategic_players[i]] = ultimate_calc_avg_shapley_sr(strategic_players[:i] + strategic_players[i+1:] + big_players + ["{}".format(strategic_players[i])],T)
							already_checked[strategic_players[i]] += 1
						sum_all = 0
						for i in range(s,2*s):
							sum_all += already_checked[i] * vals[i]
						bv = 1 - sum_all
						bp = sum(big_players) / (sum(big_players) + sum(strategic_players))
						max_ratio = max(max_ratio, bv / bp)
						min_ratio = min(min_ratio, bv / bp)
						#if bv / bp == max_ratio or bv / bp == min_ratio:
						#	print(bv / bp, max_ratio, min_ratio)
						#	print("Big players: {}, small: {}, T: {}".format(big_players, strategic_players, T))
				

	print("s={}".format(s))
	print(count)

	print("Values tested: {}".format(count_vals))
	print("Max ratio: {}".format(max_ratio))

	# to get the "reverse ratio" in the article, apply 1/min_ratio
	print("Min ratio: {}".format(min_ratio))

	print("HISTOGRAMS FOR CONJECTURE: {}".format(histograms))

