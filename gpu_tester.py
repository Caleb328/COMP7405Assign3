import numpy as np                         # numpy namespace
from timeit import default_timer as timer  # for timing
# from numbapro import vectorize

# @vectorize(['f8(f8, f8, f8, f8, f8)'], target='gpu')
def step_numpy(dt, prices, c0, c1, noises):
    return prices * np.exp(c0 * dt + c1 * noises)

def mc_numpy(paths, dt, interest, volatility):
    np.random.seed(0)
    c0 = interest - 0.5 * volatility ** 2
    c1 = volatility * np.sqrt(dt)

    for j in xrange(1, paths.shape[1]):
        prices = paths[:, j - 1]
        # gaussian noises for simulation
        noises = np.random.normal(0., 1., prices.size)
        # simulate
        paths[:, j] = step_numpy(dt, prices, c0, c1, noises)

# stock parameter
StockPrice = 100.0
StrikePrice = 100.0
Volatility = 0.3
InterestRate = 0.05
Maturity = 3.0

# monte-carlo parameter
NumPath = 3000000
NumStep = 50


def driver(pricer):
    paths = np.zeros((NumPath, NumStep), order='F')
    c0 = InterestRate - 0.5 * Volatility ** 2
    c1 = Volatility * np.sqrt(Maturity / NumStep)
    noises = np.random.normal(0., 1., paths.shape[0])
    paths[:, 0] = step_numpy(Maturity / NumStep, StockPrice, c0, c1, noises)
    DT = Maturity / NumStep
    ts = timer()
    pricer(paths, DT, InterestRate, Volatility)
    te = timer()
    elapsed = te - ts

    payoff = paths.mean(1)
    PaidOff = np.maximum(StrikePrice - payoff, 0)
    optionprice = np.mean(PaidOff) * np.exp(-InterestRate * Maturity)

    print "Option price: %.6f" % optionprice
    print "Time consumed: %.6f" % elapsed


if __name__ == '__main__':
    # paths = np.zeros((2, 9 + 2), order='F')
    # paths[:, 0] = StockPrice
    # ST = paths[:, -1]
    numpy_time = driver(mc_numpy)