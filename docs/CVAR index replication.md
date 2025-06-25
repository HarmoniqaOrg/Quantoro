**Applied Economics**

**ISSN: 0003-6846 \(Print\) 1466-4283 \(Online\) Journal homepage: https://www.tandfonline.com/loi/raec20**

**CVaR-LASSO Enhanced Index Replication \(CLEIR\):** **outperforming by minimizing downside risk** **Brian Gendreau, Yong Jin, Mahendrarajah Nimalendran & Xiaolong Zhong** **To cite this article:** Brian Gendreau, Yong Jin, Mahendrarajah Nimalendran & Xiaolong Zhong \(2019\): CVaR-LASSO Enhanced Index Replication \(CLEIR\): outperforming by minimizing downside

risk, Applied Economics, DOI: 10.1080/00036846.2019.1616072

**To link to this article: ** https://doi.org/10.1080/00036846.2019.1616072

Published online: 20 May 2019. 

Submit your article to this journal 

Article views: 44

View Crossmark data

Full Terms & Conditions of access and use can be found at

https://www.tandfonline.com/action/journalInformation?journalCode=raec20



APPLIED ECONOMICS

https://doi.org/10.1080/00036846.2019.1616072

CVaR-LASSO Enhanced Index Replication \(CLEIR\): outperforming by minimizing downside risk

Brian Gendreaua, Yong Jin

b, Mahendrarajah Nimalendrana and Xiaolong Zhongc

aDepartment of Finance, Insurance & Real Estate, Warrington College of Business Administration, University of Florida, Gainesville, FL, USA; bSchool of Accounting and Finance, The Hong Kong Polytechnic University, Hung Hom, Hong Kong; cAmazon ABSTRACT

KEYWORDS

Index-funds are one of the most popular investment vehicles among investors, with total assets Stochastic programming; 

indexed to the S&P500 exceeding $8.7 trillion at-the-end of 2016. Recently, enhanced-index-conditional value-at-risk; 

funds, which seek to outperform an index while maintaining a similar risk-profile, have grown in LASSO; enhanced indexation

popularity. We propose an enhanced-index-tracking method that uses the linear absolute shrink-JEL CLASSIFICATION

age selection operator \(LASSO\) method to minimize the Conditional Value-at-Risk \(CVaR\) of the G11; D81; C63

tracking error. This minimizes the large downside tracking-error while keeping the upside. Using historical and simulated data, our CLEIR method outperformed the benchmark with a tracking error of ,1%. The effect is more pronounced when the number of the constituents is large. Using 50–80 large stocks in the S&P 500 index, our method closely tracked the benchmark with an alpha 2:55%. 

I. Introduction

Index Funds \(ETFs\) and index tracking mutual funds attractive because of their low transaction Since the introduction of Index tracking funds by costs and the perception that they track their under-Vanguard in 1976, the industry has grown drama-lying indices closely. These expectations make index tically, accounting for 19.3% of all equity invest-replication a critical task for the institutions that ments at the end of 2016 \(Investment Company create these Index Funds and ETFs \(Blume and Institute \(US\) 2017\). Indexing or benchmarking Edelen 2002\). 

investments is popular because it provides inves-Currently, two main replication strategies exist in tors with simple passive investment vehicles that the market: full or exact replication, and sampling or have low transactions costs. This has led to a huge partial replication. The full replication strategy is demand for the creation and sale of index tracking straightforward but difficult to implement. A full funds \(Arnott, Hsu, and Moore 2005\). 

replication of the S&P500, for example, would Modern portfolio theory recommends that inves-require the fund to hold all 500 constituent stocks tors hold capitalization-weighted portfolios \(the at their capitalization weights at all times. Market market portfolio\) of risky assets, which according frictions including illiquidity, monitoring costs, to the CAPM model, is mean-variance efficient. 

redemptions and inflows, taxes, and dividends lead However, many papers, both in academia and indus-to frequent rebalancing that makes it difficult to try, have shown that capitalization-weighted indices implement a full replication strategy. The strategy such as the S&P500 and Russell 1000 do not lie on is even more expensive to implement for an index the efficient frontier. At the same time, it is, almost such as the Russell 2000 that has 2000 smaller, less impossible to find an index that unambiguously lies liquid stocks. Because of these concerns most index on the efficient frontier ex ante. The belief among funds use sampling strategies that choose a subset of investors nonetheless seems to be that the capitaliza-stocks in the benchmark to track the index. Further, tion-weighted indices are almost efficient, which if the index is not value weighted – for example may explain why investing in such indices is still equally weighted – then it may require frequent quite popular. Investors find Exchange-Traded CONTACT Yong Jin

jimmy.jin@polyu.edu.hk

School of Accounting and Finance, The Hong Kong Polytechnic University

© 2019 Informa UK Limited, trading as Taylor & Francis Group

2

B. GENDREAU ET AL. 

rebalancing. Hence, using a subset of stocks becomes cases to linear programming \(see Rockafellar and more attractive as it will reduce transactions costs. 

Uryasev 2000, 2002\). 

The two basic steps involved in index replication We solve the stock selection and weighting pro-strategies are sampling and optimizing. Two widely blem via LASSO \(Least Absolute Shrinkage and used sampling strategies are stratified sampling and Selection

Operator\)

algorithm

proposed

by

large market capitalization stock sampling. In the Tibshirani \(1996\). LASSO minimizes an objective latter case, the index replicator holds only the lar-function such as the residual sum of squares or in gest stocks by market capitalization or by market our case the CVaR, subject to the sum of the volume, which are liquid and hence will have lower absolute value of the coefficients being less than implicit and explicit transactions costs. In this a constant. Because of the nature of this con-paper, we will explore large market capitalization straint, it can lead to some of the weights being stock sampling. The optimization involves obtain-exactly zero. This is an advantage when we want ing optimal weights for the stocks in the sample by to select a subset of the stocks to include in minimizing the tracking error volatility \(TEV\). 

a portfolio. A limitation of LASSO algorithm is Tracking error \(TE\) is the difference between the that it cannot restrict the weights to be nonnega-index return and benchmark return it is supposed tive. However, this is not a serious concern given to mimic over a specified time interval. 

that some funds that use indexation such as Traditionally, an index replicator’s objective has mutual funds are allowed to short sales \(Chen, been to minimize TEV. This is considered a ‘passive’

Desai, and Krishnamurthy 2013\). In this study, strategy. Recently, however, enhanced indexation we allow the weights in the replicated portfolio has gained popularity. In this strategy, the fund to be negative as well as positive. However, we set managers strive to outperform the index while keep-the LASSO penalty value low \(s ¼ 1:5\) for the l1

ing TE low. One way to enhance the index perfor-minimization constraint to reduce the amount of mance is to control or minimize the negative TE

short selling. This constraint limits the amount of \(index fund under-performs the benchmark index\) short sales or negative weights on the stocks in the rather than positive errors \(index fund outperforms

fund.1 The LASSO penalty s can be alternatively than benchmark index\). Hence, an index replicator selected by cross-validation. Besides the LASSO

would prefer to minimize the fund’s negative track-penalty, we also add one more feasibility con-P

ing error while maximizing the positive tracking straint that the weights sum to one:

p

i¼1 wi ¼ 1. 

