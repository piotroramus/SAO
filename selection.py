import random

from heapq import nlargest

from simulation import simulation


def evaluate(chromosome, environment):
    graph, init_nodes, ff_per_step = environment
    return simulation(graph, chromosome, init_nodes, ff_per_step)


def tournament_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """

    result = list()
    for _ in xrange(k):
        # select some random subpopulation
        subpopulation_size = random.randint(1, len(population) - 1)
        random_samples = sorted(random.sample(population, subpopulation_size))

        # get the best individual from the subpopulation
        winner = nlargest(1, random_samples, key=lambda p: evaluate(p, environment)[2])
        result.append(winner[0])

    return result


def roulette_wheel_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """

    weights = [(p, evaluate(p, environment)[2]) for p in population]
    weights_sum = sum(fitness for _, fitness in weights)

    result = list()
    for _ in xrange(k):
        pick = random.uniform(0, weights_sum)
        current = 0
        for p, fitness in weights:
            current += fitness
            if current > pick:
                result.append(p)
                break

    return result


def rank_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """
    raise NotImplementedError()
