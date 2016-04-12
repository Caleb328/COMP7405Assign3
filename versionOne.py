import math
import numpy as np
from scipy.stats import norm


#d1 and d2
def d_one(S, K, T, sigma, mu):
    return (math.log(S/K)+(mu+0.5*pow(sigma, 2))*T)/(math.sqrt(T)*sigma)


def d_two(S, K, T, sigma, mu):
    return (math.log(S/K)+(mu+0.5*pow(sigma, 2))*T)/(math.sqrt(T)*sigma)-math.sqrt(T)*sigma


#Geometric Asian option
#Input: S sigma r T K n type
def geo_asian_option(S, sigma, r, t, K, n, type):
    N = float(n)
    T = float(t)
    sigmaHat = sigma*math.sqrt((N+1)*(2*N+1)/(6*pow(N,2)))
    muHat = (r-0.5*pow(sigma, 2))*(N+1)/(2*N)+0.5*pow(sigmaHat, 2)

    d1 = d_one(S, K, T, sigmaHat, muHat)
    d2 = d_two(S, K, T, sigmaHat, muHat)

    if type == 'C':
        return math.exp(-r*T)*(S*math.exp(muHat*T)*norm.cdf(d1) - K*norm.cdf(d2))
    else:
        return math.exp(-r * T) * (-S * math.exp(muHat * T) * norm.cdf(-d1) + K * norm.cdf(-d2))

#Geometric basket
#Input S1 S2 sigma1 simga2 r T K corr type
def geo_basket(S1, S2, sigma1, sigma2, r, T, K ,corr, type):
    sigma = math.sqrt(sigma1*sigma1+sigma1*sigma2*corr*2+sigma2*sigma2)/2
    mu = r-(pow(sigma1, 2)+pow(sigma2, 2))/4+0.5*pow(sigma, 2)
    B = math.sqrt(S1*S2)
    d1 = d_one(B, K, T, sigma, mu)
    d2 = d_two(B, K, T, sigma, mu)
    # print "%.5f %.5f %.5f %.5f %.5f" % (B, sigma, mu, d1, d2)
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
    np.random.seed(0)
    dt = T/n
    drift = math.exp((r-0.5*sigma**2)*dt)
    arith_payoff = [0.0]*path
    geo_payoff = [0.0]*path
    for i in range(0, path):
        s_path = [0.0]*n
        growth_factor = drift * math.exp(sigma*math.sqrt(dt)*np.random.standard_normal(1)[0])
        s_path[0] = S*growth_factor
        for j in range(1, n):
            growth_factor = drift * math.exp(sigma*math.sqrt(dt)*np.random.standard_normal(1)[0])
            s_path[j] = s_path[j-1]*growth_factor

        #asian option sample payoffs:
        arith_mean = np.mean(s_path)
        geo_mean = math.exp(1/float(n)*np.sum(np.log(s_path)))

        if type == 'C':
            arith_payoff[i] = math.exp(-r*T)*max(arith_mean-K, 0)
            geo_payoff[i] = math.exp(-r*T)*max(geo_mean-K, 0)
        else:
            arith_payoff[i] = math.exp(-r*T)*max(-arith_mean+K, 0)
            geo_payoff[i] = math.exp(-r*T)*max(-geo_mean+K, 0)

    #Standard Monte Carlo:
    if cv == 'null':
        p_mean = np.mean(arith_payoff)
        p_std = np.std(arith_payoff)
        CIlow = p_mean-1.96*p_std/math.sqrt(path)
        CIhigh = p_mean+1.96*p_std/math.sqrt(path)
        print "Mean: %.5f, Std: %.5f, [%.5f, %.5f]" % (p_mean, p_std, CIlow, CIhigh)
    #Monte Carlo with control variates
    else:
        XY = [0.0]*path
        for i in range(0, path):
            XY[i] = arith_payoff[i]*geo_payoff[i]
        covXY = np.mean(XY) - (np.mean(arith_payoff)*np.mean(geo_payoff))
        theta = covXY/np.var(geo_payoff)
        geo = geo_asian_option(S, sigma,r, T, K, n, type)
        z = arith_payoff + theta*(geo - geo_payoff)
        z_mean = np.mean(z)
        z_std = np.std(z)
        CIlow = z_mean-1.96*z_std/math.sqrt(path)
        CIhigh = z_mean+1.96*z_std/math.sqrt(path)
        print "Mean: %.5f, Std: %.5f, [%.5f, %.5f]" % (z_mean, z_std, CIlow, CIhigh)


