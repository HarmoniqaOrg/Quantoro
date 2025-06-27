Risk Budgeting Allocation for Dynamic Risk

Measures

Silvana M. Pesenti

Department of Statistical Sciences, University of Toronto, Canada, silvana.pesenti@utoronto.ca

Sebastian Jaimungal

Department of Statistical Sciences, University of Toronto, Canada, & Oxford-Man Institute, University of Oxford

sebastian.jaimungal@utoronto.ca

Yuri F. Saporito

School of Applied Mathematics \(EMAp\), Getulio Vargas Foundation \(FGV\), Brazil, yuri.saporito@fgv.br

Rodrigo S. Targino

School of Applied Mathematics \(EMAp\), Getulio Vargas Foundation \(FGV\), Brazil, rodrigo.targino@fgv.br

February 29, 2024\*

We define and develop an approach for risk budgeting allocation – a risk diversification portfolio strategy

– where risk is measured using a dynamic time-consistent risk measure. For this, we introduce a notion of dynamic risk contributions that generalise the classical Euler contributions and which allow us to obtain dynamic risk contributions in a recursive manner. We prove that, for the class of coherent dynamic distortion risk measures, the risk allocation problem may be recast as a sequence of strictly convex optimisation problems. Moreover, we show that self-financing dynamic risk budgeting strategies with initial wealth of 1

are scaled versions of the solution of the sequence of convex optimisation problems. Furthermore, we develop an actor-critic approach, leveraging the elicitability of dynamic risk measures, to solve for risk budgeting strategies using deep learning. 

Key words : Dynamic Risk Measures, Portfolio Allocation, Risk Parity, Elicitability, Deep Learning arXiv:2305.11319v5 \[q-fin.MF\] 31 Oct 2024

1. Introduction

The “risk parity” portfolio has been pioneered by Bridgewater Associates, when in 1996 it launched the All Weather asset allocation strategy – a portfolio strategy withstanding all weathers – although the term risk parity was only coined in 2005 in the white paper by Qian \(2005\). Risk parity originated from the desire of a diversified portfolio and the realisation that an equally weighted portfolio is diversified in asset allocation but not in the extent in which each asset contributes to the overall portfolio risk \(Qian 2011\). Emphasised by the 2008 financial crisis, the call for

\* First version: May 18, 2023. 

1

2

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures

“maximally” diversifying a portfolio’s risk was born, see e.g. Choueifaty and Coignard \(2008\). Risk parity enjoys widespread popularity in industry as numerous portfolio \(performance\) comparison studies illustrate, see, e.g., Chaves et al. \(2011\), Lee \(2011\), and Asness et al. \(2012\). An early mathematical formalisation of risk parity strategies can be found in Maillard et al. \(2010\) and

Roncalli \(2013\). 

Risk parity strategies and more broader risk budgeting strategies are portfolio allocations where the contribution of each asset to the overall portfolio risk is prespecified, e.g. for risk parity each assets contributes equally to the portfolio risk. Thus, central to risk budgeting is the way the risk of a portfolio is quantified. While most of the extant literature measures risk using the portfolio variance and further restrict to assets that follow multivariate Gaussian distributions, recent works relax these assumptions. Bruder et al. \(2016\) and Jurczenko and Teiletche \(2019\) study the Expected Shortfall \(ES; also called Conditional Value-at-Risk\) risk measure under the assumption that assets are multivariate Gaussian distributed, resulting in explicit formulae for risk contributions. Further works on risk budgeting include Ji and Lejeune \(2018\) who utilise the downside risk measure, 

Bellini et al. \(2021\) who consider expectile risk measures, Anis and Kwon \(2022\) who incorporate asset selection, and da Costa et al. \(2023\) who propose algorithms based on the cutting planes methodology to calculate risk budgeting strategies for coherent risk measures. Haugh et al. \(2017\)

combine risk budgeting of \(overlapping\) groups of asset with simultaneously maximising return and minimising risk. Variations of risk budgeting portfolio strategies are considered in Bai et al. 

\(2016\) who propose alternative optimisation problems to solve for risk parity portfolios. Meucci

et al. \(2015\) and Roncalli and Weisang \(2016\) construct risk factor budgeting portfolios, that are portfolios where each \(uncorrelated\) factor, rather than asset, contributes equally to the portfolio variance. Lassance et al. \(2022\) continues this line of work by including independent component analysis. 

None of these works, however, addresses the dynamic nature of investments, i.e., that portfolio strategies are typically holistically considered over a time horizon larger than one period; we henceforth refer to the one period setting as the “static” setting. In this paper, we develop a dynamic setting in which an investor trades over a finite time horizon using a self-financing risk budgeting strategy. Specifically, the investor aims to create a portfolio strategy, such that at every decision point each asset contributes a prespecified percentage to the future risk of the portfolio. 

This means that the investor’s problem is a multi-period decision problem. Whenever decisions occur over multiple periods, the investor’s “optimal” choices should be coherent over time. This can be achieved, for example, by optimising a time-consistent criterion.1 Indeed, when decisions 1 There are a number of alternative approaches to time-inconsistencies, see, e.g., Björk et al. \(2021\), we however, opt to use time-consistent criteria. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 3

are stemming from a time-inconsistent objective \(e.g. a static risk measure\), the “optimal” decision at a future point in time and state may not be optimal when one arrives at that future point in time in that very state \(Bielecki et al. 2018\). This is in contrast to time-consistent objectives \(e.g., dynamic time-consistent risk measures\), which result in decisions that are coherent across time and state. Thus, we consider dynamic time-consistent risk measures to evaluate the risk of a portfolio strategy. 

Dynamic time-consistent risk measures have been extensively studied to evaluate the risk of a sequence of random costs, such as the profit and loss \(P&L\) of a portfolio strategy; indicatively see

Cheridito et al. \(2006\), Ruszczy´

nski \(2010\), Bielecki et al. \(2022\), Coache et al. \(2023\), Bielecki et al. 

\(2023\). For dynamic risk budgeting, however, we further require the allocations of the dynamic risk to each asset and each time point, a topic whose literature is sparse. An early work for allocations of coherent dynamic risk measures is Cherny \(2009\) and for BSDE-based dynamic time-consistent risk measures we refer to Kromer and Overbeck \(2014, 2017\), and Mastrogiacomo and Rosazza-Gianin

\(2022\). Related but conceptually different is the work of Schilling et al. \(2020\) who axiomatically study how to decompose a risk dynamically. While working in a dynamic setting, their risk is the portfolio loss itself and not a dynamic risk measure applied to it. 

In this work, we consider the class of dynamic time-consistent risk measures that arise from conditional one-step distortion risk measures. A case in point is the ES whose security level may depend on the investor’s wealth or asset price. For this class, we define their dynamic risk contributions via Gâteaux derivatives and derive explicit formulae. While most of our results hold for conditional distortion risk measures, we focus on the subset of conditional coherent distortion risk measures, as defining risk allocations for non-coherent risk measures provide an “incentive for infi-nite fragmentation of portfolios” \(Tsanakas 2009\). In the static setting, Gâteaux derivatives enjoy a long history as risk contributions, also in connection to cooperative game theory. We provide a detailed literature review in Section 3. With this definition of dynamic risk contributions at hand, we define a dynamic risk budgeting portfolio as a strategy whose risk contributions at each point in time are a predefined percentage of the future risk of the strategy. We prove, under mild conditions, that a self-financing dynamic risk budgeting strategy with initial wealth of 1 is a scaled version of the solution of a sequence of strictly convex optimisation problems. Furthermore, we develop an actor-critic approach to solve the sequence of optimisation problems using deep learning techniques and provide illustrative examples. 

This manuscript is organised as follows. Section 2 introduces dynamic time-consistent risk measures and in Section 2.2, we apply a dynamic time-consistent risk measure to a self-financing

4

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures strategy and derive a recursive representation. In Section 3 we define dynamic risk contributions via the Gâteaux derivative and derive explicit formulae for the class of dynamic distortion risk measures. Section 4 is devoted to dynamic risk budgeting portfolio strategies and we show in Theorem 3 that a self-financing dynamic risk budgeting strategy with initial wealth of 1 can be obtained as a scaled version of the solution to a collection of strictly convex optimisation problems. Section

5 discusses how to solve this family of optimisation problems using neural networks leveraging elicitability of conditional risk measures \(Subsection 5.2\). Illustrations of risk budgeting strategies are provided in Section 6. Delegated to the appendix are auxiliary definitions and results \(A\), additional technical proofs \(B\), elaborations on conditional elicitability \(C\), and details on the numerical implementation \(D\). 

2. Dynamic Risk Assessment

We work on a filtered and completed probability space \(Ω, F, \(Ft\)t∈T , P\), where T := \{0, 1, . . . , T \+

1\}, and T ∈ N is a known and finite time horizon. The information available to the investor is encapsulated in the filtration \(Ft\)t∈T , and we assume that F0 = \(∅, Ω\) is the trivial σ-algebra, and simply write E\[·\] := E\[· |F0\]. We further denote the spaces of square-integrable random variables \(rvs\) and sequences by Z := \{Z ∈ F : E\[Z2\] < \+∞\}, Zt := \{Zt ∈ Z : Zt ∈ Ft\}, and Zt:T\+1 :=

\{\(Zt, Zt\+1, . . . , ZT\+1\) ∈ Zt × Zt\+1 × · · · × ZT\+1\}, for all t ∈ T . Similarly, we define the spaces of n-dimensional random vectors and sequences by Z := \{Z = \(Z1, . . . , Zn\) : Zi ∈ Z , ∀i = 1, . . . , n\}, Zt := \{Zt ∈ Z : Zt ∈ Ft\}, and Zt:T\+1 := \{\(Zt, Zt\+1, . . . , ZT\+1\) ∈ Zt × Zt\+1 × · · · × ZT\+1\}, for all t ∈ T . We further define L∞ := L∞\(Ω, F, P\) and L∞ := L∞\(Ω, F

t

t, P\) for all t ∈ T . Unless otherwise

stated, all \(in\)equalities of random vectors are to be understood component-wise and in a P-almost sure \(a.s.\) sense. 

2.1. Dynamic Risk Measures

The agent assesses the risk associated with a trading strategy by a dynamic time-consistent risk measure, which are families of conditional risk measures that satisfy the property of strong time-consistency; see Definition 2 below. We adopt the setting of Cheridito et al. \(2006\) and Ruszczy´

nski

\(2010\) for dynamic risk measures and refer the interested reader to those works and reference therein. 

Definition 1 \(Dynamic Risk Measures\). A dynamic risk measure on T is a family \{ρt,T\+1\}t∈T , where for each t ∈ T , the conditional risk measure is a mapping ρt,T\+1 : Zt:T\+1 → Zt. We say that a dynamic risk measure possesses one of the following properties, if for all t ∈ T : i\) **Normalisation: **ρt,T\+1\(0, . . . , 0\) = 0. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 5

ii\) **Monotonicity: **ρt,T\+1\(Zt:T\+1\) ≤ ρt,T\+1\(Yt:T\+1\), for all Zt:T\+1, Yt:T\+1 ∈ Zt:T\+1 with Zt:T\+1 ≤

Yt:T\+1. 

iii\) **Translation invariance: **ρt,T\+1\(Zt:T\+1\) = Zt \+ ρt,T\+1\(0, Zt\+1, . . . , ZT\+1\), for all Zt:T\+1 ∈ Zt:T\+1. 

iv\) **Convexity: **ρt,T\+1\(λ Zt:T\+1 \+ \(1 − λ\) Yt:T\+1\) ≤ λ ρt,T\+1\(Zt:T\+1\) \+ \(1 − λ\) ρt,T\+1\(Yt:T\+1\), for all λ ∈ Ft with 0 ≤ λ ≤ 1 and Yt:T\+1, Zt:T\+1 ∈ Zt:T\+1. 

v\) **Positive homogeneity: **ρt,T\+1\(λ Zt:T\+1\) = λ ρt,T\+1\(Zt:T\+1\), for all λ ∈ L∞ with λ > 0 and Z

t

t:T \+1 ∈

Zt:T\+1. 

vi\) **Coherency: **ρt,T\+1 is monotone, translation invariant, convex, and positive homogeneous. 

The mapping ρt,T\+1 thus assesses the risk of the sequence Zt:T\+1 ∈ Zt:T\+1 viewed from time t, by mapping it to an Ft-measureable rv. The investor may view this as the Ft-measurable quantity they are willing to exchange in place of the sequence of future risks. 

Next, we recall the notion of strong time-consistency, which, for simplicity, we refer to as time-consistency. A dynamic risk measure is time-consistent if it compares risks coherently over time. 

Specifically, if the time-s risk of one stochastic process is larger than another, then the former should also be riskier at an earlier time t < s, if the processes are a.s. equal at all times u satisfying t ≤ u < s. Thus, time-consistency is a property that results in optimal sequential decisions that are coherent when optimised at different points in time, and that further leads to a dynamic programming principle for optimising dynamic risk measures. 

Definition 2 \(Strong time-consistency – Cheridito et al. \(2006\)\). A dynamic risk measure \{ρt,T\+1\}t∈T is \(strong\) time-consistent if for all Zt:T\+1, Yt:T\+1 ∈ Zt:T\+1 that satisfy for some s ∈

\{t, . . . , T \+ 1\}

Zt:s = Yt:s and ρs,T\+1\(Zs:T\+1\) ≤ ρs,T\+1\(Ys:T\+1\)

it holds that

ρt,T\+1\(Zt:T\+1\) ≤ ρt,T\+1\(Yt:T\+1\) , 

and where Zt:s := \(Zt, . . . , Zs, 0, . . . , 0\) is understood as the projection of Zt:T\+1 onto Zt × · · · × Zs. 

While not apparent at first, the theorem below shows that time-consistency creates a connection between dynamic risk measures and so-called one-step risk measures. In particular, the theorem states that a dynamic time-consistent risk measure induces a family of one-step risk measures and conversely, any family of one-step risk measures defines a dynamic time-consistent risk measure. 

The following theorem is due to Cheridito et al. \(2006\) and Ruszczy´

nski \(2010\). 

6

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures Theorem 1 \(Recursive Relation\). Let \{ρt,T\+1\}t∈T be a dynamic risk measure which is monotone, normalised, and translation invariant. Then \{ρt,T\+1\}t∈T is time-consistent if and only if the following recursive representation holds:





\! 



ρt,T\+1\(Zt, . . . , ZT\+1\) = Zt \+ ρt Zt\+1 \+ ρt\+1 Zt\+2 \+ · · · \+ ρT−1 ZT \+ ρT ZT\+1

· · ·

, 

\(1\)

where the one-step risk measures \{ρt\}t∈T are mappings ρt : Zt\+1 → Zt, defined by ρt\(Zt\+1\) :=

ρt,T\+1\(0, Zt\+1, 0, . . . , 0\), for Zt\+1 ∈ Zt\+1. Moreover the one-step risk measures are monotone, normalised, and translation invariant. 

By Theorem 1, any family of mappings ρt : Zt\+1 → Zt that are monotone, normalised, and translation invariant, for all t ∈ T ,T := \{0, 1, . . . , T \}, gives rise to a dynamic time-consistent risk measure and vice-versa. Thus, without loss of generalisation, we make a slight abuse of terminology and call \{ρt\}t∈T a dynamic time-consistent risk measure \(DRM\) with representation \(1\). 

For defining risk budgeting strategies we further require the DRM to be positive homogeneous and convex; thus, coherent. Throughout the remainder of the exposition we focus on coherent distortion DRMs, which are a generalisation of the class of distortion risk measures to the dynamic setting. Coherent distortion risk measures span the subclass of law-invariant coherent risk measures that are comonotonic additive \(Kusuoka 2001\). Dynamic distortion risk measures with deterministic distortion function have been considered in Bielecki et al. \(2023\) who focus on coherent dynamic acceptability indices generated by families of distortion functions. Here, we allow the distortion function to be both time and state dependent, which differs from earlier works. For this we first define for each t ∈ T the regular cumulative distribution function \(cdf\) of Z ∈ Zt\+1 conditional on Ft as FZ|F \(z\) := P\(Z ≤ z | F

t

t\), and the regular \(left-\) quantile function of Z conditional on Ft as F −1 \(u\) := inf\{y ∈ R | F

\(u\) ≥ y\}. Moreover, define U

