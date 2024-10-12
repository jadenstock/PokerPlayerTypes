
### Env Set-up

run command `.\venv\Scripts\activate` to setup venv. Run `uv sync` to sync dependencies.

### Getting input Data


### Running the commands

```invoke alias```
Generates a list of player aliases which are possibly the same player.
It uses a combination of string similarity as well was stats closeness. 

```invoke cluster```
Main function(s) for generating player clusters. Stores the clusters info in csv files.

```invoke color-function```
Runs a decision tree classifier on the player clusters and converts that into a function string
to be used by PT4 for coloring a player report. 