error that occurs when the fund outperforms the We also theoretically show the oracle property of benchmark. In this paper we replicate a benchmark the estimators, which guarantees that our estima-index \(is the value-weight index return of all CRSP

tors are best sparse linear approximation of the firms incorporated in the US and listed on the NYSE, true values. In the online Appendix, we analyse AMEX, or NASDAQ, or S&P500\) by selecting a full the behaviour of the objective function and pro-set or subset of firms from the set of the whole vide theoretical evidence why the portfolio portfolio universe or largest 100 firms by market obtained via CLEIR outperforms the benchmark. 

capitalization, and determine the portfolio weights The remainder of this paper is organized as that minimize the Conditional Value-at-Risk follows: In section 2 we briefly review the existing \(CVaR\) of the tracking error. CVaR has several literature. Section 3 describes CVaR-LASSO

nice properties as a metric for risk management: \(1\) Enhanced Index Replication \(CLEIR\) model and CVaR is a coherent risk measure \(Artzner et al. 1999\)

the

formulation

of

the

problem. 

We

use

and CVaR of a portfolio of returns is a convex func-a transformation developed by Rockafellar and tion of the weights; \(2\) CVaR minimizes the left tail Uryasev \(2000\) that makes it easier to solve the of the TE distribution and hence allows the index to optimization problem. Section 4 presents empiri-outperform the benchmark; \(3\) CVaR optimization cal results and compares the CLEIR method with can be reduced to convex programming and in some the additional weighting methods in different 1Chen, Desai, and Krishnamurthy \(2013\) find that the magnitude of short sales is around 15:65% of net assets on average; thus, we choose a penalty level s ¼ 1:5, which limits the short sales up to 25%. 

APPLIED ECONOMICS

3

portfolio universes from year 1988 to 2018, with equally weighting stocks in a risk cluster \(Chow the value-weighted index as the benchmark. 

et al. 2011\). Fernholz \(1995\) employs a diversity Section 4 further examines the out of sample weighting design that blends the portfolio based properties of CLEIR performance using daily on different weighting schemes. For example, the stock return data from 2003 to 2012 to track blending could be based on market capitalization S&P 500 index. We present our conclusion in and equal weighting. Arnott, Hsu, and Moore Section 5. 

\(2005\) propose an indexation method where the weights are based on the fundamental character-istics \(e.g. sales, earnings, or size\). Recently II. Literature review

Lejeune

and

Samatli-Pa

\(2013\)

address

The main strategies that have been proposed to a sampling replication strategy based on stochastic implement index tracking are full replication, par-integer problem to construct risk-averse enhanced tial replication, and enhanced replication. Full index funds. Their innovative method takes the replication involves holding all the constituent derivation of a deterministic equivalent for the securities in the exact same proportion as in the risk constraint and then use a block decomposi-benchmark portfolio at all times. However, in tion technique to provide a well scale and fast many instances market frictions may not permit convergent solution. 

this strategy to be feasible. In these instances, the In terms of optimization-based weighting indexa-index replicator can use a partial replication strat-tion, mean-variance optimization is the traditional egy using a subset of the most liquid firms in the way to construct an alternative indexation. Chopra index. An enhanced replication strategy, in con-and Ziemba \(1993\) address the importance of the trast, seeks to outperform an index while main-estimation risk in forming the mean-variance opti-taining a similar risk profile. Our methodology mal portfolio. Michaud \(1989\), Kan and Zhou falls into the enhanced replication category. 

\(2007\) and others emphasize the estimation loss in A comprehensive review of traditional index covariance matrix estimation. In order to reduce the tracking methodology is provided by Blume and significant estimation risk, Chopra and Ziemba Edelen \(2002\) and Chavez-Bedoya and Birge

\(1993\) suggest a fixed mean vector \(that is, the \(2014\). In addition to traditional indexations stra-minimum variance portfolio\) to improve the port-tegies, researchers and practitioners are also inter-folio performance. Haugen and Baker \(1991\) and ested in alternative indexations \(sometimes called Clarke, De Silva, and Thorley \(2006\) propose smart-beta indexation\). The goal in these strate-a minimum-variance strategy, and they provide gies is to outperform a benchmark index while empirical evidence to support that their strategy keeping close to the risk profile of the index. 

will improve the cap-weighted indexation return Heuristic-based weighting methodologies and and reduce the volatility. Goto and Xu \(2015\) optimization-based weighting methodologies are argue the estimation of the covariance matrix is two main methods used in alternative indexing still problematic, and they apply the graphical strategies. Chow et al. \(2011\) define heuristic-LASSO method to estimate the sparse inverse covar-based weighting methodologies as ‘ad hoc weightiance matrix. In addition, Basak and Shapiro \(2001\) ing schemes established on simple and, arguably, analyse the portfolio policies which maximize the sensible rules.’ For example, naive diversification, utility when the investors manage market risk using or the ‘1/N’ rule is one kind of heuristic-based Value-at-Risk \(VaR\). Further, Basak, Shapiro, and weighting methodology, which assigns equal Tepla \(2006\) also discuss a framework, which max-weight for each stock in the sampling pool. 

imizes the utility under the constraint of risk mea-DeMiguel, Garlappi, and Uppal \(2009\) provide sures, to evaluate relative performance evaluation. 

empirical evidence that portfolios based on equal Goel, Sharma, and Mehra \(2018\) implement the weighting perform well relative to portfolios based mixed Conditional Value-at-Risk to design portfo-on mean-variance optimization. Another heuris-lios for index tracking and enhanced indexing pro-tic-based weighting methodology is risk-cluster blems. And further Goel, Sharma, and Mehra \(2019\) equal weighting, which weights the portfolio by develop the methodology for robust optimization of

4

B. GENDREAU ET AL. 

mixed Conditional Value-at-Risk stable tail-adjusted minimizing the likelihood the tracking portfolio return ratio using copulas, with the applications in will underperform the benchmark by a large amount portfolio construction. Besides the literature using \(i.e. it minimizes the extreme tail risk of the tracking risk measures, Bonami and Lejeune \(2009\) discuss error\). In contrast, most other loss functions pena-an exact solution approach for the portfolio optimi-lize both under-performance and over-performance. 

zation when there are stochastic and integer con-Although the traditional loss functions may effi-straints. Choueifaty and Coignard \(2008\) and ciently control the tracking errors, they also limit Amenc et al. \(2011\) develop several indexation stra-the ability to outperform the benchmark. Our objec-tegies which maximize the Sharpe ratio. Chow et al. 

tive of partial penalization using CVaR should be \(2011\) provide a comprehensive analysis of most of more attractive to portfolio managers who would the passive investing alternative indexations in their naturally prefer to minimize underperformance survey paper and Cai et al. \(2018\) empirical exam-while outperforming the benchmark. There are ines several popular alternative indexations’ perfor-other partial penalization methods such as VaR. 

mance in the Chinese A-Share market. 

However, VaR does not account for properties of the distribution beyond its specified confidence level. This may lead to undesirable outcomes for III. CVaR-LASSO Enhanced Index

skewed or discrete distributions. On the other Replication\(CLEIR\)

hand, CVaR controls for the overall performance over a range of possibilities below the specified α

Objective

level in which a loss actually occurs. 

The objective in the enhanced replication strategy The optimization of CVaR can be achieved using we propose is to use a small subset of the most several techniques. We propose to use the LASSO

