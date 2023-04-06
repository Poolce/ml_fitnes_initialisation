import numpy as np
import math
from source.select.classification import classification
from collections import namedtuple
import source.select.param as param


def getRandomParamsAB(depth):
    Aj = np.random.random()*(-depth)
    m_j = min(-Aj, Aj+depth)
    Bj = np.random.uniform(-m_j, m_j)
    Aa = np.random.random()*(-depth)
    m_a = min(-Aa, Aa+depth)
    Ba = np.random.uniform(-m_a, m_a)

    lst = {'Aj', 'Bj', 'Aa', 'Ba'}
    sinParameters = namedtuple('sinParameters', lst)
    return sinParameters(Aj, Bj, Aa, Ba)


def getEightMParameters(depth, optimal_depth, sig1, sig2, sinParameters):
    M1 = sig1 * (sinParameters.Aj + depth)
    M2 = -sig2 * (sinParameters.Aj + depth + sinParameters.Bj/2)
    M3 = -2*(math.pi*sinParameters.Bj)**2
    M4 = -((sinParameters.Aj+optimal_depth)**2-(sinParameters.Bj**2)/2)
    M5 = sig1 * (sinParameters.Aa + depth)
    M6 = -sig2 * (sinParameters.Aa + depth + sinParameters.Ba/2)
    M7 = -2*(math.pi*sinParameters.Ba)**2
    M8 = -((sinParameters.Aa+optimal_depth)**2-(sinParameters.Ba**2)/2)

    lst = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
    Macroparameters = namedtuple('Macroparameters', lst)
    return Macroparameters(M1, M2, M3, M4, M5, M6, M7, M8)


def getPRSQ(alphaA, alphaJ, betaA, betaJ, gammaA, gammaJ, deltaA, deltaJ, Macroparameters):
    p = alphaJ*Macroparameters.M1 + betaJ * \
        Macroparameters.M3 + deltaJ*Macroparameters.M4
    r = alphaA*Macroparameters.M5 + betaA * \
        Macroparameters.M7 + deltaA*Macroparameters.M8
    q = gammaJ*Macroparameters.M2
    s = gammaA*Macroparameters.M6

    lst = ['P', 'R', 'S', 'Q']
    Macroparameters = namedtuple('PRSQ', lst)
    return Macroparameters(p, r, s, q)


def getFitness(PRSQ):
    Fitness = -1
    if (4*PRSQ.R*PRSQ.P+np.square(PRSQ.P+PRSQ.Q-PRSQ.S) >= 0):
        Fitness = -PRSQ.S-PRSQ.P-PRSQ.Q + \
            (np.sqrt((4*PRSQ.R*PRSQ.P+(PRSQ.P+PRSQ.Q-PRSQ.S)**2)))

    return Fitness


def Generation(depth, optDepth, alphaA, alphaJ, betaA, betaJ, gammaA, gammaJ, deltaA, deltaJ, sigma1, sigma2):
    sinParams = getRandomParamsAB(depth)
    Mparams = getEightMParameters(depth, optDepth, sigma1, sigma2, sinParams)
    prsq = getPRSQ(alphaA, alphaJ, betaA, betaJ, gammaA,
                   gammaJ, deltaA, deltaJ, Mparams)

    Fitnes = getFitness(prsq)

    lst = ['Fitnes', 'sinParameters', 'Macroparameters', 'PRSQ']
    list = namedtuple('Sel', lst)
    return list(Fitnes, sinParams, Mparams, prsq)


def SelectUsingParams():
    res = Generation(param.depth, param.optimal_depth, param.alpha_a, param.alpha_j, param.beta_a,
                     param.beta_j, param.gamma_a, param.gamma_j, param.delta_a, param.delta_j, param.sigma1, param.sigma2)
    return res


def Compair(leftSel, rightSel):
    Classification = classification(leftSel, rightSel)

    Mults = []
    for i in leftSel.Macroparameters:
        Mult = []
        for j in rightSel.Macroparameters:
            Mult.append(i*j)
        Mults.append(Mult)

    lst = ['Classification', 'Mults', 'leftSel', 'rightSel']
    list = namedtuple('CompareObj', lst)
    return list(Classification, Mults, leftSel, rightSel)
