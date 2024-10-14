## Background and Methodology
For the clusters below, I ran the clustering algorithm only on stats that could be available in a HUD. I did not include stats
like currency won, bb won, number of hands. I then sorted the clusters by win-rate. We can see that the result roughly aligns with expectations.
The two most profitable player clusters play a TAG style, followed by the loose-passive styles. One interesting note is that the LAG player cluster
is by far the biggest loser by win-rate. 

The goal of the clusters is mostly to know who to watch our for at the table and who to target. For individual exploits is will be better to look at each
individual's stats. 

For this analysis I have about 500 players and a little over 600k hands. Most players have an average of around 1k hands. I didn't include any players with less than 300 hands. 

## Clusters

Note: the cluster names given below were given by me. The analysis given is a combination of responses from ChatGPT, pokerGpt, and my intuition. 

| Cluster | Cluster Name   | PFR/VPIP | VPIP | PFR | Limp | CC 2Bet PF | Total AFq | 3Bet PF | 4Bet PF | 2Bet PF & Fold | Avg PF All-In Equity | CBet F | Fold to F CBet | XR Flop | Fold to Steal | Att To Steal | Call R Eff | WWSF | BB Won/100 |
| --- |----------------| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Orca           | 67.08 | 24.84 | 16.46 | 2.26 | 10.97 | 47.12 | 9.53 | 6.57 | 38.04 | 45.39 | 64.24 | 46.18 | 6.76 | 64.66 | 37.1 | 1.69 | 42.99 | 13.16 |
| 3 | Shark          | 66.43 | 32.28 | 21.26 | 2.97 | 13.33 | 52.14 | 12.94 | 7.7 | 31.97 | 43.85 | 67.83 | 38.26 | 13.17 | 48.24 | 45.94 | 1.31 | 47.08 | 6.6 |
| 4 | Jellyfish      | 28.53 | 33.56 | 9.52 | 21.04 | 26.9 | 38.44 | 4.97 | 4.09 | 20.88 | 46.09 | 67.27 | 49.25 | 4.45 | 56.9 | 19.53 | 1.5 | 37.19 | 2.96 |
| 5 | Crab           | 51.94 | 35.68 | 18.33 | 6.59 | 23.62 | 40.8 | 9.08 | 5.43 | 21.56 | 46.2 | 59.89 | 43.85 | 5.54 | 45.55 | 40.23 | 1.41 | 39.31 | 0.3 |
| 2 | Sardine        | 28.56 | 52.33 | 15.1 | 36.14 | 40.59 | 43.18 | 7.8 | 4.25 | 23.69 | 43.04 | 56.21 | 44.75 | 4.84 | 37.21 | 26.91 | 1.18 | 40.73 | -17.18 |
| 0 | Mantish Shrimp | 61.64 | 45.51 | 27.94 | 4.18 | 24.61 | 47.22 | 16.45 | 8.93 | 19.75 | 45.46 | 64.34 | 40.1 | 7.7 | 34.83 | 55.6 | 1.48 | 43.58 | -39.92 |


### Orca (Cluster 1)

#### Summary 
Orcas are classic TAG players. They play a tight range and they usually prefer aggressive actions to passive ones.
They have the highest PFR/VPIP (67.08), lowest limp (2.26), lowest CC 2B PF (10.97).
They also have highest River Call Efficiency (while not being too high), making them formidible opponents throughout the hand. 

When faced with aggression they tend to not like calling. Instead, they fold or bring more aggression back. 
This makes their 2Bet PF & Fold, Fold to F Cbet, and Fold to Steal stats quite high.

#### Exploits
- Apply pressure post-flop.
- 3 bet wider.

### Shark (Cluster 3)

#### Summary 
Sharks are generally strong players. They play slightly wider than Orcas (the highest earning cluster) but not as wide as the other aggressive cluster, the Mantis Shrimp.
Sharks have very similar PFR/VPIP to Orcas but 4 points higher on both PFR and VPIP. They have the highest AFq of all of the clusters.
They fold to 3bets preflop less than orcas (probably because they are more likely to call).
They have highest cbet flop and highest XR flop (by far), showing a lot of post-flop aggression. This leads to them having the highest WWSF stat.
Their main problem is being perhaps slightly too wide pre-flop. 

#### Exploits
- Take advantage of their post flop aggression. Call down more.
- They have the lowest fold to flop C-bet so check more on flops with speculative hands.

### Jellyfish (Cluster 4)

#### Summary 
Jellyfish are almost as fishy as the Sardines. They show very similar levels of aggression (or rather, passivity), but they play fewer hands in general. 

#### Exploits
- Same exploits as Sardines (below)

### Crab (Cluster 5)

#### Summary 
Crabs aren't bad players, but they aren't good players either. They aren't as aggressive and dialed in as the Orcas and Sharks but not as fishy as the Sardines and Jellyfish.
They 7% limp shows that they can lack discipline pre-flop. Their low WWSF also shows that they aren't battling post-flop enough either. 

#### Exploits
- punish their limps when they do limp.
- Apply lots of pressure post-flop to push them off of their hands. 

### Sardines (Cluster 2)

#### Summary 
Sardines are the epitome of fish. They play a loose passive style with a VPIP of 52, PFR of only 15, and a staggering limp of 36.
They cold call pre-flop a lot, they have the lowest average pre-flop all in-equity (suggesting they get in bad).
They also have the lowest flop c-bet and very low flop XR as well. In general, they are the most passive cluster.

#### Exploits

- Raise against limps
- Steal blinds aggressivly
- use delayed aggression with flop and turn bets

### Mantis Shrimp (Cluster 0)

#### Summary 
The Mantish Shrimp are classic LAG players. They have the highest PFR of 27.94 on average and a very high VPIP of 45.51 (only behind the Sardines). 
They also are characterized by having the highest attempt to steal (55.6) and lowest fold to steal (34.38).

#### Exploits
- 3 bet light to exploit their high PFR
- Apply pressure to their blinds given they are less likely to fold. Raise their attempts to steal give how aggressive they are. 
- float and XR to take advantage of their post-flop aggression
- be more trappy