:= F

\(Z\), which is F

Z|F

Z|F

Z|F

Z|F

t\+1-measurable

t

t

t

t

and, conditional on Ft, uniform distributed on \(0, 1\).2 We refer the reader to Appendix A, Definition 8 for further discussion of one-step distortion risk measures and their representation via Choquet integrals. 

Definition 3 \(Coherent One-step Distortion Risk Measures\). For each t ∈ T , let γt : R

\[0, 1\] × Ω →

1

R\+ be a \(state dependent\) distortion weight function. This means that γ

0

t\(u, ω\) du = 1

and γt\(·, ω\) is non-decreasing for all ω ∈ Ω, and that the rv γt\(u, ·\) : Ω → R\+ is Ft-measurable for every 2 If FZ|F \(·\) is continuous, then U

is, conditionally on F

\(·\) is discontinuous, define

t

Z|Ft

t, a uniform rv. If FZ|Ft

˜

FZ|F \(z, λ\) := P \(Z < z | F

t

t\) \+ λ P \(Z = z | Ft\). Next, let V be a uniform Ft\+1-measurable rv that is, conditional on Ft, independent of Z. Then ˜

UZ|F := ˜

F

\(Z, V \) is, conditional on F

t

Z|Ft

t, a uniform rv, see \(R¨

uschendorf 2013, Def. 

1.2.\). For simplicity, we use the notation UZ|F := ˜

U

. 

t

Z|Ft

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 7

u ∈ \[0, 1\] and for all t ∈ T . Then, the coherent distortion dynamic risk measure with weight functions

\{γt\}t∈T is the family \{ρt\}t∈T , where for each t ∈ T and Z ∈ Zt\+1, the one-step risk measure ρt is defined as

Z 1

h



i

h



i

ρ





t\(Z \) :=

F −1 \(u\) γ

Z γ

\(Z\)

= E Z γ

, 

\(2\)

Z|F

t\(u\) du = E

t

FZ|F

Ft

t

UZ|F

Ft

t

t

t

0

where, as usual, we suppress the dependence of γt on its second argument. 

Allowing for a time- and state-dependent distortion weight function includes, e.g., Expected Shortfall at level α

1

t ∈ Ft, αt ∈ \[0, 1\), in which case γt\(u\) =

1

. The level α

1−α

u≥α

t may, e.g., 

t

t

decrease as wealth decreases to express the fact that the investor becomes more risk averse if their wealth drops. 

One-step distortion risk measures that are coherent give raise to coherent DRM via representation

\(1\). Throughout, we work with coherent dynamic DRM. 

Assumption 1. We assume that \{ρt\}t∈T is a coherent distortion DRM with representation \(2\)

R

that satisfy

1 γ

0

t\(u\)2 du < C a.s., for some C < \+∞, for all t ∈ T . 

The integrability condition on \{γt\}t∈T guarantees by Lemma 1, that any coherent one-step distortion risk measure is a mapping ρt : Zt\+1 → Zt, t ∈ T /\{0\} and ρ0 : Z1 → R. 

2.2. Risk-to-go of a Strategy

We denote by X = \(Xt\)

∈

t∈T

Z0:T\+1 the \(strictly\) positive a.s. n-dimensional price process of the universe of assets and consider an investor who invokes a long-only self-financing trading strategy and invests in all assets. We also denote by θ = \(θt\)t∈T ∈ Z0:T a \(not necessarily self-financing\) strategy, where θt = \(θt,1, . . . , θt,n\) is an n-dimensional, positive a.s. random vector representing the amount of shares invested in each asset at time t. In the sequel, we often use the “slice notation” 

θt

:= \(θ , θ

\) for 0 ≤ t

1:t2

t1

t1\+1, . . . , θt2

1 < t2 ≤ T . 

A strategy θ induces a self-financing strategy ϑ = \(ϑt\)t∈T – referred to as the induced self-financing strategy – as follows

ϑ⊺ Xt

ϑ

t−1

0 := θ0

and

ϑt :=

θ

θ⊺X

t , 

∀ t ∈ T /\{0\}. 

t

t

Recall that the investor invokes a long-only strategy and invests in all assets, thus θt,i > 0, a.s., for all i ∈ N := \{1, . . . , n\} and t ∈ T , and hence ϑ0:T is well-defined. The strategy ϑ is self-financing, i.e. it satisfies \(ϑt − ϑt−1\)⊺ Xt = 0, for all t ∈ T /\{0\}. To simplify notation, we define the weight process wθ = \(wθ\)

t t∈T :

θ⊺X

wθ :=

t

t\+1

, 

∀ t ∈ T , 

t

θ⊺ X

t\+1

t\+1

8

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures and notice that, 



\! 

t−1

Y

ϑt =

wθ

θ

s

t , 

∀ t ∈ T /\{0\}. 

s=0

For each t ∈ T , wθ is F

t

t\+1-measurable and if the original strategy θ0:T is already self-financing, then wθ = 1. 

t

We denote the \(negative\) price increment by ∆Xt := −\(Xt\+1 − Xt\). As the investor aims to invest in a risk budgeting portfolio, they only consider strategies that are long-only and satisfy the following integrability conditions. 

Definition 4. For any c ≥ 0 define the set of admissible strategies by X h



i

2

Ac := θ0:T ∈ Z0:T | θ0:T > c a.s. , 

wθ ∈ L∞ , ∀t ∈ T , 

and

θ⊺∆X

< \+∞

. 

t

t\+1

E

t

t

t∈T

For any c ≥ 0, by Lemma 2, Ac is a a convex set and any induced self-financing strategy ϑ belongs to A0. We further use the notation Ac,t, t ∈ T , to denote the sliced set of admissible strategies at time t, that is Ac,t := \{θt | θ0:T ∈ Ac\} for each t ∈ T . We use the terminology that the strategy θ

is admissible, if there exists a c ≥ 0 such that θ ∈ Ac. 

The investor assesses the risk of an admissible strategy θ0:T ∈ Ac at time t = 0 with a coherent distortion DRM \{ρt\}t∈T by





R\[θ0:T \] = ρ0 θ⊺ ∆X

wθ θ⊺ ∆X

wθwθ θ⊺ ∆X

0

0 \+ ρ1

0

1

1 \+ ρ2

0

1

2

2 \+ · · ·





\!\! 

\!\!\! 

T −2

Y

T −1

Y

\+ ρT−1

wθ θ⊺

∆X

wθ

∆X

· · ·

s

T −1

T −1 \+ ρT

s′ θ⊺

T

T

s=0

s′=0





= ρ0 ϑ⊺ ∆X

ϑ⊺ ∆X

∆X

∆X

· · ·

. 

0

0 \+ ρ1

1

1 \+ · · · \+ ρT −1

ϑ⊺T−1

T −1 \+ ρT \(ϑ⊺

T

T \)

Hence, R\[θ0:T \] is the dynamic risk of the induced self-financing strategy, but parameterised by θ0:T . We can view the risk recursively by defining the risk-to-go process \(Rt\[θt:T \]\)t∈T via RT\+1 := 0 and

\(3a\)



Rt\[θt:T \] := ρt θ⊺∆X

R

, 

∀ t ∈ T . 

\(3b\)

t

t \+ wθ

t

t\+1\[θt\+1:T \]

At time t = 0, it holds that R0\[θ0:T \] = R\[θ0:T \]. By Lemma 3, any admissible strategy θ ∈ Ac, c ≥ 0, \(and thus also any induced self-financing strategy\) has finite risk R\[θ0:T \] < \+∞, and satisfies Rt\[θt:T \] ∈ Zt for all t ∈ T /\{0\}. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 9

The risk-to-go evaluated along a self-financing strategy ψ

∈

0:T

Z0:T satisfies a slightly simpler

recursion





R



t\[ψ

\] := R

= ρ

∆X

\] , 

∀ t ∈ T , 

t:T

t\[θt:T \] θ

t ψ⊺

t

