This repo is a proof of concept for automatically adjusting the difficulty of a video game. This is to get rid of the concept of setting difficulty of a game: easy, medium, hard, pros_only and instead adjust the difficulty of a game so that a player is always challenged without being too frustrated.

We had plans to test this out on pacman but ended up creating our own implementation of breakout to do this.

The way this works is that after every game, the skill of a player is assessed and the player is given an easier level if they're OK or an insanely difficult level if they're 360 no scopers. 

## Game Engine
* Given a state (brick locations and score etc..) and an action (move paddle left or right) give the new state
* Some state variables control the difficulty of a game, in the case of pong we used two things - the speed of the ball and the likelihood of powerups being generated

## How to generate a continuous space of difficulty settings
* We train a Reinforcement Learning Agent (using a Neural Policy gradient algorithm) for 1, 1,000, 10,000, 1,000,0000 steps etc. on an extremely difficult version of Pong 
* For each trained agent we start with the most difficult level and see if they pass, if not we make the level easier. The difficulty benchmark is the first level where the agent fails. 

## How we change up the difficulty to human players
* After every game run we monitor some metrics for how well a player did (e.g: how long the game lasted, the score etc..) and then essentially use a binary search like algorithm with randomization to most efficiently reach the appropriate level of difficulty
