class Genome:
    """
    this class holds genes for a genome
    """
    def __init__(self, genes = []):
        self._genes = genes
        self._score = 0

    def add_gene(self, gene):        
        self._genes.append(gene)

    def get_genes(self):
        return self._genes

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score

    def count(self):
        return len(self._genes)


class Population:
    """
    this class holds all genomes of a population,
    with its score
    """     
    def __init__(self, id, genomes = []):
        self._id = id
        self._genomes = genomes
        self._score = 0
        self._sorted = False

    def add_genome(self, genome):  
        self._genomes.append(genome)

    def get_genomes(self):
        return self._genomes

    def get_score(self):
        return self._score

    def get_id(self):
        return self._id

    def set_score(self, score):
        self._score = score

    def count(self):
        return len(self._genomes)

    def sort(self):
        self._genomes = sorted(self._genomes, key=lambda genome: genome.get_score(), reverse=True)
        self._sorted = True

    def get_best_genome(self):
        if False == self._sorted:
            self.sort()
        return self._genomes[0]

class Individual:
    """
    this class an individual (resource)'s availabilities,
    with its id
    """

    _id = None
    _dispos = []

    def __init__(self, id, dispos):
        self._id = id
        self._dispos = dispos

    def get_id(self):
        return self._id
    
    def get_dispos(self):
        return self._dispos

    def get_dispo(self, date):
        try:
            return [dispo for dispo in self._dispos if dispo['date'] == date][0]
        except IndexError:            
            return None


class Blocks:
    """
    this class holds date's block's availabilities,    
    """
    _dispos = []

    def __init__(self, dispos):
        self._dispos = dispos

    def get_dispos(self):
        return self._dispos 
    
    def get_dispo(self, index):
        return self._dispos[index] 