t \+ Rt\+1\[ψt\+1:T

t:T =ψt:T

as wψ = 1, for all t ∈ T /\{0\}, for self-financing strategies. 

t

The next proposition connects the risk-to-go process of θ0:T with the risk-to-go process of its induced self-financing strategy ϑ0:T . 

Proposition 1. Let θ0:T be an admissible strategy and denote by ϑ0:T its induced self-financing strategy. Then the following holds

R0\[ϑ0:T \] = R0\[θ0:T \]

and



\! 

t−1

Y

Rt\[ϑt:T \] =

wθ

R

s

t\[θt:T \] , 

∀ t ∈ T /\{0\} . 

\(4\)

s=0

Proof:

The equation for t = 0 follows by definition. To show the equalities for t ∈ T /\{0\}, we proceed by induction starting backwards in time. At time T , we use positive homogeneity of the conditional risk measures, since by admissibility of θ0:T , we have 0 < wθ ∈ L∞ , for all t ∈ T . Thus, t

t\+1



\! 



\! 

T −1

Y

T −1

Y

RT \[ϑT \] = ρT \(ϑ⊺ ∆X

wθ ρ

∆X

wθ R

T

T \) =

s

T \(θ⊺

T

T \) =

s

T \[θT \] . 

s=0

s=0

Next, assume Equation \(4\) holds for t \+ 1 and note that wθ is F

s

t-measurable for all 0 ≤ s < t. Then

at time t, we have

Rt\[ϑt:T \] = ρt \(ϑ⊺∆X

t

t \+ Rt\+1\[ϑt\+1:T \]\)



\! 



\! 

\! 

t−1

Y

t

Y

= ρt

wθ θ⊺∆X

wθ

R

s

t

t \+

s

t\+1\[θt\+1:T \]

s=0

s=0



\! 

t−1

Y



=

wθ ρ

∆X

R

s

t

θ⊺t

t \+ wθ

t

t\+1\[θt\+1:T \]

s=0



\! 

t−1

Y

=

wθ R

s

t\[θt:T \] , 

s=0

where the first equality holds from the induction assumption. The second follows from positive Q

homogeneity of the conditional risk measures and that 0 < 

t−1 wθ ∈ L∞. The last equality follows

s=0

s

t

from Equation \(3\). 

□

Here, as in the static risk budgeting problem, positive homogeneity of the risk measure plays a central role. Therefore, we next discuss the positive homogeneity of the risk-to-go process. For this, it is convenient to split the arguments of Rt into two parts, specifically we write Rt\[θt:T \] =

Rt\[\(θt, θt\+1:T \)\] to emphasise the difference of the position at t, θt, and the remaining ones, θt\+1:T . 

10

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures Proposition 2 \(Positive homogeneity of Risk-to-go Process\). Let θ0:T be an admissible strategy. Then, the risk-to-go process is positive homogeneous viewed as a function of θt and also viewed as a function of θt:T , that is for all t ∈ T and for all at ∈ L∞, a t

t > 0, 

at Rt \[θt:T \] = Rt \[\(at θt, θt\+1:T \)\] = Rt \[at \(θt, θt\+1:T \)\] . 

\(5\)

Proof:

The first equality, i.e. positive homogeneity of Rt\[θt:T \] in θt, follows from representation

\(3\), linearity of wθ in θ

t

t, noting that Rt\+1\[θt\+1:T \] does not depend on θt, and from ρt\(·\) being positive homogeneous. 

To see the second equality, we proceed by induction. First, RT \[θT \] = ρT \(θ⊺ ∆X

T

T \) is positive

⊺

homogeneous in

X

θ

t

t\+1

T . Next, as wθ is invariant under scaling of both θ

= θ

=

t

t and θt\+1, i.e. wθ

t

⊺

θ

X

t\+1

t\+1

⊺

at θ X

t

t\+1

⊺

= wθ′, a

, a

is s.t. θ′ = a

= a

a

t

t ∈ L∞

t

t > 0, where θ′0:T

t

tθt, θ′t\+1

tθt\+1, with all remaining

t θ

X

t\+1

t\+1

θ′ = θ

is admissible. Now, assume the second equality in \(5\) holds s

s for s /

∈ \{t, t \+ 1\}. Moreover, θ′0:T

for t \+ 1, then we have





Rt \[at\( θt, θt\+1:T \)\] = ρt at θ⊺∆X

R

t

t \+ wθ′

t

t\+1\[at \(θt\+1:T \)\]



= ρt at θ⊺∆X

a

= a

t

t \+ wθ

t

t Rt\+1\[θt\+1:T \]

t Rt \[θt; θt\+1:T \] , 

where the first equality follows from \(3\), the second equality follows from the inductive assumption and that wθ = wθ′, and the last equality follows by positive homogeneity of ρ

t

t

t\(·\). 

□

We next discuss how to allocate the risk-to-go onto its components at each point in time. 

3. Dynamic Risk Contributions

The literature on risk contribution – also called capital \(cost\) allocation – in the static setting is extensive. Approaches ranging from performance measurement \(Tasche 1999\), cooperative game theory including Aumann-Shapley allocation \(see e.g., Mirman and Tauman \(1982\) and Billera and

Heath \(1982\) for early works on cost allocation and Denault \(2001\) in a risk management setting\) and allocation in the fuzzy core \(Tsanakas and Barnett \(2003\)\), as well as Gâteaux derivatives and Euler allocations \(Kalkbrener 2005\). Using an axiomatic approach, Kalkbrener \(2005\) showed that for any positive homogeneous and sub-additive static risk measure, the only linear and diversifying capital allocation rule is the Gâteaux derivative. 

Here, we proceed inline with Kalkbrener \(2005\) by defining risk contributions as a sub-differential, specifically through the Gâteaux derivative. We note that in case of coherent risk measures, the allocation defined via the Gâteaux derivatives is the same as the Aumann-Shapley allocation \(Tsanakas 2009\). An advantage of defining risk contributions through Gâteaux derivatives of a distortion risk measure is that they satisfy full allocation, the property that the sum of

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 11

the risk contributions adds up to the total risk. In the sequel, we show that our dynamic risk contributions also satisfies a dynamic version of the full allocation property. When defining dynamic risk budgeting strategies, the full allocation property is imperative as it allows to allocate the entire risk to its components. 

As we work in a dynamic setting, at each time t ∈ T , the investor faces the future risk of the induced self-financing strategy and aims to allocate the risk-to-go to each asset i. Thus for each t ∈ T , we define the risk contribution of asset i as the one-sided Gâteaux derivative of the risk-to-go processes Rt\[θt:T \] in direction θt,i. This allows to measure the degree to which the risk-to-go is impacted by the investor’s position in the ith asset at time t. Moreover, as we show in Corollary 1, 

this approach allows for full allocation. 

We start by recalling the definition of one-sided Gâteaux derivative of a functional. 

Definition 5. For a functional Ft : Zt:T → Zt, t ∈ T , we denote by Dζ F

i

t its one-sided Gâteaux

derivative of Ft to the ith component in direction ζ ∈ Zt. That is, for t ∈ T , and Zt:T ∈ Zt:T

1 



Dζ F

F

, 

i

t\[Z t:T \] := lim

t\[Z t:T \+ ε 1t,iζ \] − Ft\[Z t:T \]

ε↓0 ε

where \(1t,i\)t∈T is the stochastic process taking value 1 in component i at time t, and 0 otherwise. 

We consider the one-sided Gâteaux derivative as we work with long-only portfolios. Thus, when taking directional derivatives with respect to θt,i, its perturbed values should also be positive, which is guaranteed with non-negative ε in Definition 5. 

Definition 6. For each t ∈ T , we define the risk contribution of the risk-to-go to the ith investment as RCt,i\[θt:T \] := Dθt,i R

i

t\[θt:T \] . 

Note that the risk contributions RCt,i\[θt:T \] are Ft-measurable rvs. 

The next result shows that also the risk contribution are positive homogeneous. 

Proposition 3 \(Positive homogeneity of Risk Contributions\). The risk contributions of an admissible strategy θ0:T to the ith investment at time t ∈ T are positive homogeneous in the following way. For all t ∈ T and for all at ∈ L∞, a

t

t > 0, we have that

at RCt,i \[θt:T \] = RCt,i \[\(at θt, θt\+1:T \)\] = RCt,i \[\(at θt:T \)\] . 

\(6\)

Proof:

This follows as RCt,i are the Gâteaux derivatives of a positive homogeneous function. 

For completeness we provide a short proof. For any t ∈ T and i ∈ N , we obtain from positive homogeneity of Rt\[θt:T \] in θt, see Proposition 2, 

1



RCt,i \[\(at θt, θt\+1:T \)\] = lim

Rt \[\(at \(θt \+ ε ei θt,i\) , θt\+1:T \)\] − Rt\[\(at θt, θt\+1:T \)\]

ε↓0 ε

1



= lim at

Rt \[\(\(θt \+ ε ei θt,i\) , θt\+1:T \)\] − Rt\[\(θt, θt\+1:T \)\]

ε↓0

ε

= at RCt,i\[θt:T \] , 

12

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures where ei is the unit vector having value 1 at position i \(and 0 otherwise\). The second equality in

\(6\) follows via similar arguments using positive homogeneity of Rt\[θt:T \] in θt:T , see Proposition 2. 

□

By positive homogeneity of the risk-to-go process, we obtain for all t ∈ T an Euler-like theorem, as stated in the next corollary, which guarantees full allocation. 

Corollary 1 \(Full Allocation\). Let \{ρt\}t∈T be a coherent distortion DRM. Then it holds for any admissible strategy θ0:T that

X

Rt\[ θt:T \] =

RCt,i\[θt:T \] , 

a.s. , 

∀ t ∈ T . 

i∈N

Proof:

This proof follows similar steps as the classical Euler allocation. By positive homogeneity of the risk-to-go, Proposition 2, we have for all real numbers a > 0

a Rt \[θt:T \] = Rt \[\(a θt, θt\+1:T \)\] , 

t ∈ T . 

\(7\)

Next, viewing Equation \(7\) as a function of a, we take a one-sided partial derivative with respect to a of both sides of the above equation, that is

1 





Rt \[θt:T \] = lim

Rt \(a \+ ε\) θt, θt\+1:T

− Rt \(a θt, θt\+1:T \)

ε↓0 ε

X





=

Dθt,i R \(a θ

. 

i

t

t, θt\+1:T \)

i∈N

Evaluating the above at a = 1 concludes the proof. 

□

In Tsanakas \(2004\) the author derives, in the static setting, a closed form formula for the risk contributions of distortion risk measures. Our next result extends this to the dynamic setting. 

Theorem 2 \(Risk Contributions\). Let \{ρt\}t∈T be a coherent distortion DRM with weight functions \{γt\}t∈T . Then, the risk contribution of an admissible strategy θ0:T to the ith-investment at time t ∈ T is given by





X





RC

t\+1,i



t,i\[θt:T \] = E

θt,i ∆Xt,i \+

R

γ U

F , 

θ⊺ X

t\+1\[θt\+1:T \]

t

t\[θt:T \]

t

t\+1

t\+1

where Ut\[θt:T \] is a uniform rv comonotonic to θ⊺∆X

R

t

t \+ wθ

t

t\+1\[θt\+1:T \]. 

Furthermore, 





E |RCt,i\[θt:T \]| < \+∞ for all t ∈ T and i ∈ N . 

Proof

Using Prop. 1 Tsanakas and Millossovich \(2016\) and Prop. 3.2 in Pesenti et al. \(2021\), we have that for Y , Y ′ ∈ Zt\+1, a differentiable function h : Rd → R, and a conditional distortion risk measure ρt, it holds that



ρ

− ρ

h



i

lim t h\(Y ′ \+ ε ei Y \)

t\(h\(Y ′\)\) = E Y ∂

i

h\(Y ′\) γt Uh\(Y ′\)|F |Ft , 

\(9\)

ε↓0

ε

∂yi

t

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 13

where Uh\(Y ′\)|F is a uniform rv that is comonotonic to the rv h\(Y ′\) conditional on the information t

Ft, see also Equation \(2\). In Appendix A, Proposition 11, we provide an alternative proof of Equation \(9\). 

Next, note that the risk contributions are

RCt,i\[θt:T \] = Dθt,i R

i

t\[θt:T \]



= Dθt,i ρ

∆X

R

i

t

θ⊺t

t \+ wθ

t

t\+1\[θt\+1:T \]

X 

\! 

X

= Dθt,i ρ

θ

∆X

t\+1,i

R

. 

i

t

t,i

t,i \+ θ⊺ X

t\+1\[θt\+1:T \]

t\+1

i∈N

t\+1

Applying Equation \(9\) and noting that Rt\+1\[θt\+1:T \] is a function of θt\+1:T only, and not a function of θt,1, concludes the first part of the statement. The last part follows from Lemma 4. 

□

The next representation of the risk contributions illustrates that a decision at time t, via θt, cascades through time and impacts all later decision points. This is because restricting to self-financing strategies implies that the investor’s future wealth, and thus also possible investment decisions, depend on the current choice of θt. The proof is delegated to Appendix B.1. 

Proposition 4 \(Impact of a Decision\). Let \{ρt\}t∈T be a coherent distortion DRM with weight functions \{γt\}t∈T . Then, the risk contribution of an admissible strategy θ0:T to the ith-investment at time t ∈ T may be written as

h



i

RC



t,i\[θt:T \] = E θt,i ∆X t,i Γθ

t Ft





θ



\+



E

t,i Xt\+1,i \(θ⊺ ∆X

Γθ

F

θ⊺ X

t\+1

t\+1\) Γθ

t

t\+1

t

t\+1

t\+1





θ



\+



E

t,i Xt\+1,i wθ \(θ⊺ ∆X

Γθ

Γθ

F

θ⊺ X

t\+1

t\+2

t\+2\) Γθ

t

t\+1

t\+2

t

t\+1

t\+1





θ



\+ · · · \+



E

t,i Xt\+1,i wθ · · · wθ

\(θ⊺ ∆X

· · · Γθ F

θ⊺ X

t\+1

T −1

T

T \) Γθ

t

T

t

t\+1

t\+1



where Γθ := γ

, with U

s

s Us\[θs:T \]

s\[θs:T \] as defined in Theorem 2, for all s ∈ T . 

From the above proposition, we can interpret the first expectation as the time t impact of θt,i, the second expectation as the effect the choice θt,i has at time t \+ 1, and so on. 

Note that the risk contribution of investment-i at time t of a induced self-financing strategy ϑ is θ

RC

t,i



t,i\[ϑt:T \] := D

R

. 

i

t\[θt:T \]θ=ϑ

The next statement relates the risk contributions of a strategy with those of its induced self-financing strategy. 

14

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures Proposition 5. Let \{ρt\}t∈T be a coherent distortion DRM with weight functions \{γt\}t∈T . Let θ0:T

be admissible and ϑ0:T its induced self-financing strategy. Then the following holds: RC0,i\[ϑ0:T \] = RC0,i\[θ0:T \] and



\! 

t−1

Y

RCt,i\[ϑt:T \] =

wθ RC

s

t,i\[θt:T \] , 

∀t ∈ T /\{0\} . 

s=0

Proof:

Case t = 0 follow immediately from Proposition 1. For t ∈ T /\{0\}, define the scalar rv Q

cθ :=

t−1 wθ ∈ L∞ and recall that ϑ

θ

t

s=0

s

t

t = cθ

t

t. Then, we have that



RC



t,i\[ϑt:T \] = Dθt,i R

i

t\[θt:T \]θ=ϑ





X



t\+1,i



\(by Theorem 2\) = E ϑt,i

∆Xt,i \+

R

γ

F

ϑ⊺ X

t\+1\[ϑt\+1:T \]

t Ut\[ϑt:T \]

t

t\+1

t\+1





X



t\+1,i



\(by Proposition 1\) = E ϑt,i

∆Xt,i \+

cθ R

γ

F

ϑ⊺ X

t\+1

t\+1\[θt\+1:T \]

t Ut\[ϑt:T \]

t

t\+1

t\+1





X



= cθ

θ

∆X

t\+1,i



R

γ

. 

\(10\)

t E

t,i

t,i \+

F

θ⊺ X

t\+1\[θt\+1:T \]

t Ut\[ϑt:T \]

t

t\+1

t\+1

Next, Ut\[ϑt:T \] may be simplified by noting

ϑ⊺∆X

R

∆X

t

t \+ wϑ

t

t\+1\[ϑt\+1:T \] = ϑ⊺

t

t \+ Rt\+1\[ϑt\+1:T \]

\(as ϑ is self-financing\)

\(by Proposition 1\) = ϑ⊺∆X

R

t

t \+ cθ

t\+1

t\+1\[θt\+1:T \]

θ

\(as ϑ

θ⊺∆X

R

t = c

θ

t

t \)

= cθt t

t \+ cθ

t\+1

t\+1\[θt\+1:T \]



θ

θ

θ

\(as c

= c w \) = cθ

θ⊺∆X

R

. 

t\+1

t

t

t

t

t \+ wθ

t

t\+1\[θt\+1:T \]

Furthermore, as cθ > 0 a.s., the bivariate vector

t





ct θ⊺∆X

R

, θ⊺∆X

R

is comonotonic

t

t \+ wθ

t

t\+1\[θt\+1:T \]

t

t \+ wθ

t

t\+1\[θt\+1:T \]

and therefore Ut\[ϑt:T \] = Ut\[θt:T \] a.s., that is both θt:T and ϑt:T generate the same comonotonic uniform rv. 

Finally, applying this result and continuing from \(10\), we have X



RC

t\+1,i



t,i\[ϑ\] = cθ

θ

∆X

R

γ

= cθ RC

t E

t,i

t,i \+

F

θ⊺ X

t\+1\[θt\+1:T \]

t Ut\[θt:T \]

t

t

t,i\[θt:T \] , 

t\+1

t\+1

as required. 

□

Consequently, the risk contributions of the induced self-financing strategy are by definition positive homogeneous, as stated in Proposition 3, and satisfy the full allocation. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 15

4. Dynamic Risk Budgeting Portfolios

Using the dynamic risk contributions defined in the last section, we now define a dynamic risk budgeting strategy. 

Definition 7. Let \{ρt\}t∈T be a DRM. A strategy θ0:T ∈ Ac, c ≥ 0, is called a *dynamic risk budgeting* P

*strategy * with budget B = \(bt,i\)t∈T ,i∈N satisfying bt,i > 0 and b

i∈N

t,i = 1, for all t ∈ T , if

RCt,i\[θt:T \] = bt,i Rt\[ θt:T \] , 

∀t ∈ T

and i ∈ N . 

\(11\)

A dynamic risk budgeting strategy is therefore a strategy such that at each time t ∈ T the risk contribution of investment i ∈ N is equal to bt,i % of the risk-to-go at time t. For example, if the risk budget is bt,i = 1 for all i ∈ N and t ∈ T , then we call the risk budgeting strategy risk parity, n

which means equal risk contributions, since it satisfies

RCt,i\[θt:T \] = RCt,j\[θt:T \] , 

∀i, j ∈ N and ∀ t ∈ T . 

Proposition 6. Let \{ρt\}t∈T be a coherent distortion DRM, θ an admissible strategy and ϑ its corresponding induced self-financing strategy. If θ is a risk budgeting strategy with risk budget B, then ϑ is a risk budgeting strategy with risk budget B. 

Proof:

The case when t = 0 is trivial since R0\[θ0:T \] = R0\[ϑ0:T \] and RC0,i\[θ0:T \] = RC0,i\[ϑ0:T \]. 

Next, let t > 0 and assume that θ0:T is a risk budgeting strategy. Then, for each t ∈ T /\{0\} and i ∈ N , it holds that



\! 



\! 



\! 

t−1

Y

t−1

Y

t−1

Y

RCt,i\[ϑt:T \] =

wθ RC

wθ b

wθ R

s

t,i\[θt:T \] =

s

t,i Rt\[θt:T \] = bt,i

s

t\[θt:T \] = bt,i Rt\[ ϑt:T \] , 

s=0

s=0

s=0

where we used Proposition 5 in the first equation, then the fact that θ0:T is a risk budgeting strategy, and finally Proposition 1. 

□

The next result pertains to the characterisation of self-financing risk budgeting strategies as a unique solution of a series of strictly convex and recursive \(backward in time\) optimisation problems. Moreover, we show under technical conditions that if a self-financing risk budgeting strategy with initial wealth of 1 exists, then it is given by a rescaled version of the solution to the series of convex optimisation problems. 

Theorem 3. Let \{ρt\}t∈T be a coherent distortion DRM with weight functions \{γt\}t∈T and B =

\(bt,i\)t∈T ,i∈N a risk budget. For c > 0 consider the recursive optimisation problems

" 

\#

X

θ∗ : = arg min

R

\)\] −

b

, 

∀t ∈ T . 

\(P \)

t

E

t\[\(θt, θ∗

t\+1:T

t,i log θt,i

θt∈Ac,t

i∈N

There exists a unique solution to \(P \). Furthermore, if θ∗ ∈ A˜c, for some ˜c > 0, then it satisfies Rt\[θ∗ \] = 1 a.s., for all t ∈ T , and moreover

t:T

16

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures \(a\) the self-financing strategy ϑ∗ , induced by θ∗ , is in A

0:T

0:T

0 and is a self-financing risk budgeting

strategy with risk budget B; 

\(b\) the normalised strategy ϑ†

:=

1

ϑ∗

is in A

0:T

∗⊺

ϑ

X

0:T

0 and is a self-financing risk budgeting strat-

0

0

egy with the same risk budget B and initial wealth 1. 

Proof:

As the risk-to-go process is convex, recall that the one-step risk measures are convex, and the \(− log\) is strictly convex, the objective functional is strictly convex. Moreover, the set of admissible strategies is convex, thus a unique solution to \(P \) exists. The proof that the risk-to-go process is a.s. equal to 1 follows from the proof of part \(a\). 

Part \(a\): Let the unique solution to \(P \) be denoted by θ∗ and for simplicity assume that θ∗ ∈ Ac. 

For t ∈ T , consider the objective function \(where for ease of notation we suppress the dependence of Lt on θ∗

\)

t\+1:T

" 

\#



X

Lt\[θt\] := E Rt \(θt, θ∗

\) −

b

for

θ

t\+1:T

t,i log θt,i

t ∈ Ac,t . 

\(12\)

i∈N

Next, take any θ′ ∈ A

−

t

c,t. Then, by Lemma 2 it holds that for all ε ∈ \[0, 1\], the strategy θt \+ ε

θ′t



θt = \(1 − ε\) θt \+ ε θ′ ∈ A

t

c,t. By Proposition 10, we can interchange limit and expectation, thus the one-sided Gâteaux derivative of Lt\[θt\] in direction δθ := \(θ′ − θ

t

t\) is

1 



lim

Lt\[θt \+ ε δθ\] − Lt\[θt\]

ε↓0 ε

X 



δθ

=

E Dδθi R

\)\] − b

i

i

t\[\(θt, θ∗

t\+1:T

t,i θt,i

i∈N

X 





δθ 

=

E E Dδθi R

\)\] − b

i 

i

t\[\(θt, θ∗

t\+1:T

t,i θ

Ft

t,i

i∈N

X 





X





b



=



E δθ

t\+1,i

t,i

i E

∆Xt,i \+

R

θ∗

γ

\)\] −

F

. 

\(13\)

θ∗ ⊺ X

t\+1

t\+1:T

