import math
import numpy as np
from scipy.stats import norm
from timeit import default_timer as timer


#d1 and d2
def d_one(S, K, T, sigma, mu):
    return (math.log(S/K)+(mu+pow(sigma, 2))*T)/math.sqrt(T)*sigma


def d_two(S, K, T, sigma, mu):
    return (math.log(S/K)+(mu+pow(sigma, 2))*T)/math.sqrt(T)*sigma-math.sqrt(T)*sigma


#Geometric Asian option
#Input: S sigma r T K n type
def geo_asian_option(S, sigma, r, T, K, n, type):
    sigmaHat = sigma*math.sqrt((n+1)*(2*n+1)/(6*pow(n, 2)))
    muHat = (r-pow(sigma, 2)/2)*(n+1)/(2*n) + pow(sigmaHat, 2)/2
    d1 = d_one(S, K, T, sigmaHat, muHat)
    d2 = d_two(S, K, T, sigmaHat, muHat)
    if type=='C':
        return math.exp(-r*T)*(S*math.exp(muHat*T)*norm.cdf(d1)-K*norm.cdf(d2))
    elif type=='P':
        return math.exp(-r*T)*(-S*math.exp(muHat*T)*norm.cdf(-d1)+K*norm.cdf(-d2))
    else:
        print "Neither CALL nor PUT option"


#Geometric Asian basket
#Input S1 S2 sigma1 simga2 r T K corr type
def geo_asian_basket(S1, S2, sigma1, sigma2, r, T, K ,corr, type):
    sigma = math.sqrt(sigma1*sigma1+sigma1*sigma2*corr*2+sigma2*sigma2)/2
    mu = r-(pow(sigma1, 2)+pow(sigma2, 2))/4+pow(sigma, 2)/2
    B = math.sqrt(S1*S2)
    d1 = d_one(B, K, T, sigma, mu)
    d2 = d_two(B, K, T, sigma, mu)
    if type == 'C':
        return math.exp(-r*T)*(B*math.exp(mu*T)*norm.cdf(d1)-K*norm.cdf(d2))
    elif type == 'P':
        return math.exp(-r*T)*(-B*math.exp(mu*T)*norm.cdf(-d1)+K*norm.cdf(-d2))
    else:
        print "Neither CALL nor PUT option"


#Arithmetic Asian option
#Input: S sigma r T K n type path cv
#path: number paths for Monte Carlo simulation
#cv: type of control variate (null or geo_asian)
def arith_asian_option(S, sigma, r, T, K, n, type, path, cv):
    start = timer()
    np.random.seed(1)
    dt = T/n
    drift = math.exp((r-0.5*pow(sigma, 2))*dt)
    arith_payoff = [0.0]*path
    geo_payoff = [0.0]*path
    for i in range(0, path):
        s_path = [0.0]*n
        growth_factor = drift * math.exp(sigma*math.sqrt(dt)*np.random.standard_normal(1)[0])
        s_path[0] = S*growth_factor
        for j in range(1, n):
            growth_factor = drift * math.exp(sigma*math.sqrt(dt)*np.random.standard_normal(1)[0])
            s_path[j] = s_path[j-1]*growth_factor

        #arithmetic asian option:
        arith_mean = np.mean(s_path)
        if type == 'C':
            arith_payoff[i] = math.exp(-r*T)*max(arith_mean-K, 0)
        else:
            arith_payoff[i] = math.exp(-r*T)*max(-arith_mean+K, 0)

        #geometrick asian option
        geo_mean = math.exp(0.01*np.sum([math.log(x) for x in s_path]))
        # print geo_mean
        if type == 'C':
            geo_payoff[i] = math.exp(-r*T)*max(geo_mean-K, 0)
        else:
            geo_payoff[i] = math.exp(-r*T)*max(-geo_mean+K, 0)

    #Standard Monte Carlo:
    if cv == 'null':
        p_mean = np.mean(arith_payoff)
        p_std = np.std(arith_payoff)
        CIlow = p_mean-1.96*p_std/math.sqrt(path)
        CIhigh = p_mean+1.96*p_std/math.sqrt(path)
        print "Mean: %.5f, Std: %.5f, [%.5f, %.5f]" % (p_mean, p_std, CIlow, CIhigh)
        time_one = timer() - start
        print "Time used: %s" % time_one
    #Monte Carlo with control variates
    else:
        XY = [0.0]*path
        for i in range(0, path):
            XY[i] = arith_payoff[i]*geo_payoff[i]
        covXY = np.mean(XY) - np.mean(arith_payoff)*np.mean(geo_payoff)
        theta = covXY/np.var(geo_payoff)
        z = [0.0]*path
        for i in range(0, path):
            z[i] = arith_payoff[i] + theta*(np.mean(geo_payoff) - geo_payoff[i])
        z_mean = np.mean(z)
        z_std = np.std(z)
        CIlow = z_mean-1.96*z_std/math.sqrt(path)
        CIhigh = z_mean+1.96*z_std/math.sqrt(path)
        print "Mean: %.5f, Std: %.5f, [%.5f, %.5f]" % (z_mean, z_std, CIlow, CIhigh)
        time_two = timer() - start
        print "Time used: %s" % time_two


if __name__ == '__main__':
    print "Hello world"
    arith_asian_option(10, 0.1, 0.06, 1.0, 9, 100, 'C', 10000, 'null')
    arith_asian_option(10, 0.1, 0.06, 1.0, 9, 100, 'C', 10000, 'control_viriate')