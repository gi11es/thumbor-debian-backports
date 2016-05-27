from __future__ import absolute_import, division, print_function

from itertools import product

import numpy as np

from .core import normalize_chunks, Array
from ..base import tokenize
from ..utils import different_seeds, ignoring

def doc_wraps(func):
    """ Copy docstring from one function to another """
    def _(func2):
        func2.__doc__ = func.__doc__.replace('>>>', '>>').replace('...', '..')
        return func2
    return _


class RandomState(object):
    """
    Mersenne Twister pseudo-random number generator

    This object contains state to deterministicly generate pseudo-random
    numbers from a variety of probabilitiy distributions.  It is identical to
    ``np.random.RandomState`` except that all functions also take a ``chunks=``
    keyword argument.

    Examples
    --------

    >>> import dask.array as da
    >>> state = da.random.RandomState(1234)  # a seed
    >>> x = state.normal(10, 0.1, size=3, chunks=(2,))
    >>> x.compute()
    array([  9.95487579,  10.02999135,  10.08498441])

    See Also:
        np.random.RandomState
    """
    def __init__(self, seed=None):
        self._numpy_state = np.random.RandomState(seed)

    def seed(self, seed=None):
        self._numpy_state.seed(seed)

    def _wrap(self, func, *args, **kwargs):
        size = kwargs.pop('size')
        chunks = kwargs.pop('chunks')

        if not isinstance(size, (tuple, list)):
            size = (size,)

        chunks = normalize_chunks(chunks, size)

        # Get dtype
        kw = kwargs.copy()
        kw['size'] = (0,)
        dtype = func(np.random.RandomState(), *args, **kw).dtype

        # Build graph
        sizes = list(product(*chunks))
        seeds = different_seeds(len(sizes), self._numpy_state)
        token = tokenize(seeds, size, chunks, args, kwargs)
        name = 'da.random.{0}-{1}'.format(func.__name__, token)
        keys = product([name], *[range(len(bd)) for bd in chunks])
        vals = ((_apply_random, func.__name__, seed, size, args, kwargs)
                for seed, size in zip(seeds, sizes))
        dsk = dict(zip(keys, vals))

        return Array(dsk, name, chunks, dtype=dtype)

    @doc_wraps(np.random.RandomState.beta)
    def beta(self, a, b, size=None, chunks=None):
        return self._wrap(np.random.RandomState.beta, a, b,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.binomial)
    def binomial(self, n, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.binomial, n, p,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.chisquare)
    def chisquare(self, df, size=None, chunks=None):
        return self._wrap(np.random.RandomState.chisquare, df,
                         size=size, chunks=chunks)

    with ignoring(AttributeError):
        @doc_wraps(np.random.RandomState.choice)
        def choice(self, a, size=None, replace=True, p=None, chunks=None):
            return self._wrap(np.random.RandomState.choice, a,
                             size=size, replace=True, p=None, chunks=chunks)

    # @doc_wraps(np.random.RandomState.dirichlet)
    # def dirichlet(self, alpha, size=None, chunks=None):

    @doc_wraps(np.random.RandomState.exponential)
    def exponential(self, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.exponential, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.f)
    def f(self, dfnum, dfden, size=None, chunks=None):
        return self._wrap(np.random.RandomState.f, dfnum, dfden,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.gamma)
    def gamma(self, shape, scale=1.0, chunks=None):
        return self._wrap(np.random.RandomState.gamma, scale,
                         size=shape, chunks=chunks)

    @doc_wraps(np.random.RandomState.geometric)
    def geometric(self, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.geometric, p,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.gumbel)
    def gumbel(self, loc=0.0, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.gumbel, loc, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.hypergeometric)
    def hypergeometric(self, ngood, nbad, nsample, size=None, chunks=None):
        return self._wrap(np.random.RandomState.hypergeometric,
                         ngood, nbad, nsample,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.laplace)
    def laplace(self, loc=0.0, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.laplace, loc, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.logistic)
    def logistic(self, loc=0.0, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.logistic, loc, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.lognormal)
    def lognormal(self, mean=0.0, sigma=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.lognormal, mean, sigma,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.logseries)
    def logseries(self, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.logseries, p,
                         size=size, chunks=chunks)

    # multinomial

    @doc_wraps(np.random.RandomState.negative_binomial)
    def negative_binomial(self, n, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.negative_binomial, n, p,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.noncentral_chisquare)
    def noncentral_chisquare(self, df, nonc, size=None, chunks=None):
        return self._wrap(np.random.RandomState.noncentral_chisquare, df, nonc,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.noncentral_f)
    def noncentral_f(self, dfnum, dfden, nonc,  size=None, chunks=None):
        return self._wrap(np.random.RandomState.noncentral_f,
                         dfnum, dfden, nonc,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.normal)
    def normal(self, loc=0.0, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.normal, loc, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.pareto)
    def pareto(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.pareto, a,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.poisson)
    def poisson(self, lam=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.poisson, lam,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.power)
    def power(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.power, a,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.randint)
    def randint(self, low, high=None, size=None, chunks=None):
        return self._wrap(np.random.RandomState.randint, low, high,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.random_integers)
    def random_integers(self, low, high=None, size=None, chunks=None):
        return self._wrap(np.random.RandomState.random_integers, low, high,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.random_sample)
    def random_sample(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.random_sample,
                         size=size, chunks=chunks)

    random = random_sample

    @doc_wraps(np.random.RandomState.rayleigh)
    def rayleigh(self, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.rayleigh, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.standard_cauchy)
    def standard_cauchy(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_cauchy,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.standard_exponential)
    def standard_exponential(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_exponential,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.standard_gamma)
    def standard_gamma(self, shape, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_gamma, shape,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.standard_normal)
    def standard_normal(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_normal,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.standard_t)
    def standard_t(self, df, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_t, df,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.tomaxint)
    def tomaxint(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.tomaxint,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.triangular)
    def triangular(self, left, mode, right, size=None, chunks=None):
        return self._wrap(np.random.RandomState.triangular, left, mode, right,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.uniform)
    def uniform(self, low=0.0, high=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.uniform, low, high,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.vonmises)
    def vonmises(self, mu, kappa, size=None, chunks=None):
        return self._wrap(np.random.RandomState.vonmises, mu, kappa,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.wald)
    def wald(self, mean, scale, size=None, chunks=None):
        return self._wrap(np.random.RandomState.wald, mean, scale,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.weibull)
    def weibull(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.weibull, a,
                         size=size, chunks=chunks)

    @doc_wraps(np.random.RandomState.zipf)
    def zipf(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.zipf, a,
                         size=size, chunks=chunks)


