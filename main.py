import argparse
import os
from functools import partial
from multiprocessing import Pool

import imageio
import numpy as np
from cma.fitness_transformations import EvalParallel

from plotting import create_surface, plot_surface_with_points, process_image_for_gif
from problems import *
from solvers import CMAES, SimpleSolver


def evaluate_in_parallel(samples, problem, num_process=6):
    with Pool(num_process) as p:
        fitness = p.map(problem, samples)
    return np.array(fitness)


def main(prob, solvers, params):
    X, Y, obj = create_surface(prob, num=1000)

    plots = []
    for gen in range(params["num_generations"]):
        print("generation {}".format(gen))
        all_samples = np.zeros(len(solvers) * params["population_size"])

        old_mean, new_mean, all_samples = [], [], []
        for num, solver in enumerate(solvers):
            samples = solver.ask()
            fitness = evaluate_in_parallel(samples, prob)

            old_mean.append(solver.mean)
            solver.tell(samples, fitness)
            new_mean.append(solver.mean)

            all_samples.append(samples)

        all_samples = np.array(all_samples).reshape(-1, 2)
        old_mean = np.array(old_mean).reshape(-1, 2)
        new_mean = np.array(new_mean).reshape(-1, 2)

        title = repr(solver) + "\n"
        title += repr(prob) + " - generation {}".format(gen)
        title += "\n sigma {}".format(params["sigma"])

        fig = plot_surface_with_points(
            prob,
            X,
            Y,
            obj,
            samples=all_samples,
            mean=old_mean,
            best=new_mean,
            title=title,
        )

        plots.append(process_image_for_gif(fig))
        os.makedirs("./figs", exist_ok=True)
        imageio.mimsave(
            "./figs/{}-{}.gif".format(prob.name, repr(solver)), plots, fps=1
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problem")
    parser.add_argument("solver")
    args = parser.parse_args()

    problems = {
        "h1": H1,
        "schwefel": Schwefel,
        "sphere": Sphere,
        "rastrigin": Rastrigin,
    }

    solver_registry = {"simple": SimpleSolver, "cma": CMAES}

    params = {
        "population_size": 64,
        "num_solvers": 64,
        "num_generations": 16,
        "sigma": 2.0,
        "initial_mean": "random",
    }

    prob = problems[args.problem]()
    if args.solver == "cma":
        solvers = [
            CMAES(
                prob,
                population_size=params["population_size"],
                num_parameters=prob.dims,
                initial_mean=params["initial_mean"],
                sigma=params["sigma"],
            )
            for _ in range(params["num_solvers"])
        ]
    else:
        solvers = [
            SimpleSolver(
                prob,
                population_size=params["population_size"],
                num_parameters=prob.dims,
                initial_mean=params["initial_mean"],
            )
            for _ in range(params["num_solvers"])
        ]

    main(prob, solvers, params)
