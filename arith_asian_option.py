import numpy as np                         # numpy namespace
import versionOne
# from timeit import default_timer as timer  # for timing
# from numbapro import vectorize

# @vectorize(['f8(f8, f8, f8, f8, f8)'], target='gpu')
def browianMotion(S, dt, c1, c2, random):
    return S * np.exp(c1 * dt + c2 * random)


def arith_asian_option(S, sigma, r, T, K, step, type, path, cv):
    # np.random.seed(0)
    paths = np.zeros((path, step), order='F')
    c1 = r - 0.5 * sigma ** 2
    dt = float(T) / step
    c2 = sigma * np.sqrt(dt)

    #initialize first step result
    random = np.random.normal(0, 1, path)
    paths[:, 0] = browianMotion(S, dt, c1, c2, random)

    #simulate the remaining steps in monte carlo
    for i in range(1, step):
        s = paths[:, i - 1]
        random = np.random.normal(0, 1, path)
        paths[:, i] = browianMotion(s, dt, c1, c2, random)

    arithMean = paths.mean(1)
    logPaths = np.log(paths)
    geoMean = np.exp(1 / float(step) * logPaths.sum(1))

    if type == 'C':
        arith_payoff = np.maximum(arithMean - K, 0)
        geo_payoff = np.maximum(geoMean - K, 0)
    elif type == 'P':
        arith_payoff = np.maximum(K - arithMean, 0)
        geo_payoff = np.maximum(K - geoMean, 0)
    else:
        return 404

    #Standard Monte Carlo
    if cv == 'NULL':
        return np.mean(arith_payoff)*np.exp(-r*T)

    #Control variates
    else:
        XY = arith_payoff*geo_payoff
        covXY = np.mean(XY) - (np.mean(geo_payoff) * np.mean(arith_payoff))
        theta = covXY/np.var(geo_payoff)
        geo = versionOne.geo_asian_option(S, sigma,r, T, K, step, type)
        z = arith_payoff + theta*(geo - geo_payoff)
        return np.mean(z)

if __name__ == '__main__':
    # versionOne.arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 100000, 'null')
    # versionOne.arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 100000, 'geo_asian')
    print arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 1000000, 'NULL')
    print arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 1000000, 'CV')