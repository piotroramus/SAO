import evaluate as ev
import draw_plots as dp


def eval_compare_all():
    return ev.generate_configs(), "results/80_035_2/", 10


def plot_compare_all():
    cd = "results/80_035_2/"

    for gb in ["mutation", "population_size", "crossover", "selection"]:
        configs = ev.generate_configs({}, group_by=gb)
        dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=cd)


def get_compare_succession_spec():
    return {
        "population_size": [10, 50, 100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["injection"],
        "succession": ["best", "rank", "best_then_random"],
        "iters": [5000],
    }


def eval_compare_succession():
    return ev.generate_configs(get_compare_succession_spec()), "results/succession_comparison_m/", 3


def plot_compare_succession():
    cd = "results/succession_comparison_m/"
    gb = "succession"
    configs = ev.generate_configs(get_compare_succession_spec(), group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=cd)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=cd)


def get_v320_spec():
    return {
        "population_size": [100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["injection"],
        "succession": ["best", "best_then_random"],
        "iters": [5000],
        "input_file": ["graphs/320_0.009_1.rgraph"],
    }


def v320_results():
    prefix = "results/320_009_1/"
    tries = 3

    return ev.generate_configs(get_v320_spec()), prefix, tries


def v320_plot():
    prefix = "results/320_009_1/"
    gb = "succession"
    configs = ev.generate_configs(get_v320_spec(), group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=prefix)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=prefix)


if __name__ == "__main__":
    ev.evaluate(*v320_results())
    v320_plot()
