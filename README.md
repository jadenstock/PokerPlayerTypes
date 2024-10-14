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