t Ut\[\(θt, θ∗

t\+1:T

t

t\+1

θt,i

i∈N

t\+1

As Ac,t is a convex set, the unique optima θ∗ is attained where the one-sided Gâteaux derivative t

is non-negative for all θ′ ∈ A

t

c,t, see e.g., Thm. 23.2 in Rockafellar \(2015\), i.e., 1 



lim

Lt\[θ∗ \+ ε \(θ′ − θ∗\)\] − L

\] ≥ 0 , 

∀ θ′ ∈ A

t

t

t

t\[θ∗

t

t

c,t , 

ε↓0 ε

which by Equation \(13\) is equivalent to

X 



RC

\] − b

E \(θ′ − θ∗ \)

t,i\[θ∗

t:T

t,i

≥ 0 , 

∀ θ′ ∈ A

t,i

t,i

θ∗

t

c,t . 

\(14\)

i∈N

t,i

We next show that θ∗ fulfils \(14\) if, and only if, it satisfies t

RCt,i\[θ∗ \] = b

t,T

t,i , 

∀ i ∈ N . 

\(15\)

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 17

To prove this, note that if θ∗ satisfies \(15\), then \(14\) holds. To show that \(14\) implies \(15\), we t

proceed by contradiction. Suppose the equality in \(15\) does not hold a.s. for some i = k and let B\+ ∈ F, B− ∈ F, B0 ∈ F denote the sets on which \(RCt,k\[θ∗ \] − b t,T

t,k \) is positive, negative, and

zero respectively. By assumption, P\(B\+\) \+ P\(B−\) > 0. Then, define θ′ , s.t. θ′ = θ∗ for all i ̸= k, t

t,i

t,i

and

θ′ := 2 θ∗ 1

\(c \+ θ∗ \) 1

1

t,k

t,k

B− \+ 1

2

t,k

B\+ \+ θ∗

t,k

B0 , 

Note that θ′ > c a.s., moreover, θ′ ≤ 2 θ∗. Hence, we have that X

X

t

t

t

E\[\(θ′⊺

t

t\)2\] ≤ 4E\[\(θ∗⊺

t

t\)2\] < \+∞, 

′⊺

∗⊺

and θ X

X

t

t\+1

t

t\+1

∗⊺

≤ 2θ∗⊺

= 2 wθ∗ < \+∞. Therefore, θ′ ∈ A

θ

X

θ

X

t

t

c,t. However, 

t\+1

t\+1

t\+1

t\+1

1 





lim

Lt\[θ∗ \+ ε θ′ − θ∗ \] − L

\]

t

t

t

t\[θ∗

t

ε↓0 ε





\(RCt,k\[θ∗ \] − bt,k\)

= E

θ∗ 1

\(c − θ∗ \) 1

t,T

< 0, 

t,k

B− \+ 1

2

t,k

B\+

θ∗t,k

and therefore θ∗ does not satisfy \(14\), and we arrive at a contradiction. 

t

Thus, θ∗ must satisfy Equation \(15\) and by Corollary 1, it holds t

X

X

Rt\[θ∗ \] =

RC

\] =

b

\] = b

\] , 

t:T

t,i\[θ∗

t:T

t,i = 1 , 

which implies that

RCt,i\[θ∗t:T

t,i Rt\[θ∗

t:T

i∈N

i∈N

and θ∗

satisfies the risk budgeting equation \(11\) for all t ∈ T . 

t:T

Finally by Proposition 6, the self-financing strategy ϑ∗

induced by θ∗

is a risk budgeting

0:T

0:T

strategy with budget B. Moreover, if θ∗ ∈ A

∈ A

0:T

c, we have ϑ∗

0:T

0. 

Part \(b\): Define ϑ†

:=

1

ϑ∗ , clearly ϑ†

has initial wealth of 1, is self-financing, and is

0:T

∗ ⊺

ϑ

X

0:T

0:T

0

0

an element of A0, as ϑ∗⊺X

0

0 > 0, and we claim that it is a risk budgeting strategy with budget B. 

Indeed, we have for all t ∈ T and i ∈ N





RC

\]

b

1

RC

t,i\[ϑ∗

t:T

t,i

t,i\[ϑ†

\] =

=

R

\] = b

R

\] = b

\] , 

t:T

ϑ∗ ⊺X

ϑ∗ ⊺X

t\[ϑ∗

t:T

t,i

ϑ∗ ⊺X

t\[ϑ∗

t:T

t,i Rt\[ϑ†

t:T

0

0

0

0

0

0

where we applied positive homogeneity of the risk contributions, see Proposition 3, and the fact that ϑ∗

is a risk-budgeting strategy. Thus, ϑ†

is in A

0:T

0:T

0 and a self-financing risk budgeting

strategy with risk budget B and initial wealth of 1. 

□

The above result states that the unique optimiser of \(P \) is a risk budgeting strategy. In the next theorem, whose proof is delegated to Appendix B.2, we show that, under technical conditions, any self-financing risk budgeting strategy with initial wealth of 1 is a rescaled version to the solution of the optimisation problem \(P \), and in particular given in Theorem 3\(b\). 

Theorem 4 \(Uniqueness\). Let \{ρt\}t∈T be a coherent distortion DRM. Consider an admissible self-financing dynamic risk budgeting strategy ϕ

∈ A

0:T

c, for some c > 0, that has initial wealth

1 and budget B. If the corresponding risk-to-go process satisfies 0 < cR ≤ Rt\[ϕ

\] ≤ cR < \+∞ for

t:T

all t ∈ T , then the risk budgeting strategy is the unique solution to \(P \) with lower bound on the strategy c , and characterised by Theorem 3\(b\). 

cR

18

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 5. Approximation of Risk Budgeting Strategies

While Theorems 3 and 4 provide a characterisation of risk budgeting strategies as solutions to a sequence of convex optimisation problems, they do not provide a methodology for finding them. 

Thus, we develop a deep learning approach that leverages the flexibility of neural networks \(NNs\) to approximate high dimensional functions \(see e.g., Goodfellow et al. \(2016\)\), together with new techniques that have been developed for optimising convex DRMs \(Coache and Jaimungal \(2023\)

and Coache et al. \(2023\)\). The latter works solve portfolio allocation and algorithmic trading problems by making explicit use of the dual representation of convex risk measures. In contrast, our proposed approach relies on the analytical results developed for the class of coherent distortion DRM and in particular their risk contributions given in Theorem 2. 

To optimise the performance criterion Lt\[θt:T \] \(given in Equation \(12\)\) of \(P \) we make use of gradient descent methods. The Gâteaux derivative is related to the risk contributions \(see Theorem 2\) and requires evaluating the risk-to-go Rt\[θt:T \] and the rv Ut\[θt:T \]. Therefore, we develop algorithms for estimating and sampling from Rt\[θt:T \] and Ut\[θt:T \], and for estimating the Gâteaux derivative of Lt\[θt:T \]. 

The general strategy behind our actor-critic algorithm is:

1.\) Parameterise the strategy θ0:T by a NN with parameters β. 

2.\) For estimating Ut\[θt:T \], we approximate the conditional cdf of gt := θ⊺∆X

R

t

t \+ wθ

t

t\+1 given

Ft, i.e. Fg

\(z\) := P\(g

t|Ft

t ≤ z|Ft\), by a NN with parameters f. 

3.\) For estimating Rt\[θt:T \], we approximate the risk-to-go by a NN with parameters r. 

To implement points 2\) and 3\), we use the notion of elicitability – see Section 5.2 –, which provides a numerically efficient alternative to nested simulations when calculating conditional risk measures and cdfs \(Coache et al. 2023\). Specifically, we use Proposition 15 for approximating Fg

\(·\) and Proposition 14 for approximating R

t|Ft

t\[θt:T \]. 

The parameterised strategies θ0:T are the so-called “actors”, as they are at the investor’s discre-tion. The approximation of the conditional cdf and the risk-to-go are the “critics”, as they evaluate the effectiveness of a strategy. In the following subsections, we provide details on the algorithm and the gradients for training the NNs \(Section 5.1\), how conditional elicitability is leveraged in the algorithm \(Section 5.2\), and the specific NN architectures used \(Section 5.3\). 

5.1. Algorithms and Gradient Formulas

Here, we explain the general structure of the algorithm. Optimisation of the criterion Lt\[θt:T \]

proceeds in an iterative fashion, where for each iteration we update \(i\) the risk-to-go mr-times, then \(ii\) the conditional cdf mf -times, and then \(iii\) the strategy once. For the risk-to-go we employ

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 19

Algorithm 1: Actor-critic algorithm for learning risk budgeting strategies Input: NN parameters β, r, r′, and f, number of risk-to-go updates mr ≥ 1 per iteration, number of conditional cdf updates mf ≥ 1 per iteration, learning rates, soft-update rate τ

1

do

2

for i = 1, 2, . . . , mr do

3

get simulations of X0:T , Θ0:T , and \(Rt\)t∈T using Algorithm 2; 

4

compute the expected score Sρ \(18\) using the risk-to-go with main parameters r; 5

use a gradient step to minimise the score and update the risk-to-go main parameters parameters r; 6

perform a soft-update of the target to the main NN parameters r′ ← \(1 − τ \) r′ \+ τ r; 7

for j = 1, 2, . . . , mf do

8

get simulations of X0:T , Θ0:T , and \(Rt\)t∈T using Algorithm 2; 

9

compute the expected score Scdf \(19\) using conditional cdf parameters f; 10

use a gradient step to minimise the score and update the cdf parameters f; 11

get simulations of X0:T , Θ0:T , and \(Rt\)t∈T using Algorithm 2; 

12

perform a gradient step to minimise the objective \(12\) using \(16\) and update the strategy parameters β; 13

while not converged ; 

a main and a target network \(with parameters r and r′, respectively\), which is known to improve stability and convergence rates of actor-critic methods \(Mnih et al. 2015\). The main network of the risk-to-go is updated using stochastic gradient descent, while the target network is updated using soft-updates, i.e., via a convex combination of the current main and target network parameters, r′ ← \(1 − τ \)r′ \+ τ r, with soft-update rate τ ∈ \(0, 1\) \(Fujita et al. 2021\). The detailed algorithm is provided in Algorithms 1 and 2. 

Algorithm 2: Simulate asset prices, strategy, and risk-to-go. 

Input: NN parameters β and r′; 

1

simulate asset prices X0:T ; 

2

use asset prices to generate samples of the strategy Θ0:T with policy parameters β; 3

compute the risk-to-go for all simulations and time points with NN target parameters r′; Output: asset prices: X0:T , strategies: Θ0:T , risk-to-go: \(Rt\)t∈T ; Next, we discuss how the NN parameters of the strategy θ0:T are trained. Recall that the strategy’s parameters are a set of vectors \(β \)

∈ B, B ⊂ Rm. We

t t∈T , where for all t ∈ T , we have βt

write, with slight abuse of notation, θβt =

\), where

t

θt\(X0, . . . , Xt; β

θ

t

t : Rn×t × B → R. We call

β

a policy, as it parametrises the investor’s strategy. Next, for t ∈ T we view the criterion in 0:T

Equation \(12\) as a function of β , and aim to minimise it over these parameters. To this end, we t

write the time t loss function as

" 

\#



X

β∗



L

t\+1

β∗

T

t\[β ; β∗

\] :=

R \(θβt, θ

\) −

b

, 

t

t\+1:T

E

t

t

t\+1 , . . . , θT

t,i log θβt

t,i

i∈N

20

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures where β∗

are the optimal policies from time t \+ 1 onwards. We adopt for the methodology of t\+1:T

deterministic policy gradient and, starting from the current estimate of the parameters, update the parameters using the gradient step rule



β ← β − η ∇

\]

, 

t

t

β Lt\[β; β∗

t\+1:T β=βt

where 0 < η ≪ 1 is a learning rate. Hence, we require an efficient way to estimate the gradient of Lt. By the chain rule, \(as in the proof of Theorem 2\), we have

" 

\( 

\! 

X

h β∗

i

∂

t\+1,i

t\+1

β∗

T

β L

\] = E ∂ θβ

∆X

R

θ

k

t\[β; β∗

t\+1:T

βk t,i

t,i \+

β∗

⊺

t\+1

t\+1 , . . . , θT

θ t\+1

X

t\+1

t\+1

\)\#

\(16\)





β∗

b

× γ

t\+1

β∗

T

t,i

t

Ut\[\(θβ, θ

, . . . , θ

\)\] −

. 

t

t

T

θβt,i

Given a policy β, we estimate the expectation in \(16\) using its sample average, which however, h β∗

i

β∗

requires samples of

β∗

β∗

R

t\+1

T

t\+1

T

t\+1

θ

. . . , 

and U

, 

\)\]. Thus, we next elaborate on

t

θ

θ

T

