import random

GENES = 'abcdefghijklmnopqrstuvwxyz'  # 基因


class Individual(object):
    '''此类代表种群中的个体'''

    def __init__(self, target, chromosome=None):
        self.target = target
        if chromosome:  # 个体染色体，也就是所猜的单词解
            self.chromosome = chromosome
        else:  # 若没有，创建一个随机的染色体
            self.chromosome = self.create_gnome()
        self.fitness = self.cal_fitness()  # 此个体的适用能力值

    @classmethod  # 修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数
    def mutated_genes(cls):
        # 基因突变，也就是从a-z中随机挑选一个字母
        global GENES
        gene = random.choice(GENES)
        return gene

    def create_gnome(self):
        # 初始化个体基因
        gnome_len = len(self.target)  # 根据目标单词长度随机构建一个字符串
        return [self.mutated_genes() for _ in range(gnome_len)]

    def mate(self, parent, mutation=0.1):
        # 进行繁衍，产生新一代
        child_chromosome = []  # 后代染色体
        p1_proba = (1 - mutation) / 2  # 取得父母基因概率是一样
        for p1, p2 in zip(self.chromosome, parent.chromosome):
            # 遍历父母每一个基因，通过一定概率随机获取父母其中一方的基因，还有0.1概率发生变异
            prob = random.random()  # 获取一个0-1的随机数
            if prob < p1_proba:  # 一半概率选择选择p1
                child_chromosome.append(p1)
            elif prob < p1_proba * 2:  # 一半概率选择选择p2
                child_chromosome.append(p2)
            else:  # 剩下1-probability概率发生基因突变
                child_chromosome.append(self.mutated_genes())
                # 创建一个新个体，并返回
        return Individual(self.target, chromosome=child_chromosome)

    def cal_fitness(self):
        # 计算适应能力值，记录正确的字符数量
        fitness = 0
        for gs, gt in zip(self.chromosome, self.target):
            if gs == gt: fitness += 1
        return fitness


class GeneticAlgorithm(object):
    '''遗传算法'''

    def __init__(self, target, population_size=100,
                 proba_elitism=10, proba_crossover=50,
                 mutation=0.1, max_generation=100):
        self.population_size = population_size  # 种群大小
        self.target = target  # 目标单词
        self.proba_elitism = proba_elitism  # 精英模式的比例
        self.proba_crossover = proba_crossover  # 交配概率
        self.mutation = mutation  # 突变概率
        self.max_generation = max_generation  # 最大进化代数，也就是循环最多次数
        self.found = False  # 初始化时没有找到最优解
        self.generation = 1  # 当前进化的世代，创世纪是1
        self.population = []  # 种群,初始化为空

    def init_population(self):
        # 初始化第一代个体
        for _ in range(self.population_size):
            self.population.append(Individual(self.target))

    def main(self):
        # 主函数
        self.init_population()  # 产生第一代个体
        # 若没有找到答案，并且没有达到最大进化代数，继续下一代演化
        while not self.found and self.generation < self.max_generation:
            # 按照适应能力排序-内置排序法
            self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
            # 一旦发现有适应值和目标长度一样，说明我们找到这个单词
            if self.population[0].fitness == len(self.target):
                self.found = True
                break
            # 记录下一代个体
            new_generation = []
            # 精英模式，选择前10%的个体进入下一代
            s = int((self.proba_elitism * self.population_size) / 100)
            new_generation.extend(self.population[:s])
            # 90%的个体是通过上一代的交配得到
            s = int(((100 - self.proba_elitism) * self.population_size) / 100)
            # 前50%有繁衍下一代的个体数量
            num_crossover = int(self.proba_crossover * self.population_size / 100)
            for _ in range(s):
                # 前50%的个体可以有繁衍权力，在这些个体中随机挑选两个
                parent1 = random.choice(self.population[:num_crossover])
                parent2 = random.choice(self.population[:num_crossover])
                child = parent1.mate(parent2, mutation=self.mutation)  # 进行繁衍
                new_generation.append(child)  # 得到新的一代个体
            self.population = new_generation  # 新一代的个体代替上一代的
            # print("第{}代\t单词: {}\t适应值: {}".format(
            #     self.generation,
            #     "".join(self.population[0].chromosome),
            #     self.population[0].fitness))
            self.generation += 1  # 记录进化的代数
        # print("第{}代\t单词: {}\t适应值: {}".format(
        #     self.generation,
        #     "".join(self.population[0].chromosome),
        #     self.population[0].fitness))

def test_population_size(target):
    for p in range(100, 1000, 100): # 种群大小，每次增加100
        generate = 0
        for _ in range(10): # 每一种种群经过10次运算
            ga = GeneticAlgorithm(target, population_size=p)
            ga.main()
            generate += ga.generation # 统计总共经过多少次进化
        print('种群数量为%d, 总进化代数为%d, 平均每次通过%.1f进化得到结果' % (p, generate, generate/10))

def test_mutation(target):
    for m in range(10, 50, 5): # 突变概率
        generate = 0
        for _ in range(10): # 每一种种群经过10次运算
            ga = GeneticAlgorithm(target, mutation=m/100)
            ga.main()
            generate += ga.generation # 统计总共经过多少次进化
        print('突变概率为%.2f, 总进化代数为%d, 平均每次通过%.1f进化得到结果' % (m/100, generate, generate/10))

def test_crossover(target):
    for n in range(10, 100, 10): # TOP n 具有繁衍权力
        generate = 0
        for _ in range(10): # 每一种种群经过10次运算
            ga = GeneticAlgorithm(target, proba_crossover=n)
            ga.main()
            generate += ga.generation # 统计总共经过多少次进化
        print('TOP%d具有繁衍权力, 总进化代数为%d, 平均每次通过%.1f进化得到结果' % (n, generate, generate/10))

if __name__ == '__main__':
    target = 'generation'
    test_population_size(target)
    test_mutation(target)
    test_crossover(target)
    generate1 = 0
    generate2 = 0
    for _ in range(10): # 每一种种群经过10次运算
        ga = GeneticAlgorithm(target)
        ga.main()
        generate1 += ga.generation
        ga = GeneticAlgorithm(target, population_size=400, proba_crossover=40, mutation=0.15)
        ga.main()
        generate2 += ga.generation
    print('默认参数：总进化代数为%d, 平均每次通过%.1f进化得到结果' % (generate1, generate1/10))
    print('调优参数：总进化代数为%d, 平均每次通过%.1f进化得到结果' % (generate2, generate2 / 10))