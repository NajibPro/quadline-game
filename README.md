## QuadLine Game Against AI:

This is a game inspired from the famous connect4 game (actually i was willing to implement it instead but i didn't read the rules of it well so I ended up creating a whole new game hehe :) ). You play against an AI created using the MinMax algorithm, lets see if you can beat it.

## To run it locally:

First, download the nessacery packages:

```bash
pip install -r requirements.txt
```

Then, run it using this command:

```bash
python3 play.py
```


## How to play:

- You are playing against an AI, your turn starts first.
- Hover over an empty cell you desire and click on it to fill it with your symbol (the cross symbol).
- Now it's the AI's turn, he will also fill one empty cell with his symbol (the cyrcle symbol).
- The process is repeated.
- The game ends when the whole board is filled and there is no empty cell left.
- The winner is the player that has the most sequences of 4 of his symbol aligned consecutively either horizontally, vertically, or diagonally.
- When you want to start a new game, even if the current one didn't end yet, click on the "r" letter in your keyboard.

## Game Recording:

[Screencast from 30 جوان, 2024 CET 05:38:53 م.webm](https://github.com/NajibPro/connect4-game/assets/96317571/47204dc5-ea96-41ef-a9e8-16d9194a3f81)


## Remarks

- This game is still under development, in order to make the AI player faster at choosing its next move and also smarter.
- This desktop app is developed using pygame.