#arithmetric basket
#Input: S1 S2 sigma1 sigma r T K corr type path cv
#path: number paths for Monte Carlo simulation
#cv: type of control variate (null or geo_basket)
def arith_basket(S1, S2, sigma1, sigma2, r, T, K, corr, type, path, cv):
    np.random.seed(0)
    z1 = np.random.normal(loc=0, scale=1, size=path)
    z = np.random.normal(loc=0, scale=1, size=path)
    z2 = corr*z1+math.sqrt(1-corr**2)*z
    S1_T = S1*np.exp((r-0.5*sigma1*sigma1)*T+sigma1*np.sqrt(T)*z1)
    S2_T = S2*np.exp((r-0.5*sigma2*sigma2)*T+sigma2*np.sqrt(T)*z2)
    ba_T = (S1_T+S2_T)/2
    bg_T = np.exp((np.log(S1_T)+np.log(S2_T))/2)
    if type == 'C':
        arith_payoff = (ba_T-K)*math.exp(-r*T)
        geo_payoff = (bg_T-K)*math.exp(-r*T)
    else:
        arith_payoff = (K-ba_T)*math.exp(-r*T)
        geo_payoff = (K-bg_T)*math.exp(-r*T)
    for i in range(0, path):
        arith_payoff[i] = max(arith_payoff[i], 0)
        geo_payoff[i] = max(geo_payoff[i], 0)

    #Standard Monte Carlo
    if cv == 'null':
        p_mean = np.mean(arith_payoff)
        p_std = np.std(arith_payoff)
        print "Mean: %.5f, Std: %.5f" % (p_mean, p_std)
    #Monte Carlo with control variates
    else:
        XY = [0.0]*path
        for i in range(0, path):
            XY[i] = arith_payoff[i]*geo_payoff[i]
        covXY = np.mean(XY) - np.mean(arith_payoff)*np.mean(geo_payoff)
        theta = covXY/np.var(geo_payoff)

        Z = [0.0]*path
        geo = geo_basket(S1, S2, sigma1, sigma2, r, T, K ,corr, type)
        # print "Geo: %.5f: Geo_sample: %.5f" % (geo, np.mean(geo_payoff))
        for i in range(0, path):
            Z[i] = arith_payoff[i]+theta*(geo-geo_payoff[i])
        z_mean = np.mean(Z)
        z_std = np.std(Z)
        print "Mean: %.5f, Std: %.5f" % (z_mean, z_std)


def bino_tree(S, K, r, T, sigma, N, type):
    dt = float(T)/N
    u = math.exp(sigma*math.sqrt(dt))
    d = 1/u
    p = (math.exp(r*dt)-d)/(u-d)
    DF = math.exp(-r*dt)
    stock = [0.0]*(N+1)
    pay_off = [0.0]*(N+1)
    if type == 'C':
        for i in range(0, N+1):
            stock[i] = S*pow(u, N-i)*pow(d, i)
            pay_off[i] = max(S*pow(u, N-i)*pow(d, i)-K, 0)
        for j in range(0, N):
            for i in range(0, N-j):
                stock_price = math.sqrt(stock[i]*stock[i+1])
                pay_off[i] = max(stock_price-K, DF*(p*pay_off[i]+(1-p)*pay_off[i+1]))
                stock[i] = stock_price
        return pay_off[0]
    else:
        for i in range(0, N+1):
            stock[i] = S*pow(u, N-i)*pow(d, i)
            pay_off[i] = max(-S*pow(u, N-i)*pow(d, i)+K, 0)
        for j in range(0, N):
            for i in range(0, N-j):
                stock_price = math.sqrt(stock[i]*stock[i+1])
                pay_off[i] = max(-stock_price+K, DF*(p*pay_off[i]+(1-p)*pay_off[i+1]))
                stock[i] = stock_price
        return pay_off[0]

if __name__ == '__main__':
    print "Hello world"
    # print geo_asian_option(100, 0.3, 0.05, 3, 100, 50, 'P')
    # print geo_asian_option(100, 0.3, 0.05, 3, 100, 100, 'P')
    # print geo_asian_option(100, 0.4, 0.05, 3, 100, 50, 'P')
    # print geo_asian_option(100, 0.3, 0.05, 3, 100, 50, 'C')
    # print geo_asian_option(100, 0.3, 0.05, 3, 100, 100, 'C')
    # print geo_asian_option(100, 0.4, 0.05, 3, 100, 50, 'C')
    arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 1000000, 'null')
    arith_asian_option(100, 0.3, 0.05, 3.0, 100, 50, 'P', 1000000, 'geo_asian')
    # arith_basket(100, 100, 0.3, 0.3, 0.05, 3.0, 100, 0.5, 'C', 1000000, 'null')
    # arith_basket(100, 100, 0.3, 0.3, 0.05, 3.0, 100, 0.5, 'C', 1000000, 'geo_basket')
    # print bino_tree(50, 50, 0.05, 0.25, 0.3, 500, 'C')
    # print bino_tree(50, 52, 0.05, 2, 0.223144, 500, 'P')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, 'P')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.9, 'P')
    # geo_basket(100, 100, 0.1, 0.3, 0.05, 3, 100, 0.5, 'P')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 80, 0.5, 'P')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 120, 0.5, 'P')
    # geo_basket(100, 100, 0.5, 0.5, 0.05, 3, 100, 0.5, 'P')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, 'C')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.9, 'C')
    # geo_basket(100, 100, 0.1, 0.3, 0.05, 3, 100, 0.5, 'C')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 80, 0.5, 'C')
    # geo_basket(100, 100, 0.3, 0.3, 0.05, 3, 120, 0.5, 'C')
    # geo_basket(100, 100, 0.5, 0.5, 0.05, 3, 100, 0.5, 'C')