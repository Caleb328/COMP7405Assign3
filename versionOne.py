import math
import numpy as np
from scipy.stats import norm
from timeit import default_timer as timer


#d1 and d2
def d_one(S, K, T, sigma, mu):
    return (math.log(S/K)+(mu+0.5*pow(sigma, 2))*T)/math.sqrt(T)*sigma


def d_two(S, K, T, sigma, mu):
    return (math.log(S/K)+(mu+0.5*pow(sigma, 2))*T)/math.sqrt(T)*sigma-math.sqrt(T)*sigma


#Geometric Asian option
#Input: S sigma r T K n type
def geo_asian_option(S, sigma, r, T, K, n, type):
    N = float(n)
    sigsqT = pow(sigma, 2)*T*(N+1)*(2*N+1)/(6*N*N)
    muT = 0.5*sigsqT+(r-0.5*pow(sigma, 2))*T*(N+1)/(2*N)
    d1 = (math.log(S/K)+(muT+0.5*sigsqT))/(math.sqrt(sigsqT))
    d2 = d1 - math.sqrt(sigsqT)
    if type == 'C':
        return math.exp(-r*T)*(S*math.exp(muT)*norm.cdf(d1)-K*norm.cdf(d2))
    else:
        return math.exp(-r*T)*(-S*math.exp(muT)*norm.cdf(-d1)+K*norm.cdf(-d2))


#Geometric basket
#Input S1 S2 sigma1 simga2 r T K corr type
def geo_basket(S1, S2, sigma1, sigma2, r, T, K ,corr, type):
    sigma = math.sqrt(sigma1*sigma1+sigma1*sigma2*corr*2+sigma2*sigma2)/2
    mu = r-(pow(sigma1, 2)+pow(sigma2, 2))/4+0.5*pow(sigma, 2)
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
    np.random.seed(0)
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
        geo_mean = math.exp(1/float(n)*np.sum([math.log(x) for x in s_path]))
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
    #Monte Carlo with control variates
    else:
        XY = [0.0]*path
        for i in range(0, path):
            XY[i] = arith_payoff[i]*geo_payoff[i]
        covXY = np.mean(XY) - np.mean(arith_payoff)*np.mean(geo_payoff)
        theta = covXY/np.var(geo_payoff)
        z = [0.0]*path
        geo = geo_asian_option(S, sigma,r, T, K, n, type)
        for i in range(0, path):
            z[i] = arith_payoff[i] + theta*(geo - geo_payoff[i])
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
    arith_payoff = [0.0]*path
    geo_payoff = [0.0]*path
    for i in range(0, path):
        S1_T = S1*math.exp((r-0.5*pow(sigma1, 2))*T+sigma1*math.sqrt(T)*np.random.standard_normal(1)[0])
        S2_T = S2*math.exp((r-0.5*pow(sigma2, 2))*T+sigma2*math.sqrt(T)*np.random.standard_normal(1)[0])
        ba_T = (S1_T+S2_T)/2
        bg_T = math.sqrt(S1_T*S2_T)
        if type == 'C':
            arith_payoff[i] = max(ba_T-K, 0)
            geo_payoff[i] = max(bg_T-K, 0)
        else:
            arith_payoff[i] = max(K-ba_T, 0)
            geo_payoff[i] = max(K-bg_T, 0)

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
    arith_asian_option(10, 0.1, 0.06, 1.0, 9, 100, 'C', 10000, 'null')
    arith_asian_option(10, 0.1, 0.06, 1.0, 9, 100, 'C', 10000, 'geo_asian')
    arith_basket(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, 'C', 10000, 'null')
    arith_basket(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, 'C', 10000, 'geo_basket')
    print bino_tree(50, 50, 0.05, 0.25, 0.3, 500, 'C')
    print bino_tree(50, 52, 0.05, 2, 0.223144, 500, 'P')