def _apply_random(func, seed, size, args, kwargs):
    """ Apply RandomState method with seed

    >>> _apply_random('normal', 123, 3, (10, 1.0), {})
    array([  8.9143694 ,  10.99734545,  10.2829785 ])
    """
    state = np.random.RandomState(seed)
    func = getattr(state, func)
    return func(*args, size=size, **kwargs)


_state = RandomState()


seed = _state.seed


beta = _state.beta
binomial = _state.binomial
chisquare = _state.chisquare
exponential = _state.exponential
f = _state.f
gamma = _state.gamma
geometric = _state.geometric
gumbel = _state.gumbel
hypergeometric = _state.hypergeometric
laplace = _state.laplace
logistic = _state.logistic
lognormal = _state.lognormal
logseries = _state.logseries
negative_binomial = _state.negative_binomial
noncentral_chisquare = _state.noncentral_chisquare
noncentral_f = _state.noncentral_f
normal = _state.normal
pareto = _state.pareto
poisson = _state.poisson
power = _state.power
rayleigh = _state.rayleigh
random_sample = _state.random_sample
random = random_sample
randint = _state.randint
random_integers = _state.random_integers
triangular = _state.triangular
uniform = _state.uniform
vonmises = _state.vonmises
wald = _state.wald
weibull = _state.weibull
zipf = _state.zipf

"""
Standard distributions
"""

standard_cauchy = _state.standard_cauchy
standard_exponential = _state.standard_exponential
standard_gamma = _state.standard_gamma
standard_normal = _state.standard_normal
standard_t = _state.standard_t
