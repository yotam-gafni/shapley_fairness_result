from copy import copy
import math
import time
import random
import pickle

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

''' 
For the experiments detailed in the paper, 4 instances were run, with seeds {10000,20000,30000,40000}, each generating 8000 random instances. 
'''
random.seed(20000)


FACTORIALS = [1,1]

for i in range(2,2400):
	FACTORIALS.append(FACTORIALS[-1] * i)

handle = open("PARTITIONS","rb")
PARTITIONS, PARTITIONS_IND = pickle.load(handle)


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


''' 
Given a polynomial in string form, extract the coefficients using string operations and sum according to the formula in the paper.
'''
def gen_thresh(expanded_poly, m, t, T):
	shapley_string = ""
	tot_sum = 0
	for j in range(T):
		if T == 1 and j == 0:
			coeff = int(expanded_poly[:expanded_poly.find(" ")])
			shapley_string = "N[{}* {} * {} / {}".format(coeff, FACTORIALS[j],FACTORIALS[m+t-j-1],FACTORIALS[m+t])
		elif j == 0:
			ind = expanded_poly.find("x^{} ".format(j))
			if ind == -1:
				coeff = 0
			else:
				ind2 = expanded_poly.rfind(" ", 0, ind)
				if ind2 + 1 == ind:
					coeff = 1
				else:
					coeff = int(expanded_poly[ind2+1:ind-1])
			shapley_string = "N[{} * {} * {} / {} ".format(coeff,FACTORIALS[j],FACTORIALS[m+t-j-1],FACTORIALS[m+t])
		else:
			ind = expanded_poly.find("x^{}*z^{} ".format(T-1,j))
			if ind == -1:
				coeff = 0
			else:
				ind2 = expanded_poly.rfind(" ", 0, ind)
				if ind2 + 1 == ind:
					coeff = 1
				else:
					coeff = int(expanded_poly[ind2+1:ind-1])


			shapley_string += "+ {} * {} * {} / {}".format(coeff,FACTORIALS[j],FACTORIALS[m+t-j-1],FACTORIALS[m+t])



	shapley_string += ",100]"

	# There is a very weird occurence with seed 20000 and random_try 3673 where Mathematica gives ~9.89x10^-10 but the python interface omits the exponential, only returning 9.89 and resulting in an invalid result. 
	tot_sum = float(session.evaluate(wlexpr(shapley_string)))

	return tot_sum

''' 
Given parameters for a weighted majority game, generate the polynomial that allows calculation of Shapley values for any threshold.
'''
def generating_shapley(strategic_players, m):
	t = len(strategic_players)
	poly_string = "ExportString[Expand[(1+z*x)^({}-1)".format(m)
	for sp in strategic_players:
		poly_string += "*(1+z*x^{})".format(sp)

	poly_string += "],\"Text\"]"

	expanded_poly = session.evaluate(wlexpr(poly_string))

	return expanded_poly

'''for m in range(100,1000,100):
	max_ratio = 1
	args = []
	k = 4 * int(math.sqrt(m))
	print(k)
	T = int((m + k) / 2)
	exp_polyA = generating_shapley([k],m)

	valA = 1 - m *gen_thresh(exp_polyA,m, 1, T)

	if valA/(2*k/(m+k)) > max_ratio:
		args = [k,m,T]
		max_ratio = max(max_ratio, realSlim/(2*k/(m+k)))
'''


max_ratio = 0
min_ratio = 7 
histograms = {}
histograms_corr = {}
for random_try in range(10000):
	if random_try % 1000 == 0 or random_try % 1000 == 1:
		print("Round number: {}".format(random_try))
		print("Histograms: {}".format(histograms))
		print("Max ratio: {}".format(max_ratio))
		print("Min ratio: {}".format(min_ratio))
	t = random.randint(20,30)
	m = random.randint(t+1,400)
	strategic_players = []
	for i in range(t):
		strategic_players.append(random.randint(1,59))

	total_sum = sum(strategic_players)



	subpar = []
	for sp in strategic_players:
		rc = random.choice(PARTITIONS[sp])
		for spp in rc:
			subpar.append(spp)



	T = random.randint(1,m+total_sum)

	if random_try >= 9990:
		exp_polyA = generating_shapley(strategic_players,m)
		exp_polyB = generating_shapley(subpar,m)
		valA = 1 - m *gen_thresh(exp_polyA,m, t, T)
		valB = 1 - m *gen_thresh(exp_polyB,m, len(subpar), T)
		valProp = sum(strategic_players) / (sum(strategic_players) + m)

		#print("m={},t={},T={},valA={},valB={},A={},B={}".format(m,sum(strategic_players), T,valA,valB,strategic_players,subpar))
		ratio = valA / valB
		partRatio = valB / (valA / 2)
		boundRatio = 2 * valProp / (valA /2)
		if ratio < 0:
			continue
		logForm = math.log(partRatio, boundRatio)
		max_ratio = max(max_ratio, ratio)
		min_ratio = min(min_ratio, ratio)
		rounded_ratio = int(ratio*10) / 10
		rounded_corr = int(logForm * 20) / 20 
		if rounded_ratio in histograms:
			histograms[rounded_ratio] += 1
		else:
			histograms[rounded_ratio] = 1

		if rounded_corr in histograms_corr:
			histograms_corr[rounded_corr] += 1
		else:
			histograms_corr[rounded_corr] = 1

print("Max ratio: {}".format(max_ratio))

# to get the "reverse ratio" in the article, apply 1/min_ratio
print("Min ratio: {}".format(min_ratio))


print("HISTOGRAMS FOR CONJECTURE: {}".format(histograms))
print("HISOTGRAMS FOR COROLLARY: {}".format(histogram_corr))


