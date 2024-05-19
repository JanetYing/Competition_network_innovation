# Competition, Networks, and Innovation - Proposal

## Research Question
Given the previous study by [Aghion et al., 2005](https://doi.org/10.1093/qje/120.2.701) shows the inverted U-shaped relationship between competition and innovation, when the innovation gap between leader firms (with high technology advancement) and follower firms (with low tech advancement) is large enough, the firms in the market are less likely to innovate. For leader firms, (explain the logic for leader and follower firms based on the paper). However, technology spillover could alter this pattern to some extent (explain based on the paper). This research uses Agent-based modeling to simulate how competitiveness and network effect/technology spillover could change firms' innovation decisions.

## Terminology Explanation
- **Technology Advancement Ranking (TAR)**: Firm i's ranking in market technology advancement (represented as percentile).
- **Two types of agents**:
  - **Leader Firm**: Firms with a TAR higher than the market average (higher than 50th percentile).
  - **Follower Firm**: Firms with a technological lag, trying to catch up with the leader in innovation (TAR lower than or equal to 50th percentile).
- **Network Effect (NE) & Grid**: The grid of Agent-based modeling visualization represents the existence of networks between firms; Firm i would benefit from the R&D of Firm j if the connection between them exists and Firm j has a higher TAR than Firm i.
- **Innovation Gap**: According to the paper by [Aghion et al., 2005](https://doi.org/10.1093/qje/120.2.701), leader firms would stop innovating if the gap between follower firm i and leader firms' innovations average exceeds the predetermined number. The follower firm would stop innovating (explain this based on the paper).
- **Baseline Success Probability ($P_{pre}$)**: A baseline success probability is set for all firms. The success probability ($P_{s}$) would be adjusted by the network effect in each step based on the baseline success probability.
- **Innovation cost**: To simulate real-world business operations and decision-making, innovation cost is added as a kind of risk. Since financial considerations like profit and cost are not central to this study and to better focus on the research of interest, cost is incorporated as an element of success probability. When innovation fails, firms would have fewer financial resources to invest in the next step's innovation, thus decreasing the success probability for the next step.

## Initialization/Parameter Set-Up
- **Innovation Gap**: Adjustable by slider, ranging from 1 to 100 with intervals of 20. The larger the gap set, the higher tolerance for firms on TAR.
- **TAR distribution**: Three types of initial TAR distributions could be chosen: left-skewed (more firms centered on low TA), normal distribution, and right-skewed distribution. This allows observation of how different initial distribution conditions influence later innovation decision changes in the market. For example, if a left-skewed distribution is chosen initially, firms are less likely to benefit from the network effect since most firms around them have the same or lower level of technology advancement.

## Interactions in Each Step
The simulation details for each step are illustrated in the flowchart below. The innovation success probability ($P_{s}$) is calculated based on the baseline probability ($P_{pre}$) and network effect. Here is the equation:

\[ P_{is} = P_{i\text{pre}} \left( \left( \sum_{j=1}^n \mathbf{1}(N_{i,j} = 1) \cdot \mathbf{1}(TAR_j > TAR_i) \cdot (TAR_j - TAR_i) \right) \times NE + 1 \right) \]

(explain this equation, combine with the flowchart, explain the details in the simulation step)

![Flowchart describing the decision process](./Graphics/flowchart.jpg)

## Data Collection
Given that the model is unlikely to achieve a definitive steady state, it will incorporate a stop function that will terminate the simulation after a specified number of steps. The initial conditions, as well as the innovation rates for both types of firms—leaders and followers—and the cumulative market innovation rate, will be recorded at each step.

## Analysis
Regression analysis will be conducted to understand the correlation between innovation rates and network structures.

## References
- Aghion, P., Bloom, N., Blundell, R., Griffith, R., & Howitt, P. (2005). Competition and Innovation: An Inverted-U Relationship. Quarterly Journal of Economics, 120(2), 701-728.
