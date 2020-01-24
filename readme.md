# Evolutionary algorithms

A simple library with two evolutionary algorithms:
- `simple` - uses best mean from previous generation (single sample), constant & diagonal covariance
- `cma` - CMA-ES - wrapper around `cma.CMAEvolutionStrategy` from [pycma](https://github.com/CMA-ES/pycm://github.com/CMA-ES/pycma)

There are four 2D optimization problems taken from [DEAP Benchmarks](https://deap.readthedocs.io/en/master/api/benchmarks.html):
- `sphere`
- `schwefel`
- `h1`
- `rastrigin`

## Example

There are more figures in `./figs`.

### The rastrigin optimization problem

![](./figs/rastrigin.png)

### CMAES on rastrigin

![](./figs/rastrigin-pycma.gif)

### SimpleSolver on rastrigin

![](./figs/rastrigin-simple-solver.gif)

## Setup

Developed on Python 3.6.8.  Install dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Use

```bash
python main.py h1 cma

python main.py rastrigin simple
```

Plot 3D surfaces for all problems - saves into `./figs/*.png`

```bash
python plotting.py
```

## References

[A Visual Guide to Evolution Strategies](http://blog.otoro.net/2017/10/29/visual-evolution-strategies)

[DEAP Benchmarks](https://deap.readthedocs.io/en/master/api/benchmarks.html)

[pycma](https://github.com/CMA-ES/pycm://github.com/CMA-ES/pycma)
