## Description

## Env Set-up
run command `.\venv\Scripts\activate` to setup venv. Run `uv sync` to sync dependencies.

## Getting input Data

First you will need poker logs in Poker Track 4.
This program works best is you have a decent number of hands on a small pool of players.
If you play on pokernow you can use a converter software like [PokerNowLogConverter](https://github.com/charlestudor/PokerNowLogConverter)
which will convert the logs to pokerstars format. Once you have some logs you will need to set up a players report.
I have included the player report that I use under `./etc/pn_player_report.pt4rp`. You can download this and import it to PT4.

## Generating Clusters

Once you have collected sufficient logs, if you want to generate your own clusters you must first export your report data and
point to it's path in `./etc/config.toml`. Then you can run the following commands:

```invoke cluster```
Main function(s) for generating player clusters. Stores the clusters info in csv files.

```invoke color-function```
Runs a decision tree classifier on the player clusters and converts that into a function string
to be used by PT4 for coloring a player report. 

You can play around with the min and max number of clusters and inspect the output files generated until you are happy with the clusters.
Then by running the color-function command you generate a decision tree classification function which colors each cluster with a given rgb code.
this function string can then be used by PT4 to color each row of your report, allowing you to see each cluster.

## Using Clusters

Once you have the coloring function you can go back to your PT4 report and click on Advanced and then add the color function string to the Row Color Expression field. 

Note: You can simply use the report and the clusters function I have provided under `./data/color_function`. In this case there are 6 clusters which are described below. 

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

#### Exploits


### Jellyfish (Cluster 4)

#### Summary 

#### Exploits


### Crab (Cluster 5)

#### Summary 

#### Exploits


### Sardines (Cluster 2)

#### Summary 
Sardines are the epitome of fish. They play a loose passive style with a VPIP of 52, PFR of only 15, and a staggering limp of 36.
They cold call pre-flop a lot, 


#### Exploits


### Mantis Shrimp (Cluster 0)

#### Summary 
The Mantish Shrimp are classic LAG players. They have the highest PFR of 27.94 on average and a very high VPIP of 45.51 (only behind the Sardines). 
They also are characterized by having the highest attempt to steal (55.6) and lowest fold to steal (34.38).

#### Exploits
- 3 bet light to exploit their high PFR
- Apply pressure to their blinds given they are less likely to fold. Raise their attempts to steal give how aggressive they are. 
- float and XR to take advantage of their post-flop aggression
- be more trappy