t\[\(θβ

t

t\+1

. . . , θT

how we leverage the notion of conditional elicitability to simulate from these rvs. 

5.2. Conditional Elicitability

As the risk-to-go Rt\[θt:T \] = ρt \(θ⊺∆X

R

t

t \+ wθ

t

t\+1\[θt\+1:T \]\) consists of one-step \(conditional\) risk

measures, both the risk-to-go and the conditional cdf could be estimated via nested simulations, which, however is numerically expensive. To overcome this, we use the notion of elicitable functionals which circumvents the need for nested simulations. The key concept is that a functional is elicitable, e.g., mean, VaRα, ESα, if it is the minimiser of the expected value of a scoring function. Thus, an elicitable functional may be estimated by solving a convex optimisation problem. 

Furthermore, conditional elicitable functionals can be estimated by minimising the expected score over arbitrary functions of the conditioning variables \(see e.g., Proposition 7\). For completeness, in Appendix C we collect known results on elicitability and conditional elicitability that are relevant to the exposition, as well as new results pertaining to the specific risk measures considered here. 

A large class of one-step distortion risk measures are elicitable – in particular those with piecewise constant weight function – see Fissler and Ziegel \(2016\) for the static and Coache et al. \(2023\)

for the dynamic setting. In the numerical examples we consider a subclass of coherent distortion DRM given by the weighted average of the ES and expected value, but our approach can be generalised to other elicitable coherent distortion DRMs. Specifically, we consider the family of coherent distortion DRMs \{ρt\}t∈T parametrised by p ∈ \[0, 1\]

ρt\(Z\) := p ESα\(Z | Ft\) \+ \(1 − p\) E\[ Z | Ft\] , 

Z ∈ Zt\+1

\(17\)

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 21

which for each t ∈ T is a one-step distortion risk measure with weight function γ

1

t\(u\) = p

1

1−α

u≥α \+

\(1 − p\). For each p ∈ \[0, 1\], ρt\(·\) is coherent since the distortion weight function γt\(·\) is increasing. 

If p = 0, then ρt\(·\) = E\[·| Ft \] and if p = 1, then ρt\(·\) = ESα\(·| Ft \). 

For the remainder of this subsection, let \(X, Y \) be a F-measurable random vector with joint cdf FX,Y , where Y is a univariate rv with cdf FY and X an n-dimensional random vector with cdf FX. The next result explains how the one-step risk measures in \(17\) can be estimated using conditional elicitability. 

Proposition 7 \(Mean-ES risk measure\). Let ρt be given in \(17\) with p ∈ \(0, 1\). Denote by G := \{g | g : Rn → R\}. Then it holds





VaRα\(Y |X\) , ESα\(Y |X\), ρt\(Y |X\) =

arg min

E Sρ\(g1\(X\), g2\(X\), g3\(X\), Y \) , 

\(g1,g2,g3\)∈G×G×G

where, for 0 < D < \+∞, Sρ is the strictly consistent scoring function given by z



z

1





\{

z

z

2

S

2 \+ D

2

y≤z1\} − α

1 \+ 1\{y>z1\} y

3 − p z2

ρ\(z1, z2, z3, y\) : = log

−

\+

\+

− y

. \(18\)

y \+ D

z2 \+ D

\(z2 \+ D\)\(1 − α\)

1 − p

Thus, to estimate ρt\(Y |X\) we proceed similarly to Fissler and Pesenti \(2023\) and Coache et al. 

\(2023\) and parameterise each function gi with a NN gi with parameters νi, i = 1, 2, 3. Then, the NN parameters are estimated via



1 N

X





ˆ

ν1, ˆ

ν2, ˆ

ν3 = arg min

Sρ g1 \(x\(k\)\), g2 \(x\(k\)\) , g3 \(x\(k\)\) , y\(k\) , 

ν1

ν2

ν3

\(ν

N

1 , ν2 , ν3 \)

k=1

over independent simulated mini-batches \(x\(k\), y\(k\)\)k∈\{1,...,N\} of \(X, Y \). As ESα is always larger than VaRα, we set g2 := g1 \+ g4 , where g4 is a NN with parameters ν

ν2

ν1

ν2

ν2

2 and a softplus output

layer, so that g4 \(·\) ≥ 0. 

ν2

Elicitability of cdfs was shown in Gneiting and Raftery \(2007\), here we provide its conditional version; see also Proposition 15 in the appendix. 

Proposition 8 \(Conditional Distribution Function\). Denote by H := \{h | h : Rn × R →

\[0, 1\], h\(·, z\) increasing in z\}. Then it holds that





Z

FY |X\(·\) = arg min E Scdf \(F \(X, ·\), Y \) , 

where

Scdf \(x, y\) :=

\(F \(x, z\) − 1z≥y\)2 dz . 

\(19\)

F ∈H

R

As above, we parameterise the functions F ∈ H by NNs F with parameters f and estimate the parameters by

N

X L

X 

2

ˆ

1



f = arg min

Ff x\(k\), zl − 1

∆z, 

zl≥y\(k\)

f

N k=1 l=1

over independent simulated mini-batches \(x\(k\), y\(k\)\)k∈\{1,...,N\}, of \(X, Y \), and where zl := z \+ \(l −

1\)∆z, l = 1, . . . , L with ∆z := 1 \(z − z\) for truncation limits z, z, such that z < z. The inner L−1

summation is an approximation to the Riemann integral in \(19\), while the outer summation is an empirical approximation to the expectation. 

22

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 5.3. Neural Network Approximators

This section focuses on NN architectures for the strategy θ0:T , the risk-to-go process R0:T , and the uniform rvs \(Ut\[θt:T \]\)t∈T . As it is not clear whether the optimal strategy or the risk-to-go process are Markovian in asset prices, we proceed using non-Markovian parameterisations. In the context of NN approximations, recurrent NNs \(RNNs\) can be used to accomplish this goal. Our implementation employs gated recurrent units \(GRUs\) to encode non-Markovian features, though long short-term memory \(LSTM\) networks \(attention networks are viable alternatives\). Below we describe the architecture for the actor critic approach in detail. 

First, the actor \(strategy\) NN \(visualised in Figure 1\) consists of a five layered GRU, with each layer consisting of hidden states of dimension n \(recall that n is the asset dimension\). The input features into the GRU are time, the wealth process of the induced self-financing strategy, and asset prices. We denote them by yt = \(t, ϑ⊺ X

t−1

t, X t\) ∈ Rn\+2, t ∈ T , and call them the state. At each

time t ∈ T , the output from all hidden layers from the previous time step, denoted by ht−1, and the state from the current time step, yt, are concatenated and passed through a five layer feed forward NN \(FFN\) to produce an n-dimensional output corresponding to θt. The internal layers of the FFN have sigmoid linear units \(SiLU\) activation functions, while, to ensure the strategy is long only, the last layer has a softplus activation function. 

h1

h2

h3

h0

GRU

GRU

GRU

y0

y1

y2

F F N0

F F N1

F F N2

θ0

θ1

θ2

Figure 1: Directed graph representation for encodings and parameterisation of θ0:T functions. 

Next, the critic \(risk-to-go\) NN \(visualised in Figure 2\) has the same GRU and FFN structure as the strategy network, however, the final output of the FFN is three dimensional corresponding to the conditional VaR \(VaRt in Figure 2 and g1 in Proposition 7\), the difference between the conditional ES and the conditional VaR \(ESt in Figure 2 and g4 in Proposition 7\), and the conditional risk measure \(Rt in Figure 2 and g3 in Proposition 7\). There is no activation function in the final layer for VaR and the risk measure, while we have a softplus activation for the difference of ES

and VaR to ensure ES is always larger or equal to VaR. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 23

h1

h2

h3

h0

GRU

GRU

GRU

y0

y1

y2

F F N

F F N

F F N

R0

ES0

VaR0

R1

ES1

VaR1

R2

ES2

VaR2

Figure 2: Directed graph representation for encodings and parameterisation of the risk-to-go Rt, conditional ES, and conditional VaR. 

h1

h2

h3

h0

GRU

GRU

GRU

y0

y1

y2

F F N

F F N

F F N

z0

z1

z2

F0

F1

F2

Figure 3: Directed graph representation for encodings and parameterisation of Ft\(·\) := Fg \(·\). 

t|Ft

The second critic’s NN architecture \(for the conditional cdf Fg \(·\)\) is provided in Figure 3

t|Ft

and is similar to that of the risk-to-go. Two important differences are \(i\) we concatenate not only the hidden layers from the previous time step and the state, but also the value z corresponding to Fg

\(z\), and \(ii\) the output activation function is a sigmoid to ensure that F

\(z\) ∈ \(0, 1\). 

t|Ft

gt|Ft

R

We also add the additional penalty

1\{∂zF\(x,z\)<0\}\(∂zF \(x, z\)\)2 dz to the score in Proposition 15 to ensure that Fg

\(z\) is increasing in z. 

t|Ft

6. Numerical Illustrations

In this section, we explore a stochastic volatility market model and an investor searching for a risk parity allocation, i.e., bt,i = 1 for all t and i, and a risk budgeting strategy with budget n

bt = \( 1 , 2 , 3 , 4 , 5 \), under the coherent distortion DRM given in \(17\). We consider n = 5 assets 15 15 15 15 15

and a time horizon of T \+ 1 = 12, which corresponds to one year and monthly time steps. First, we describe the market model and then the optimal risk budgeting strategy. 

24

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 101

i = 1

i = 2

i = 3

i = 4

i = 5

100

10 10.75 0.50 0.25 0.00 0.25 0.50 0.75

log\(XT, i/X0, i\)

Figure 4: Distribution of log returns of various assets. 

6.1. Market Model and NN Hyperparameters

We use a discrete time version of a Heston inspired market model over a time horizon of T \+ 1 =

12 months, where asset returns have a student-t copula dependence. The investor updates their strategy monthly, corresponding to time index t ∈ T in our optimisation problem. For simulating the market model we use the real time variable tk := k ∆t \(with ∆t = 1 year\) such that t ∈ T

48

corresponds to a real time point of t4t – i.e., we take four discretisation steps between decision points. Specifically, we use a model inspired by the Milstein discretisation of the Heston model and assume





X

q

t

log

k\+1,i

= \(µ

\) ∆t \+

\(v

, 

X

i − 0.5\(vtk,i\)2\+

tk,i\)\+ ∆W X

tk,i

tk,i



q



vt

e−κi∆t \+ η

\(v

\+ 1 η2 \(∆W v \)2 − ∆t . 

k\+1,i = θi \+

\(vtk,i\)\+ − θi

i

tk,i\)\+ ∆W v

tk,i

4 i

tk,i

Here, \(·\)\+ := max\(·, 0\), \(∆W X , ∆W v \)

t

i∈N

are independent across k but not i rvs. They are

k ,i

tk,i

marginally normal with mean zero and variance ∆t. For i ̸= j and t ∈ T , we have that \(a\)

∆W X and ∆W v

are independent, and \(b\) ∆W v

and ∆W v

are independent. Moreover, 

tk,i

tk,j

tk,i

tk,j

\(∆W X , ∆W X \)

, ∆W v \)

t

i,j∈N have a student-t copula with 4 degrees of freedom and \(∆W X

i∈N

k ,i

tk,j

tk,i

tk,i

follow a Gaussian copula. The corresponding correlation matrix for the dependence structure and the additional market model parameters are provided in Appendix D.1. 

Figure 4 shows the distribution of the terminal log return while Table 6.1 provides basic statistics of the asset’s total return. As can be seen in Figure 4, the distributions are all left skewed and volatility and expected return increases with the asset index label i. 

When training the NNs we use a learning rate of 0.001, a soft-update parameter of τ = 0.001, the ADAMW method for computing gradient updates of the NN parameters, and a scheduler that decreases the learning rate by a multiplicative factor of 0.99 every 20 outer iterations of Algorithm

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 25

std. 

Sharpe

correlation

Asset

mean

dev. 

ratio

i = 1

i = 2

i = 3

i = 4

i = 5

i = 1

0.05

0.10

0.49

1

i = 2

0.08

0.16

0.48

0.17

1

i = 3

0.11

0.22

0.47

0.16

0.15

1

i = 4

0.13

0.29

0.46

0.16

0.15

0.14

1

i = 5

0.16

0.35

0.46

0.16

0.15

0.15

0.15

1

Table 1: Statistics of the asset’s total return XT,i − 1. 

X0,i

1. As well, use mr = 20 iterations for updating the risk-to-go and mf = 5 iterations for updating the conditional cdfs. The specific NN architectures we employ are as follows: \(i\) the GRUs have five layers with each layer having five hidden states, and \(ii\) the feed forward layers all have five layers with thirty two hidden nodes in each layer. We refer to Appendix D.2 for computational time metrics. 

6.2. Risk budgeting strategy

In Figure 5, we provide convergence results for the case p = 0.5 and α = 0.75. The x-axis in the figures are iterations and, for each t ∈ T , we plot the risk contributions for all assets, the sum of risk contributions across assets, and the risk-to-go. The left column contains the results for case when bt = \( 1 , 1 , 1 , 1 , 1 \) and the right panel when b

, 2 , 3 , 4 , 5 \). The shaded region shows a

5 5 5 5 5

t = \( 1

15 15 15 15 15

measure of the confidence in the estimator, that is the standard deviation of the last 200 estimates \(resulting from the learnt NN approximation of the risk-to-go and the simulated values of the risk contributions\), while the solid lines show the moving average using the last 200 estimates. 

As the figure shows, the risk-to-go all converge to the value of 1, a result of Theorem 3, and the risk contributions all converge to bt,i a result of Equation \(15\). As the risk-to-go all converge to the theoretical value of 1 and the risk contributions converge to their targeted values, this brings confidence that the numerical scheme has converged to a good approximation to the true solution of the problem. Interestingly, the risk contributions converge faster to their target values than the risk-to-go. 

To gain a deeper understanding of the learnt risk budgeting strategy, we present histograms in Figure 6 showing the percentage held in each asset across the twelve time steps. Each column in the figure represents a fixed choice of p and choice of the risk budget bt,i, while the rows correspond to different assets. 

26

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures equal bt,i

unequal bt,i

2.00

2.00

RC

RCt, 1

0.4

RCt, 1

t, i

RCt, i

1.75

0.2

i

1.75

i

0.2

1.50

1.50

0.0

0.0

1.25

0

1000

2000

3000

4000

1.25

0

1000

2000

3000

4000

1.00

RCt, 2

1.00

0.4

RCt, 2

0.2

0.75

0.75

0.2

0.50

0.0

0.50

0.0

0

1000

2000

3000

4000

0

1000

2000

3000

4000

0.25

0.25

0.00

RCt, 3

0.00

0.4

RCt, 3

0

1000

2000

3000

4000

0.2

0

1000

2000

3000

4000

0.2

2.00

2.00

t

0.0

t

0.0

1.75

0

1000

2000

3000

4000

1.75

0

1000

2000

3000

4000

1.50

RC

1.50

t, 4

0.4

RCt, 4

0.2

1.25

1.25

0.2

1.00

1.00

0.0

0.0

0

1000

2000

3000

4000

0

1000

2000

3000

4000

0.75

0.75

0.50

RCt, 5

0.50

0.4

RCt, 5

0.2

0.25

0.25

0.2

0.00

0.0

0.00

0.0

0

1000

2000

3000

4000

0

1000

2000

3000

4000

0

1000

2000

3000

4000

0

1000

2000

3000

4000

iter

iter

iter

iter

Figure 5: Risk contributions and risk-to-go versus iterations for the optimal strategy θ∗

when

0:11

p = 50% and α = 75%. Left: equal risk contributions, right: bt = \( 1 , 2 , 3 , 4 , 5 \). RC

15 15 15 15 15

t,i\[θt:T \] are

estimated using 500 simulations at each iteration. The bands and lines correspond to the moving standard deviation and moving average \(100 lags\) of the corresponding quantities. 

equal bt,i

unequal bt,i

p = 50%

p = 90%

p = 50%

p = 90%

200

50

1

50

1

100

1

1

25

i=

25

i=

50

i=

100

i=

0

0

0

0

50

50

2

2

50

2

50

2

25

i=

25

i=

25

i=

i=

0

0

0

0

40

40

40

40

3

3

3

3

20

i=

20

i=

20

i=

20

i=

0

0

0

0

40

40

40

4

4

20

4

4

20

i=

20

i=

i=

20

i=

0

0

0

0

40

50

5

50

5

20

5

5

20

i=

25

i=

10

i=

25

i=

0

0

0

0

0.0

0.1

0.2

0.3

0.4

0.0

0.1

0.2

0.3

0.4

0.0

0.1

0.2

0.3

0.4

0.0

0.1

0.2

0.3

0.4

Figure 6: Percentage of wealth invested in each asset for each point in time for α = 0.75, p = 50%

and 90%, and bt = \( 1 , 1 , 1 , 1 , 1 \) and b

, 2 , 3 , 4 , 5 \). 

5 5 5 5 5

t = \( 1

15 15 15 15 15

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 27

In the first column of Figure 6, which corresponds to the case p = 0.5 and bt,i = 1 , we observe a 5

general trend, whereby the investment in asset-i decreases as i increases. This trend is consistent with the fact that assets become increasingly volatile as the index-i increases, making it reasonable to allocate less capital to the riskier assets to generate an equal risk budgeting portfolio. For the less risky assets i = 1, 2, 3, as time increases, investments become more disperse. Contrastingly, for the more risky assets i = 4, 5, as time increases, investments become more concentrated. This is sensible, as the investor aims to have a risk parity portfolio at all point in times and hence needs to deleverage the more risky assets. It is more challenging to provide a full description of how the distributions vary with p, as there are a number of competing factors that are difficult to disentangle. If we fix e.g., the fifth row, i = 5, and compare the p = 50% case to the p = 90%

case, where the investor puts more weight on the ES, the investment becomes less variable and more left skewed meaning that they invest less in the most risky asset. If we fix, e.g., the fourth row, i = 4, we observe that as p increases, the distribution of the percentage of wealth at time 2

becomes more variable, but shifts to the left; once again indicating a deleverage. Focusing on the unequal bt,i cases in Figure 6, we see that the percentage of wealth invested in asset-i increases as i increases, which is inline with the choices of bt,i; they are now willing to take on more risk in the assets with a higher index. 

Figure 7 provides an alternative view of the evolution of the weights invested in each asset. It shows the medianm percentage of wealth invested for all assets as a function of time, together with the 20% to 80% quantile bands for the same cases shown in Figure 6. Figure 7 shows that increasing p generally induces less variability in the percentage of wealth invested. Moreover, when the risk contributions are equal, the amounts invested start almost equal weighted, but then spread out, while when the risk contributions are unequal, the amounts invested start unequal but move towards an equally weighted portfolio. 

7. Conclusion

In this work, we show how an investor can allocate investments in risky assets to attain a predefined risk budget in a dynamic setting. To do so, we first propose a notion of risk contributions for coherent distortion DRM and demonstrate that they satisfy the full allocation property. For the class of coherent distortion DRM, we derive explicit formulae for risk contributions and prove that strategies that attain a particular risk budget are specified by the solution to a collection of convex optimisation problems. Leveraging elicitability of coherent distortion DRM, we further provide a deep learning approach for solving those optimisation problems. Finally, we demonstrate the stability of the numerical scheme through several examples using a stochastic volatility market model. 

28

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures equal bt,i

p = 50%

p = 90%

0.35

0.35

i = 1

i = 1

i = 2

i = 2

0.30

i = 3

0.30

i = 3

i = 4

i = 4

i = 5

i = 5

0.25

0.25

0.20

0.20

0.15

0.15

0.10

0.10

0.05

0.05

0

3

6

9

0

3

6

9

unequal bt,i

p = 50%

p = 90%

0.35

0.35

i = 1

i = 1

i = 2

i = 2

0.30

i = 3

0.30

i = 3

i = 4

i = 4

i = 5

i = 5

0.25

0.25

0.20

0.20

0.15

0.15

0.10

0.10

0.05

0.05

0

3

6

9

0

3

6

9

Figure 7: Percentage of wealth invested in each asset for each point in time for α = 0.75, p = 50%

and 90%, and bt = \( 1 , 1 , 1 , 1 , 1 \) and \( 1 , 2 , 3 , 4 , 5 \). The lines show the median and the bands 5 5 5 5 5

15 15 15 15 15

show the 20% and 80% quantiles. 

Appendix

A. Auxiliary Definition and Results

The following definition of one-step distortion risk measures is in terms of the Choquet integral. 

Definition 8 \(One-step Distortion Risk Measures\). For each t ∈ T , let gt : \[0, 1\] × Ω → \[0, 1\]

be a \(state dependent\) distortion function such that for all ω ∈ Ω, the function gt\(·, ω\) is non-decreasing and satisfies gt\(0, ω\) = 0 and gt\(1, ω\) = 1. Further, we assume that the rv gt\(x, ·\) : Ω → \[0, 1\] is Ft-measurable for every x ∈ \[0, 1\] and for all t ∈ T . Then, the one-step \(conditional\) distortion risk measure with distortion functions \{gt\}t∈T is the family \{ρt\}t∈T , where for each t ∈ T and Z ∈ Zt\+1, ρt is defined as

Z 0 h

i

Z \+∞



ρt\(Z\) := −

1 − gt 1 − FZ|F \(x\)

dx \+

g

\(x\) dx . 

t

t 1 − FZ|Ft

−∞

0

If gt\(·, ω\) is absolutely continuous for all ω ∈ Ω, then the one-step risk measure admits representation \(2\), where the distortion weight function γt : \(0, 1\) × Ω → R\+ is given by γt\(u, ω\) := ∂− g\(x, ω\)|

∂x

x=1−u, where

∂− is the left derivative with respect to x, for all u ∈ \(0, 1\) and ω ∈ Ω, see e.g., Dhaene et al. \(2012\) for

∂x

a proof in the static setting. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 29

Lemma 1. Under Assumption 1, any coherent one-step distortion risk measure ρt is a mapping ρt : Zt\+1 → Zt, t ∈ T /\{0\} and ρ0 : Z1 → R. 

Proof:

Take Z ∈ Zt\+1, then we have by \(2\) that ρt\(Z\) is Ft-measurable, and E\[|ρ





t\(Z \)|\] = E

E Z γt\(UZ|F \)|F

t

t

h





i

1



1

1



1

≤ E E Z2|F

2

2

2

2

t

E \(γt\(UZ|F \)2|F

≤ C

E E Z2|F

< \+∞, 

t

t

t

where the first inequality follows from Cauchy-Schwartz, the second from Assumption 1, and third from Z ∈ Zt\+1. 

□

Lemma 2. For any c ≥ 0, the set of admissible strategies Ac is a convex set. 

Proof:

Let θ\(0\) and θ\(1\) be two admissible strategies and define θ\(a\) := a θ\(0\) \+ \(1 − a\) θ\(1\) for a ∈ \[0, 1\]. First note that θ\(a\) ∈ Z0:T . 

Part 1: θ\(a\) is lower bounded by c. Indeed for t ∈ T , θ\(a\) = a θ\(0\) \+ \(1 − a\) θ\(1\) > ac \+ \(1 − a\)c = c. 

0:T

t

t

t

Part 2: it holds that wθ\(a\) ∈ L∞ . For this note that

t\+1

θ\(a\)⊺X

θ\(0\)⊺X

θ\(1\)⊺X

wθ\(a\) = t

t\+1 = a

t

t\+1

\+ \(1 − a\)

t

t\+1

t



⊺



⊺

θ\(a\)⊺

t\+1 X t\+1

a θ\(0\)

X

a θ\(0\)

X

t\+1 \+ \(1 − a\) θ\(1\)

t\+1

t\+1

t\+1 \+ \(1 − a\) θ\(1\)

t\+1

t\+1

θ\(0\)⊺X

θ\(1\)⊺X

≤ a

t

t\+1

\+ \(1 − a\)

t

t\+1

= wθ\(0\) \+ wθ\(1\) < \+∞ , 

t

t

a θ\(0\)⊺

\(1 − a\) θ\(1\)⊺

t\+1 X t\+1

t\+1 X t\+1

where the first inequality follows as θ\(i\)⊺X

t

t ≥ 0 and the last by admissibility of θ\(0\) and θ\(1\). 

Part 3: For every t ∈ T , it holds that

h



1

i1





2

2

2



2

⊺

E

θ\(a\)⊺∆X

=

a θ\(0\) \+ \(1 − a\) θ\(1\) ∆X

t

t

E

t

t

t



1



1

2

2



2

2

≤ E

a θ\(0\) ⊺∆X

\+

\(1 − a\) θ\(1\) ⊺∆X

t

t

E

t

t

< \+∞ , 

where the inequality is the triangle inequality and the strict inequality by admissibility of θ\(0\) and P

h

i

2

θ\(1\). Hence, we have that

θ\(a\)⊺∆X

< \+∞. 

t∈T E

t

t

Parts 1–3 imply that θ\(a\) is admissible. 

□

Lemma 3. For any c ≥ 0, if the risk measure is a coherent distortion DRM satisfying Assumption

1, then any admissible strategy θ ∈ Ac satisfies Rt\[θt:T \] ∈ Zt, t ∈ T /\{0\}, and R\[θ0:T \] < \+∞. 

Proof:

Recall that for all t ∈ T /\{0\}, the one-step distortion risk measures are mappings ρt : Zt\+1 → Zt. Next, we proceed by induction backwards in time. At time T , the risk is RT \[θT \] = ρT θ⊺ ∆X

. 

T

T

30

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures By admissibility of θ, we have θ⊺ ∆X

T

T ∈ ZT \+1 thus RT \[θT \] ∈ ZT . Next assume that Rt\+1\[θt\+1\] ∈

Zt\+1, then the risk-to-go at time t is



Rt\[θt:T \] = ρt θ⊺∆X

R

. 

t

t \+ wθ

t

t\+1\[θt\+1:T \]

By admissibility of θ, we have θ⊺∆X

∈ L∞ , and thus wθR

t

t ∈ Zt\+1, wθ

t

t\+1

t

t\+1\[θt\+1:T \] ∈ Zt\+1 , which

implies that Rt\[θt:T \] ∈ Zt. A similar argument yields that R\[θ0:T \] < \+∞. 

□

Lemma 4. For any c ≥ 0 and θ0:T ∈ Ac, we have that E\[|RCt,i\[θt:T \]|\] < \+∞. 

Proof:

Note that





θ



E \[|RC



t,i Xt\+1,i



t,i\[θt:T \]|\] ≤ E

θt,i∆Xt,iγt Ut\[θt:T \] \+ 

R

θ⊺ X

t\+1\[θt\+1:T \]γt Ut\[θt:T \] 

t\+1

t\+1

h

i h

i1

2

2

≤ E \(θt,i∆Xt,i\)2 E γt Ut\[θt:T \]

" 

\#

\!1

θ

2

h

i 2

2

\+ E

t,i Xt\+1,i R

E

γ

θ⊺ X

t\+1\[θt\+1:T \]

t Ut\[θt:T \]

t\+1

t\+1

" 

\#\!1

X

2

h

i1

1

1

2

2

≤ C 2

E

\(θ⊺∆X

\+ C 2

wθ R

< \+∞, 

t

t\)2

E

t

t\+1\[θt\+1:T \]

t∈T

where the last inequality follows as \(i\) wθ are in L∞, \(ii\) θ is admissible, and \(iii\) R

t

t\+1\[θt\+1:T \] ∈ Zt\+1

from Lemma 2. 

□

Proposition 9 \(Lipschitz continuity of One-step Coherent Distortion Risk Measures\). 

Let ρt be a one-step coherent distortion risk measure with distortion weight function γt satisfying Assumption 1. Then, ρt is Lipschitz continuous w.r.t the conditional L2 norm, i.e. for any X, Y ∈ Zt\+1, it holds that





1

ρ



2

t\(X \) − ρt\(Y \) ≤ C

∥X − Y ∥t

a.s. , 



1

where the conditional norm ∥ · ∥



2

t is defined for all Z ∈ Zt\+1 by ∥Z ∥t :=

E Z2 Ft

, ∀ t ∈ T /\{0\}. 

Furthermore, ρ0 : Z1 → R. 

Proof

This is an adaption of Lemma 2.1 in Inoue \(2003\) to one-step distortion risk measures. 

By sub-additivity of the conditional distortion risk measure we have a.s. 



h

i

ρ



t\(X \) − ρt\(Y \) ≤ ρt X − Y

= E \(X − Y \)γt\(UX−Y |F \)F

t

t



h

i1

1

2

2

1

≤



E \(X − Y \)2F

2

2

t

E γt\(UX−Y |F \) F

≤ C ||X − Y ||

t

t

t . 

where in the second inequality we use the conditional Cauchy-Schwarz inequality, and the last inequality follows by assumption on γt. Interchanging X and Y concludes the proof. 

The fact that ρ0 : Z1 → R follows by e.g., Def. 6.37 in Shapiro et al. \(2021\). 

□

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 31

Proposition 10 \(Interchanging Expectation and Limits\). Suppose that θ = \(θt, θ∗

\) and

t\+1:T

θ′ = \(θ′ , θ∗

\) are admissible strategies, and let δθ := θ′ − θ

t

t\+1:T

t

t, then we have that





1

X

δθ

lim \(L

i

t\[θt \+ εδθ\] − Lt\[θt\]\) =

E Dδθi R

\)\] − b

. 

i

t\[\(θt, θ∗

t\+1:T

t,i

ε↓0 ε

θt,i

i∈N

Proof:

For any ε ∈ \[0, 1\], let θε := θ \+ ε δθ = \(1 − ε\) θ \+ ε θ′. By Lemma 2, θε is admissible. 

Then, by definition, we have that

1

lim \(Lt\[θt \+ εδθ\] − Lt\[θt\]\)

ε↓0 ε

1 h

X

i

= lim E Rt\[\(θε , θ∗

\)\] − R

\)\] −

b

− log θ

t

t\+1:T

t\[\(θt , θ∗

t\+1:T

t,i

log θεt,i

t,i

ε↓0 ε

i∈N

1 h





= lim E ρt θε⊺∆X

R

\] − ρ

∆X

R

\]

t

t \+ wθε

t

t\+1\[θ∗

t\+1:T

t θ⊺

t

t \+ wθ

t

t\+1\[θ∗

t\+1:T

ε↓0 ε

|

\{z

\}

=:At

X

i

−

bt,i log θε − log θ

. 

\(21\)

t,i

t,i

i∈N

|

\{z

\}

=:Bt





We next show that 1 |A

A

< \+∞, and similarly for

ε

t| ≤ At s.t. At is independent of ε and E

t





1 |B

B

< \+∞. 

ε

t| ≤ Bt s.t. Bt is independent of ε and E

t

To this end, by Proposition 9, we have that 1 





1

1

A ≤

C 



2 εδθ⊺∆X

− wθ\)R

\]

ε

t

ε

t \+ \(wθε

t

t

t\+1\[θ∗

t\+1:T

t





1

δθ⊺X

= C 

t\+1



2 δθ⊺∆Xt \+

R

\]

θ∗⊺ X

t\+1\[θ∗

t\+1:T

t\+1

t\+1

t





1





δθ⊺Xt\+1



\(by △ inequality\) ≤ C 2

δθ⊺∆Xt

\+ 

R

\]

=: A

t

θ∗⊺ X

t\+1\[θ∗

t\+1:T

t

a.s. 

t\+1

t\+1

t

Note At is independent of ε, furthermore, 

h h

i i12

C− 12 E\[At \] ≤ E E \(δθ⊺∆Xt\)2 | Ft

\(by def. ∥ · ∥t and Jensen\)

" " 



\# \#\!1

δ

2

2

θ⊺X



\+



E E

t\+1 R

\]

F

θ∗⊺ X

t\+1\[θ∗

t\+1:T

t

t\+1

t\+1





δθ⊺X



= ∥δθ⊺∆X



t\+1



t∥ \+

R

\]

0

θ∗⊺ X

t\+1\[θ∗

t\+1:T 

t\+1

t\+1

0





\(by △ inequality\) ≤ ∥θ⊺∆X

\+ θ′⊺∆X

t

t∥0

t

t

0





θ⊺X



θ′⊺X



\+ 

t

t\+1



t

t\+1





R

\]

\+

R

\]

θ∗⊺ X

t\+1\[θ∗

t\+1:T 

θ∗⊺ X

t\+1\[θ∗

t\+1:T 

t\+1

t\+1

0

t\+1

t\+1

0





= ∥





θ⊺∆X

\+ θ′⊺∆X \+ wθ R

\] \+

\]

t

t∥0

t

t

wθ1 R



0

t\+1\[θ∗

t\+1:T

0

t\+1\[θ∗

t\+1:T

0

P

1

P

1

≤ E

\(θ⊺∆X

2 \+ E

\(θ1,⊺∆X

2

t∈T

t

t\)2

t∈T

t

t\)2





\+ wθ R





t\+1\[θ∗

\]

\+ wθ1 R

\]

t\+1:T

0

t\+1\[θ∗

t\+1:T

0

< \+∞ , 

32

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures where the last inequality follows from the admissibility of θ and θ1 and from Lemma 3. 

Next, as | log\(x\) − log\(y\)| ≤ 1 |x − y| for all x, y ≥ c > 0, we have that c

X

X

X

| 1 B

c |θε − θ

|δθ

c\(|θ′ | \+ |θ

ε

t| ≤

ε

t,i

t,i| = c

t,i| ≤

t,i

t,i|\) =: Bt

i∈N

i∈N

i∈N

where c is the lower bound for admissible strategies and Bt is independent of ε. As θ and θ′ are in Z, we have that E\[Bt\] < \+∞. 

Putting these bounds together, we have by Lebesgue dominated convergence that the limε↓0 in

\(21\) may be moved under the expectation, and the claim follows. 

□

Proposition 11. Let ρt be a one-step coherent distortion risk measures with distortion weight function γt satisfying Assumption 1. Let t ∈ T and Y, W ∈ Zt\+1, where we assume that \(Y, W \) has a joint density, though the proof can be generalised to include point masses. If ε → F −1

\(u\) is

Y \+εW

differentiable in a neighbourhood around ε = 0 with bounded derivative, for all u ∈ \(0, 1\), then it holds that

ρ





lim t \(Y \+ ε W \) − ρt\(Y \) = E W γt UY |F |F

, 

\(22\)

t

t

ε→0

ε

Proof:

First we define the conditional cdfs F \(y\) := P\(Y ≤ y | Ft\) and F \(y, ε\) := P\(Y \+ ε W ≤

y | Ft\) and their corresponding densities by f \(y\) and f \(y, ε\). We further write F −1\(u\) and F −1\(u, ε\) for the quantile functions of F \(·\) and F \(·, ε\), respectively. 

Next using ρt \(Y \+ ε W \) = E \[F −1\(U, ε\) γt\(U\) | Ft\], for a uniform rv U ∈ Ft, the integrability assumption on γt, and the differentiability assumption on F −1\(u, ε\), the mean value theorem together with Lebesgue dominated convergence allows us to interchange expectation and limit to obtain

ρ





lim t \(Y \+ ε W \) − ρt\(Y \) =



E ∂εF −1\(U, ε\) γt\(U \) | Ft 

. 

\(23\)

ε→0

ε

ε=0

By taking a derivative with respect to ε of the equation F \(F −1\(u, ε\), ε\) = u, we obtain for all u ∈ \(0, 1\), 

∂



∂

εF \(y, ε\) 

εF −1\(u, ε\) = −



\(24\)

f \(y, ε\) y=F−1\(u,ε\)

Next, we calculate the derivative ∂εF \(y, ε\). For this note that 1

∂εF \(y, ε\) = ∂εE\[1Y \+εW≤y | Ft\] = lim E \[1Y \+εW≤y − 1Y ≤y | Ft\]

ε→0 ε

Z





1





1

y



= lim

E E 1



Y ∈\(y−εW,y\] | W

| Ft = lim

E

dFY |W \(y′\)

ε→0 ε

ε→0 ε

Ft

y−ε W





= − E W fY |W \(y\) | Ft , 

\(25\)

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 33

where, FY |W and fY |W are the distribution and density, respectively, of Y conditional on W . 

Plugging \(24\) and \(25\) into Equation \(23\), we obtain

" 





\#

ρ

E W f





lim t \(Y \+ ε W \) − ρt\(Y \) =

Y |W \(y\) 



E



γt\(U \) Ft

ε→0

ε

f \(y\)

y=F −1\(U \)





=



E E \[W | Y = y\] 

γ



t\(U \) Ft

y=F −1\(U \)

= E \[E \[W | F \(Y \) = U\] γt\(U\) | Ft\]





= E W γt\(UY |F \) | F . 

t

t

□

B. Additional Proofs

B.1. Proof of Proposition 4

First we generalise the Gâteaux derivative as follows. For a functional Ft : Zt:T → Zt, t ∈ T and s ≥ t, we denote by Dζ F

s,i

t, its Gâteaux derivative of the ith component at time s in direction ζ ∈ Zs. That is, for s, t ∈ T , s ≥ t, and Zt:T ∈ Z

1 



Dζ F

F

. 

s,i

t\[Z t:T \] := lim

t\[Z t:T \+ ε 1s,iζ \] − Ft\[Z t:T \]

ε→0 ε

Next, note that



RCt,i\[θt:T \] = Dθt,i ρ

∆X

θ

i

t

θ⊺t

t \+ Rt\+1\[wθ

t

t\+1:T \]

1 n 

= lim

ρt εθt,i∆Xt,i \+ εDθt,iR

θ

t,i

t\+1\[wθ

t

t\+1:T \]

ε→0 ε



o

\+ θ⊺∆X

θ

− R

t

t \+ Rt\+1\[wθ

t

t\+1:T \]

t\[θt:T \]

h





i

by \(9\)

=



E

θt,i∆Xt,i \+ Dθt,iR

θ

Γθ

. 

\(26\)

t,i

t\+1\[wθ

t

t\+1:T \]

t Ft

Next, we show that for all s ∈ \{t, . . . , T \}, that





T

X

θ



Dθt,i



R

wθ θ

=

t,i Xt\+1,i \(θ⊺∆X

· · · Γθ

\(27\)

t,i

s

t

s:T

E

F

θ⊺ X

r

r \) Γθ

s

r

s

t\+1

r=s

t\+1

While we require the above equation for the case s = t \+ 1 only, to make the proof easier to understand, we introduce an additional variable s and use mathematical induction over s. First we show that Equation \(27\) holds for s = T . To see this we calculate 1

θ



Dθt,i R

wθ θ

= lim

ρ

wθ\(θ⊺ ∆X

t,i Xt\+1,i \(θ⊺ ∆X

− ρ

\(θ⊺ ∆X

t,i

T

t

T

T

t

T

T \) \+ ε

T

T \)

T

wθt T

T \)

ε→0 ε

θ⊺ X

t\+1

t\+1





θ



=



E

t,iXt\+1,i \(θ⊺ ∆X

F

, 

θ⊺ X

T

T \) Γθ

T

T

t\+1

t\+1

34

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures where we applied Equation \(9\) to obtain the last equality. Next, assuming Equation \(27\) holds for all r ∈ \{s \+ 1, . . . , T \}, we show that it also hols for s. Indeed, using the definition of a Gâteaux derivative, i.e., that Fs\[Zs:T \+ ε 1t,iζ\] = ε Dζ F

t,i

s\[Z s:T \] \+ Fs\[Z s:T \] \+ o\(ε\), we obtain



by \(3\)





Dθt,i R wθ θ

= Dθt,i ρ

θ⊺∆X

wθ θ

t,i

s

t

s:T

t,i

s

wθt s

s \+ Rs\+1

t

s\+1:T



1

θ⊺ Xt\+1,i

= lim

ρ

t,i

s

ε

θ⊺∆X

θ⊺∆X

s

s \+ wθ

t

s

s

ε→0 ε

θ⊺ X

t\+1

t\+1





\+ ε Dθt,i R

wθ θ

\+ R

wθ θ

− R wθ θ

t,i

s\+1

t

s\+1:T

s\+1

t

s\+1:T

s

t

s:T





by \(9\)

θ⊺ Xt\+1,i





=



E

t,i

θ⊺∆X

R

wθ θ

Γθ F

θ⊺ X

s

s \+ Dθt,i

t,i

s\+1

t

s\+1:T

s

s

t\+1

t\+1

θ⊺ Xt\+1,i

= E

t,i

θ⊺∆X

θ⊺ X

s

s

t\+1

t\+1

\#

T

X



\! 

θ





\+





E

t,iXt\+1,i θ⊺∆X

· · · Γθ F

Γθ F

θ⊺ X

r

r Γθ

s\+1

r

s\+1

s

s

t\+1

r=s\+1

t\+1

T

X 





θ





=





E E

t,iXt\+1,i θ⊺∆X

· · · Γθ F

Γθ F

θ⊺ X

r

r Γθ

s\+1

r

s\+1

s

s

t\+1

r=s

t\+1

T

X 



θ



=



E

t,iXt\+1,i θ⊺∆X

· · · Γθ F , 

θ⊺ X

r

r Γθ

s

r

s

t\+1

r=s

t\+1

where we use the induction argument in fourth equation and that Γθ ∈ F

s

s in the last equality. This

concludes the proof of Equation \(27\). 

Finally combining \(27\) with \(26\), noticing that Γθ ∈ F

t

t, and using the law of iterated expectations

concludes the proof. 

□

B.2. Proof of Theorem 4

Proof:

Let ϕ

∈ A

0:T

c denote a self-financing risk budgeting strategy with budget B and initial wealth of 1, whose risk-to-go satisfies cR ≤ Rt\[ϕ

\] ≤ cR a.s. for all t ∈ T . We show that ϕ

=

t:T

0:T

1

∗ ⊺

ϑ∗ , where ϑ∗

is the induced self-financing strategy of the unique solution to optimisation ϑ

X

0:T

0:T

0

0

problem \(P \), i.e., given by Theorem 3\(b\) with lower bound c′ := c . For this we proceed by cR

contradiction. Assume ϕ

̸=

1

ϑ∗

and define the \(not necessarily self-financing\) strategy

0:T

∗ ⊺

ϑ

X

0:T

0

0

ψ

via

0:T

1

ψ :=

ϕ , 

∀t ∈ T . 

\(28\)

t

R

t

t\[ϕ

\]

t:T

It holds that ψ ∈ Ac′. This follows as the bounds on Rt\[ψ

\] implies that wψ ∈ L∞, and R

\] ≤

t:T

t

t

t\[ψt:T

cR guarantees that ψ =

1

ϕ ≥ c′, for all t ∈ T . Next, we show that the risk-to-go process of t

Rt\[ϕ

t

t:T \]

ψ

satisfies

0:T

Rt\[ψ

\] = 1 , 

∀t ∈ T . 

\(29\)

t:T

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 35

We proceed by induction. At time T , by positive homogeneity of RT , and since cR ≤ RT \[ϕ \] ≤ cR: T

1

RT \[ψ \] =

R

\] = 1 . 

T

R

T \[ϕT

T \[ϕ \]

T

Assume Equation \(29\) holds for t \+ 1, then, again using cR ≤ Rt\[ϕ

\] ≤ cR, 

t:T



Rt\[ψ

\] = ρ

∆X

\]

t:T

t

ψ⊺t

t \+ wψ

t Rt\+1\[ψt\+1:T





ψ⊺X

= ρ

t

t\+1

t

ψ⊺∆X

t

t \+ ψ⊺ X

t\+1

t\+1





1

R

\] ϕ⊺

= ρ

t\+1\[ϕt\+1:T

t X t\+1

t

ϕ⊺∆X

R

t

t \+

t\[ϕ

\]

R

\]

ϕ⊺

t:T

t\[ϕt:T

t\+1X t\+1

1



\(by positive homogeneity of ρ

ρ

∆X

\]

t \(·\) and ϕ is self-financing\) = R

t

ϕ⊺t

t \+ Rt\+1\[ϕt\+1:T

t\[ϕ

\]

t:T

= 1 , 

Thus, Equation \(29\) holds for all t ∈ T . 

Next, we show that ψ

is a risk budgeting strategy with budget B. By positive homogeneity 0:T

of risk contributions \(Proposition 3\) we obtain 1

1

RCt,i\[ψ

\] =

RC

\] =

b

\] = b

\] . 

