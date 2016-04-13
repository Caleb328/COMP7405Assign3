import numpy as np                         # numpy namespace
import versionOne
from timeit import default_timer as timer  # for timing
# from numbapro import vectorize

# @vectorize(['f8(f8, f8, f8, f8, f8)'], target='gpu')
def browianMotion(S, dt, c1, c2, random):
    return S * np.exp(c1 * dt + c2 * random)


def arith_asian_option(S, sigma, r, T, K, step, type, path, cv):
    np.random.seed(0)
    paths = np.zeros((path, step), order='F')
    random = np.zeros((path, step), order='F')
    for i in range(0, path):
        random[i, :] = np.random.standard_normal(step)
    c1 = r - 0.5 * sigma ** 2
    dt = float(T) / step
    c2 = sigma * np.sqrt(dt)

    #initialize first step result
    # random = np.random.standard_normal(path)
    paths[:, 0] = browianMotion(S, dt, c1, c2, random[:, 0])

    #simulate the remaining steps in monte carlo
    for i in range(1, step):
        s = paths[:, i - 1]
        # random = np.random.standard_normal(path)
        paths[:, i] = browianMotion(s, dt, c1, c2, random[:, i])

    arithMean = paths.mean(1)
    logPaths = np.log(paths)
    geoMean = np.exp(1 / float(step) * logPaths.sum(1))

    if type == 'C':
        arith_payoff = np.maximum(arithMean - K, 0)*np.exp(-r*T)
        geo_payoff = np.maximum(geoMean - K, 0)*np.exp(-r*T)
    elif type == 'P':
        arith_payoff = np.maximum(K - arithMean, 0)*np.exp(-r*T)
        geo_payoff = np.maximum(K - geoMean, 0)*np.exp(-r*T)
    else:
        return 404

    #Standard Monte Carlo
    if cv == 'NULL':
        return np.mean(arith_payoff)

    #Control variates
    else:
        XY = arith_payoff*geo_payoff
        covXY = np.mean(XY) - (np.mean(geo_payoff) * np.mean(arith_payoff))
        theta = covXY/np.var(geo_payoff)
        geo = versionOne.geo_asian_option(S, sigma,r, T, K, step, type)
        # print np.mean(geo - geo_payoff)
        z = arith_payoff + theta*(geo - geo_payoff)
        return np.mean(z)

if __name__ == '__main__':
    ts = timer()
    price = arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 1000000, 'NULL')
    te = timer()
    elapsed = te - ts
    print "Option price: %.5f, Time consumed: %.5f" % (price ,elapsed)
    ts = timer()
    price = arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 1000000, 'CV')
    te = timer()
    elapsed = te - ts
    print "Option price: %.5f, Time consumed: %.5f" % (price ,elapsed)