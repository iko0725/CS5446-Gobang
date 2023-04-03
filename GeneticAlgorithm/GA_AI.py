'''遗传算法'''
from GeneticAlgorithm.GA_grade import eval_individual
import copy
import random
from collections import Counter
import time

class Board:
    def __init__(self, input_board, n_in_line=5):
        assert type(n_in_line) == int, "n_in_line para should be INT!"
        self.width = len(input_board[0])
        self.height = len(input_board)
        self.board = copy.deepcopy(input_board)
        self.n_in_line = n_in_line
         # all available postions
        self.availables = [
            (i, j) for i in range(self.height) for j in range(self.width) if input_board[i][j] == 0
        ]
        self.unavailables = [
            (i, j) for i in range(self.height) for j in range(self.width) if input_board[i][j] != 0
        ]
        # print(self.availables, self.unavailables)

    def get_avail(self):
        # avialble points in the board
        x_unfree = list(set([i[0] for i in self.availables]))
        xu = min(x_unfree)
        xb = max(x_unfree) + 1
        y_unfree = list(set([i[1] for i in self.availables]))
        y_unfree.sort()
        # decide the border
        yl = min(y_unfree)
        yr = max(y_unfree) + 1
        xu -= (xu != 0)
        xb += (xb != self.height)
        yl -= (yl != 0)
        yr += (yr != self.width)
        # return available position
        avail_pos = [
            (i, j) for i in range(xu,xb) for j in range(yl,yr) if self.board[i][j] == 0
        ]
        return avail_pos

    def is_free(self, x, y):
        return self.board[x][y] == 0

    def update(self, player, move):
        """
        update the board
        """
        assert len(move) == 2, "move is invalid, length = {}".format(len(move))
        self.board[move[0]][move[1]] = player
        self.availables.remove(move)
        self.unavailables.append(move)

def mutate(origin_individual, poten_gene):
    'change on gene'
    individual = [ i for i in origin_individual]
    pos = random.randint(0,len(individual)-1)
    gene = individual[pos]
    while gene == individual[pos]:
        gene = random.sample(poten_gene,1)[0]
    individual[pos] = gene
    return individual

def crossover(origion_individual1,origion_individual2):
    'crossover the gene'
    individual1 = [i for i in origion_individual1]
    individual2 = [i for i in origion_individual2]
    assert len(individual1) == len(individual2),"Individual must have same length!"
    pos = random.randint(0, len(individual1) - 1)
    tem = individual1[pos:]
    individual1[pos:] = individual2[pos:]
    individual2[pos:] = tem
    return individual1,individual2

class Population:
    '''
    control population, natural selsection
    '''
    def __init__(self,select_function,# check_function,
                 potential_gene,DNA_length = 7,
                 mutate_rate_limit = 0.01,
                 start_number = 2000, number_limit = 3500,
                 survival_rate = 0.1):
        # individual gene
        self.DNA_base = potential_gene
        self.DNA_length = DNA_length
        # self.check_function = check_function 
        self.start_number = start_number
        self.number_limit = number_limit
        # next generation
        self.mutate_rate_limit = mutate_rate_limit # mutation rate
        # naturual selection
        self.survival_rate = survival_rate
        self.select_function =select_function
        self.best_5 = [None for _ in range(5)] # best five generations
        self.currentgeneration = self.__begin_generation()

    def __begin_generation(self):
        '''initialze the generation'''
        assert len(self.DNA_base) >= self.DNA_length, "Potential gene is not adequate!"
        generation = []
        for _ in range(self.start_number):
            DNA = random.sample(self.DNA_base,self.DNA_length)
            generation.append(DNA)
        return generation

    def select(self):
        '''筛选存活体'''
        grades = list(map(lambda x: (self.select_function(x), x), self.currentgeneration))
        self.currentgeneration = list(map(lambda xy: xy[1],
                                          sorted(grades,key= (lambda x: x[0]),reverse=True)
                                          [:int(len(self.currentgeneration)*self.survival_rate)]))

    def find_best_firsts(self,add=True):
        '''找到当前的最好的第一步,
        add：是否要记录这一步'''
        # print(Counter([i[0] for i in self.currentgeneration]).most_common(1))
        best_first = Counter([i[0] for i in self.currentgeneration]).most_common(1)[0]
        stop = best_first[1] == len(self.currentgeneration) # stop标识提前结束搜索
        if add: # 将当前最优添加在best_5尾部
            del self.best_5[0]
            self.best_5.append(best_first[0])
        return best_first[0],stop


    def generate_next(self):
        '''产生下一代'''
        mutate_number = random.randint(0,self.mutate_rate_limit
                                       * self.number_limit)
        crossover_number = self.number_limit -\
                           len(self.currentgeneration) -\
                           mutate_number
        # 交叉
        valid = 0 # 新生合格个体数目
        while valid < crossover_number:
            individual1,individual2 = random.sample(self.currentgeneration,2)
            new_DNA = crossover(individual1,individual2)
            # if self.check_function(new_DNA):
            #     valid += 1
            #     self.currentgeneration.append(new_DNA)
            valid += 2
            self.currentgeneration.append(new_DNA[0])
            self.currentgeneration.append(new_DNA[1])
        # 突变
        valid = 0
        while valid < mutate_number:
            selected = random.sample(self.currentgeneration,1)[0]
            new_DNA = mutate(selected,self.DNA_base)
            # if self.check_function(new_DNA):
            #     valid += 1
            #     self.currentgeneration.append(new_DNA)
            valid += 1
            self.currentgeneration.append(new_DNA)

class Gobang_GA:
    def __init__(self,input_board,players_in_turn,n_in_line=5,
                 time_limit = 5.0,
                 DNA_length=7,mutate_rate_limit = 0.01,
                 start_number=2000,number_limit=3500,sruvival_rate=0.1):
        # gobang rules
        self.current_board = Board(input_board)
        self.player_turn = players_in_turn
        self.n_in_line = n_in_line
        self.time_limit = time_limit
        # natural selection
        self.potential_position = self.current_board.get_avail()
        self.population = Population(self.select_function,#self.check_function,
                                     self.potential_position,DNA_length,
                                     mutate_rate_limit,start_number,number_limit,
                                     sruvival_rate)

    def select_function(self,moves,n_in_line=5):
        '''grade individual'''
        return eval_individual\
            (self.current_board.board,self.player_turn,moves,n_in_line)

    def check_function(self,individual):
        '''check individual'''
        return len(set(individual)) == len(individual)

    def get_action(self):
        begin_time = time.time()
        gene = 0
        while time.time()-begin_time < self.time_limit:
            self.population.select() #select 

            # print(gene)
            gene += 1

            best_first,stop = self.population.find_best_firsts() 
            if stop:
                return best_first
            if len(set(self.population.best_5)) == 1: # converge
                return self.population.best_5[0]
            else:
                self.population.generate_next()
        best_5 = Counter(self.population.best_5).most_common(5)
        for i in range(len(best_5)):
            if best_5[len(best_5) - i - 1][0] != None:
                return best_5[len(best_5) - i - 1][0]
            