liquid stocks to replicate and track a benchmark method that yields sparse models, which is an index such as S&P500. Instead of the traditional advantage given we would like to replicate the objective of minimizing tracking error volatility benchmark index with a small subset of stocks. 

\(TEV\), we minimize the CVaR of the TE. The This is because LASSO can shrink some weights optimization is achieved via the LASSO optimiza-to zero. Further, with some mild conditions on the tion methodology proposed by Tibshirani \(1996\). 

objective function, the results are guaranteed to be The objective function and the constraints are the best weights when the sample size is large, as is given by

typically the case for financial data. Also, the



\! 

X

LASSO constraint can be easily changed into p

min CVaR

a collection of linear constraints. This makes it α

Y 

t

wiRit ; 

wi

i¼1

a more feasible convex optimization problem to solve. Finally, the simple linear constraints increase subject to, 

the speed of obtaining a solution when sample size Pp j j 

is large, but also make the solutions more robust. 

i¼1 wi

s; 

Pp

¼

In sum, the TE-CVaR objective and LASSO

i¼1 wi

1; 

method can be used to create an index that can where Yt is the rate of return of the index at time t, track a benchmark with fewer stocks and at the CVaRα is the α percent level of the Conditional Value-same time has the potential to outperform the bench-at-Risk, Rit is the rate of return of the ith candidate mark by minimizing the large expected negative TE. 

stock at time t. There are a total of p candidate stocks and w ¼ w1; . . . ; wp is the weight of ith stock in the fi

Risk measures: VaR and CVaR

nal index replicating portfolio. We allow short position in stocks and hence wi can be negative. 

In this section, we briefly discuss the definition and The CVaR objective function is a new way to properties of VaR \(Value-at-Risk\) and CVaR

replicate an index compared to the usual square \(Conditional Value-at-risk\), two widely used mea-error loss or other types of overall mean loss func-sures in risk management. Unlike volatility mea-tions. CVaR has the attractive property of it sures such as the variance of returns that measure

APPLIED ECONOMICS

5

the variability in both upside \(gain\) and downside LASSO method

\(loss\) of an asset, the VaR and CVaR describe the In this section, we first provide some necessary loss associated with an asset or portfolio and hence definitions and outline without proof that LASSO

are more appropriate for risk management. See method can asymptotically converge to an opti-Sarykalin, Serraino, and Uryasev \(2008\) for mum with a good choice of a penalty parameter. 

a discussion of the pros and cons of VaR and The detailed proof is given in the Appendix. 

CVaR in risk management and optimization. Here We assume all the random variables we con-we provide a brief summary of some major differ-sider are continuous, i.e., all the distributions of ences between the two measures and their use in stocks and the index are continuous. Let α be the optimization of portfolios. 

significant level for CVaR. Let w;α be the α quan-P

tile for the random variable Y 

p

i¼1 wiRi. Let

VaR



\! 



\! 

Let be a loss random variable such as the loss X

p

X

p

ρ

w

¼ 1

P

iRi; Y

wiRi I

p

\(negative returns\) on an index or portfolio of w;α

1 α Y 

½Y

w

; 

i Ri > wi;α

i¼1

i¼1

i¼1

assets. 

The

VaRαðÞ

at

a

confidence

be the loss function where I

Pp

level α 2 ð0; 1Þ, 

½Y

w

is an

iRi > w

i¼1

i;α

indicator function. The excess shortfall, ρw VaR

i;α, is

α ¼ inffζjPð ζÞ αg:

convex in w

ð

Þ

i for all i. Let

Yt; Rit , t ¼ 1; . . . ; n

The VaR concept was introduced in 1990 by JP

be our sample, and assume they are i .i.d. Let Morgan for risk management following the 1987



\! 

X

n

X

p

market crash. VaR is a very popular measure as it Eρ

Eρ

w

w

iRit; Yt

i;α ¼ 1

wi;α

is simple and provides one number to describe the n t¼1

i¼1



\! 

potential loss during a set time period with X

p

¼

; 

a certain probability. A major criticism of VaR is CVaRα Y 

wiRi

i¼1

that it does not address scenarios in which the VaR is exceeded. In addition, VaR has some unde-and

sirable

mathematical

properties. 

It

is

not



\! 

X

n

X

p

a coherent measure of risk and is not sub-Enρ

ρ

wiRit; Yt ; 

additive. For these reasons we consider CVaR

w;α ¼ 1

n

w;α

t¼1

i¼1

instead as the objective function to minimize in replicating a benchmark portfolio. 

which is a sample version of CVaRa. Define w0 ¼ argmin Eρw;α

CVaR

w



\! 

X

p

¼ argmin CVaRα Y 

wiRi ; 

w

CVaRα ¼

1

i¼1

1 α EI½VaRα:

standing for the best w in theory when we CVaR was proposed as a risk measure by

consider CVaR

Rockafellar and Uryasev \(2000\) as an alternative a. Define

to VaR. CVaR, under certain conditions, equals E w

ð Þ ¼ Eρw;α Eρw0;α

the average of the loss beyond a specified confi-



\! 

X

p

dence level, and hence its name conditional value ¼ CVaRα Y 

wiRi

at risk. In this sense it is a measure that sum-i¼1



\! 

marizes all the potential losses below a specified X

p



; 

confidence level. It has some nice mathematical CVaRα Y 

w0R

i

i

i¼1

properties. It is a coherent measure and also sub-additive. More importantly, Rockafellar and measuring how far our estimation is from the Uryasev \(2000, 2002\) show that it is superior to optimum. Theorem 1 described later shows that VaR in optimization applications. 

the optimization will eventually converge to the

6

B. GENDREAU ET AL. 

optimum weights provided we have enough data. 

where S f1; 2; . . . ; pg. 

The LASSO estimator in its Lagrange multiplier form is

We can view oracle w be a best approximation to w0 with l0 penalty for number of nonzero Definition 1. \(Margin Condition\) We say the entries under CVaRα loss. In our index replication margin condition holds with some strictly convex case, these optimal weights incorporate the trade-function

G, 

if

there

exits

η > 0, for all

P

P 



off between tracking error and penalty on includ-n

p



2

w0 R

η, 

ing too many stocks. Let

t¼1

i¼1 wi

i

it





\! \! 

pffiffiffiffiffiffiffi\! 

X

n

X

p 



2





4λ

S

j j

E

þ

w

ð Þ



2ε ¼ 3E w

2H

:

i > G

wi

w0 R

:

S

i

it

φ S

ð Þ

t¼1

i¼1

This condition restricts our population error to be Define empirical process to be

exactly larger than zero if w is not from the true νn w

ð Þ ¼ Enρ

; 

w;α Eρw;a

model. 

which measures the error between sample loss



\! 

and population loss. Let

X

p

^

8

9

w ¼ arg min

Enρ

jwij :

< 

=

w

w:α þ λ

i¼1

T ¼

Y

ð ; RÞ :

sup

:

P

ν

j n w

ð Þ νn w

ð Þj < ε;; 

λ

p

j

jε

Our objective in using LASSO is to choose 0

wiw

i¼1

i

some of the stock weights wi to be exactly zero. 

and if we choose the proper λ0 having order pffiffiffiffiffiffiffiffiffiffiffiffi

This is an important reason for choosing the ln p=n, T will have a large probability by con-LASSO

method

for