t:T

R

t,i\[ϕt:T

t,i Rt\[ϕt:T

t,i = bt,i Rt\[ψt:T

t\[ϕ

\]

R

\]

t:T

t\[ϕt:T

Thus, ψ

is not only a risk budgeting strategy but also a solution to optimisation problem \(P \)

0:T

with lower bound c′, that is for all t ∈ T it satisfies Equations \(15\). As ψ ∈ Ac′ is a solution to optimisation problem \(P \) with Ac′, it induces a self-financing, risk budgeting strategy, with initial wealth of 1 as given in Theorem 3\(b\), and denoted here by ϑ0:T . Specifically, we have



\! 

1

1

t−1

Y

ϑ0 :=

ψ , 

and

ϑ

wψ

ψ , 

∀t ∈ T /\{0\} , 

ψ⊺X

0

t := ψ⊺X

s

t

0

0

0

0

s=0

Finally, we show that ϑ0:T = ϕ

. For this recall that ϕ

is a self-financing strategy with initial

0:T

0:T

wealth of 1, thus

1

R

\]

ϕ

ϑ

0\[ϕ0:T

0

0 =

ψ =

= ϕ . 

ψ⊺X

0

ϕ⊺

R

\]

0

0

0

0X 0

0\[ϕ0:T

For t ∈ T /\{0\}, we have



\! 

1

t−1

Y ψ⊺X

ϑ

s

s\+1

t =

ψ

ψ⊺X

ψ⊺

X

t

0

0

t\+1

s=0

s\+1



\! 

t−1

R

\]

Y R

\] ϕ⊺X

ϕ

=

0\[ϕ0:T

s\+1\[ϕs\+1:T

s

s\+1

t

ϕ⊺0X0

Rs\[ϕ

\]

ϕ⊺

Rt\[ϕ

\]

s=0

s:T

s\+1X t\+1

t:T



\! 

t−1

Y Rs\+1\[ϕ

\]

s\+1:T

ϕt

\(as ϕ

\]

0:T is self-financing\) = R0\[ϕ0:T

Rs\[ϕ

\]

Rt\[ϕ

\]

s=0

s:T

t:T

= ϕ . 

t

Thus, ϕ

= ϑ

0:T

0:T and as ϑ0:T is given by Theorem 3\(b\), we arrive at a contradiction. Uniqueness follows from strict convexity of the optimisation problem \(P \). 

□

36

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures C. Elicitability

We first recall the classical definition of elicitability and scoring functions, see e.g., Fissler and

Ziegel \(2016\). For this first define the set of cdfs M := \{FY | Y ∈ FT\+1\}. 

Definition 9 \(Elicitability\). A functional T : M → A, A ⊂ Rk, is called k-elicitable on f M ⊆ M, 

if there exists a measurable function S : A × R → \[0, ∞\] – called a strictly consistent scoring function –

if for all F ∈ f

M and for all z ∈ A

Z



Z

S T\(F \), y dF \(y\) ≤

S\(z, y\) dF \(y\) , 

\(30\)

and equality in \(30\) holds only if z = T\(F \). 

In the numerical examples, we consider the family of coherent distortion DRM \{ρt\}t∈T , a convex combination of the mean and ES, given in \(17\). We first illustrate that its static version ρ\(Z\) := p ESα\(Z\) \+ \(1 − p\) E\[X\] , 

Z ∈ ZT\+1 , 

\(31\)

is elicitable. While the mean is well-known to be 1-elicitable, the ESα is only jointly elicitable together with VaRα at the same α-level. We recall these well-known results. 

Proposition 12 \(Mean – Gneiting \(2011\)\). Let φ : R → R be strictly convex with subgradient R

φ′ and denote by M† ⊂ M be the class of cdfs with finite mean such that

|φ\(y\)| dF \(y\) < \+∞ for

all F ∈ M†. Then

SE\(z, y\) := φ′\(z\)\(z − y\) − φ\(z\) \+ φ\(y\) , 

z, y ∈ R , 

is strictly M†-consistent for the mean. 

Proposition 13 \(\(VaR, ES\) – Acerbi and Szekely \(2014\), Fissler and Ziegel \(2016\)\). 

Let α ∈ \(0, 1\), A := \{\(z1, z2\) ∈ R2 : z1 ≥ z2\} and define the scoring functions SVaR,ES : A × R → R

by





SVaR,ES\(z1, z2, y\) = 1\{y≤z

g\(z

1\} − α

1\) − g\(y\)





\+ Φ′\(z2\) z2 − 1 S\+\(z

− Φ\(z

1−α

α

1, y\)

2\) \+ Φ\(y\) , 

where S\+\(z

α

1, y\) = \(1\{y≤z1\} − α\)z1 − 1\{y≤z1\}y \+ y, Φ : R → R is strictly convex with subgradient Φ′

and g : R → R is such that for all z2 ∈ R

z1 7→ g\(z1\) − z1Φ′\(z2\)/\(1 − α\)

is strictly increasing. 

R

Let M‡ ⊂ M be the cdfs with unique α-quantile, finite mean, and such that

|g\(y\)| dF \(y\) < \+∞

R

and

|Φ\(y\)| dF \(y\) < \+∞ for all F ∈ M‡. Then SVaR,ES is strictly M‡-consistent for the couple \(VaRα, ESα\). 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 37

Next, we show that for p ∈ \(0, 1\), the risk measure ρ given in \(31\) is 3-elicitable, that is jointly elicitable together with VaRα and ESα. The following proposition is different to Corollary 5.4 in Fissler

and Ziegel \(2016\), which states that ρ is 4-elicitable, specifically they show that \(VaRα, ESα, E, ρ\) is jointly elicitable. 

Proposition 14 \(Mean-ES risk measure\). For p ∈ \(0, 1\), let ρ be given in \(31\) and let the assumptions of Propositions 12 and 13 be enforced. Then the function Sρ : A × R2 → \[0, ∞\] given by





z

S

3 − p z2

ρ\(z1, z2, z3, y\) : = SVaR,ES\(z1, z2, y\) \+ SE

, y

, 

\(32\)

1 − p

is a strictly M‡-consistent scoring function for the triplet \(VaRα, ESα, ρ\). 

Proof:

From Propositions 12 and 13, the functionals \(VaRα, ESα\) and E are elicitable. Using Lemma 2.6 in Fissler and Ziegel \(2016\), we obtain that \(VaRα, ESα, E\) is elicitable with consistent scoring function given by

SVaR,ES,E\(z1, z2, z3, y\) = SVaR,ES\(z1, z2, y\) \+ SE\(z3, y\) . 

Next, we apply Osband’s revelation principle, see e.g., Theorem 4 in Gneiting \(2011\). First, 

⊺

define the bijective function g : R3 → R3 by g\(z1, z2, z3\) = z1, z2, pz2 \+ \(1 − p\)z3

with inverse



⊺

g−1\(a1, a2, a3\) = a1, a2, a3−pa2

. The revelation principle states that g\(VaR, ES, E\) = \(VaR, ES, ρ\)⊺

1−p

is elicitable with scoring function





z

S

3 − p z2

VaR,ES,ρ\(z1, z2, z3, y\) = SVaR,ES,E g−1\(z1, z2, z3\)⊺, y = SVaR,ES\(z1, z2, y\) \+ SE

, y

. 

1 − p

Moreover, if the scoring functions SVaR,ES\(z1, z2, y\) and SE\(z3, y\) are strictly consistent for \(VaR, ES\) and E, respectively, then SVaR,ES,ρ\(z1, z2, z3, y\) is strictly consistent for \(VaR, ES, ρ\). 

□

In our implementations, we make the specific choices of φ\(z\) = z2, g\(z\) = C and Φ\(z\) = − log\(z \+

C\), where C > 0. 

Finally, we need to elicit the conditional cdf FY |X : R → \[0, 1\], defined by FY |X\(y\) := P\(Y ≤

y | X = x\), for any Y ∈ Zt\+1, X ∈ Zt, and x ∈ Rn. Cdfs are known to be elicitable with the continuous ranked probability score, see e.g. Equation \(20\) in Gneiting and Raftery \(2007\). Here we recall the key result. 

Proposition 15 \(Distribution Function – Gneiting and Raftery \(2007\)\). Let M† be the set of cdfs with finite mean. Then the scoring function Scdf : M† × R → \[0, ∞\] given by Z

Scdf \(F, y\) :=

\(F \(z\) − 1z≥y\)2 dz , 

\(33\)

R

38

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures is a strictly consistent scoring function for FY . In particular, it holds that arg min E\[ Scdf \(F, Y \) \] , 

F ∈M†

is attained by the cdf FY : R → \[0, 1\]. 

Next, we consider the concept of conditional elicitability. Let \(X, Y \) be a random vector with joint cdf FX,Y , where Y is a univariate rv with cdf FY and X an n-dimensional random vector with cdf FX. Further, let S : A × R → \[0, ∞\] be a strictly consistent scoring function that elicits the functional T : M → A. Next define the expected score S : Mn\+1 → \[0, ∞\] by Z





Z Z



S\(FX,Y , g\) :=

S g\(x\), y FX,Y \(dx, dy\) =

S g\(x\), y FY |X=x\(dy\) FX\(dx\) , 

where Mn\+1 is the space of cdfs of \(n \+ 1\)–dimensional random vectors, and G := \{g | g : Rn →

R , with S\(F, g\) < \+∞\}. Then the expected score satisfies

Z Z





S\(FX,Y , g\) =

S g\(x\), y FY |X=x\(dy\) FX\(dx\)

Z Z





\(by def. 9\) ≥

S T\(FY |X=x , y\) FY |X=x\(dy\) FX\(dx\)

Z





=

S T\(FY |X=x\) , y FX,Y \(dx, dy\) = S FX,Y , T\(FY |X\) . 

Therefore, T\(FY |X\) minimises the expected score S\(F, g\) over all functions g. Note, we may also write S\(F, g\) := E\[S\(g\(X\), Y \)\] with the expectation taken over a probability measure where \(X, Y \) has cdf FX,Y . We can approximate the minimiser of this expected score by seeking over a rich parameterised class of functions \(such as NNs\) and estimate the expectation using the empirical mean from simulations. This is what we use when eliciting approximations of Rt\[θt:T \] and Ut\[θt:T \]. 

D. Additional Information on Numerical Implementation

D.1. Parameters used in Market Model Simulation. 

This section contains further details on the simulated market model simulation. In particular, Table

2 specifies the market model parameters and Table 3 gives the correlation matrix of the dependence structure. 

i = 1

i = 2

i = 3

i = 4

i = 5

κi

4

4.5

5

5.5

6

θi

0.01

0.0225

0.04

0.0625

0.09

ηi

0.5

0.875

1.25

1.625

2

µi

0.05

0.075

0.10

0.125

0.15

Table 2: Market model parameters. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 39

X1

X2

X3

X4

X5

v1

v2

v3

v4

v5

X1

1.0

0.3

0.3

0.3

0.3 -0.5

X2

0.3

1.0

0.3

0.3

0.3

-0.5

X3

0.3

0.3

1.0

0.3

0.3

-0.5

X4

0.3

0.3

0.3

1.0

0.3

-0.5

X5

0.3

0.3

0.3

0.3

1.0

-0.5

v1

-0.5

1.0

v2

-0.5

1.0

v3

-0.5

1.0

v4

-0.5

1.0

v5

-0.5

1.0

Table 3: Correlation matrix of dependence structure for the market model. Only non-zero entries are shown. 

D.2. Computation Times

Table 4 shows the average time the algorithm takes to execute one full outer iteration, which includes mr = 20 iterations for updating the risk-to-go, mf = 5 iterations for updating the conditional cdf, and one iteration for updating the strategy. Models were trained on a Intel\(R\) Xeon\(R\) CPU E5-2630 v4@2.20GHz \(from 2016\) with 64GB of RAM equipped with an NVDIA TITAN

RTX GPU \(from 2018\). As the results show, the timing scales approximately linearly with time steps, but increases only marginally with number of assets. The largest limitation is the size of memory on the GPUs for computing gradients. 

T\+1

d

2

4

8

16

2

0.71 1.44 3.26

8.05

4

0.73 1.46 3.28

8.83

8

0.75 1.54 3.39 10.10

Table 4: Average execution time \(in seconds\) per outer iteration with mr = 20 and mf = 5. 

Acknowledgments

SJ and SP acknowledge support from the Natural Sciences and Engineering Research Council of Canada \(grants RGPIN-2018-05705, RGPAS-2018-522715, and DGECR-2020-00333, RGPIN-2020-04289\). 

RT acknowledges the support from CNPq \(200293/2022-2\) and FAPERJ \(E-26/201.350, E-26/211.426, E-26/211.578\). YS acknowledges the support from CNPq \(306695/2021-9\) and FAPERJ \(E-26/201.375/2022

272760\)

40

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures References

Acerbi C, Szekely B \(2014\) Backtesting Expected Shortfall. Risk Magazine . 

Anis HT, Kwon RH \(2022\) Cardinality-constrained risk parity portfolios. European Journal of Operational Research 302\(1\):392–402. 

Asness CS, Frazzini A, Pedersen LH \(2012\) Leverage aversion and risk parity. Financial Analysts Journal 68\(1\):47–59. 

Bai X, Scheinberg K, Tutuncu R \(2016\) Least-squares approach to risk parity in portfolio selection. Quantitative Finance 16\(3\):357–376. 

Bellini F, Cesarone F, Colombo C, Tardella F \(2021\) Risk parity with expectiles. European Journal of Operational Research 291\(3\):1149–1163. 

Bielecki TR, Chen T, Cialenco I \(2022\) Risk-sensitive markov decision problems under model uncertainty: finite time horizon case. Stochastic Analysis, Filtering, and Stochastic Optimization: A Commemorative Volume to Honor Mark HA Davis’s Contributions, 33–52 \(Springer\). 

Bielecki TR, Cialenco I, Liu H \(2023\) Time consistency of dynamic risk measures and dynamic performance measures generated by distortion functions. arXiv preprint arXiv:2309.02570 . 

Bielecki TR, Cialenco I, Pitera M \(2018\) A unified approach to time consistency of dynamic risk measures and dynamic performance measures in discrete time. Mathematics of Operations Research 43\(1\):204–221. 

Billera LJ, Heath DC \(1982\) Allocation of shared costs: A set of axioms yielding a unique procedure. 

Mathematics of Operations Research 7\(1\):32–39. 

Björk T, Khapko M, Murgoci A, et al. \(2021\) Time-inconsistent control theory with finance applications, volume 732 \(Springer\). 

Bruder B, Kostyuchyk N, Roncalli T \(2016\) Risk parity portfolios with skewness risk: An application to factor investing and alternative risk premia. Available at SSRN 2813384 . 

Chaves D, Hsu J, Li F, Shakernia O \(2011\) Risk parity portfolio vs. other asset allocation heuristic portfolios. 

The Journal of Investing 20\(1\):108–118. 

Cheridito P, Delbaen F, Kupper M \(2006\) Dynamic monetary risk measures for bounded discrete-time processes. Electronic Journal of Probability 11:57–106. 

Cherny AS \(2009\) Capital allocation and risk contribution with discrete-time coherent risk. Mathematical Finance 19\(1\):13–40. 

Choueifaty Y, Coignard Y \(2008\) Toward maximum diversification. The Journal of Portfolio Management 35\(1\):40–51. 

Coache A, Jaimungal S \(2023\) Reinforcement learning with dynamic convex risk measures. Mathematical Finance \(forthcoming\). 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 41

Coache A, Jaimungal S, Cartea Á \(2023\) Conditionally elicitable dynamic risk measures for deep reinforcement learning. SIAM Journal on Financial Mathematics 14\(4\):1249–1289. 

da Costa BFP, Pesenti SM, Targino R \(2023\) Risk budgeting portfolios from simulations. European Journal of Operational Research 311\(3\):1040–1056. 

Denault M \(2001\) Coherent allocation of risk capital. Journal of Risk 4:1–34. 

Dhaene J, Kukush A, Linders D, Tang Q \(2012\) Remarks on quantiles and distortion risk measures. European Actuarial Journal 2:319–328. 

Fissler T, Pesenti SM \(2023\) Sensitivity measures based on scoring functions. European Journal of Operational Research 307\(3\):1408–1423. 

Fissler T, Ziegel JF \(2016\) Higher order elicitability and Osband’s principle. The Annals of Statistics 44:1680–

1707. 

Fujita Y, Nagarajan P, Kataoka T, Ishikawa T \(2021\) Chainerrl: A deep reinforcement learning library. The Journal of Machine Learning Research 22\(1\):3557–3570. 

Gneiting T \(2011\) Making and Evaluating Point Forecasts. Journal of the American Statistical Association 106\(494\):746–762. 

Gneiting T, Raftery AE \(2007\) Strictly proper scoring rules, prediction, and estimation. Journal of the American statistical Association 102\(477\):359–378. 

Goodfellow I, Bengio Y, Courville A \(2016\) Deep learning \(MIT press\). 

Haugh MB, Iyengar G, Song I \(2017\) A generalized risk budgeting approach to portfolio construction. Journal of Computational Finance 21\(2\):29–60. 

Inoue A \(2003\) On the worst conditional expectation. Journal of Mathematical Analysis and Applications 286\(1\):237–247. 

Ji R, Lejeune MA \(2018\) Risk-budgeting multi-portfolio optimization with portfolio and marginal risk con-straints. Annals of Operations Research 262\(2\):547–578. 

Jurczenko E, Teiletche J \(2019\) Expected Shortfall asset allocation: A multi-dimensional risk-budgeting framework. The Journal of Alternative Investments 22\(2\):7–22. 

Kalkbrener M \(2005\) An axiomatic approach to capital allocation. Mathematical Finance 15\(3\):425–437. 

Kromer E, Overbeck L \(2014\) Representation of BSDE-based dynamic risk measures and dynamic capital allocations. International Journal of Theoretical and Applied Finance 17\(05\):1450032. 

Kromer E, Overbeck L \(2017\) Differentiability of bsvies and dynamic capital allocations. International Journal of Theoretical and Applied Finance 20\(07\):1750047. 

Kusuoka S \(2001\) On law invariant coherent risk measures. Advances in mathematical economics 83–95. 

Lassance N, DeMiguel V, Vrins F \(2022\) Optimal portfolio diversification via independent component analysis. Operations Research 70\(1\):55–72. 

42

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures Lee W \(2011\) Risk-based asset allocation: A new answer to an old question? The Journal of Portfolio Management 37\(4\):11–28. 

Maillard S, Roncalli T, Te¨ıletche J \(2010\) On the properties of equally weighted risk contribution portfolios. 

The Journal of Portfolio Management 36\(4\):60–70. 

Mastrogiacomo E, Rosazza-Gianin E \(2022\) Dynamic capital allocation rules via BSDEs: An axiomatic approach. Annals of Operations Research 1–24. 

Meucci A, Santangelo A, Deguest R \(2015\) Risk budgeting and diversification based on optimized uncorrelated factors. Risks 11\(29\):70–75. 

Mirman LJ, Tauman Y \(1982\) Demand compatible equitable cost sharing prices. Mathematics of Operations Research 7\(1\):40–56. 

Mnih V, Kavukcuoglu K, Silver D, Rusu AA, Veness J, Bellemare MG, Graves A, Riedmiller M, Fidje-land AK, Ostrovski G, et al. \(2015\) Human-level control through deep reinforcement learning. nature 518\(7540\):529–533. 

Pesenti SM, Millossovich P, Tsanakas A \(2021\) Cascade sensitivity measures. Risk Analysis 41\(12\):2392–

2414. 

Qian E \(2005\) Risk parity portfolios: Efficient portfolios through true diversification. Panagora Asset Management . 

Qian E \(2011\) Risk parity and diversification. The Journal of Investing 20\(1\):119–127. 

Rockafellar RT \(2015\) Convex analysis:\(pms-28\) . 

Roncalli T \(2013\) Introduction to risk parity and budgeting \(Chapman & Hall, Boca Raton, FL\). 

Roncalli T, Weisang G \(2016\) Risk parity portfolios with risk factors. Quantitative Finance 16\(3\):377–388. 

Rüschendorf L \(2013\) Mathematical risk analysis. Springer Ser. Oper. Res. Financ. Eng. Springer, Heidelberg

. 

Ruszczyński A \(2010\) Risk-averse dynamic programming for Markov decision processes. Mathematical programming 125\(2\):235–261. 

Schilling K, Bauer D, Christiansen MC, Kling A \(2020\) Decomposing dynamic risks into risk components. 

Management Science 66\(12\):5738–5756. 

Shapiro A, Dentcheva D, Ruszczynski A \(2021\) Lectures on stochastic programming: modeling and theory \(SIAM\). 

Tasche D \(1999\) Risk contributions and performance measurement. Report of the Lehrstuhl für mathematis-che Statistik, TU München . 

Tsanakas A \(2004\) Dynamic capital allocation with distortion risk measures. Insurance: Mathematics and Economics 35\(2\):223–243. 

Pesenti, Jaimungal, Saporito, Targino: Risk Budgeting Allocation for Dynamic Risk Measures 43

Tsanakas A \(2009\) To split or not to split: Capital allocation with convex risk measures. Insurance: Mathematics and Economics 44\(2\):268–277. 

Tsanakas A, Barnett C \(2003\) Risk capital allocation and cooperative pricing of insurance liabilities. Insurance: Mathematics and Economics 33\(2\):239–254. 

Tsanakas A, Millossovich P \(2016\) Sensitivity analysis using risk measures. Risk Analysis 36\(1\):30–48. 


# Document Outline

+ Introduction 
+ Dynamic Risk Assessment  
	+ Dynamic Risk Measures 
	+ Risk-to-go of a Strategy 
	+ Dynamic Risk Contributions 
	+ Dynamic Risk Budgeting Portfolios  
		+ Approximation of Risk Budgeting Strategies  
			+ Algorithms and Gradient Formulas 
			+ Conditional Elicitability 
			+ Neural Network Approximators 

		+ Numerical Illustrations  
			+ Market Model and NN Hyperparameters 
			+ Risk budgeting strategy 



+ Conclusion 
+ Auxiliary Definition and Results 
+ Additional Proofs  
	+ Proof of Proposition 4 
	+ Proof of Theorem 4 
	+ Elicitability 
	+ Additional Information on Numerical Implementation  
		+ Parameters used in Market Model Simulation.  
		+ Computation Times



