import argparse
import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

from solvers import run_framework


def avg(values):
    return sum(values) / float(len(values))


def _build_cfg_filepath(config, type='csv', plot_category=None):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(script_dir, 'results', config['graph_desc'])

    filebase = "{}_{}_{}_{}_{}".format(
        config['population_size'],
        config['selection'],
        config['crossover'],
        config['mutation'],
        config['graph_desc']
    )

    if type == 'csv':
        filename = "{}.csv".format(filebase)
        dir_path = os.path.join(base_dir, 'csv')
    elif type == 'plot':
        filename = "{}.png".format(filebase)
        dir_path = os.path.join(base_dir, 'plots', plot_category)
    else:
        raise ValueError('Invalid filepath type')

    if not os.path.exists(dir_path):
        print "{} does not exists. Creating one...".format(dir_path)
        os.makedirs(dir_path)

    full_path = os.path.join(dir_path, filename)
    return full_path


def get_possible_factors():
    population_sizes = [10, 20, 50]
    selection_ops = ['tournament', 'roulette', 'rank']
    crossover_ops = ['cycle', 'injection', 'multi_injection', 'pmx', 'single_pmx']
    # 'adjecent_swap' mutation does not perform very well in general, so it is skipped
    mutation_ops = ['insertion', 'inversion', 'slide', 'random_swap', 'scramble', 'single_swap']

    return population_sizes, selection_ops, crossover_ops, mutation_ops


def generate_configs(iters, ffs, graph_desc, input_file):
    population_sizes, selection_ops, crossover_ops, mutation_ops = get_possible_factors()

    # generate all possible combinations of defined operators and population size
    configs = list()
    for ps in population_sizes:
        for so in selection_ops:
            for co in crossover_ops:
                for mo in mutation_ops:
                    config = {
                        'population_size': ps,
                        'selection': so,
                        'crossover': co,
                        'mutation': mo,
                        'iters': iters,
                        'ffs': ffs,
                        'graph_desc': graph_desc,
                        'input_file': input_file,
                    }
                    configs.append(config)

    return configs


def generate_plot_profiles():
    population_sizes, selection_ops, crossover_ops, mutation_ops = get_possible_factors()

    profiles = list()
    # profiles for population_size
    for so in selection_ops:
        for co in crossover_ops:
            for mo in mutation_ops:
                profiles.append({
                    'population_size': None,
                    'selection': so,
                    'crossover': co,
                    'mutation': mo,
                })

    # profiles for selection
    for ps in population_sizes:
        for co in crossover_ops:
            for mo in mutation_ops:
                profiles.append({
                    'population_size': ps,
                    'selection': None,
                    'crossover': co,
                    'mutation': mo,
                })

    # profiles for crossover
    for ps in population_sizes:
        for so in selection_ops:
            for mo in mutation_ops:
                profiles.append({
                    'population_size': ps,
                    'selection': so,
                    'crossover': None,
                    'mutation': mo,
                })

    # profiles for mutation
    for ps in population_sizes:
        for so in selection_ops:
            for co in crossover_ops:
                profiles.append({
                    'population_size': ps,
                    'selection': so,
                    'crossover': co,
                    'mutation': None,
                })

    return profiles


def calculate_results(configs, iterations=10):
    configs_num = len(configs)
    processed_config_num = 1
    for cfg in configs:
        csv_file = _build_cfg_filepath(cfg, type='csv')

        results = dict()
        for iteration in xrange(iterations):
            print "[{}/{}][Iteration {}/{}] Calculating {}...".format(processed_config_num, configs_num, iteration + 1,
                                                                      iterations,
                                                                      csv_file)
            results[iteration] = run_framework(
                loggers='',
                population_size=cfg['population_size'],
                selection=cfg['selection'],
                crossover=cfg['crossover'],
                mutation=cfg['mutation'],
                iters=cfg['iters'],
                ffs=cfg['ffs'],
                input_file=cfg['input_file'],
            )

        iteration_results = defaultdict(list)
        for iteration in results:
            for i in results[iteration].iteration_results:
                iteration_results[i].append(results[iteration].iteration_results[i])

        with open(csv_file, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for i in iteration_results:
                writer.writerow(iteration_results[i])

        processed_config_num += 1


def draw_plots(plot_profile, configs):
    categories = list()
    for plot_label in plot_profile:
        if plot_profile[plot_label]:
            categories.append(plot_label)
    if len(categories) != 3:
        raise ValueError('Invalid plot profile - exactly one category should be left empty')

    profiled_category = [cat for cat in plot_profile.keys() if cat not in categories][0]

    # find only results matching criteria in plot_profile
    matched_results = list()
    for cfg in configs:
        matching = True
        for plot_label in categories:
            if cfg[plot_label] != plot_profile[plot_label]:
                matching = False
                break
        if matching:
            matched_results.append(cfg)

    xdata = dict()
    ydata = dict()
    plt.clf()
    for cfg in matched_results:

        plot_label = cfg[profiled_category]
        x = list()
        y = list()

        csv_file = _build_cfg_filepath(cfg, type='csv')

        with open(csv_file, 'rb') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            rows_num = 0
            for row in plots:
                rows_num += 1
                y.append(avg([float(d) for d in row]))
            x = range(1, rows_num + 1)

        xdata[plot_label] = x
        ydata[plot_label] = y

    if matched_results:
        for plot_label in xdata:
            plt.plot(xdata[plot_label], ydata[plot_label], label=plot_label)

        title = "{};{};{};{};{}".format(
            plot_profile['population_size'],
            plot_profile['selection'],
            plot_profile['crossover'],
            plot_profile['mutation'],
            matched_results[0]['graph_desc'],
        )
        plt.xlabel('Iteration')
        plt.ylabel('Saved %')
        plt.title(title)
        plt.legend()

        plot_path = _build_cfg_filepath(
            {
                'population_size': plot_profile['population_size'],
                'selection': plot_profile['selection'],
                'crossover': plot_profile['crossover'],
                'mutation': plot_profile['mutation'],
                'graph_desc': matched_results[0]['graph_desc']
            },
            type='plot',
            plot_category=profiled_category)
        plt.savefig(plot_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-gi', '--giters',
                        type=int,
                        default=2000,
                        help='number of iterations performed inside genetic framework')
    parser.add_argument('-fi', '--fiters',
                        type=int,
                        default=10,
                        help='number of times to invoke genetic framework')
    parser.add_argument('-d', '--graph_desc',
                        default='80_035_2_agr',
                        help='concise graph description used to tag result files')
    parser.add_argument('-in', '--input_file',
                        default='graphs/80_035_2.rgraph',
                        help='path to file containing graph definition')
    parser.add_argument('-f', '--ffs',
                        type=int,
                        default=3,
                        help='number of firefighters assigned per step')

    args = parser.parse_args()

    fiters = args.fiters
    giters = args.giters
    graph_desc = args.graph_desc
    input_file = args.input_file
    ffs = args.ffs
    configs = generate_configs(giters, ffs, graph_desc, input_file)

    calculate_results(configs, iterations=fiters)

    plot_profiles = generate_plot_profiles()
    for i, plot_profile in enumerate(plot_profiles):
        print "Drawing plot {} out of {}".format(i, len(plot_profiles))
        draw_plots(plot_profile, configs)