optimization. 

Let

centration inequality in Bousquet \(2002\). 

S f1; . . . ; pg, 

and

SC ¼ 1

f ; . . . ; pgnS

and

w

¼

S;i

wiI

j j

i

½ 2S. Let S be the number of elements

\(3.1\) Theorem 1. \(Oracle Inequality for in S. The next condition sets l1 norm of the coeffi-LASSO\) Assume compatibility condition holds cients bounded by some generalized l2 norm. 

for all S 1

f ; 2; . . . ; pg . Assume margin con-

P

P 



n

p



2 

Definition 2

dition

holds. 

w0 R

η

. \(Compatibility Condition\) We say

t¼1

i¼1 wi

i

it

P 

p





ε

the compatibility condition is met for the set S, for

all

λ0 i¼1 wi w

and

i

P

P 

2

with constant φ S

ð Þ > 0, if for all w

n

p





i, that satisfy

P 

P 

w0 R

η: Suppose λ > 8λ

t¼1

i¼1 w

i

i

it

0, 

p



p 

then on T , we have

i¼1 wSc;i

2

i¼1 wS;i , it holds that



\! 



\! 

X

p 

2

X

n

X

p

2

j

X

p 

Sj





w





E ^w

ð Þ þ λ

^w w 4ε:

S;i

wiRit

:

φ

i

i

2ðSÞ

i¼1

t¼1

i¼1

i¼1

Let H v

ð Þ be the conjugate convex for G u

ð Þ

Note that if all assumptions hold and w ¼ w0, i

i

pffiffiffiffiffiffiffi



defined in 3.3, margin condition, and G 0

ð Þ ¼ 0, 

then ε ¼ H 4λ

S

j j=φ S

ð Þ , with proper λ0 hav-

pffiffiffiffiffiffiffiffiffiffiffiffi

ing the order

ln p=n, when n \! 1; ε \! 0. In

H v

ð Þ ¼ sup uv

ð

G u

ð ÞÞ; u 0:

u

other words, our LASSO estimator ^

w \! 

i

w0. This

i

Now we can define the concept oracle, which is is the asymptotic consistency property of LASSO. 

the true target of LASSO estimator, 

The above theorem guarantees that w are the Definition 3. \(Oracle\) w is oracle if

best sparse linear approximation if the relation pffiffiffiffiffi\!\! 

between Y and Ri is linear. In our application, 4λ

S

j j

the weights of stocks ^

w we obtain using LASSO

w; S

ð

Þ ¼ arg min 3Eðw Þ

S þ 2H

; 

penalty will approach the best sparse linear w;S

φðSÞ

weights w when our estimation \(training\) sample

APPLIED ECONOMICS

7

8

P

is large enough, even if the underlying relation

> z 



p



t

Yt

ζ; 

> 

i¼1 wiRit

t ¼ 1; . . . ; n; 

between Y and R

> 

> 

i is not linear. This justifies the

>z 

t

0; 

t ¼ 1; . . . ; n; 

> 

<P

use of the CVAR objective and the LASSO method p



i¼1 ui

s; 

for selecting the stocks and their weights to

> u 

i

wi; 

i ¼ 1; . . . ; p; 

> 

> 

include in the index. 

> 

>u 

i

wi

> 

; 

i ¼ 1; . . . ; p; 

:Pp

¼

i¼1 wi

1:

Computational technique

We use the techniques outlined by Rockafellar and IV. Empirical analysis

Uryasev \(2002\) to transform the stochastic pro-Data and performance measures

gramming problem into a linear programming problem. The standard CVaR minimization pro-To assess the performance of CLEIR replication blem can be converted to a LP problem by intro-methodology, we conducted an out-of-sample ducing slack variables zt; for t ¼ 1; . . . ; n, where analysis of the strategy using the ‘rolling horizon n is the length of time. The resulting LP pro-approach’. The data are assembled from several blem is

sources including Ken French’s website, the Center for Research in Security Prices \(CRSP\) X

n

1

and

other

stock/portfolio

return

databases. 

min ζ þ

1

zt; 

ζ;w;z

1 α

n

Following Kan and Zhou \(2007\), DeMiguel, t¼1

Garlappi, and Uppal \(2009\), Goel, Sharma, and subject to constraints, 

Mehra \(2018\), we consider the following well-diversified portfolio universes: \(1\) 25 portfolios 8

P

> z 



p



formed on size and book-to-market ratios, \(2\) t

Yt

ζ; 

> 

i¼1 wiRit

t ¼ 1; . . . ; n; 

<z

100 portfolios formed on size and book-to-t 0; 

t ¼ 1; . . . ; n; 

Pp

> 

j j 

> 

market ratios, \(3\) Fama and French \(1997\) 49

i¼1 wi

s; 

:Pp

¼

industry portfolios, \(4\) 100 portfolios formed on i¼1 wi

1:

size and book-to-market ratios and 49 industry Note that w

j

portfolios, \(5\) simulated 300 individual stocks ij ¼ max w

f i; wig, hence we can

change the LASSO type penalty constraint with \(using the equal weighted portfolio returns as the absolute values for the weights into several linear

benchmark\).2 The benchmark is the value-constraints

by

introducing

dummy

vari-

weighted index return of all CRSP firms incorpo-ables u

rated in the US and listed on the NYSE, AMEX, or i; i ¼ 1; . . . ; p, 

NASDAQ. 

8 Pp

< 



The data sample is from November 1988 to i¼1 ui

s; 

u 

October 2018. For each year t, we first estimated i

wi; 

i ¼ 1; . . . ; p; 

: u 

the weighted for the portfolios/stocks to include in i

wi; 

i ¼ 1; . . . ; p:

the index using the daily stock return data So the stochastic programming can be written from year t 1. Then we used the estimated as a LP problem; 

stock weights to calculate the enhanced index return and its properties and at year t compare it X

n

to the benchmark index. Following Rockafellar min ζ þ

1

zt; 

and Uryasev \(2002\) and Bamberg and Wagner ζ;w;z;u

nð1 αÞ t¼1

\(2000\), we use risk-tolerance level ω ¼ 0:95 in the CVaR constraint. The LASSO penalty equals subject to constraints, 

to 1:5, which keeps the number of negative 2Following Goto and Xu \(2015\), we randomly select 300 stocks with careful imputation of the missing data using the value-weighted index returns, then calculate the mean vector and variance-covariance matrix as the true parameters to generate 30 years return vectors under the multivariate normal distribution assumptions. Next, we still use the ‘rolling horizon approach’ as the portfolio universes \(1\)-\(4\), and use the equal weighted portfolio returns as the benchmark. 

8

B. GENDREAU ET AL. 

weights low \(less short selling\). The LASSO pen-schemes in different portfolio universes. Value alty s can be alternatively selected by cross-weighted portfolios have zero tracking error validation. 

since they are full replication of the benchmark We compare the CLEIR performance with the index, while CLEIR has very robust performance several alternative weighting schemes: \(1\) CLEIR

with an annualized tracking error \(sSTD\) around without LASSO constraint \(CEIR\) \(2\) value 1:5%. Without the LASSO constraint, the CEIR

