TOTAL_SAMPLES = 30 * 1000


hist = []
hist.append({1.0: 7392, 0.9: 444, 0.7: 33, 0.8: 36, 0.4: 26, 0.6: 20, 0.5: 15, 1.1: 13, 0.2: 7, 0.3: 13, 0.1: 1})
hist.append({1.0: 1839, 0.9: 107, 0.8: 16, 1.1: 3, 0.6: 5, 0.7: 11, 0.3: 3, 0.5: 11, 0.4: 4, 0.2: 1})
hist.append({1.0: 2754, 0.9: 166, 0.6: 9, 0.8: 15, 0.5: 11, 0.4: 8, 1.1: 9, 0.2: 6, 0.3: 9, 0.7: 10, 0.1: 3})
hist.append({1.0: 3686, 0.9: 212, 0.6: 17, 0.5: 15, 0.7: 20, 0.3: 10, 0.8: 18, 1.1: 13, 0.1: 3, 0.4: 4, 0.2: 2})
hist.append({1.0: 899, 0.3: 3, 0.9: 79, 0.4: 3, 0.8: 3, 0.7: 6, 0.5: 4, 0.2: 1, 0.1: 1, 1.1: 1})
hist.append({1.0: 1837, 0.9: 115, 0.6: 6, 0.8: 7, 0.4: 7, 1.1: 6, 0.7: 9, 0.3: 2, 0.5: 6, 0.1: 3, 0.2: 2})
hist.append({1.0: 6396, 0.9: 423, 0.6: 24, 0.7: 35, 0.8: 39, 1.1: 26, 0.3: 17, 0.5: 11, 0.2: 10, 0.4: 15, 0.1: 4})
hist.append({1.0: 910, 0.9: 66, 0.2: 1, 0.4: 8, 0.5: 2, 0.7: 4, 0.6: 2, 0.8: 6, 1.1: 1})
hist.append({1.0: 1828, 0.9: 128, 0.4: 3, 0.6: 9, 0.5: 5, 1.1: 10, 0.8: 6, 0.7: 7, 0.3: 2, 0.1: 1, 0.2: 1})

combined = {}


for i in range(20):
	for h in hist:
		val = i/10
		if val in h and val not in combined:
			combined[val] = h[val]
		elif val in h:
			combined[val] += h[val]

# sanity check - should have 30k samples
sumall = 0
combined_frac = {}
final_str = ""
for key,item in combined.items():
	sumall+= item
	combined_frac[key] = item/TOTAL_SAMPLES
	final_str += "({},{}) ".format(key, combined_frac[key])

print("Total samples: {}, expected: {}".format(sumall, TOTAL_SAMPLES))

print("Latex input: {}".format(final_str))
