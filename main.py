from ga import GA, RandomDatasGA, CustomDatasGA
from os import sys
    

# 1. instantiate algorithm
ga = RandomDatasGA(
    coef_available=2,
    coef_unavailable=-2,
    max_generations=30,
    population_size=250,
    mock_individuals_size=50,
    nb_mutations=2
)

# 2. get almost feasible blocks and individuals from random generation
ga.set_datas()

# 3. run the evolution
ga.run()