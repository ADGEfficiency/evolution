import cma
import numpy as np
from numpy.random import multivariate_normal


def get_best_samples(samples, fitness, num=1):
    assert samples.shape[0] == fitness.shape[0]
    best_idx = fitness.argsort()[::-1][-num:]
    return samples[best_idx], fitness[best_idx]


class SimpleSolver:
    def __init__(
            self,
            problem,
            num_parameters,
            population_size,
            initial_mean=0
    ):
        self.prob = problem
        self.num_parameters = num_parameters
        self.population_size = population_size

        if initial_mean == 'random':
            initial_mean = np.random.randint(*self.prob.lims, size=2)

        self.mean = np.full(
            num_parameters,
            initial_mean
        ).reshape(1, self.num_parameters)

        self.cov = np.identity(self.num_parameters) * self.prob.lims[1] * 0.02
        assert self.mean.shape[1] == self.cov.shape[0]

    def __repr__(self):
        return 'simple-solver'

    def ask(self):
        self.samples = multivariate_normal(
            self.mean.reshape(self.num_parameters),
            self.cov,
            size=self.population_size,
            check_valid='raise'
        )
        return self.samples

    def tell(self, samples, fitness):
        self.mean, _ = get_best_samples(
            self.samples,
            fitness,
            num=1
        )


class CMAES:
    def __init__(
        self,
        problem,
        num_parameters,
        population_size=64,
        initial_mean='random',
        sigma=0.5
    ):
        self.num_parameters = num_parameters

        if initial_mean == 'random':
            initial_mean = np.random.randint(*problem.lims, size=num_parameters)
        else:
            initial_mean = np.full(num_parameters, initial_mean)

        self.solver = cma.CMAEvolutionStrategy(
            initial_mean,
            sigma,
            {'popsize': population_size}
        )

    def __repr__(self):
        return 'pycma'

    def ask(self):
        samples = self.solver.ask()
        return np.array(samples).reshape(-1, self.num_parameters)

    def tell(self, samples, fitness):
        return self.solver.tell(samples, fitness)

    @property
    def mean(self):
        return self.solver.mean
