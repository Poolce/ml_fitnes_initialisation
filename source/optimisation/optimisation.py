import source.select.generation as generation
from collections import namedtuple
from scipy.optimize import minimize
import source.select.param as param


def fitnessByParameters(params):
    # optDepth - 0, alphaJ - 1, alphaA - 2, betaJ - 3, betaA - 4, gammaJ - 5, gammaA - 6, deltaJ - 7, deltaA - 8, sigma1 - 9, sigma2 -10
    # Фиксируем глубину
    depth = 140

    # Фиксируем параметры А Б
    lst = {'Aj', 'Bj', 'Aa', 'Ba'}
    sinParametersList = namedtuple('sinParameters', lst)
    sinParameters = sinParametersList._make([-20.73, -3.93, -51.10, -39.17])

    Macroparameters = generation.getEightMParameters(
        depth, params[0], params[9], params[10], sinParameters)

    PRSQ = generation.getPRSQ(
        params[2], params[1], params[4], params[3], params[6], params[5], params[8], params[7], Macroparameters)

    Fitness = generation.getFitness(PRSQ)

    return Fitness


def fitnessByParametersConstOptD(params):
    # alphaJ - 0, alphaA - 1, betaJ - 2, betaA - 3, gammaJ - 4, gammaA - 5, deltaJ - 6, deltaA - 7, sigma1 - 8, sigma2 - 9
    # Фиксируем глубину
    depth = 140
    optD = 80

    # Фиксируем параметры А Б
    lst = {'Aj', 'Bj', 'Aa', 'Ba'}
    sinParametersList = namedtuple('sinParameters', lst)
    sinParameters = sinParametersList._make([-20.73, -3.93, -51.10, -39.17])

    Macroparameters = generation.getEightMParameters(
        depth, optD, params[8], params[9], sinParameters)

    PRSQ = generation.getPRSQ(
        params[1], params[0], params[3], params[2], params[5], params[4], params[7], params[6], Macroparameters)

    Fitness = generation.getFitness(PRSQ)

    return Fitness


def optimizationFBP():
    # optDepth - 0, alphaJ - 1, alphaA - 2, betaJ - 3, betaA - 4, gammaJ - 5, gammaA - 6, deltaJ - 7, deltaA - 8, sigma1 - 9, sigma2 -10

    # Начальное значение
    # x0 = [80, 0.0016, 0.006, 0.0000007, 0.000000075,0.00008,0.004,0.000016,0.00006, 0.25,0.03]
    x0 = [0.0016, 0.006, 0.0000007, 0.000000075,
          0.00008, 0.004, 0.000016, 0.00006, 1, 1]

    res = minimize(fitnessByParametersConstOptD, x0,
                   method='SLSQP', options={'eps': 1e-20})

    print("res = ", res)


def fitnessByAB(params):
    lst = {'Aj', 'Bj', 'Aa', 'Ba'}
    sinParametersList = namedtuple('sinParameters', lst)
    sinParameters = sinParametersList._make(
        [params[0], params[1], params[2], params[3]])

    Macroparameters = generation.getEightMParameters(
        param.depth, param.optimal_depth, param.sigma1, param.sigma2, sinParameters)

    prsq = generation.getPRSQ(param.alpha_a, param.alpha_j, param.beta_a, param.beta_j,
                              param.gamma_a, param.gamma_j, param.delta_a, param.delta_j, Macroparameters)

    return generation.getFitness(prsq)


def optimizationByAB():
    x0 = [-20.73, -3.93, -51.10, -39.17]

    res = minimize(fitnessByAB, x0, method='SLSQP')

    print("res = ", res)
