# Competition, Networks, and Innovation

**Author**: Janet Cao  
**Date**: \today  

## Research Question

Given the findings by Aghion et al. (2005) that illustrate an inverted-U shaped relationship between competition and innovation, this research aims to simulate how competitiveness and network effects can influence firms' innovation decisions using agent-based modeling. Specifically, the study examines how market innovation competitiveness, innovation gap between leader firms (with high technological advancement) and follower firms (with lower technological advancement), and technological spillover impacts their likelihood to innovate.

## Background

Previous studies indicate that moderate competition can spur innovation, but excessive competition or a significant lead by the market leader can stifle the incentive to innovate. Leader firms may cease to innovate when the benefits of maintaining a lead diminish, while follower firms may find it unfeasible to catch up if the gap is too large. This study uses agent-based modeling to explore these dynamics, incorporating the influence of network effects on firms' innovation success probability.

## Terminology Explanation

- **Technology Advancement Ranking (TAR)**: Firm \(i\)’s ranking in market technology advancement, represented as a percentile.
- **Leader Firm**: Firms with a TAR higher than the market average (higher than the 50th percentile).
- **Follower Firm**: Firms with a technological lag, trying to catch up with the leader in innovation (TAR lower than or equal to the 50th percentile).
- **Network Effect (NE) & Grid**: The grid of the agent-based modeling visualization represents the existence of networks between firms. Firm \(i\) benefits from the R&D of firm \(j\) if a connection exists and firm \(j\) has a higher TAR.
- **Innovation Gap**: According to Aghion et al. (2005), leader firms may stop innovating if the gap between follower firm \(i\) and leader firms' innovations exceeds a predetermined threshold.
- **Baseline Success Probability (\(P_{\text{pre}}\))**: A baseline success probability set for all firms, the Success Probability **P_s** would be adjusted by network effect in each step based on baseline success probability.
- **Innovation Cost**: To simulate real-world business operations and decision-making, innovation costs are incorporated into success probability as a risk factor. If innovation fails, the firm has fewer financial resources for future innovation, reducing the success probability for subsequent attempts.

## Initialization/Parameter Set-Up

- **Innovation Gap**: Adjustable by slider, ranging from 1 to 100 with an interval of 20. The innovation gap sets a threshold for the technological advancement difference (\(|TAR_{\text{bar}} - TAR_i|\)) between firms. If the difference exceeds the gap, firms will stop innovating. Thus, a larger gap allows for greater tolerance in technological differences before firms cease their innovation efforts.
- **TAR Distribution**: Three initial TAR distributions can be chosen: left-skewed (more firms with low TA), normal, and right-skewed. Different initial distributions influence subsequent innovation decisions. For example, a left-skewed distribution means firms are less likely to benefit from network effects, as most neighboring firms have similar or lower TA levels.
- **Network Effect (NE)**: Adjustable by a slider, ranging from 0 to 1 with an interval of 0.1. The higher the network effect, the greater the ability of firms to benefit from the R&D of their network connections. This parameter is the study's focus and is simulated in finer detail.

## Simulation Explanation
[add flowchart here]
The simulation details for each step are illustrated in the flowchart.

- **Setup in the first step of simulation**: Firms are assigned initial TAR values randomly based on TAR distribution selected.
- **Decision to Innovate**: Based on their classification and the technological gap, firms decide whether to innovate.
- **Calculation of Innovation Success Probability**: The innovation success probability (\(P_s\)) is calculated based on the baseline probability (\(P_{\text{pre}}\)) and the network effect. The equation for \(P_s\) is:

    \(P_s = P_{\text{pre}} \left( \left( \sum_{j=1}^{n} \mathds{1}(N_{i,j} = 1) \cdot \mathds{1}(TAR_j > TAR_i) \cdot (TAR_j - TAR_i) \right) \times NE + 1 \right)\)

    For each firm \(i\), its innovation success probability (\(P_s\)) is determined by the baseline success probability (\(P_{\text{pre}}\)) multiplied by the network influence. Firm \(i\) benefits from firm \(j\) if there is a connection between them and \(j\) has a higher TAR. The network influence is calculated by summing the differences between these connected firms' TARs and firm \(i\)’s TAR, then multiplying by the network effect parameter (\(NE\)). Therefore, the wider the difference between firm \(i\) and its connected firms \(j\) and the higher the network effect parameter (\(NE\)), the higher the probability of success.

- **Outcome of innovation**: It is determined by comparing \(P_s\) with a randomly generated number. If innovation is successful, the firm's TAR increases by 1. If it fails, the TAR will remain unchanged and the \(P_s\) for the next step would decrease by 0.5%.
- **Recalculation of TAR**: The TAR of firms are updated based on the outcomes of innovation in preparation for the next step.

## Data Collection

Data will be collected on the following parameter sweeps: Innovation Gap, TAR Distribution, and Network Effect. The detailed sweeps are illustrated in Section \ref{parameter set_up}.

The model will be run about 50 iterations to capture enough variation. Data on innovation rates for both leader and follower firms, as well as the cumulative market innovation rate, will be recorded at each step.

## Analysis

Regression analysis will be conducted to understand the correlation between innovation rates and network structures. Additionally, plots will be generated to visualize the relationships and patterns observed in the simulation data. The analysis will focus on:
- The impact of innovation gaps on the likelihood of innovation success for leader and follower firms.
- How different TAR distributions influence innovation dynamics and market structure.
- The role of network effects in enhancing the success probability of innovation.

## Conclusion

This paper presents a detailed agent-based model of firm innovation dynamics, incorporating economic principles and empirical insights to explain the behavior of leader and follower firms. However, I am not yet certain about the exact simulation of innovation costs since, so far, I have included them in the probability of success as a fixed number. Perhaps a variable or random number would better fit real-life situations. Further refinement is needed to accurately simulate financial constraints and their impact on innovation decisions.

## References

Aghion, P., Bloom, N., Blundell, R., Griffith, R., & Howitt, P. (2005). Competition and Innovation: An Inverted-U Relationship. *Quarterly Journal of Economics*, 120(2), 701-728.
