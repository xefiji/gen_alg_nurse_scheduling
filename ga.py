from random import choice, choices, randint, randrange, random
from collections import namedtuple
from functools import partial
from os import sys
from datetime import datetime
from model import Blocks, Genome, Population, Individual

class GA:
    """
    main class that holds all parameters, population and references,
    and knows how to run computation on itself
    """
    _population = None
    _individuals = {}
    _blocks = None
    _passed_individuals = []
    _best_population = None
    _best_genome = None

    def __init__(
        self, 
        coef_available=2,
        coef_unavailable=-1,
        max_generations=100,
        population_size=250,
        mock_individuals_size=500,
        nb_mutations=1
    ):
        self._coef_available = coef_unavailable
        self._coef_unavailable = coef_unavailable
        self._max_generations = max_generations
        self._population_size = population_size
        self._mock_individuals_size = mock_individuals_size
        self._nb_mutations = nb_mutations

        print('----------------------------')
        print('coef available:          {}'.format(coef_available))
        print('coef unavailable:        {}'.format(coef_unavailable))
        print('max generations:         {}'.format(max_generations))
        print('population size:         {}'.format(population_size))
        print('individual size:         {}'.format(mock_individuals_size))
        print('nb mutations:            {}'.format(nb_mutations))

    # Random population generation to init GA
    def generate_population(self, size=None):
        size = size if size is not None else self._population_size                
        population = Population(0, [])        
        
        for _ in range(size):
            # foreach dispos assign a random individual
            genome = Genome([])
            for i, _ in enumerate(self._blocks.get_dispos()):
                indiv = self.pick_random_individual()
                # assign block and individual and encode genome
                gene = '{}-{}'.format(i, indiv.get_id())                
                genome.add_gene(gene)                
                # store passed individuals    
                self._passed_individuals.append(indiv)
                        
            population.add_genome(genome)

        # ensure all individuals have been picked up at least one time ?? 
        # or maybe we will do this in the mutation part ?
        self._population = population
        self.start()

    # getter
    def get_population(self):
        return self._population

    # setter
    def set_population(self, id, generation):
        self._population = Population(id, generation)

    # counter
    def count(self):
        return len(self._population.get_genomes())

    # sorts population's genomes by score
    def sort(self):
        self._population.sort()

    # The select function selects a pair of parents for the next generation
    def select(self):        
        return choices(population=self._population.get_genomes(), weights=[genome.get_score() for genome in self._population.get_genomes()], k=2)

    # crosses between two genomes: first half of a and second half of b
    def single_point_crossover(self, a, b):        
        if a.count() != b.count():
            raise ValueError("Genomes a and b must be of same length")
        
        if a.count() < 2:
            return a, b

        # pick a random point in genome
        p = randint(1, a.count()-1)        
        genes_a = a.get_genes()[0:p] + b.get_genes()[p:]
        genes_b = b.get_genes()[0:p] + a.get_genes()[p:]
        return Genome(genes_a), Genome(genes_b)
        
    # randomly selects an individual
    def pick_random_individual(self):
        picked = None
        while picked is None:
            picked = choice(list(self._individuals.keys()))
        return self._individuals[picked]

    # makes mutation
    def mutate(self, genome, prob = 0.5):
        if genome.count() == 0:
            return genome 
        
        # nb of possible mutations is a mutable parameter
        for _ in range(self._nb_mutations):
            # add prob: 50% chance to generate a mutation
            if random() > prob:
                index = randrange(genome.count() - 1 if genome.count() > 1 else 1)        
                parts = genome.get_genes()[index].split('-')            

                # assign a random individual to this gene (planning block)
                indiv = self.pick_random_individual()            
                genome.get_genes()[index] = '{}-{}'.format(parts[0], indiv.get_id())                    
        
        return genome

    # gets random targets with their dispos
    def set_random_individuals(self, max=None):                
        max = max if max is not None else self._mock_individuals_size        
        for _ in range(max):        
            keep_going = True
            while keep_going is True:
                id = str(randint(1000, 5000))
                try:
                    _ = self._individuals[id]                
                except KeyError:                
                    keep_going = False                
                    self._individuals[id] = Individual(id, self._get_random_schedules())        

    # gets random blocks
    def set_random_blocks(self, default_date_start = '2020-11'):
        self._blocks = Blocks(self._get_random_schedules(False, default_date_start))    

    # gets random dispos
    def _get_random_schedules(self, with_status = True, default_date_start = '2020-11'):        
        s = randint(1, 28)
        e = randint(s, 30)

        dispos = []
        for i in range(s, e):             
            day = str(i)
            if i - 10 < 0:
                day = '0{}'.format(day)

            tmp = randint(0, 20)
            starth = tmp
            if starth - 10 < 0:
                starth = '0{}'.format(starth)
            startm = randint(0, 59)
            if startm - 10 < 0:
                startm = '0{}'.format(startm)
            
            endh = randint(tmp + 1 , 23)
            if endh - 10 < 0:
                endh = '0{}'.format(endh)
            endm = randint(0, 59)
            if endm - 10 < 0:
                endm = '0{}'.format(endm)

            dispo = {
                'date': '{}-{}'.format(default_date_start, day),
                'start': str('{}:{}'.format(starth, startm)),
                'end': str('{}:{}'.format(endh, endm))
            }

            if with_status is True:
                dispo['status'] = randint(0, 1)

            dispos.append(dispo)

        return dispos

    # returns final score and its avg
    def get_final_score(self):
        s = (self._best_population.get_score() / self._best_population.count())
        return self._best_population.get_score(), s

    # for each gene of each genome, runs constraint checks and score inc/decr
    def fit(self):
        value = 0
        for _, genome in enumerate(self._population.get_genomes()):
            genome_score = 0                        
            for _, gene in enumerate(genome.get_genes()):            
                parts = gene.split('-')
                try:            
                    block = self._blocks.get_dispo(int(parts[0]))                    
                    indiv = self._individuals[parts[1]]                    
                except KeyError:                               
                    continue
                
                if block is None or indiv is None:                    
                    continue
                
                # check no vals in block or indiv
                all_indiv_len = sum([len(innerlist) for innerlist in indiv.get_dispos()])
                if all_indiv_len == 0:                
                    continue

                # get same dispo block
                found_dispos = []
                for dispo in indiv.get_dispos():
                    if dispo['date'] != block['date']:            
                        continue
                    found_dispos.append(dispo)
                
                # check no date match
                if len(found_dispos) == 0:
                    continue

                # compute overlaps
                
                block_start = self.get_dt(block['date'], block['start'])
                block_end = self.get_dt(block['date'], block['end'])
                
                for dispo in found_dispos:

                    found_dispos_start = self.get_dt(dispo['date'], dispo['start'])
                    found_dispos_end = self.get_dt(dispo['date'], dispo['end'])

                    #skip if dispo finishes before block starts or starts after block finishes
                    if found_dispos_end < block_start or found_dispos_start > block_end:
                        continue

                    # set actual start and end
                    start = found_dispos_start if found_dispos_start > block_start else block_start
                    end = found_dispos_end if found_dispos_end < block_end else block_end

                    diff = (end - start).seconds / 3600
                    if dispo['status'] == 1:
                        coef = self._coef_available
                        genome_score += abs((diff * coef))
                    elif dispo['status'] == 0:
                        coef = self._coef_unavailable         
                        genome_score += (diff * coef)    

            genome.set_score(genome_score)                       
            value += genome_score
        
        self._population.set_score(value)

    # set random datas
    def set_random_datas(self):
        self.set_random_individuals()
        self.set_random_blocks()

    # wrapper for datetime gen
    def get_dt(self, date, time):
        return datetime.fromisoformat('{} {}'.format(date, time))

    # detects best population and genome and sets them as attribute
    def upgrade(self):
        best_genome = self._population.get_best_genome()
        if self._best_genome is None or self._best_genome.get_score() < best_genome.get_score():
            self._best_genome = best_genome
        if self._best_population is None or self._best_population.get_score() < self._population.get_score():
            self._best_population = self._population

    # main method
    def run(self):

        self.generate_population()

        # 1. score and sort by fitness
        self.fit()
        self.sort()        

        print('----------------------------')       
        for i in range(self._max_generations):
            # 2. checks
            # TODO: break if threshold is reached

            # 3. keep the bests 2 of this generation
            next_generation = self._population.get_genomes()[0:2]    

            # 4. cut population in half, and runs reproduction 
            # (it will double this half so that next gen is same size)
            half_pop_len = int(self.count() / 2) - 1
            for _ in range(half_pop_len):

                # 5. select parents
                parents = self.select()
            
                # 6. apply crossover between parents 
                offspring_a, offspring_b = self.single_point_crossover(parents[0], parents[1])        

                # 7. make them mutate
                offspring_a = self.mutate(offspring_a)
                offspring_b = self.mutate(offspring_b)

                # 8. make them part of the new generation
                next_generation += [offspring_a, offspring_b]

            self.set_population(i, next_generation)

            # 9. fit and sort the new gen
            self.fit()
            self.sort()
            self.upgrade()
            print(' pop {} score:           {}'.format(i, self.get_final_score()))

        self.end()

    # outputs metrics (generated datas)
    def start(self):
        print('----------------------------')       
        print('generated individuals:   {}'.format(len(self._individuals)))
        print('generated dispos:        {}'.format(len(self._blocks.get_dispos())))
        print('generated genomes:       {}'.format(self.get_population().count()))

    # outputs metrics (globals)
    def end(self):        
        print('\n----------------------------')
        print('FINAL BEST SCORE:        {}'.format(self.get_final_score()))
        the_max = max(self._population.get_genomes(), key=lambda genome: genome.get_score())
        print('max:                     {}'.format(the_max.get_score()))
        the_min = min(self._population.get_genomes(), key=lambda genome: genome.get_score())
        print('min:                     {}'.format(the_min.get_score()))
        the_sum = sum(genome.get_score() for genome in self._population.get_genomes())
        print('sum:                     {}'.format(the_sum))
        the_avg = the_sum / self._population.count()
        print('avg:                     {}'.format(the_avg))
        print('best population:         {} {}'.format(self._best_population.get_score(), self._best_population.get_id()))
        print('best genome:             {} {}'.format(self._best_genome.get_score(), self._best_genome.get_genes()))
        print('----------------------------')

    # outputs metrics (details)
    def details(self):        
        for block in self._blocks.get_dispos():
            print(block)
        print('----------------------------')

        for id in self._individuals:
            indiv = self._individuals[id]
            print('indiv {}'.format(indiv.get_id()))            
            for dispo in indiv.get_dispos():
                print(dispo)
        print('----------------------------')
                
        for gene in self._best_genome.get_genes():
            parts = gene.split('-')
            block = self._blocks.get_dispo(int(parts[0]))                    
            indiv = self._individuals[parts[1]]                 
            dispo = indiv.get_dispo(block['date'])
            if dispo is not None:
                print('{} {} {}'.format(block['date'], block['start'], block['end']))
                print('{} {} {}'.format(indiv.get_id(), dispo['start'], dispo['end']))  
            else:
                print('nothing for {} {} {}'.format(block['date'], block['start'], block['end']))
            print('----------------------------')            
