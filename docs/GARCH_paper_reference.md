Portfolio Optimization on Multivariate Regime-Switching GARCH Model with Normal Tempered Stable Innovation

Cheng Peng ∗ Young Shin Kim † and Stefan Mittnik ‡

Abstract

This paper uses simulation-based portfolio optimization to mitigate the left tail risk of the portfolio. The contribution is twofold. (i) We propose the Markov regime-switching GARCH model with multivariate normal tempered stable innovation (MRS-MNTS-GARCH) to accom- modate fat tails, volatility clustering and regime switch. The volatility of each asset inde- pendently follows the regime-switch GARCH model, while the correlation of joint innovation of the GARCH models follows the Hidden Markov Model. (ii) We use tail risk measures, namely conditional value-at-risk (CVaR) and conditional drawdown-at-risk (CDaR), in the portfolio optimization. The optimization is performed with the sample paths simulated by the MRS-MNTS-GARCH model. We conduct an empirical study on the performance of optimal portfolios. Out-of-sample tests show that the optimal portfolios with tail measures outperform the optimal portfolio with standard deviation measure and the equally weighted portfolio in various performance measures. The out-of-sample performance of the optimal portfolios is also more robust to suboptimality on the ecient frontier.

1  Introduction

Empirical studies have found in the return of various nancial instruments skewness and leptokur- totic|asymmetry, and higher peak around the mean with fat tails. Normal distribution has long been recognized as insucient to accommodate these stylized facts, relying on which could dras- tically underestimate the tail risk of a portfolio. The -stable distribution is a candidate to in- corporate this fact into decision-making, but its lack of nite moments could cause diculties in modeling. The class of tempered stable distributions serves as a natural substitution, since it has nite moments while retaining many attractive properties of the -stable distribution. The class of tempered stable distributions is derived by tempering the tails of the -stable distribution (See [Ko- ponen 1995;](#_page25_x66.89_y265.28) [Boyarchenko and Levendorskii 2000; and](#_page25_x66.89_y297.16) [Carr et al. 2002), or](#_page25_x66.89_y329.04) from the time changed Brownian motion. Since [Barndor-Nielsen and Levendorskii (2001) and](#_page25_x66.89_y360.92) S[hephard et al. (2001) ](#_page25_x66.89_y392.80)presented the normal tempered stable (NTS) distribution in nance using the time changed Brow- nian motion, it has been successfully applied for modeling the stock returns with high accuracy

in literature including [Kim et al. (2012), ](#_page25_x66.89_y424.68)[Kurosaki and Kim (2018), ](#_page25_x66.89_y468.52)[Anand et al. (2016) and ](#_page25_x66.89_y500.40)Kim [(2022).](#_page25_x66.89_y532.28)

∗Stony Brook University, cheng.peng.1@stonybrook.edu![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.001.png)

†Stony Brook University, aaron.Kim@stonybrook.edu

‡Ludwig Maximilians University in Munich, n metrics@stat.uni-muenchen.de

1

Deviation from normality exists not only in raw returns, but also in ltered innovations of

time series models. Since the foundational work in [Engle (1982) and](#_page25_x66.89_y576.11) [Bollerslev (1986), GAR](#_page25_x66.89_y607.99)CH model has been widely applied to model volatility. This motivates us to use NTS distribution to accommodate the asymmetry, interdependence, and fat tails of the innovations of GARCH models. Several studies have found NTS distribution to be more favorable than other candidates. Kim [et al. (2011)](#_page26_x66.89_y93.05) found that normal and t-distribution are rejected as innovation of GARCH model in hypothesis testing. [Shi and Feng (2016) ](#_page26_x66.89_y136.88)found that tempered stable distribution with exponential tempering yields better calibration of Markov Regime-Switching (MRS) GARCH model than t or generalized error distribution. Generalized hyperbolic distribution, while very exible, has too many parameters for estimation. NTS distribution has only three standardized parameters and is exible enough to serve the purpose.

A drawback of GARCH model is the inadequate ability in modeling volatility spikes, which could indicate that the market is switching within regimes. Various types of MRS-GARCH models

have been proposed, many of which suggest that the regime-switching GARCH model achieves a better t for empirical data (for example, in [Hamilton 1996). ](#_page26_x66.89_y168.77)[Marcucci (2005) nds](#_page26_x66.89_y200.65) that MRS- GARCH models outperform standard GARCH models in volatility forecasting in a time horizon shorter than one week. Naturally, the most exible model allows all parameters to switch among regimes. However, as is shown in [Henneke et al. (2011), ](#_page26_x66.89_y244.48)the sampling procedure in the MCMC method for estimating such a model is time-consuming and renders it improper for practical use.

We construct a new model based on the regime-switching GARCH model specied in Haas[ et al. (2004),](#_page26_x66.89_y276.36) which circumvents the path dependence problem in the Markov Chain model by specifying parallel GARCH models.

[Bollerslev (1990)](#_page26_x66.89_y308.24) proposes the GARCH model with constant conditional correlation. The par- simonious DCC-GARCH model in [Engle (2002) op](#_page26_x66.89_y352.08)ens the door to modeling multivariate GARCH process with dierent persistence between variance and correlation. While exible models allowing time-varying correlation are preferred in many cases, specication of multivariate GARCH models

with both regime-specic correlations and variance dynamics involves a balance between exibility and tractability. The univariate MRS-GARCH model in Haas[ et al. (2004) is generali](#_page26_x66.89_y276.36)zed in Haas [and Liu (2004)](#_page26_x66.89_y395.91) to a multivariate case. Unfortunately, it suers from the curse of dimensionality,

and thus is unsuitable for a high dimensional empirical study. In our model, we decompose variance

and correlation so that the variance of each asset evolves independently according to a univariate MRS-GARCH model. The correlation is incorporated in the innovations modeled by a exible Hid-

den Markov Model (HMM) that has multivariate NTS distribution as the conditional distribution in each regime. We will use the calibrated model to simulate returns for portfolio optimizations.

Modern portfolio theory is formulated as a trade-o between return and risk. The classical Markowitz Model nds the portfolio with the highest Sharpe ratio. However, variance has been criticized for not containing enough information on the tail of the distribution. Moreover, correlation is not sucient to describe the interdependence of asset returns with non-elliptical distribution. Current regulations for nancial business utilize the concept of Value at Risk (VaR), which is the percentile of the loss distribution, to model the risk of left tail events. There are several undesired properties that rendered it an insu cient criterion. First, it is not a coherent risk measure due to

a lack of sub-additivity. Second, VaR is a non-convex and non-smooth function of positions with multiple local extrema for non-normal distributions, which causes diculty in developing ecient optimization techniques. Third, a single percentile is insucient to describe the tail behavior of a distribution, and thus might lead to an underestimation of risk.

Theory and algorithm for portfolio optimization with a conditional value-at-risk (CVaR) measure

2

proposed in [Krokhmal et al. (2001) ](#_page26_x66.89_y439.75)and Ro[ckafellar and Uryasev (2000) ee](#_page26_x66.89_y471.63)ctively addresses these problems. For continuous distributions, CVaR is dened by a conditional expectation of losses exceeding a certain VaR level. For discrete distributions, CVaR is de ned by a weighted average of some VaR levels that exceed a specied VaR level. In this way, CVaR concerns both VaR and the losses exceeding VaR. As a convex function of asset allocation, a coherent risk measure and a more informative statistic, CVaR serves as an ideal alternative to VaR. A study on the comparison of the two measures can be found in [Sarykalin et al. (2014).](#_page26_x66.89_y503.51)

Another closely related tail risk measure is conditional drawdown-at-risk (CDaR). Drawdown has been a constant concern for investors and is often used in the performance evaluation of a portfolio. It is much more dicult to climb out of a drawdown than drop into one, considering that it takes 100% return to recover from 50% relative drawdown. In behavioral nance, it is well documented that investors fear losses more than they value gains. However, the commonly used maximum drawdown only considers the worst scenario that only occur under some very special circumstances, and thus is very sensitive to the testing period and asset allocation. On the other hand, small drawdowns included in the calculation of average drawdown are acceptable and might be caused by pure noise, of which the minimization might result in overtting. For instance, a Brownian motion would have drawdowns in a simulated sample path.

CDaR is proposed in [Checkhlov et al. (2004) to](#_page26_x66.89_y535.39) address these concerns. While CVaR is de- termined by the distribution of return, CDaR is path-dependent. CDaR is essentially CVaR of the distribution of drawdowns. By this, we overcome the drawbacks of average drawdown and maximum drawdown. CDaR takes not only the depth of drawdowns into consideration, but also the length of them. Since the CDaR risk measure is the application of CVaR in a dynamic case, it naturally holds nice properties of CVaR, such as convexity with respect to asset allocation. The optimization method with constraints on CDaR has also been developed and studied in Chec[khlov et al. (2004, ](#_page26_x66.89_y535.39)[2005).](#_page26_x66.89_y567.27)

An optimization procedure could lead to an underperformed portfolio by magnifying the esti- mation error. Using historical sample paths as input implies an assumption that what happened in the past will happen in the future, which requires careful examination. It is found in Lim [et al. (2011)](#_page26_x66.89_y599.15) that estimation errors of CVaR and the mean is large, resulting in unreliable allocation. An alternative way is to use multiple simulated returns. It is reasonable to expect outperformance during a crisis if we use the simulation of a model that captures extreme tail events as input for optimization with tail risk measures. Relevant research that resorts to copula does not address a regime switch (See [Sahamkhadam et al. 2018).](#_page27_x66.89_y93.05)

We have identied several issues in GARCH-simulation-based portfolio optimization: deviation from normality, regime switch, high dimensional calibration and tail risk measures. This paper intends to address these issues in one shot. First, we propose the MRS-MNTS-GARCH model to accommodate fat tails, volatility clustering and regime switch. In the model, the volatility of each asset independently follows a regime-switch GARCH model, while the correlation of joint innovation of GARCH models follows a Hidden Markov Model. We specify the method for ecient model calibration. The MRS-MNTS-GARCH model is used to simulate sample paths. Then, the sample paths are used as input to portfolio optimization with tail risk measures CVaR and CDaR. We conduct in-sample tests sow show the goodness-of-t. We conduct out-of-sample tests to show the outperformance of our approach in various measures. The optimal portfolios are also more robust to suboptimality of the optimization. The results suggest that, in practice, performance ratios can be improved compared to equally weighted portfolio by adopting simulation-based portfolio optimization with the MRS-MNTS-GARCH model. The empirical study suggests that using tail

3

risk measures outperforms using standard deviation in terms of various performance measures and robustness.

The remainder of the paper is organized as follows. Section 2 [intro](#_page3_x91.80_y181.67)duces the preliminaries on NTS distribution and GARCH model. Section 3 [species](#_page9_x91.80_y497.01) our model and methods for estimation and simulation. Section 4[ in](#_page12_x91.80_y334.29)troduces the portfolio optimization with tail risk measures. Section 5 is an empirical study on in-sample goodness-of-t and out-of-sample performance in recent years.

2  Preliminaries

<a name="_page3_x91.80_y181.67"></a>This section reviews the background knowledge on dierent risk measures, scenario-based esti- mation, normal tempered stable (NTS) distribution, and GARCH and regime-switching GARCH model.

1. Tail Risk Measures

In this subsection, we discuss and summarize popular tail risk measures in nance such as Value at Risk (VaR), Conditional VaR (CVaR), and conditional drawdown-at-risk (CDaR). Denitions of CDaR, and related properties of drawdown are following [Checkhlov et al. (2004, ](#_page26_x66.89_y535.39)[2005).](#_page26_x66.89_y567.27)

Consider a probability space (;F1;P) and a portfolio with N assets. Suppose that Pn is a stochastic process of a price for the n-th asset in the portfolio on the space

Pn : [0;1)   ! R; n = 1;2;;N

with the real initial value Pn(0;) = Pn;0 > 0.

The stochastic process of the compounded return of the n-th asset between time 0 to time t > 0 is dened by

P (t;!)   P

Rn(t;!) = n P n;0 ; t > 0;

n;0

with Rn(0;) = 0. Then, the compounded portfolio return R(x;t;!) at time t > 0 is equal to

XN

R(x;t;!) = xnRn(t;!):

n=1

The denition of VaR for R(x;t; ) with the condence level is

VaR(R(x;t; )) = minfzjP(R(x;t; )  z) g: If R(x;t; ) has a continuous cumulative distribution, then we have

 1

VaR(R(x;t; )) = F R(x;t;)(1   );

where F  1 is the inverse cumulative distribution function of  R(x;t; ). The denition of

 R(x;t;)

CVaR for R(x;t; ) with the condence level is

Z 1

CVaR(R(x;t; )) = 1  1  VaRz (R(x;t; ))dz:



4

Equivalently, CVaR can be obtained by a minimization formula

 

1

<a name="_page4_x507.47_y116.50"></a>CVaR (R(x;t; )) = min + E [maxf0; R(x;t; )   g] : (1) Following [Checkhlov et al. (2004), ](#_page26_x66.89_y535.39)denote the uncompounded return of the n-th asset by

Qn(t;w). The uncompounded portfolio return is dened by

XN

Q(x;t;!) = xnQn(t;!):

n=1

Let T > 0, and ! 2 , then (R(x;t;!))t2[0;T ] = fR(x;t;!)jt 2 [0;T]g is one sample path of port- folio return with the capital allocation vector x from time 0 to T. The drawdown (DD(;!))t2[0;T ] of the portfolio return is dened by

<a name="_page4_x190.58_y264.29"></a>DD(t;!) = max Q(x;s;!)   Q(x;t;!); for t 2 [0;T] (2)

s2[0;t]

is a risk measure assessing the decline from a historical peak in some variable, and fDD(t;!)jt 2 [0;T];! 2 g is a stochastic process of the drawdown. The average drawdown (ADD) up to time

T for ! 2 is dened by Z T

1

ADD(T;!) = DD(t;!)dt: (3)

T 0

It is the time average of drawdowns observed between time 0 to T. The maximum drawdown (ADD) up to time T for ! 2 is dened by

<a name="_page4_x240.14_y389.56"></a>MDD(T;!) = max DD(t;!): (4)

t2(0;T )

It is the maximum of drawdowns that have occurred up to time T for ! 2 .

Let Z

<a name="_page4_x236.70_y444.98"></a>FDD(z;!) = T1 0T 1DD(t;!) z dt (5) and (

inffzjF (z;!) g if 2 (0;1]

(!) = DD : (6)

0 if = 0

According to [Checkhlov et al. (2005), ](#_page26_x66.89_y567.27)the CDaR is dened as the CVaR of drawdowns. Applying

[(1)](#_page4_x507.47_y116.50) to drawdowns, we have

( Z )

1 T

CDaR(T;!) = min + T 0 max fDD(t;!)   ;0gdt :

It can also be represented as

CDaR

- F(T(;!1)( !);!)    (!) + (1  1)T 0

<a name="_page4_x507.47_y625.03"></a>Z T

DD DD(t;!)1DD(t;!)>(!)dt: (7)

5

Note that CDaR0(T;!) = ADD! (T) and CDaR1(T;!) = MDD! (T).

Let "Z #

<a name="_page5_x233.14_y123.44"></a>FDD(z) = T1 E 0T 1DD(t;) z dt (8) and (

inffzjFDD(z) g if 2 (0;1]

 = FDD 1() = 0 if = 0 : (9) ConsideringCDaRalltheF(Tsample(1) ())  path (1   )T 0 DD(t;)>()dt

fR(x;t;!)jt 2 [0;T];! 2 g, we dene CDaR at by

"Z #

DD 1 T

- <a name="_page5_x502.49_y239.05"></a>() +~~ E DD(t; )1 : (10)
2. Scenario-Based Estimation

In this subsection, we discuss the risk estimation using given scenarios (historical scenario or simula- tion). Suppose that the time interval [0;T] is divided by a partition f0 = t0 < t1 < < tM = Tg,

and denote

Rm(x) = R(x;tm;):

We select !s 2 where s 2 f1;2;;Sg and S is the number of scenarios. Then, we obtain scenarios of the portfolio return process R at time tm:

Rs (x) = R(x;t ;! )

m m s

where m 2 f 0;1;2;;Mg, and s 2 f 1;2;;Sg. We calculate VaR, CVaR, DD, and CDaR under the simulated scenarios. The VaR with signicant level under the simulated scenario is estimated by

VaR (R (x)) =  inf (u S1 X 1R > 1   ) : (11)

S

- m s (x)<u

m

s=1

Let R(mk)(x) be the k-th smallest value in fRsm (x) js = 1;2;;Sg, then CVaR at the signicant level is estimated according to the formula

CVaR(R (x))

-  1 0@1mdS(X)e 1  dSe   1 (x)1A ;

(k) (dSe)

- S Rm (x) +   S Rm (12) k=1

where dxe denotes the smallest integer larger than x (See [Rachev et al. 2008 ](#_page27_x66.89_y148.84)for details).

The rate of return of the n-th asset between time ti 1 and time ti is dened by

r (ti;!) = Pn(ti;!)   Pn(ti 1;!); t > 0;

n Pn(ti 1;!)

6

with rn(0;) = 0. It is referred to as return in this paper. Let x = (x1;x2;;xN )T 2 RN be

a capital allocation vector of a long-only portfolio satisfying PNn=1 xn = 1 and xn 2 [0;1] for all n 2 f1;2;;Ng. Then, the portfolio return U(x;ti;!s) between time ti 1 and time ti is

XN

U(x;ti;!s) = xnrn(ti;!s):

n=1

The scenario-based estimation on uncompounded cumulative return at time ti is

Xt

Q(x;ti;!s) = Un(x;ti;!s):

t=1

Denote Q(x;ti;!s) by Qsi(x). Using [(2){(4),](#_page4_x190.58_y264.29)[ DD,](#_page4_x240.14_y389.56) ADD, and MDD on a single simulated scenario are estimated, respectively, by

s s

<a name="_page6_x502.49_y273.02"></a>DDm;s := DD(tm;!s) = max Qj (x)   Qm(x); (13)

j2f0;1;2;;mg

1 XM

ADDM;s := ADD(tM ;!s) = M DDm;s; (14)

m=1

MDDM;s := MDD(tM ;!s) = max DDm;s: (15)

m 2f 1;2;;M g

Furthermore, using [(5){(7), ](#_page4_x507.47_y625.03)CDaR is estimated on a single simulated scenario by

1 XM

) = DD 1 ; CDaR(T;s) := CDaR(T;!s (1   )M m;s DDm;s>s

m=1

where (

s := (w ) = inffzjFDD(z;s) g if 2 (0;1] :

-  s 0 if = 0

with

XM

FDD(z;s) = M1 1DD z :

m;s

m=1

Equivalently, it is estimated by the optimization formula

( )

1  XM

CDaR(T;s) = min + (1   )M max(DDm;s   ;0) :

m=1

With [(8){(10),](#_page5_x502.49_y239.05) DD and CDaR on multiple scenarios are estimated by

1 XS

DD(m) = DD

S m;s

s=1

7

and

CDaR(T)



- FDD(())    () + 1 XS XM 1DD 1 ;<a name="_page7_x502.49_y137.76"></a> (16) 1    (1   )M S m;s DDm;s>()

s=1 m=1

respectively, where

FDD(z) = S1 X FDD(z;s)

S

s=1

and ( 

inf z FDD (z)  if 2 (0;1] :

 = 0 if = 0

In this paper, we will apply time series models to generate the scenario of rn(m;s) for m 2 f1;2;;Mg, s 2 f 1;2;;Sg and n 2 f 1;2;;Ng.

3. Multivariate Normal Tempered Stable Distribution

Let T be a strictly positive random variable dened by the characteristic function for 2 (0;2) and  >0 !

21  ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.002.png)![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.003.png)![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.004.png)

T (u) = exp   2 ((  iu) 2   2 ) :

Then, T is referred to as a tempered stable subordinator with parameters and . Suppose that  = (1;;N )T is a N-dimensional standard normal distributed random vector with a

N  N covariance matrix , i.e.,  (0;). The N-dimensional NTS distributed random vector

X = (X1;:::;XN )T is dened by

p ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.005.png)

X = + (T   1) + Tdiag( );

where  = ( 1;;N )T 2 RN ,  = ( 1;;N )T 2 RN , = ( 1;; )T 2 RN and T is

N + independent of . The N-dimensional multivariate NTS distribution specied above is denoted by

X  MNTSN (; ;; ;;):

q ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.006.png) q ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.007.png)

Let n = 0, and n = 1   n2( 22  ), jnj < 2  for n 2 f1;;Ng. This yields a random

2

variable having zero mean and unit variance. In this case, the random variable is referred to

as standard NTS distributed random variable and denoted by X  stdMNTSN (; ;;). The covariance matrix of X is given by

 = diag( )diag( ) + 2  ~~ >:

X 2

8

4. Regime-Switching GARCH Model

GARCH(p;q) model has been studied extensively as a model for volatility.

rt = + t t ;

ut = t t ;

Xp Xq

t2 = ! + iu2t i + it i:

2

i=1

where rt is the return at time t, t is the variance at time GARCH(1,1) in this paper.

Before specifying our model, it would be clear to rst switching model in [Haas et al. (2004) as](#_page26_x66.89_y276.36) follows

i=1

t, ;!; i; i are parameters. We will use specify the univariate Markov regime-

rt = t + t;tt;

<a name="_page8_x244.28_y283.86"></a>ut = t;tt;

2 = ! + u2 + 2 ; (17)

t t 1 t 1

t iid N(0;1);

where

- k = number of regimes in a Markov chain;
- t = f1;;kg = Markov chain with an irreducible and primitive transition matrix that determines the regime at time t;
- rt = return at time t;
- 2 = ( 2 ;::::;2 ) = vector of parallel variance;

t 1;t k;t

- ! = ( ! 1;::::;! k), = ( 1;::::; k), = ( 1;::::; k). ! , , are vectors of coecien ts;
-  t = regime specic mean return in regime  t at time t;
-  t ;t = the standard deviation in regime  t at time t;
- denotes element-wise product.

There are k parallel GARCH models evolving simultaneously. The Markov chain t determines which GARCH model is realized at next moment.

To better understand [(17), ](#_page8_x244.28_y283.86)let us create the following matrix

2

1;1 1;2 662;1 2;2

[t;t]t=1;:::;k; t=1;:::T = 64 ... ...

k;1 k;2

3 ::: 1;t :::

::: 1;t :::77 .. 7 :

. ::: :::5

::: k;t :::

Each column is a total of k parallel standard deviations at time t. Each row is the process of one regime through time 1 to T. The process of standard deviation is generated as follows:

9

Step 1: At t = 1, the initial column is generated.

Step 2: 1 decides which row is realized.

For example, suppose 1 = 2. That is, 2;1 is realized in real-world at t = 1. Step 3: By vector calculation, 2nd column is generated.

For example, suppose 2;1 is realized at t = 1. We calculate

2  3 2 3 2 3 2 3 2 3 61;277 66!17 6 27 6 27 61;17

    ! 1 1

   66 2..;27 = 6 ..277 + 2;11 66 .. 77 + 66 .. 77 66 2..;177 : 4 . 5 4 . 5 4 . 5 4 . 5 4 . 5

   k;2 !k k k k;1

Step 4: 2 Decides which row is realized.

For example, suppose 2 = 1. That is, 1;2 is realized in real world at t = 2. A regime switch from regime 2 to regime 1 takes place.

Step 5: Repeat Step 1 to Step 4.

It is important to note that in the example, the realized variance at time t = 2, 1;2, is calculated with both the realized variance at time t = 1, 2;1, and unrealized 1;1. This is obvious from the vector equation shown above. 1;1 is in the parallel process and is not realized in real world.

More generally, when there is a regime switch, from the vector equation 2 = ! + u 2+ 2 , t t t 1

we know that the variance  ;t is determined by  ;t 1 rather than t 1;t 1.  is a variance in regime t at timett, which is generated sim tultaneously with t 1;t 1, but tdo;t es1 not

exist in reality at time t or t   1. This makes the model dierent from the one in [Henneke et al. (2011)](#_page26_x66.89_y244.48) that requires all parameters to switch regime according to a Markov chain. In that model, there is no parallel process, and  ;t is determined by  ;t 1.

The stationary conditions derivedtin Haas[ et al. (2004)](#_page26_x66.89_y276.36) t [require](#_page26_x66.89_y276.36)1 denitions of the matrices:

Mji = pji( + e>i ); i;j = 1;:::;k and the block matrix

M = [Mji]; i;j = 1;::::;k:

The necessary and sucient condition for stationarity is (M) < 1, where (M) denotes the largest eigenvalue of matrix M.

3  MRS-MNTS-GARCH<a name="_page9_x91.80_y497.01"></a> Model

This section denes the MRS-MNTS-GARCH model and introduces the procedures for model tting and sample path simulation.

1. Model Specication

To model a multivariate process, we assume that the variance of each individual asset evolves independently according to the univariate regime-switching GARCH model specied previously with possibly dierent number of regimes, while the correlation between assets is modeled separately by stdMNTS distribution in the joint standard innovations. The joint innovations is dened bya HMM with stdMNTS as conditional distribution in each regime.

10

The MRS-MNTS-GARCH model is dened by

- (i)u2t == tt +t u(i) 2

rt t t

t = !(i) + (i) t 1 + (i) t( i)12 ;i = 1;:::;N



t iid stdMNTS( Dt ;Dt ;Dt ;Dt );

where

- N = number of assets;
- k(i) = number of regimes of the i-th asset;
- (i) = f1;;k(i)g = Markov chain with an irreducible and primitive transition matrix that determines the regime of the i-th asset at time t;
- (ti) = f1;;k(i)g = realization of  (i) at time t;
- D = f1;;kD g = Markov chain with an irreducible and primitive transition matrix that determines the regime of the joint innovations at time t;
- Dt = f1;;kD g = realization of  D at time t;
- r t = ( rt(1) ;:::;rt(N )) = vector return of N assets at time t;
-  = ( (1) ;:::;(N ) ) = vector mean return at time t;

t (1) (N )

t t

- (i) = mean return of the i-th asset at time t, (i) is determined by the regime of the i-th (i) (ti)

  assett at time t, (ti);



- t = (1) ;:::;(N ) = vector of standard deviation of N assets at time t;

(1)t ;t (tN );t

-   2
- t(i) = 1(i;t);:::;k(i()i )2;t = standard deviation vector of the i-th asset with t(i) = 1(i;t) 2;:::; k(i()i);t ;
- 
- u(t i)1 = the i-th element of u t , with u t = u(1)t ;:::;u(tN ) ;
- ! (i) = ( ! 1(i);:::;! k(i()i ) ), (i) = ( (1i);:::; (ki()i ) ), (i) = ( 1(i);:::; k(i()i ) ). ! (i), (i), (i) are the vector of coecients of the i-th asset in k(i) regimes;
- t = ( (1)t ;:::;(tN )) = joint innovations;
- denotes element-wise product.

11

For each asset, the volatility process is the same as that of the univariate regime-switching GARCH model in [(17).](#_page8_x244.28_y283.86) It is a classical GARCH process when it does not shift within regimes. Unlike the most exible model in which the variance at time t is calculated with the variance at time t   1 in the last regime, when a regime shift takes place at time t, the variance in the model at time t is determined by the variance at time t   1 within the new regime. The regimes of each asset and joint innovations evolve independently, mitigating the diculty in estimation caused by

all parameters switching regimes simultaneously.

2. Parameter Estimation

Although NTS distribution is exible enough to accommodate many stylized facts of asset return,

the absence of an analytical density function presents some diculties in estimation. Our estimation methodology is adapted from [Kim et al. (2011, ](#_page26_x66.89_y93.05)[2012), whic](#_page25_x66.89_y424.68)h are among the rst works to incorporate NTS distribution in portfolio optimization. Another estimation of stdMNTS distribution with EM algorithm combined with fast Fourier transform is studied in Bian[chi et al. (2016). Belo](#_page27_x66.89_y192.68)w we describe the procedure to t the model.

First, we t the univariate Markov regime-switching GARCH model with t innovation on the index return and extract the innovations and the regimes at each time t, D . It is intuitive to

t

assume that the correlation between assets change drastically when a market regime shift takes place. Thus, here we assume that the Markov chain D that determines the regime of innovations

is the same as the Markov chain that determines the regime of the market index. That is, the sample path of the regime of the innovation is derived by extracting the sample path of the regime of the market index. The innovations of the model calibrated by the market index are used to estimate tail parameters D ;D in each regime.

Next, we t the univariate model on each asset and extract the innovations for subsequent estimation of stdMNTS distribution. In each regime, the stdMNTS distribution has two tail pa- rameters D ;D and one skewness parameter vector D . Common tail parameters D ;D are assumed for individual constituents, which are estimated from the market index in each regime. The skewness parameter D is calibrated by curve tting for each asset.

Finally, we plug the empirical covariance matrix of the innovations in each regime  D in the formula  = diag( ) 1(   2  D >  )diag( ) 1 to compute  .XNote that

D D X D 2D D D D D

D is supposed to be a positive denite matrix. To guarantee this, we can either substitute D with the closest vector to D in L norm which renders X D   22  D >D D positive denite

2

D 

matrix, or directly nd the closest positive denite matrix to D . We choose the second method. Furthermore, the usual issue of estimating covariance matrix arises here as well, especially when a regime only has a short lasting period. To address this issue, we apply the denoising technique in [Laloux et al. (1999) ](#_page27_x66.89_y236.51)on the positive denite matrix derived earlier to estimate D .

The number of regimes of each asset is set as equal to that of the market index. We nd that univariate Markov switching model with more than three regimes often has one unstable regime

that lasts for a very short period and switches frequently and sometimes has one regime with clearly bimodal innovations distribution. Thus, it is desirable to limit the number of regimes smaller than 4, check unimodal distribution with Dip test and choose the one with the highest BIC value.

The procedure is summarized as follows.

Step 1: Fit the univariate Markov regime-switching GARCH model with t innovation on the index return and extract the innovations and the sample path of regimes.

Step 2: Estimate common tail parameters D ;D in each regime.

12

Step 3: Fit univariate model on each asset and extract the innovations. q ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.008.png)

Step 4: Estimate skewness parameters D for assets in each regime, calculate D = 1   D 2( 2  D ). 2D

Step 5: Calculate the matrix diag( D ) 1(X D   22  D > D )diag( D ) 1, nd the closest

D

positive denite matrix and apply the denoising technique Dtoestimate D .

3. Simulation

To conduct simulation with the calibrated model, we follow the procedures specied below.

Step 1: Simulate S sample paths of standard deviation of N assets for T days with the tted model. Step 2: Simulate S sample paths of a Markov chain D with the market's transition matrix.

Calculate the total number of each regime in all sample paths.

Step 3: Draw i.i.d. samples from stdMNTS distribution in each regime. The number of samples is determined by the calculation in Step 2. To draw one sample, we follow the procedure below.

Step 3.1: Sample from multivariate normal distribution N(0,D ).

Step 3.2: Sample from the tempered stablepsubordinator T with parameters D and D .![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.009.png)

Step 3.3: Calculate X = D (T   1) + T( D D ).

Step 4: Multiply the standard deviation in Step 1 with standard joint innovations in Step 3 accord- ingly. Add regime-specic mean D to get simulated asset returns.

4  Portfolio<a name="_page12_x91.80_y334.29"></a> Optimization

In this section, we discuss issues on portfolio optimization.

1. Problem Formulation

Conditioned on given sample path(s), classical portfolio optimization is formulated as a trade-o between risk and return

min W(R(x;t;!)jt 2 [0;T]; ! 2 )

x

s.t. E [R(x;T;!)j! 2 ] d;

x 2 V;

where d is the benchmark return, R(x;t;!) is the portfolio return at time t 2 [0;T] in given sample paths ! 2 , W(R(x;t;!)jt 2 [0;T]) is a risk measure of R(x;t;!) for time t 2 [0;T] estimated based on given sampleP paths , and x = (x1;:::;xn) is the allocation vector of n assets. A typical setting of V is fxj N x = 1;x 0g, meaning that short selling is not allowed.

i=1 i i

2. Discussion on Risk Measures and Constraint

If the historical sample paths of asset returns are used as input to the CVaR optimization, we minimize the CVaR of daily portfolio return from time t = 1 to t = T. In the setting where we use simulation as input, we can choose to minimize the CVaR of daily returns from time t = 1 to t = T or CVaR of compounded returns at time t = T. We can set constraints on average daily returns from time t = 1 to t = T or compounded portfolio return at time t = T. Notice that the daily return in the simulation of GARCH model is not i.i.d. Furthermore, it is reasonable to focus

on the the return at the nal time. Thus, we choose to minimize the CVaR of return at time t = T

13

instead of return from time t = 1 to t = T subject to constraint on compounded portfolio return

at time t = T.

The denition of drawdown needs some clarication as well. The portfolio drawdown at time t is dened in [(13).](#_page6_x502.49_y273.02)

Xm

DDm;s := max Q(x;tj ;!s)   Q(x;tm;!s) = r(x;ti;ws);

j2f0;1;2;;mg

i=h

where h = argmaxj2f0;1;2;;mg Q(x;tj ;!s), is the sum of daily returns from its peak. It is somewhat unconventional at rst sight compared with the absolute drawdown dened by

Ym

absDDm;s := max P (x;tj ;!s)   P (x;tm;!s) = P (x;th;!s) (1 + r(x;ti;ws))

j2f0;1;2;;mg

i=h

and the relative drawdown dened by

m;s j2fmax0;1;2;j2f;m0;1g;2;;mg P (x;tj ;!s) iY=mh(1 + r(x;ti;ws));

max P (x;tj ;!s)   P (x;tj ;!s)

reDD :=~~ =

where h = argmaxj2f0;1;2;;mg Q(x;tj ;!s). CDaR is essentially an average of drawdowns that exceed the threshold. CDaR dened in [(16) with](#_page7_x502.49_y137.76) DDm;s satises good properties such as nonneg- ativity, insensitivity to constant shift, positive homogeneity and convexity (See Chec[khlov et al. 2005),](#_page26_x66.89_y567.27) which gives great advantage in developing optimization techniques. CDaR can be dened in a similar way with absDDm;s and reDDm;s.

It is possible to use the algorithm designed for CDaR dened by DDm;s to minimize CDaR dened by absDDm;s. By substituting the input r(x;ti;ws) with P (x;ti;!s)   P (x;ti 1;!s), the calculation of DDm;s becomes

Xm

P (x;ti;!s)   P (x;ti 1;!s) = absDDm;s

i=h

where h = argmaxj2f0;1;2;;mg Q(x;tj ;!s). However, it is obvious from the denitions that CDaR dened absDDm;s and reDDm;s do not satisfy basic axioms such as positive homogeneity.

Another drawback of absolute drawdown is that when we consider a long time period, drawdowns could vary greatly in absolute value but be close in relative value, the latter of which we are more concerned about. Uncompounded cumulative return is determined by rate of returns regardless of the price. This discussion justies our denition of drawdown with DDm;s.

5  Empirical<a name="_page13_x91.80_y558.10"></a> Study

In this section, we demonstrate the superiority of our approach with various in-sample and out-of- sample tests. We conduct model tting, sample path simulation and portfolio optimization. In the in-sample test, we conduct a KS test on the marginal NTS distribution and marginal t-distribution to show that the NTS distribution has a much better t on the innovations. We also provide the transition matrix and the correlation matrices of the joint innovations in each regime. In the

14

out-of-sample test, we use various performance measures and visualizations for the rolling-window studies in recent years to show the outperformance of our portfolio.

For diversication purposes, we set the range of weights as [0:01;0:15]. A case study in [Krokhmal et al. (2002)](#_page27_x66.89_y268.39) found that without constraints on weights, the optimal portfolio only consists of a few assets among hundreds. Investors often empirically categorize the market as bull, bear and sideways market. [Haas et al. (2004) exp](#_page26_x66.89_y276.36)eriments with two and three regimes. We limit the number of regimes to be smaller than or equal to three. The Dip test is conducted on innovations to ensure unimodal innovation distribution. Starting tting with three regimes, a model with fewer regimes is used instead when the p-value is lower than 0:1 or have a regime lasting shorter than 40 days in total. Preliminary tests show that without these selection criteria, the model would have a risk of overt in some cases. For example, the innovation could be multimodal, and the regime switches hundreds of times within the tested period. The phenomena is even more pronounced when the number of regimes is higher than three. To be concise in notation, we denote the portfolios in a convenient manner. For example, 0.9-CDaR portfolio denotes the optimal portfolio derived from the optimization with 0.9-CDaR as the risk measure. The standard deviation optimal portfolio is the optimal portfolio in the classical Markowitz model that maximizes Sharpe ratio, which we also denoted by mean-variance (MV) optimal portfolio. The word optimal is sometimes omitted. Since we simulate returns for 10 days, all CVaR with varying condence levels are calculated with the simulated cumulative returns on the 10-th day. We omit the time and denote the optimal portfolio simply as CVaR portfolio.

1. Data

The data are comprised of the adjusted daily price of DJIA index, 29 of the constituents of DJIA Index and three ETFs of bond, gold and shorting index (Tickers: TMF, SDOW and UGL) from January 2010 to September 2020. One constituent DOW is removed because it is not included in the index throughout the time period. Since we use 1764 trading days' (about 7 years) data to t the model, the time period for out-of-sample rolling-window test is from January 2017 to September 2020, which includes some of the most volatile periods in history caused by the a pandemic and some trade tensions. By reweighting the index constituents, it can be regarded as an enhanced index portfolio.

2. Performance Measures

Various performance measures are discussed in [Biglova et al. (2004), Rac](#_page27_x66.89_y312.23)[hev et al. (2008), ](#_page27_x66.89_y148.84)[Cheridito and Kromer (2013).](#_page27_x66.89_y344.11) Similar to Markowitz Model, an ecient frontier can be derived by changing the value of constraint. Each portfolio on the ecient frontier is optimal in the sense that no portfolio has a higher return with the same value of risk measure. In this paper, we refer to the portfolio with the highest performance ratio E[R(x;T;)] as an optimal portfolio and the others on the

W (R(x;t;)jt2[0;T ])

ecient frontier as suboptimal portfolios. Note that E [R(x;T; )] is CVaR (R(x;T; )). Thus, the mean-CVaR ratio can be regarded as a special case of the Rachev ratio CVCV0aRaR1 (R(x;T;)) . We test

with 1 = 2 = 0:1 to focus on the distribution tails. 2 (R(x;T;))

15

3. In-Sample Tests

We present various in-sample test results. The time period during which 2-regime model is rst selected is used in tting is from 30 April 2010 to 5 May 2017. 100 days is classied as regime 1, and 1665 days is classied as regime 2. The standard deviation of the DJIA index is 0:00217 in regime 1 and 0:00801 in regime 2. Regime 2 is more volatile than regime 1. One might expect that the market is in a less volatile regime longer and has a spiked standard deviation during a short

but much more volatile regime. It is not the case in this tested period according to our model.

1. Kolmogorov{Smirnov Tests on Marginal Distributions

We conduct a Kolmogorov{Smirnov test (KS test) on the marginal distributions of the joint innova- tion of MRS-MNTS-GARCH model in the tested period. The results are presented in Table 1. For comparison, we also t multivariate t-distribution on the joint innovations and report the results

of KS tests on the marginal distributions. The degree of freedom of multivariate t-distribution in regime 1 and regime 2 are 5:34 and 5:68, respectively. Note that the marginal distribution of stdMNTS distribution is still NTS distribution. Since we assume common parameters and in MNTS distribution, we report the parameter of each asset in both regimes. The data are rounded

to 3 decimals place.

For NTS distribution, there are 5 p-values smaller than 0:05. For t-distribution, there are 31 p-values smaller than 0:05. Most of the rejections correspond to Regime 2, indicating that the marginal t-distribution is outperformed by marginal NTS distribution in describing the return in the more volatile regime. We can also observe that varies signicantly in dierent regimes. Generally, for all assets, in regime 1 has larger absolute values.

2. Transition Matrix and Denoised Correlation Matrices of Joint Innovation

The transition matrix of the innovations is presented in Table 2. [The](#_page17_x91.80_y89.06) self-transition probability in two regimes are close, and both are high.

We also provide the denoised correlation matrices of stdMNTS innovations in two regimes in Table [3.](#_page18_x91.80_y89.06) Since there are two regimes identied in this period, we combine the two correlation matrices for easier comparison. The upper triangle of the matrix is the upper triangle of correlation matrix in regime 1, while the lower triangle of the matrix is the lower triangle of correlation matrix in regime 2. We nd that the innovations have distinctively dierent correlation matrices in two regimes, validating the regime-switching assumption. The innovations are highly correlated in regime 2, which corresponds to more volatile periods.

4. Out-of-Sample Tests

We conduct out-of-sample tests to demonstrate the outperformance of the optimal portfolios. We use 3 types of risk measures with di erent condence levels in the optimization, namely, maximum drawdown, 0.7-CDaR, 0.3-CDaR, average drawdown, 0.5-CVaR, 0.7-CVaR, 0.9-CVaR and standard deviation. Note that 0-CVaR is equal to the expected return, which does not make sense as a risk measure. Minimizing -CVaR with small means that we include the positive part of the return distribution as risk. This is a drawback of standard deviation, and thus we set at 0.5, 0.7, and 0.9 to demonstrate the superiority.

16

<a name="_page16_x91.80_y89.06"></a>Table 1: Kolmogorov{Smirnov tests on marginal distributions of joint innovation



||Regime|beta|KS Statistics of NTS||p-value|KS Statistics of t|p-value|
| :- | - | - | - | :- | - | - | - |
|<p>AAPL AMGN AXP BA CAT CRM CSCO CVX DIS GS HD HON IBM INTC JNJ JPM KO MCD MMM MRK</p><p>MSFT</p><p>NKE PG TLT TMF TRV UGL UNH V</p><p>VZ WBA WMT</p>|<p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2 1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p><p>1</p><p>2</p>|<p>2\.048 0.038</p><p>1\.133 0.139 -0.513 -0.021 -1.129 -0.075</p><p>1\.681 0.069 -0.861 0.095</p><p>1\.297 0.058 -1.523 -0.055 -0.644 0.025</p><p>1\.274 -0.046 -1.431 0.025 -1.496 0.131</p><p>0\.64 -0.019</p><p>-1.551 0.061</p><p>1\.87 -0.013</p><p>1\.857 0.026 -1.674 0.013 -1.956 -0.005</p><p>0\.658 -0.1 2.367</p><p>0\.076 -2.175</p><p>0\.26 1.652</p><p>0\.079 1.035 0.12</p><p>-0.283</p><p>-0.161 -0.273</p><p>-0.152 -1.532</p><p>-0.033 1.139</p><p>-0.074 1.543</p><p>0\.054 1.45</p><p>0\.016 -0.406 -0.043</p><p>1\.011 0.166</p><p>1\.804 -0.047</p>|<p>0\.129 0.018</p><p>0\.054 0.012</p><p>0\.022 0.022 0.016 0.009</p><p>0\.083 0.012 0.041 0.032</p><p>0\.084 0.043 0.064 0.019 0.115 0.014 0.038 0.014 0.035</p><p>0\.01 0.064 0.015 0.023 0.019</p><p>0\.045 0.008</p><p>0\.055 0.008</p><p>0\.023 0.008 0.072 0.009 0.067 0.022 0.019 0.014 0.156 0.013</p><p>0\.176 0.016</p><p>0\.05 0.022</p><p>0\.03 0.015</p><p>0\.056 0.036</p><p>0\.055 0.035</p><p>0\.055 0.011 0.066 0.012</p><p>0\.05 0.012 0.044 0.025 0.115 0.017 0.026 0.022</p><p>0\.08 0.016</p>|17|<p>0\.067 0.624 0.917 0.955</p><p>1 0.392</p><p>1 0.999</p><p>0\.476 0.973 0.993 0.071</p><p>0\.454 0.004 0.781 0.563 0.132 0.878 0.998 0.917 0.999 0.995 0.783 0.843</p><p>1 0.587</p><p>0\.981 1</p><p>0\.908</p><p>1 1</p><p>1 0.656 0.999 0.742 0.396</p><p>1 0.882 0.013 0.928</p><p>0\.003 0.753 0.956 0.416</p><p>1 0.824</p><p>0\.897 0.025</p><p>0\.907 0.036</p><p>0\.91 0.988 0.749 0.973 0.951 0.962 0.985</p><p>0\.26 0.131 0.716</p><p>1 0.368</p><p>0\.52 0.8</p>|<p>0\.125 0.055</p><p>0\.058 0.045 0.027</p><p>0\.06 0.039 0.041</p><p>0\.09 0.043</p><p>0\.045 0.071</p><p>0\.066 0.08</p><p>0\.063</p><p>0\.029 0.103 0.053 0.031 0.036 0.056 0.047</p><p>0\.064 0.054 0.041 0.057</p><p>0\.085 0.044</p><p>0\.109 0.041</p><p>0\.083 0.041 0.078 0.047</p><p>0\.092 0.061 0.025 0.054</p><p>0\.157 0.046</p><p>0\.165 0.057</p><p>0\.1 0.059 0.062 0.055</p><p>0\.042 0.028</p><p>0\.041 0.028</p><p>0\.058 0.048 0.068 0.051 0.098 0.051</p><p>0\.05 0.061 0.109 0.033 0.048 0.062</p><p>0\.076 0.054</p>|<p>0\.081 0 0.875</p><p>0\.002 1</p><p>0 0.996 0.007 0.369 0.004 0.982 0 0.75 0 0.791 0.11 0.225 0</p><p>1 0.026 0.901 0.001</p><p>0\.776 0</p><p>0\.993 0</p><p>0\.443</p><p>0\.003 0.174</p><p>0\.007 0.464</p><p>0\.007 0.546 0.001</p><p>0\.343 0</p><p>1</p><p>0 0.013 0.002</p><p>0\.007 0 0.258 0 0.815 0</p><p>0\.992</p><p>0\.144 0.993</p><p>0\.135 0.864</p><p>0\.001 0.721 0 0.274 0</p><p>0\.955 0 0.17</p><p>0\.052 0.966 0</p><p>0\.582</p><p>0</p>|

For NTS distribution, there are 5 p-values smaller than 0:05. For t-distribution, there are 31 p-values smaller than 0:05. Most of the rejections correspond to Regime 2, indicating that the marginal t- distribution is outperformed by marginal NTS distribution in the more volatile regime.

<a name="_page17_x91.80_y89.06"></a>Table 2: Transition matrix of joint innovation

regime 1 regime 2![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.010.png)

regime 1 0.8538 0.1462 regime 2 0.0301 0.9699

This table presents the transition matrix of the joint innovation of MRS-MNTS-GARCH model.

The rolling window technique is employed with 10-day forward-moving time window. In each time window, we simulate 10,000 sample paths of length 10 with the tted model. The simulation is used as input to portfolio optimization. The portfolio is held for 10 trading days before rebalancing. The portfolio optimization is performed with software Portfolio Safeguard (PSG) with precoded numerical optimization procedures.

1. Optimal Portfolios

We report the performance of the optimal portfolios in various forms. Due to a large number of risk measures, we sometimes only present representative ones in graphs for better visualization. The other optimal portfolios have similar results.

Performance Measures In Table [4, ](#_page19_x91.80_y89.06)we measure the performance of the optimal portfolios by various performance ratios. The row names are the risk measures used in portfolio optimization. The columns are the performance measures. For example, the 0.3-CDaR portfolio is optimized every 10 days to maximize the ratio of expected cumulative return over 0.3-CDaR. Note that 0-CDaR

is the average drawdown while 1-CDaR is the maximum drawdown. The risk measure standard deviation is studied in the classical Markowitz model, of which the optimization is also called MV optimization.

We can observe that the optimal portfolios of CDaR and CVaR measures have very close per- formance regardless of performance measures. The condence level has a marginal impact on the ratios. Considering all the ratios, 0.3-CDaR portfolio and 0.5-CVaR portfolio are the best among the ten portfolios. 0.3-CDaR portfolio outperforms the others in all return-CVaR ratios, while 0.5- CVaR portfolio outperforms the others in return-CDaR ratios, slightly but consistently. All of the optimal portfolios of CDaR and CVaR measures consistently outperform the MV optimal portfolio, which signicantly outperforms the DJIA and the equally weighted portfolio.

Log Cumulative Return In Figure [1, ](#_page20_x91.80_y218.95)we plot the time series of log cumulative returns of the optimal portfolios with dierent risk measures in out-of-sample tests to visualize the performance. The legend shows colors that represent dierent risk measures used in each portfolio optimization. We use log base 10 compounded cumulative returns as a vertical axis so that the scale of relative drawdown can be easily compared in graphs by counting the grids. The performance with dierent risk measures is reported separately. The labels in the legend show the condence level of the risk measure. The names of the subgures indicate the risk measures used in the optimization. DJIA index and the equally weighted portfolio are included in each graph for comparison.

18

![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.011.png) ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.012.png)

<a name="_page18_x91.80_y89.06"></a>19

<a name="_page19_x91.80_y89.06"></a>Table 4: Performance ratios of optimal portfolios with dierent risk measures![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.013.png)

Mean0-CDaRReturn Mean0:3-CDaRReturn Mean0:7-CDaRReturn Mean1-CDaRReturn Mean0:5-CVReturnaR Mean0:7-CVReturnaR Mean0:9-CVReturnaR Sharpe Ratio Rachev Ratio![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.014.png)

0-CDaR 0:072 0:051 0:027 0:008 0:258 0:156 0:077 0:117 0:965 0.3-CDaR 0:074 0:052 0:027 0:008 0:262 0:159 0:078 0:119 0:968 0.7-CDaR 0:073 0:052 0:027 0:008 0:260 0:158 0:077 0:118 0:965 1-CDaR 0:075 0:053 0:028 0:007 0:259 0:157 0:078 0:117 1:012 0.5-CVaR 0:076 0:054 0:028 0:007 0:259 0:158 0:076 0:120 1:002 0.7-CVaR 0:072 0:051 0:027 0:007 0:257 0:157 0:077 0:121 1:000 0.9-CVaR 0:071 0:050 0:027 0:007 0:243 0:147 0:072 0:116 0:986

Standard Deviation 0:064 0:045 0:024 0:006 0:238 0:145 0:071 0:109 0:966 DJIA 0:011 0:008 0:004 0:001 0:064 0:040 0:019 0:033 0:855

Equal Weight 0:032 0:023 0:011 0:003 0:136 0:083 0:037 0:065 0:900![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.015.png)

The column names are dierent ratios used to measure the performance. The row names show the risk measures used in the portfolio optimization. The DJIA index and the equally weighed portfolio are included as benchmarks.

As can be observed in the graphs, all the optimal portfolios follow a similar trend, though they dier in overall performance. They tend to alleviate both left tail and right tail events. CVaR optimal portfolios have higher cumulative returns than CDaR optimal portfolios. The condence level has only a marginal impact. CVaR optimal portfolios with condence levels 0.5 and 0.7 are almost indistinguishable. CDaR optimal portfolios with condence levels 0.5, 0.7 and 0.9 are almost indistinguishable.

Relative Drawdown Since the CVaR and CDaR risk measures only concern the tail behavior of a portfolio, we plot the relative drawdown of the optimal portfolios in out-of-sample testing period in Figure [2 ](#_page21_x91.80_y104.88)to demonstrate their ability to alleviate extreme left tail events. Due to a large number of optimal portfolios with dierent risk measures, we only plot 0-CDaR, 0.5-CVaR and MV optimal portfolios here for better visualization. The others have similar results. The 0-CDaR, 0.5-CVaR and MV optimal portfolios have signicantly smaller relative drawdown most of the time in the out-of-sample test, especially in year 2020. 0-CDaR and 0.5-CVaR optimal portfolios are slightly better than the MV optimal portfolio.

Portfolio Return Distribution In Figure [3, ](#_page21_x91.80_y418.80)we plot the kernel density estimation on the return distribution. To better compare the tails of the return distribution, we also plot the log base 10 density. We can easily observe that the optimal portfolios are very close and alleviate both right and left tail events. Unlike standard deviation (MV) optimal portfolio, 0.3-CDaR and 0.5-CVaR portfolio have thinner tails on both sides than DJIA and the equally weighted portfolio. 0.3-CDaR and standard deviation portfolio have a higher peak than the equally weighted portfolio. Among the three optimal portfolios, the 0.5-CVaR portfolio has the thinnest left tail and a fatter right tail than the other two optimal portfolios.

Allocation In Figure [4, ](#_page22_x91.80_y89.06)we report the time series of optimal weights of the 0-CDaR optimal portfolio as a representative case. The DJIA constituents are aggregated for better visualization. It is reasonable that when the total weight on DJIA constituents is high, the weights on shortselling ETF is low. The weights on ETFs hit the lower and upper bounds 0.01 and 0.15 in many periods, indicating that the constraints on weights are active in the optimizations.

20



|||||||||
| :- | :- | :- | :- | :- | :- | :- | :- |
|||||||||
||Eq DJI 0− 0.3 0.7 1− 0.5 0.7 0.9 sta|<p>ual Weight</p><p>A</p><p>CDaR −CDaR −CDaR CDaR −CVaR −CVaR −CVaR</p><p>ndard deviatio</p>|n|||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
0\.4 0.3 0.2 0.1 0.0

2017 2018 2019 2020

Date

<a name="_page20_x91.80_y218.95"></a>Figure 1: Log cumulative returns: this gure plots the time series of log cumulative return of optimal portfolios with dierent risk measures, the DJIA index and the equally weighted portfolio. The risk measures used in portfolio optimization are 0-CDaR, 0.3-CDaR, 0.7-CDaR, 1-CDaR, 0.5-CVaR, 0.7-CVaR, 0.9-CVaR and standard deviation.

21

0\.3−CDaR![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.016.png)

0\.3 0.5−CVaR

DJIA

Equal Weight

Standard Deviation 0.2

0\.1 0.0

2017 2018 2019 2020

Date

<a name="_page21_x91.80_y104.88"></a>Figure 2: Relative drawdown: this gure plots the relative drawdown paths of optimal portfolios with di erent risk measures, the DJIA index and the equally weighted portfolio. The risk measures include 0-CDaR, 0.5-CVaR and standard deviation.

80![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.017.png)

60

40

0\.3−CDaR 0.5−CVaR

20 Standard DeEqual Weightviation

DJIA

0

−0.10 −0.05 0.00 0.05 0.10

return

1) Kernel<a name="_page21_x91.80_y418.80"></a> density estimation: this gure plots the kernel density estimation of optimal portfolios with dierent risk measures, the DJIA index and the equally weighted portfolio. The risk measures in- clude 0-CDaR, 0.5-CVaR and standard deviation.

10-1

10-5![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.018.png)

0\.3−CVaR 0.5−CVaR

10-9 Standard DeEqual Weightviation

DJIA

−0.10 −0.05 0.00 0.05 0.10

return

2) log kernel density estimation: this gure plots the log kernel density estimation of optimal portfo- lios with dierent risk measures, the DJIA index and the equally weighted portfolio. The risk measures in- clude 0-CDaR, 0.5-CVaR and standard deviation.

Figure 3: Kernel density estimation and log kernel density estimation

22

1\.00 0.75 0.50 0.25 0.00![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.019.png)

2017 2018 2019 2020

Date

![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.020.png) DJIA Constituents ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.021.png) SDOW ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.022.png) TMF ![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.023.png) UGL

<a name="_page22_x91.80_y89.06"></a>Figure 4: Allocation: this gure plots the weights of 0-CDaR optimal portfolio on DJIA constituents and 3 ETFs.

2. Robustness to Suboptimality in Optimization

So far, we have been studying the optimal portfolios that maximize performance ratios. In this section, we study the sensitivity of the performance by comparing suboptimal portfolios with the optimal ones. We show that the portfolio with tail risk measure is more robust to suboptimality in optimization than the mean-variance portfolio. The performance ratios of CDaR and CVaR optimal portfolios are shown to be not sensitive to changing the value of return constraint, while

the performance ratios of mean-variance optimal portfolio shows signicant change. The graphs of log cumulative return show that the suboptimal portfolios follow a similar trend, sometimes overlapping with each other.

We use 9 portfolios with dierent constraints on return to approximate the ecient frontier for\
each risk measure. For example, in each 0.3-CDaR optimization, we perform 10 optimizations with\
varying constraints on return. The portfolio with the highest return-risk ratio is the approximated\
optimal portfolio. We denote the portfolio that has n lower level of constraint on return as level Ln suboptimal portfolio, the one that has n higher level of constraint on return as level Hn suboptimal portfolio. When a certain optimization is unfeasible, we set the allocation the same as that of a\
lower level. The constraints on return are (0.002, 0.010, 0.020, 0.030, 0.035, 0.040, 0.045, 0.050, 0.060, 0.065). For example, when the portfolio with constraint 0.050 on return has the highest\
performance ratio among the 10 portfolios, it is labeled as the optimal portfolio. Accordingly, the\
portfolio with one-level higher constraint 0.060 is labeled H1. In this case, H2 to H4 have the same      constraint 0.065, since there is no optimization performed with higher constraint. Note that at each\
rebalance, the optimal portfolio changes, so do portfolios of other levels, i.e., constraint 0.060 may\
no longer be optimal. The performance of each label is measured with portfolios of corresponding

23

level determined at each rebalance.

We report suboptimal portfolios with risk measures of 0-CDaR, 0.5-CVaR and standard de- viation in Figure 5[ and](#_page24_x91.80_y177.20) Table 5[ as](#_page23_x91.80_y220.52) representative cases. We nd that the optimal portfolio is consistently too conservative for all risk measures and input. That is, with the same risk measure, suboptimal portfolios with a higher constraint on return achieve higher performance ratios than the optimal portfolio. From H4 to L4, the ratios do not show a pattern of rst increasing the decreasing as expected. In other words, the out-of-sample ecient frontiers are usually non-convex with irregular shapes. Overall, the performance ratios of CDaR and CVaR optimal portfolios are shown to be not sensitive to changing the value of return constraint, while the performance ratios of mean-variance optimal portfolio shows signicant change.

<a name="_page23_x91.80_y220.52"></a>Table 5: Performance ratios of suboptimal portfolios with dierent risk measures

Mean0-CDaRReturn Mean0:3-CDaRReturn Mean0:7-CDaRReturn Mean1-CDaRReturn Mean0:5-CVReturnaR Mean0:7-CVReturnaR Mean0:9-CVReturnaR Sharpe Ratio Rachev Ratio![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.024.png)![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.025.png)

0-CDaR L4

L3 L2

L1 optimal H1

H2 H3

H4 0.5-CVaR L4![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.026.png)

L3 L2

L1 optimal

H1

H2

H3

H4\
Standard![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.027.png) Deviation

L4

L3

L2

L1 optimal

H1

H2

H3

H4 DJIA![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.028.png)

Equal Weight![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.029.png)

0:061 0:043

0:058 0:041

0:061 0:043

0:062 0:044 0:072 0:051

0:074 0:052

0:082 0:058

0:087 0:061

0:087 0:062

0:073 0:052

0:074 0:052

0:074 0:052

0:075 0:053 0:076 0:054

0:075 0:053

0:075 0:053

0:073 0:052

0:071 0:050

0:041 0:029 0:042 0:030 0:049 0:035 0:059 0:042

0:064 0:045 0:069 0:049 0:071 0:050 0:074 0:052 0:073 0:052

0:011 0:008 0:032 0:023

0:023 0:008 0:021 0:007 0:023 0:007 0:023 0:007 0:027 0:008 0:028 0:008 0:030 0:008 0:032 0:009 0:032 0:009

0:027 0:006 0:027 0:007 0:027 0:007 0:027 0:007 0:028 0:007 0:027 0:007 0:027 0:007 0:027 0:007 0:026 0:007

0:015 0:004 0:016 0:004 0:019 0:005 0:022 0:006 0:024 0:006 0:026 0:007 0:027 0:007 0:028 0:007 0:027 0:007 0:004 0:001 0:011 0:003

0:239 0:146 0:232 0:142 0:236 0:144 0:236 0:144 0:258 0:156 0:251 0:151 0:259 0:157 0:267 0:161 0:268 0:162

0:252 0:154 0:253 0:155 0:253 0:155 0:256 0:156 0:259 0:158 0:255 0:155 0:256 0:156 0:256 0:155 0:254 0:154

0:176 0:110 0:177 0:111 0:196 0:122 0:225 0:138 0:238 0:145 0:232 0:141 0:232 0:141 0:237 0:144 0:234 0:142 0:064 0:040 0:136 0:083

0:074 0:113 0:965 0:071 0:108 0:959 0:072 0:110 0:960 0:072 0:110 0:959 0:077 0:117 0:965 0:073 0:115 0:968 0:076 0:120 0:993 0:078 0:124 0:995 0:079 0:125 0:989

0:074 0:114 1:011 0:075 0:115 1:011 0:075 0:116 1:008 0:076 0:118 1:006 0:076 0:120 1:002 0:075 0:118 0:990 0:075 0:119 0:987 0:075 0:119 0:982 0:074 0:117 0:977

0:055 0:084 0:990 0:056 0:083 1:005 0:062 0:092 1:013 0:069 0:103 1:005 0:071 0:109 0:966 0:069 0:108 0:972 0:069 0:110 0:983 0:070 0:113 0:986 0:069 0:112 0:980 0:019 0:033 0:855 0:037 0:065 0:900

This table presents the performance ratios of suboptimal portfolios with dierent risk measures. The risk measures are shown in the row names: 0-CDaR, 0.5-CVaR and standard deviation. The constraint on return is adjusted from high to low (H4 to L4) to show the impact of suboptimality. Portfolio optimization with tail risk measures demonstrates smaller variation in out-of-sample performance ratios compared with mean-variance portfolio.

The portfolios have increasing returns as well as risk from L1 to H4. The realized paths follow a similar trend and rarely cross. The optimal portfolios, as expected, are in the medium part of all paths. The 0.5-CVaR suboptimal portfolios have almost identical performance. Some paths are not visible due to overlap. For example, the constraints on the return of H4 are sometimes not feasible, leading to the same performance with H3 portfolio.

24

0\.4![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.030.png)

Equal Weight H1

H2

H3

0\.3 H4

L1

L2

L3

L4

2. Optimal

0\.1

0\.0

2017 2018 2019 2020

Date

1) 0-CDaR<a name="_page24_x91.80_y177.20"></a> Suboptimal portfolios: this gure plots the paths of 0-CDaR suboptimal portfolios from level H1 to L4, and the equally weighted portfolio.

0\.4![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.031.png)

Equal Weight H1

H2

H3

3. H4

   L1

   L2

   L3

   L4

2. Optimal

0\.1

0\.0

2017 2018 2019 2020

Date

2) 0.5-CVaR Suboptimal portfolios: this gure plots the paths of 0.5-CVaR suboptimal portfolios from level H1 to L4, and the equally weighted port- folio.

0.4

Equal Weight H1![](Aspose.Words.0eaaf39d-082d-4756-9201-20b18bf8c405.032.png)

H2

H3

3. H4

   L1

   L2

   L3

   L4

0\.2 Optimal

0\.1

0\.0

2017 2018 2019 2020

Date

3) MV suboptimal portfolios: this gure plots the paths of mean variance suboptimal portfolios from level H1 to L4, and the equally weighted portfolio.

Figure 5: Time series of log cumulative return of suboptimal portfolios with dierent risk measures

25

6  Conclusions

We propose the MRS-MNTS-GARCH model that is suciently exible to accommodate fat tails, skewness and regime switch in asset returns. The model is used to simulate sample paths of portfolio returns, which serves as input to portfolio optimization with tail risk measures. We conduct various in-sample and out-of-sample tests to demonstrate the eectiveness of our approach. In-sample

tests show that the NTS distribution ts the innovations with high accuracy compared with t- distribution. Out-of-sample tests show that our approach signicantly improves the performance

of optimal portfolios measured by performance ratios and it successfully mitigates left tail risk. We

also nd that out-of-sample performance ratios of the portfolios with tail risk measures are more robust to suboptimality on the ecient frontier compared with mean-variance portfolio.

References

<a name="_page25_x66.89_y265.28"></a>I. Koponen. Analytic approach to the problem of convergence of truncated Levy ights towards

the gaussian stochastic process. Physical Review E, 52:1197{1199, 1995.

<a name="_page25_x66.89_y297.16"></a>S. I. Boyarchenko and S. Z. Levendorskii. Option pricing for truncated Levy processes. International

Journal of Theoretical and Applied Finance, 3:549{552, 2000.

<a name="_page25_x66.89_y329.04"></a>P. Carr, H. Geman, D. Madan, and M. Yor. The ne structure of asset returns: An empirical

investigation. Journal of Business, 75(2):305{332, 2002.

<a name="_page25_x66.89_y360.92"></a>O.E. Barndor-Nielsen and S.Z. Levendorskii. Feller processes of normal inverse gaussian type.

Journal of Business & Economic Statistics, 1(3):318{331, 2001.

<a name="_page25_x66.89_y392.80"></a>Neil Shephard, Ole E. Barndor-Nielsen, and University of Aarhus. Normal modied stable pro-

cesses. Technical Report 72, 2001.

<a name="_page25_x66.89_y424.68"></a>Young Shin Kim, Rosella Giacometti, Svetlozar T. Rachev, Frank J. Fabozzi, and Domenico

Mignacca. Measuring nancial risk and portfolio optimization with a non-Gaussian multivariate model. Annals of Operations Research, 201:325{342, 2012.

<a name="_page25_x66.89_y468.52"></a>Tetsuo Kurosaki and Young Shin Kim. Foster-Hart optimization for currency portfolios. Studies in

Nonlinear Dynamics & Econometrics, 23(2):1{15, 2018.

<a name="_page25_x66.89_y500.40"></a>Abhinav Anand, Tiantian Li, Tetsuo Kurosaki, and Young Shin Kim. Foster{Hart optimal portfo-

lios. Journal of Banking & Finance, 68:117{130, 2016.

<a name="_page25_x66.89_y532.28"></a>Young Shin Kim. Portfolio optimization and marginal contribution to risk on multivariate normal

tempered stable model. Annals of Operations Research, 2022. doi: https://doi.org/10.1007/ s10479-022-04613-7.

<a name="_page25_x66.89_y576.11"></a>Robert F. Engle. Autoregressive conditional heteroscedasticity with estimates of the variance of

united kingdom ination. Econometrica, 50(4):987{1007, 1982.

<a name="_page25_x66.89_y607.99"></a>Tim Bollerslev. Generalized autoregressive conditional heteroskedasticity. Journal of Econometrics,

31(3):307{327, 1986.

26

<a name="_page26_x66.89_y93.05"></a>Young Shin Kim, Svetlozar T. Rachev, Michele Leonardo Bianchi, Ivan Mitov, and Frank J. Fabozzi.

Time series analysis for nancial market meltdowns. Journal of Banking & Finance, 35(8):1879{ 1891, 2011.

<a name="_page26_x66.89_y136.88"></a>Yanlin Shi and Lingbing Feng. A discussion on the innovation distribution of the Markov regime-

switching GARCH model. Economic Modelling, 23:278{288, 2016.

<a name="_page26_x66.89_y168.77"></a>James D. Hamilton. Specication testing in markov-switching time-series models. Journal of

Econometrics, 70:127{157, 1996.

<a name="_page26_x66.89_y200.65"></a>Juri Marcucci. Forecasting stock market volatility with regime-switching garch models. Studies

in Nonlinear Dynamics & Econometrics, 9(4), 2005. doi: doi:10.2202/1558-3708.1145. URL [https://doi.org/10.2202/1558-3708.1145.](https://doi.org/10.2202/1558-3708.1145)

<a name="_page26_x66.89_y244.48"></a>Jan S. Henneke, Svetlozar T. Rachev, Frank J. Fabozzi, and Metodi Nikolov. MCMC-based esti-

mation of Markov switching ARMA{GARCH models. Applied Economics, 43(3):259{271, 2011.

<a name="_page26_x66.89_y276.36"></a>Markus Haas, Stefan Mittnik, and Marc S. Paolella. A new approach to Markov-switching GARCH

models. Journal of Financial Econometrics, 2(4):493{530, 2004.

<a name="_page26_x66.89_y308.24"></a>Tim Bollerslev. Modelling the coherence in short-run nominal exchange rates: A multivariate

generalized arch model. The Review of Economics and Statistics, 72(3):498{505, 1990. ISSN 00346535, 15309142. URL [http://www.jstor.org/stable/2109358.](http://www.jstor.org/stable/2109358)

<a name="_page26_x66.89_y352.08"></a>Robert Engle. Dynamic conditional correlation: A simple class of multivariate generalized autore-

gressive conditional heteroskedasticity models. Journal of Business & Economic Statistics, 20 (3):339{350, 2002.

<a name="_page26_x66.89_y395.91"></a>Markus Haas and Ji-Chun Liu. A multivariate regime-switching GARCH model with an applica-

tion to global stock market and real estate equity returns. Studies in Nonlinear Dynamics & Econometrics, 2(4):493{530, 2004.

<a name="_page26_x66.89_y439.75"></a>Pavlo Krokhmal, Stanislav Uryasev, and Jonas Palmquist. Portfolio optimization with conditional

value-at-risk objective and constraints. Journal of Risk, 4(2):43{68, 2001.

<a name="_page26_x66.89_y471.63"></a>R. Tyrrell Rockafellar and Stanislav Uryasev. Optimization of conditional value-at-risk. Journal of

Risk, 2(3):21{41, 2000.

<a name="_page26_x66.89_y503.51"></a>Sergey Sarykalin, Gaia Serraino, and Stan Uryasev. Value-at-risk vs. conditional value-at-risk in

risk management and optimization. INFORMS TutORials in Operations Research, 2014.

<a name="_page26_x66.89_y535.39"></a>Alexei Checkhlov, Stanislav Uryasev, and Mickael Zabarankin. Portfolio optimization with draw-

down constraints. Supply Chain and Finance, 2:209{228, 2004.

<a name="_page26_x66.89_y567.27"></a>Alexei Checkhlov, Stanislav Uryasev, and Mickael Zabarankin. Drawdown measure in portfolio

optimization. International Journal of Theoretical and Applied Finance, 8(1):13{58, 2005.

<a name="_page26_x66.89_y599.15"></a>Andrew E.B. Lim, J. George Shanthikumar, and Gah-Yi Vahn. Conditional value-at-risk in portfolio

optimization: Coherent but fragile. Operations Research Letters, 39(3):163{171, 2011.

27

<a name="_page27_x66.89_y93.05"></a>Maziar Sahamkhadam, Andreas Stephan, and Ralf Ostermark. Portfolio optimization based

on garch-evt-copula forecasting models. International Journal of Forecasting, 34(3):497{506, 2018. ISSN 0169-2070. doi: https://doi.org/10.1016/j.ijforecast.2018.02.004. URL [https: //www.sciencedirect.com/science/article/pii/S0169207018300396.](https://www.sciencedirect.com/science/article/pii/S0169207018300396)

<a name="_page27_x66.89_y148.84"></a>Svetlozar T. Rachev, Stoyan V. Stoyanov, and Frank J. Fabozzi. Advanced Stochastic Models,

Risk Assessment, and Portfolio Optimization: The Ideal Risk, Uncertainty, and Performance Measures. Wiley, 2008. ISBN 978-0-470-05316-4.

<a name="_page27_x66.89_y192.68"></a>Michele Leonardo Bianchi, Gian Luca Tassinari, and Frank J. Fabozzi. Riding with the four horse-

men and the multivariate normal tempered stable model. International Journal of Theoretical and Applied Finance, 19(04):1{28, 2016.

<a name="_page27_x66.89_y236.51"></a>Laurent Laloux, Pierre Cizeau, Jean-Philippe Bouchaud, and Marc Potters. Noise dressing of

nancial correlation matrices. Physical Review Letters, 83:1467{1470, 1999.

<a name="_page27_x66.89_y268.39"></a>Pavlo Krokhmal, Stanislav Uryasev, and Grigory Zrazhevsky. Comparative analysis of linear portfo-

lio rebalancing strategies: An application to hedge funds. The Journal of Alternative Investments, 5(1):10{29, 2002.

<a name="_page27_x66.89_y312.23"></a>A. Biglova, S. Ortobelli, S. Rachev, and S. Stoyanov. Dierent approaches to risk estimation in

portfolio theory. The Journal of Portfolio Management, 31:103{112, 2004.

<a name="_page27_x66.89_y344.11"></a>Patrick Cheridito and Eduard Kromer. Reward{risk ratios. Journal of Investment Strategies, 3(1):

3{18, 2013.

28
