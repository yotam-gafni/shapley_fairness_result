from copy import copy
import math
import time
import random
import pickle

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()



FACTORIALS = [1,1]

for i in range(2,1200):
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

max_ratio = 0
min_ratio = 7 
for random_try in range(100):
	print(random_try)
	t = random.randint(20,30)
	m = random.randint(t+1,400)
	strategic_players = []
	for i in range(t):
		strategic_players.append(random.randint(1,59))

	total_sum = sum(strategic_players)
	exp_polyA = generating_shapley(strategic_players,m)



	subpar = []
	for sp in strategic_players:
		rc = random.choice(PARTITIONS[sp])
		for spp in rc:
			subpar.append(spp)



	exp_polyB = generating_shapley(subpar,m)

	T = random.randint(1,m+total_sum)

	valA = 1 - m *gen_thresh(exp_polyA,m, t, T)
	valB = 1 - m *gen_thresh(exp_polyB,m, len(subpar), T)

	print("m={},t={},T={},valA={},valB={},A={},B={}".format(m,sum(strategic_players), T,valA,valB,strategic_players,subpar))
	ratio = valA / valB
	max_ratio = max(max_ratio, ratio)
	min_ratio = min(min_ratio, ratio)

print("Max ratio: {}".format(max_ratio))

# to get the "reverse ratio" in the article, apply 1/min_ratio
print("Min ratio: {}".format(min_ratio))




