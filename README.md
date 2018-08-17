Introduction
============


A genetic algorithm based approach to simulate kinetics of
co-transcriptional folding.


Progress
========

Framework
---------

Various algorithms or programs have been developed to predict RNA
folding pathway ultilizing force-field based simulations and multiple
coarse grained energy landscape sampling methods built on Markov state
model. Those present methods have succeeded in revealing multiscale
dynamic events during RNA folding, however are either designed for only
predicting annealing dynamics or limited to RNA segments with length up
to hundred bases. To quantitatively predict folding dynamics coupled
with transcription, we developed a genetic algorithm and chemical Master
equation based approach, which is capable of capturing kilobase level
kinetics. Our method is built on two following assumptions:

#### 1

All populated RNA secondary structures (SS) are linkage of locally
optimal or sub-optimal structures at various folding sites;

#### 2

Global structural rearrangement of a partial RNA segment is permitted
only if it’s folding to the optimal SS on that segment.\

Formally, we denote a domain $D_{A,\,B}$ as a segment between base $A$
and $B$ that all contacts on that segment are local. For simplicity, we
denote **foldon** as domains with optimal secondary structures:
$D^{foldon}_{A,\,B} = \text{MFE(sequence[A,B])}$. Note that $'.'$ is a
trival example of foldon. Our assumption 1 can be rewritten as

$$D_{A,\,B} = D^{foldon}_{A, i_1} \oplus D^{foldon}_{i_1, i_2} \oplus ... \oplus D^{foldon}_{i_n, B}$$

Where $\oplus$ represents a link operation. Note that all structural
information of $D_{A,\,B}$ is encoded by the sequential representation
$[A,\, i_1,\, ...,\, i_n,\, B]$; as a foldon is also a linkage of
smaller foldons, there could be multiple way to represent $D_{A,\,B}$.
Here we introduce **Irreducible Foldon Representation** (IFR) to be the
sequential representations for which linkage of every adjacent foldons
is not another foldon:
$\forall k,\, D^{foldon}_{i_k, i_{k+1}} \oplus D^{foldon}_{i_{k+1}, i_{k+2}} \neq D^{foldon}_{i_{k}, i_{k+2}}$.
Then the sufficient and necessary condition for structural rearrangement
is

$\langle D^{u}_{A,\,B} | \hat{\mathbf{T}} | D^{v}_{A,\,B} \rangle \neq 0$
if and only if $\exists\, i,\,j$ satisfies

$i,\,j \in D^{u}_{A,\,B}$.IFR, $i,\,j \in D^{v}_{A,\,B}$.IFR;

$D^{u}_{A,\,i} = D^{v}_{A,\,i},\, D^{u}_{j,\,B} = D^{v}_{j,\,B}$;

$D^{u}_{i,\,j} = D^{foldon}_{i,\,j}$ or
$D^{v}_{i,\,j} = D^{foldon}_{i,\,j}$.

Then
$\langle D^{u}_{A,\,B} | \hat{\mathbf{T}} | D^{v}_{A,\,B} \rangle = \langle D^{u}_{i,\,j} | \hat{\mathbf{T}} | D^{v}_{i,\,j} \rangle$.