weighted index return \(VW\), \(3\) equal weighted method performs well in the first three portfolio index return \(EW\), \(4\) plug-in mean variance universes however in the universe of ‘100 portfo-portfolio \(MV\), \(5\) Global Minimum Variance lios formed on size and book-to-market ratios and portfolio \(GMV\), \(6\) Equal Variance portfolio 49 industry portfolios’ and ‘simulated 300 stocks,’

\(EV\), \(7\) Jin and Wang \(2016\) method \(JW\). 

the tracking error becomes much larger and the Besides traditional portfolio measures such as portfolio based on this method cannot track the holding period returns and Sharpe Ratios, we index closely. The empirical evidence shows that further implement the following two performance the LASSO technique helps provide a more robust measures to evaluate the index tracking perfor-performance particularly when more constituents mance of the replicated index. 

are included in replicating the benchmark index. 

ffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi v

ffi

The remaining methods \(EW, MV, GMV, EV, u

u 1 X

T

JW\) have much larger tracking errors than the s

¼ t

ð 

STD

e

eÞ2; 

\(4:1\)

CLEIR method. Table 1 Panel B reports the T 1

t

t¼1

robustness check using the alternative measure s

and one robust alternative, standardized Median MAD performance, and the findings are similar to Panel A. 

Absolute Deviation \(MAD\), 

Table 2 reports the out-of-sample Sharpe Ratios of the different weighting schemes in different s

¼

1

MAD

Φ1ð3=4Þ medt0ðjet0

stock universes and Table 3 further reports the median

corresponding out-of-sample returns. When the tðetÞjÞ; where; et is the TE:

number of constituents is not large, for example, \(4:2\)

25 or 49 constituents shown in the first two rows, The measure s

the Sharpe Ratios of CLEIR are very close to the MAD is more robust because sSTD

would be influenced when there are some large benchmark. However, when the number of the absolute tracking error due to extreme event, or constituents is relatively large, for example, more outliers. Bamberg and Wagner \(2000\) provide than 100 constituents in the latter three cases, the details on the components of the risk in the track-Sharpe Ratios are much improved compared to ing index. 

the benchmark. The CEIR, CLEIR without

Table 1 reports the tracking error performance LASSO, has relatively poor performance in the measures \(s

universe of ‘100 portfolios formed on size and STD and sMAD\) of different weighting

Table 1. Out-of-sample index tracking performance measures from 1988 to 2018. 

CLEIR

CEIR

VW

EW

MV

GMV

EV

JW

Panel A: sSTDð%Þ

SZBM25

1.000

1.000

0.000

5.628

234.982

13.939

5.692

6.277

IND49

1.893

1.894

0.000

4.313

125.160

15.290

4.344

7.848

SZBM100

1.249

1.533

0.000

5.863

403.277

15.481

5.853

6.546

IND49\+ SZBM100

1.587

102.559

0.000

4.926

210.839

16.806

4.961

6.605

Simulation \(300 Stocks\)

2.611

193.587

–

0.000

T < N

T < N

0.935

4.563

Panel B: sMADð%Þ

SZBM25

0.476

0.475

0.000

4.525

21.546

10.408

4.466

3.114

IND49

0.569

0.575

0.000

3.022

41.068

11.029

2.560

5.386

SZBM100

0.848

0.888

0.000

4.739

30.495

11.032

4.631

3.995

IND49\+ SZBM100

0.963

84.805

0.000

3.895

40.083

12.435

3.730

4.031

Simulation \(300 Stocks\)

2.558

192.234

-

0.000

T < N

T < N

0.936

4.632

APPLIED ECONOMICS

9

Table 2. Out-of-sample Sharpe ratios from 1988 to 2018. 

Sharp Ratio

CLEIR

CEIR

VW

EW

MV

GMV

EV

JW

SZBM25

0.630

0.630

0.629

0.673

0.082

1.319

0.700

0.858

IND49

0.621

0.621

0.629

0.680

0.009

0.758

0.702

0.763

SZBM100

0.651

0.656

0.629

0.678

−0.074

1.469

0.709

0.872

IND49\+ SZBM100

0.648

0.463

0.629

0.684

0.398

1.252

0.714

0.889

Simulation \(300 Stocks\)

1.127

1.066

-

0.985

T < N

T < N

1.013

1.196

Table 3. Out-of-sample returns from 1988 to 2018. 

Return \(%\)

CLEIR

CEIR

VW

EW

MV

GMV

EV

JW

SZBM25

10.956

10.957

10.950

12.196

19.188

15.642

12.414

13.462

IND49

10.992

11.000

10.950

11.560

1.060

8.484

11.345

10.001

SZBM100

11.342

11.370

10.950

12.292

−29.807

15.316

12.458

13.173

IND49\+ SZBM100

11.368

48.560

10.950

12.051

83.355

13.935

12.123

12.325

Simulation \(300 Stocks\)

18.140

207.732

–

15.528

T < N

T < N

15.523

14.930

book-to-market ratios and 49 industry portfolios’. 

a comprehensive out-of-sample examination over As DeMiguel, Garlappi, and Uppal \(2009\) docu-the period 2003 to 2012. The procedure is described mented, the equal weighting strategy \(EW\) has below. 

very good and robust performance, and the Equal Variance and Jin and Wang \(2016\) methods \(1\) Choose 100 largest stocks listed on the also have good and robust performance though NYSE-AMEX by market value on the last

the tracking errors are relatively large \(see Jin trading day of year t 2. 

and Wang 2016\). The plug-in mean variance \(2\) Estimate CLEIR index stock weights using \(MV\) and global minimum variance \(GMV\) per-one year of daily data for the largest 100

formances are not very consistent in different market capitalization stocks in year t 1, portfolio universes. MV achieves low Sharpe ratios some weights could be zero. 

\(in Table 2\) and big variation in out-of-sample \(3\) Compare the performance of the index port-returns \(in Table 3\). In most of the cases, GMV

folio based on the weights chosen in ðiÞ with performs well however the return in ‘49 industry the benchmark S&P500 index for the year t. 

portfolios’ \(in Table 3\) is relatively low though the \(4\) Repeat ðiÞ, ðiiÞ and ðiiiÞ for years t= 2003 to whole portfolio based on GMV method has rea-2012. 

sonable out-of-sample Sharpe ratio \(in Table 2\).In In Table 4 we report the out-of-sample per-the next section, we provide additional out-of-formances for consecutive ten years from sample tests based on sampling replications in 2003–2012. For nine out of ten years, the out-the S&P 500. 

of-sample CLEIR return consistently beats the S&P 500 return with a minimum of .25%

per year to a maximum of 6.67% per year. 

Additional test on S&P 500 using 100 largest stocks The only year it underperformed was in 2007

To further analyse the performance of CLEIR

and the under-performance was only 0.4%

enhanced

index

replication, 

we

conducted

per year. More strikingly the CLEIR index Table 4. Out-of-sample performance of CLEIR index from 2003 to 2012. 

Year

No. Stocks

CLEIR Ret \(Annual %\)

S&P500 Ret \(Annual %\)

