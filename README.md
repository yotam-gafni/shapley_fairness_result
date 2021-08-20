Use python version 3.
First, use

- python generate_partitions.py

to generate the partitions enumerations that are used in both exhaustive search and large numbers random search. 

Steps to run the Exhaustive search:
- python generate_recursion_table.py
- python validate_recursion_table.py

Steps to run Large numbers random search:

You will need to have wolframclient installed to perform Mathematica operations within python. 
Then run -  
- python large_numbers_random_search.py 

Steps to run different definitions of small exhaustive search:

- python diff_base_small.py