Folding pathway identification & Rate calculation {#section:rate}
-------------------------------------------------

Given two domains between which rearrangement is allowed, the task is to
compute forward and backward rate constant linking each other. Multiple
methods to rigorously calculate the maximum likelihood during RNA
folding have been reported; here we proposed a computationally feasible
approach: the forward free energy barrier is estimated by sum up all
free energy associated with old stacks unzipping and new loop forming;
then rate constant
$k_{uv} = \langle D^{u}_{A,\,B} | \hat{\mathbf{T}} | D^{v}_{A,\,B} \rangle $
is calculated by Arrhenius approximation
$k_{uv} = k_0 \exp[-\frac{1}{RT}(\Delta G^{Stack}_{u}+\Delta G^{Loop}_{v})]$.
’New’ and ’old’ helices are identified by comparing elementary domains
(defined as domains that cannot be decomposed to smaller valid domains)
between reactant and product domains; identical elementary domains are
excluded.

Algorithm procedure
-------------------

During every iterative elongation step, an active species pool of
strands with unique SS and diffrent population is updated. New candidate
strands $D^{Candidate}_{0,\, L+\Delta L}$ with length $L+\Delta L$ are
generated by a recombination process: for every old strand
$D^{Strand}_{0, \text{ L}}$, all indices in its IFR is identified as
possible rearrangement site, then its child strands is generated by
linking partial domains $D^{Strand}_{0, \text{ Site}}$ with a foldon
$D^{foldon}_{\text{Site}, L+\Delta L}$ that terminated at $L+\Delta L$.

We assume that elongation will not change the inital population
distribution of secondary structures: child strands with the exact
parental SS on $[0, L]$
($D^{child}_{0, L+\Delta L} = D^{strand}_{0, L} \oplus D^{foldon}_{L, L+\Delta L}$)
will also inherit the population of their parents.

After structual generation the rate matrix among all candidate strands
within the new active species pool is calculated (see part
[section:rate]). Then the population distribution of strands after
elongation is computed by propagate the chemical master equation.

For the sake of computational efficiency, we introduce a cutoff $N $ as
the size limit of the active species pool. After each elongation step,
we impose a selection sweep on all active strands; species with top $N $
fitness is reserved. In the current edition, we simply used population
as the fitness function. Population of remaining strands within the
active pool is renormalized after selection.

Pseudocodes of the whole simulation procedure are as follows (Algorithm
[algorithm:1]):

[1] Initalize ActivePool $\text{OldPool} \gets \text{ActivePool }$
$\text{renew ActivePool }$
$\text{Current length} \gets \text{Current length} + dL$
$\text{dt} \gets dL / k_T$
$D^{foldon}_{\text{left boundary}, \text{ Current length}} \gets \text{numpy.mfe(sequence[left boundary, Current length]})$
$D^{Candidate}_{0,\text{Current length}} \gets D^{Strand}_{0, \text{ Site}} \oplus D^{foldon}_{\text{Site}, \text{ Current length}}$
$\text{update $D^Candidate^~0,~$.IFR}$
$\text{add $D^Candidate^~0,~$ to ActivePool}$
$\langle \text{ActivePool}.\textbf{population}\,|D^{Candidate}_{0,\text{Current length}}\rangle \gets \langle \text{OldPool}.\textbf{population}\,|D^{Strand}_{0, \text{ Site}}\rangle$
$\text{calculate  } D^{u}_{\text{rearrange}} ,\ D^{v}_{\text{rearrange}}$
$\langle D^{u}_{\text{rearrange}} | \hat{\mathbf{T}} |D^{v}_{\text{rearrange}} \rangle \gets k_0 \exp(-\frac{1}{RT}(\Delta G^{Stack}_{u}+\Delta G^{Loop}_{v}) )$
$\langle \text{ActivePool}.\textbf{population}\,|\, \gets \langle \text{ActivePool}.\textbf{population}\,|\, \exp(t\times\hat{\mathbf{T}}) $
$\text{reserve top $N$ populated strands in ActivePool}$
$\text{renormalize }\langle \text{ActivePool}.\textbf{population}\,|$

[algorithm:1]

Results
-------

The only remaining free parameter to be determined is $k_0/k_T$, the
ratio of pre-exponential factor in Arrhenius rate formulation and
trancription rate ($nt\cdot s^{-1}$). I tuned $k_0/k_T$ from $10^{1}$ to
$10^{15}$ and obtained the data for $k_0/k_T=\infty$ by calculate
stationary distribution ($\frac{1}{Q}\exp(-G_i)$) after every elongation
step for strand i in active pool.

#### Population analysis

For folA-WT four predominant local folding motifs within SD sequence are
identified. Figure [fig:local~f~oldings] shows exemplary secondary
structures containing these motifs; figure [fig:populations] shows
evolution of these structure motifs during co-transcriptional folding
with different $k_0/k_T$. Identical motifs are marked by the same color
as in figure [fig:local~f~oldings]. Surprisingly we noticed that when
$k_0/k_T=\infty$, exchange between dominant motifs is very frequent at
early stage of transcription, indicating the sensitivity of local
structures on long-range contacts, and dependence of motif predominance
on the limited timescale for folding.