\(CLEIR-S&P500 \(Annual %\)

Correlation

2003

76

23.34

22.32

1.02

99.1

2004

74

11.13

9.33

1.79

99.0

2005

72

4.10

3.84

0.25

98.6

2006

73

14.20

11.78

2.42

98.3

2007

70

3.25

3.65

−0.40

99.3

2008

83

−30.92

−37.59

6.67

98.3

2009

77

23.16

19.67

3.49

98.7

2010

54

13.52

11.00

2.52

99.3

2011

73

2.12

−1.12

3.24

99.4

2012

52

13.56

11.68

1.89

98.0



10

B. GENDREAU ET AL. 

outperformed the S&P500 index by 6.67% dur-Table 5. Fama and French \(1993\) and Carhart \(1997\) model risk ing the 2008 financial crisis when the market decomposition. 

α

Mkt R

fell by 37.59%. This supports our contention f

SMB

HML

MOM

Adjust R2

S&P 500

0.00

1.00

0.00

0.00

0.00

1.00

that by minimizing CVaR we can not only \(–\)

consistently ouperform the benchmark, but CLEIR

2.55

0.93

0.99

\(4.70\)

\(28.34\)

can also minimize large negative returns. The 2.31

0.91

0.07

0.99

average out-of-sample CLEIR excess return is \(4.15\)

\(26.26\)

\(1.25\)

2.55

0.93

0.00

0.99

2.3% \(over the period 2003–2012\). Also, we \(4.29\)

\(26.33\)

\(0.06\)

document that the average standard deviation 2.33

0.91

0.07

−0.01

0.99

\(3.82\)

\(24.31\)

\(1.16\)

\(−0.10\)

is close to the benchmark and the CLEIR index 2.35

0.88

0.03

0.02

−0.04

0.99

\(4.90\)

\(26.79\)

\(0.66\)

\(0.32\)

\(−2.17\)

has a high correlation with the benchmark. In the appendix, we report the out-of-sample performance of the daily return and the level of the index and the benchmark. From these fig-alpha, with an average of 2.44%. The main expo-ures, we can clearly see that our CLEIR algo-sure of CLEIR is from the market risk, with rithm also passes the out-of-sample robustness a coefficient of Mkt Rf 0.91, with t-statistic check and consistently beats the S&P 500

24:31. The coefficients on SMB and HML are benchmark. 

insignificant, which shows the outperformance by We implement the Fama and French \(1993\) CLEIR is not from SMB and HML factors but the three factor model and Carhart \(1997\) four-alpha generated by CLIER. The Fama and French factor Model to study the alpha after controlling \(1993\) and Carhart \(1997\) verify the previous for the market risk premium, Small-minus-Big findings and a significant alpha is found by factor \(SMB\), High-minus-Low factor \(HML\) CLEIR. 

and momentum factor \(MOM\). The result is

Figure 1 shows the cumulative CLEIR index reported in Table 5. The CLEIR method demon-performance from 2003 to 2012. The starting strates a very robust performance in the annual point for the CLEIR index and S&P500 is Figure 1. Out-of-sample CLEIR index performance from 2003 to 2012. 

APPLIED ECONOMICS

11

normalized to 100 on 1 January 2003. After ten crisis in 2008. We believe the methodology years, our CLEIR index outperforms the S&P500

would also be very useful for enhanced index by 60%\! 

fund managers engaged in tracking indices having large number of stocks. 

V. Conclusion

VI. Proof

In this paper, we propose a new enhanced indexation

method, 

which

we

call

CVaR-

Proof of lemma 1

LASSO Enhanced Index Replication \(CLEIR\). 

This method of enhanced replication minimizes Proof. 

the CVaR of the TE between the index and a benchmark using a LASSO-l

ð



\! 

1 minimization

1

ð

Þ2

constraint. The CVaR objective function is EðX j X ζÞ ¼ P X

ð ζÞ1

x pffiffiffiffiffi exp x μ

dx

X

f ζg

2πσ

2σ2

a new way to track a benchmark portfolio com-ð



\! 

ð

Þ2

pared to the usual square error loss or other ¼ PðX ζÞ1

ðx μ þ μÞ 1ffiffiffiffi

p ffi exp x μ

dx

fXζg

2πσ

2σ2

type of overall mean loss functions. CVaR has ð



\! 

1

ð

Þ2

an attractive property in that it minimizes the ¼ PðX ζÞ1μ

pffiffiffiffiffi exp x μ

dx

X

f ζg

2πσ

2σ2

likelihood of the tracking portfolio under per-



\! " 

\#



ð

1

ð

Þ2

ð

Þ2

forming the benchmark by a large amount, þ PðX ζÞ1 σ2

ffiffiffiffi

p ffi exp x μ

d x μ

fXζg

2πσ

2σ2

2σ2

while most other loss functions penalize both ffiffiffiffi

r ffi\! 



\!x¼þ1

σ2

ð

Þ2 

under-performance

and

over-performance. 

¼ μ þ



PðX ζÞ1 

exp x μ



2π

2σ2



Although the traditional loss functions may effi-x¼ζ

ffiffiffiffi

r ffi



\! 

ciently control the tracking errors, they also σ2

ðζ μÞ2

¼ μ þ

1

:

ð

Þ

exp 

limit the ability to outperform the benchmark. 

P X ζ

2π

2σ2

We implement a transformation similar to that developed by Rockafellar and Uryasev \(2000\)

and solve a linear programming problem along Proof of theorem 1

with the LASSO penalty and portfolio constraints. The CLEIR method has several nice properties: \(a\) sparsity in stock selection by \(6.1\) Proof

shrinking some of the weights to zero; \(b\) sam-Since the inequality \(3.1\) in result is valid pling with a subset of stocks to ensure liquidity almost surely in T , we assume Y

ð ; R Þ 2 T

i

in the

and low transactions costs; and \(c\) an automatic following proof. We first prove for some ~

w near

stock selection process l

w, the inequality \(3.1\) holds, and then show ^

w is

1 constraint. In out-of-

sample ‘rolling horizon approach,’ our CLEIR

also near w. Let

method

outperformed

the

benchmark

and

ε

other methods with low tracking error deviation t ¼

P 

ε þ λ

p





^w w ; 

\(standard deviation or median absolute devia-0

i¼1

i

i

tion\), and the effect is more pronounced when and we define ~

w ¼

þ ð

Þ

ð Þ

i

t ^

wi

1 t w, ~

E ¼ E ~w , 

i

the number of assets in the portfolio is large. 

E ¼ E w

ð Þ. Then

Further over a ten-year period \(2003–2012\) out-of-sample test, the CLEIR method outperforms X

p 

X

p





the benchmark \(S&P500\) by 2.3% per year while λ





0

~wi w ¼ tλ

^w

w

i

0

i

i

tracking the index closely. More importantly, i¼1

i¼1 P



p





^w w

the CLEIR index had a much lower loss com-¼ ε λ0 i¼1 i

i

P 

p



ε; 

pared to the S&P500 index during the financial ε þ λ



0

^

i¼1 wi

wi

12

B. GENDREAU ET AL. 



\! 

which means ~

w is around w. Then by

X

p

X

p

definition, 

Enρ~

j~w j t E

j^w j

w;α þ λ

i

nρ^w

i

i;α þ λ

i¼1

i¼1



\! 

X

p

X

p

X

p 

~

E þ λ

j~w

þ ð

Þ



ij ¼ Eρ~

j~w j

1 t

E

w

w;α Eρw0;α þ λ

i

nρw;α þ λ

i

i¼1

i¼1

h



i

i¼1



\! 

¼

E



X

p 

nρ~

E

w;α Eρ~

w;α

nρw;α Eρw;α





t E

þ ð

Þ

nρ

w

1 t

w;α þ λ

i

þ E

i¼1

nρ~



\! 

w;α Enρw;α





X

p 

þ



Eρ

Enρ

w

w;α þ λ

i

w;α Eρw0;α

i¼1

X

p 

¼ E

w

:

¼ ½ν



nρw;α þ λ

i

n ~

w

ð Þ νn w

ð Þ

" 

\! 

\!\#

i¼1

X

p

X

p 

Pp

þ

E

j j 



Hence

L 0. 

Therefore, 

~

E þ λ

j~w j 

nρ~

~w

E

w

i

w;α þ λ

i

nρw;α þ λ

i

i¼1

P 

p

i¼1

i¼1

P þ L þ E ε þ E þ λ

:

i¼1 w

By defini-

i

X

p 

þ E þ λ



tion of ε, we know E ε, then

w; 

i

i¼1

X

p

X

p

X

p

¼ 





P þ L þ E; 

~

E þ λ





~w

¼ ~

E þ

j~ j 





~ 

SC;i

λ

wi

λ

wS;i

i¼1

i¼1

i¼1



\! 

Where, 

X

p 

X

p 

ε þ E þ λ

w

λ





~w 

i

S;i

P ¼ νn ~

w

ð Þ νn w

ð Þ; 

i¼1

i¼1

X

p 

is the empirical process, 

2ε þ λ





~w



S;i w :

i



\! 

i¼1

X

p

Hence

L ¼

E

j j

nρ~

~w

w;α þ λ

i

i¼1



\! 

X

p

X



p 

~

E þ λ





~ 



wi

w

E



i

nρ

w

; 

w;α þ λ

i

i¼1

i¼1

X

p 

X

p 

¼ ~

E þ λ





~w

þ





~





SC;i

λ

wS;i

w

is the difference of objective function of CVaR-i

i¼1

i¼1

LASSO, 

X

p 

X

p 

2ε þ λ





~w þ





S;i

w

λ

~w

w

i

S;i

i

X

p 

i¼1

i¼1

E ¼ E þ λ

w

; 

i

X

p 

i¼1

2ε þ 2λ





~w 

S;i

w :

i

i¼1

is the error term evaluated at w. Because we assume Y

ð ; R Þ 2 T

The

inequality

\(3.1\)

will

hold

if

i

, and by the definition of the

P 

p





set T , 

2λ

~



i¼1 wS;i

w is also bounded by ε. Now

i

P 

we consider two cases: i\) λ

