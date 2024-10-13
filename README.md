
## Env Set-up

run command `.\venv\Scripts\activate` to setup venv. Run `uv sync` to sync dependencies.

## Getting input Data


## Running the commands

```invoke alias```
Generates a list of player aliases which are possibly the same player.
It uses a combination of string similarity as well was stats closeness. 

```invoke cluster```
Main function(s) for generating player clusters. Stores the clusters info in csv files.

```invoke color-function```
Runs a decision tree classifier on the player clusters and converts that into a function string
to be used by PT4 for coloring a player report. 

## Clusters

| Cluster | Cluster Name   | PFR/VPIP | VPIP | PFR | Limp | CC 2Bet PF | Total AFq | 3Bet PF | 4Bet PF | 2Bet PF & Fold | Avg PF All-In Equity | CBet F | Fold to F CBet | XR Flop | Fold to Steal | Att To Steal | Call R Eff | WWSF | BB Won/100 |
| --- |----------------| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Orca           | 67.08 | 24.84 | 16.46 | 2.26 | 10.97 | 47.12 | 9.53 | 6.57 | 38.04 | 45.39 | 64.24 | 46.18 | 6.76 | 64.66 | 37.1 | 1.69 | 42.99 | 13.16 |
| 3 | Shark          | 66.43 | 32.28 | 21.26 | 2.97 | 13.33 | 52.14 | 12.94 | 7.7 | 31.97 | 43.85 | 67.83 | 38.26 | 13.17 | 48.24 | 45.94 | 1.31 | 47.08 | 6.6 |
| 4 | Jellyfish      | 28.53 | 33.56 | 9.52 | 21.04 | 26.9 | 38.44 | 4.97 | 4.09 | 20.88 | 46.09 | 67.27 | 49.25 | 4.45 | 56.9 | 19.53 | 1.5 | 37.19 | 2.96 |
| 5 | Crab           | 51.94 | 35.68 | 18.33 | 6.59 | 23.62 | 40.8 | 9.08 | 5.43 | 21.56 | 46.2 | 59.89 | 43.85 | 5.54 | 45.55 | 40.23 | 1.41 | 39.31 | 0.3 |
| 2 | Sardine        | 28.56 | 52.33 | 15.1 | 36.14 | 40.59 | 43.18 | 7.8 | 4.25 | 23.69 | 43.04 | 56.21 | 44.75 | 4.84 | 37.21 | 26.91 | 1.18 | 40.73 | -17.18 |
| 0 | Mantish Shrimp | 61.64 | 45.51 | 27.94 | 4.18 | 24.61 | 47.22 | 16.45 | 8.93 | 19.75 | 45.46 | 64.34 | 40.1 | 7.7 | 34.83 | 55.6 | 1.48 | 43.58 | -39.92 |


### Dolphin (Cluster 1)

#### Summary 

#### Exploits


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

#### Exploits


### Mantis Shrimp (Cluster 0)

#### Summary 

#### Exploits

## Using the clusters