p





~



< ε

i¼1 wS;i

wi



P 

P ¼ ½ν ð Þ 



p

n ~

w

νn w

ð Þ

and ii\) λ





~w 

S;i

w

ε. 



i¼1

i

P

sup

P

jν

p

n w

ð Þ νn w

ð Þj ε:

In case i\), λ





~



< ε

i¼1 wS;i

w

, by \(7.1\)

i

λ

p

j

j

0

wiw ε

i¼1

i

0

X

p

~



E þ λ





~



Because we assume ρ is convex, and ^

w is

wi w

4ε:

i

i¼1

defined as the global minimum, 

APPLIED ECONOMICS

13

This will leads to

By the definition of H v

ð Þ, we have



\! 

X

p 

λ

X

p 

λ

λ



0





0

uv H v

ð Þ þ G u

ð Þ; 

0

~wi w ¼

λ

~w



i

λ

i w

i

λ 4ε

i¼1

i¼1

ε

hence together with marginal condition, 



; 

2

P 

if λ 8λ

p





0 and λ0

^

ε:

i¼1 wi

w

Hence, 

i

In case ii\), note that w

¼ 0, 

SC;i

X

p 

X

p 



X

p 

~

E þ λ





~w w

λ

~



i

w





~



i

SC;i

w

¼ λ

w

SC;i

SC;i

i¼1

i¼1

i¼1

X

X

p

X

p

p 





¼ ~

E þ λ

~w

þ λ

~w w

2ε þ λ





~w 

SC;i

S;i

i

S;i

wi

i¼1

i¼1

i¼1





X

p 

4λ S

j j

~

E

E

3λ





~w 

ε þ E þ H

þ þ

S;i

w :

i

φ2 S

ð Þ

2

2

i¼1

~

E

We apply the compatibility condition in ¼ 2ε þ ; 

2

Definition 2 for coefficients ~

w w and set S, 



\! 

" 

\#

or

X

p 

2

X

n

X

p

2





~

S

j j

w





S;i

w

~w

w R

:

i

S;i

i

ij

φ2 S

ð Þ

~

X

p

i¼1

t¼1

i¼1

E



þ λ





~w



i w 2ε; 

i

Hence by \(7.1\), 

2

i¼1

X

p

X

p

X





p

X

p

~





~





E þ λ

~

~

E þ

~



E þ λ





~

wi w

2λ

wi w

4ε:

w

þ





~





i

i

SC;i

λ

wS;i

wi

i¼1

i¼1

i¼1

i¼1

ε þ E

\(

" 

\# \)

X





n

X

p 



2

þ

~

2λ S

j j

w



By choosing λ 8λ0, 

S;i

w R

i

ij

φ2 S

ð Þ

t¼1

i¼1

\(

" 

\# \)

2





1 X

n

X

p 



~

4λ S

j j

w

w R

2

S;i

i

ij

φ2 S

ð Þ

t¼1

i¼1

\(

" 

\#

" 

\# \)

X





n

X

p 



2

X

n

X

p 



2

1

~

4λ S

j j

w

w0 R

þ

~w w0 R

2

S;i

i

ij

S;i

i

ij

φ2 S

ð Þ

t¼1

i¼1

t¼1

i¼1





\(

" 

\#

" 

\# \)\! 

X

n

X

p 



2

X

n

X

p 



2



4λ S

j j

1

H

þ

~



þ

~



φ

G

w

w0 R

w

w0 R

2 S

ð Þ

2

S;i

i

ij

S;i

i

ij

t¼1

i¼1

t¼1

i¼1





" 

\# \! 



" 

\# \! 

X

n

X

p 



2

X

n

X

p 



2



4λ S

j j

H

þ 1

~



þ 1

~



φ

G

w

w0 R

G

w

w0 R

2 S

ð Þ

2

S;i

i

ij

2

S;i

i

ij

t¼1

i¼1

t¼1

i¼1





~

E

E



4λ S

j j

H

þ þ

:

φ2 S

ð Þ

2

2

14

B. GENDREAU ET AL. 



\! 

X

p 

λ

X

p 

λ

References

λ





0





0

0

~wi w ¼

λ

~w

w



i

λ

i

i

λ 2ε

Amenc, N., F. Goltz, L. Martellini, and P. Retkowsky. 2011. 

i¼1

i¼1

ε

“Efficient Indexation: An Alternative to Cap-Weighted



:

Indices.” Journal Of Investment Management 9 \(4\): 1–23. 

2

Arnott, R. D., J. Hsu, and P. Moore. 2005. “Fundamental By the definition of ~

w, 

Indexation.” Financial Analysts Journal 61 \(2\): 83–99. 

P 



Artzner, P., F. Delbaen, J. M. Eber, and D. Heath. 1999. “Coherent ε

X

p 

ε λ

p





^w w

Measures of Risk.” Mathematical Finance 9 \(3\): 203–228. 

λ





^

0

i

w w ¼

i¼1

i

P 

Bamberg, G., and N. Wagner. 2000. “Equity Index 2

0t

i

i

ε þ λ

p





^w

; 

i¼1

0

i¼1

i w

i

Replication

with

Standard

and

Robust

Regression

P 

Estimators.” OR-Spectrum 22 \(4\): 525–543. 

hence λ

p





0

^

ε

i¼1 wi

wi

Basak, S., and A. Shapiro. 2001. “Value-At-Risk-Based Risk Until

now, 

we

prove

two

facts, 

a\)

P 

Management: Optimal Policies and Asset Prices.” Review λ

p





0

^

ε

of Financial Studies 14 \(2\): 371–405. 

i¼1 wi

w

, and b\) for any ~

w satisfying

i

P 

λ

p





Basak, S., A. Shapiro, and L. Tepla. 2006. “Risk Management 0

~

ε

i¼1 wi

w

, 

i

with Benchmarking.” Management Science 52 \(4\): 542–557. 

X

p

Blume, M. E., and R. M. Edelen 2002. “On Replicating the S& 

~



E þ λ





~w



P500 Index.” Rodney L White Center for Financial i w 4ε:

i

i¼1

Research - Working Papers. 

Bonami, P., and M. A. Lejeune. 2009. “An Exact Solution Hence

Approach for Portfolio Optimization Problems under Stochastic and Integer Constraints.” Operations Research X

p

^



57 \(3\): 650–670. 

E þ λ





^w 

i

w

4ε:

i

Bousquet, O. 2002. “A Bennett Concentration Inequality and i¼1

Its Application to Suprema of Empirical Processes.” 

Theorem 1 holds. 

Comptes Rendus Mathematique 334 \(6\): 495–500. 

Cai, L., Y. Jin, Q. Qi, and X. Xu. 2018. “A Comprehensive Study on Smart Beta Strategies in the A-Share Market.” 

Acknowledgments

Applied Economics 50 \(55\): 6024–6033. 

Chavez-Bedoya, L., and J. R. Birge. 2014. “Index Tracking and We thank Mark Taylor \(Editor\), the anonymous reviewer, for Enhanced Indexation Using a Parametric Approach.” Journal helpful discussions and useful suggestions. Yong Jin also of Economics Finance and Administrative Science 19 \(36\): acknowledges generous financial support of the Research 19–44. 

Grant Council of the Hong Kong Special Administrative Chen, H., H. Desai, and S. Krishnamurthy. 2013. “A First Region, China \(Project No. PolyU 25508217\) and the Look at Mutual Funds that Use Short Sales.” Journal of Learning and Teaching Enhancement Grant \(Project No.: Financial and Quantitative Analysis 48 \(3\): 761–787. 

1.21.xx.8ADP\). All errors are our own. 

Chopra, V. K., and W. T. Ziemba. 1993. “The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice.” The Journal of Portfolio Management 19 \(2\): 6–11. 

Disclosure statement

Choueifaty, Y., and Y. Coignard. 2008. “Toward Maximum Diversification.” Journal of Portfolio Management 35 \(1\): 40. 

No potential conflict of interest was reported by the authors. 

Chow, T. M., J. Hsu, V. Kalesnik, and B. Little. 2011. 

“A Survey of Alternative Equity Index Strategies.” 

Financial Analysts Journal 67 \(5\): 37–57. 

Funding

Clarke, R. G., H. De Silva, and S. Thorley. 2006. “Minimum-Variance Portfolios in the US Equity Market.” The Journal This work was supported by the Hong Kong Polytechnic of Portfolio Management 33 \(1\): 10–24. 

University \[The Learning and Teaching Enhancement DeMiguel, V., L. Garlappi, and R. Uppal. 2009. “Optimal versus Grant

\(Project

No.:

1.21.xx.8ADP\)\];Research

Grants

Naive Diversification: How Inefficient Is the 1/N Portfolio Council, University Grants Committee \[Project No. PolyU

Strategy?” Review of Financial Studies 22 \(5\): 1915–1953. 

25508217\]. 

Fernholz, R. 1995. “Portfolio Generating Functions.” 

Working paper, INTECH \(December\). 

Goel, A., A. Sharma, and A. Mehra. 2018. “Index Tracking and Enhanced Indexing Using Mixed Conditional ORCID

Value-At-Risk.” Journal of Computational and Applied Yong Jin

http://orcid.org/0000-0002-1544-1082

Mathematics 335: 361–380. 

APPLIED ECONOMICS

15

Goel, A., A. Sharma, and A. Mehra. 2019. “Robust Optimization Lejeune, M. A., and G. Samatli-Pa. 2013. “Construction of of Mixed CVaR STARR Ratio Using Copulas.” Journal of Risk-Averse Enhanced Index Funds.” INFORMS Journal Computational and Applied Mathematics 347: 62–83. 

on Computing 25 \(4\): 701–719. 

Goto, S., and Y. Xu. 2015. “Improving Mean Variance Michaud, R. O. 1989. “The Markowitz Optimization Enigma: Optimization through Sparse Hedging Restrictions.” Journal Is ‘Optimized’ Optimal?” Financial Analysts Journal 45

of Financial and Quantitative Analysis 50 \(6\): 1415–1441. 

\(1\): 31–42. 

Haugen, R. A., and N. L. Baker. 1991. “The Efficient Market Rockafellar, R. T., and S. Uryasev. 2000. “Optimization of Inefficiency of Capitalization-Weighted Stock Portfolios.” 

Conditional Value-At-Risk.” Journal of Risk 2: 21–42. 

The Journal of Portfolio Management 17 \(3\): 35–40. 

Rockafellar, R. T., and S. Uryasev. 2002. “Conditional Investment Company Institute \(US\). 2017. Investment Value-At-Risk for General Loss Distributions.” Journal of Company Fact Book. Washington, DC: Investment Banking & Finance 26 \(7\): 1443–1471. 

Company Institute. 

Sarykalin, S., G. Serraino, and S. Uryasev. 2008. “VaR Vs Jin, Y., and L. Wang. 2016. “Beat Equal Weighting: A Strategy CVaR in Risk Management and Optimization.” Tutorials for Portfolio Optimisation.” Risk December: 87–91. 

in Operations Research, INFORMS 270–294. 

Kan, R., and G. Zhou. 2007. “Optimal Portfolio Choice with Tibshirani, R. 1996. “Regression Shrinkage and Selection via Parameter

Uncertainty.” Journal of Financial and

the LASSO.” Journal of the Royal Statistical Society. Series Quantitative Analysis 42 \(3\): 621–656. 

B \(Methodological\) 58 \(1\): 267–288. 



# Document Outline

+ Abstract 
+ I. Introduction 
+ II. Literature review 
+ III. CVaR-LASSO Enhanced Index Replication\(CLEIR\)  
	+ Objective 
	+ Risk measures: VaR and CVaR  
		+ VaR 
		+ CVaR 

	+ LASSO method 
	+ Computational technique 

+ IV. Empirical analysis  
	+ Data and performance measures 
	+ Additional test on S&P 500 using 100 largest stocks 

+ V. Conclusion 
+ VI. Proof  
	+ Proof of lemma 1 
	+ Proof of theorem 1 

+ Acknowledgments 
+ Disclosure statement 
+ Funding 
+ ORCID 
+ References



