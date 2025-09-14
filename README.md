# Game of the Generals
A singleplayer Python recreation of [Game of the Generals](https://en.wikipedia.org/wiki/Game_of_the_Generals), a Filipino educational war game.

## How to play

### Summary
You are given 21 pieces representing different combantants in an army, including one representing a **flag**. The main objective of the game is essentially to eliminate your opponent's flag by manouvering your pieces across the board towards it.

### Setup and ranking

The game is played on a 9×8 board. The layout of your 21 pieces may be arranged however you like, as long as they are within the nearest 3 rows of the board. Alternatively, you have the option to randomise the positions of the pieces.

<img width="477" height="372" alt="image" src="https://github.com/user-attachments/assets/3d094ff2-cbd6-49a3-b043-5d3a949eb8d7" />

All 21 pieces are arranged into different ranks. The main idea is that any higher-ranking piece may eliminate a lower-ranking piece. If both pieces are of the same rank, both are eliminated. Note that there are a few exceptions to these rules. Below is a table listing all pieces arranged from lowest to highest rank, as well as some additional notes/exceptions.

|Piece              |Note                                            |
|:-----------------:|:----------------------------------------------:|
|Flag               |Eliminates **the opposing flag** if aggressor.  |
|Private            |Eliminates the **Spy**.                         |
|Sergeant           |—                                               |
|2nd Lieutenant     |—                                               |
|1st Lieutenant     |—                                               |
|Captain            |—                                               |
|Major              |—                                               |
|Lieutenant Colonel |—                                               |
|Colonel            |—                                               |
|Brigadier General  |—                                               |
|Major General      |—                                               |
|Lieutenant General |—                                               |
|General            |—                                               |
|General of the Army|—                                               |
|Spy                |Can eliminate anyone except for the **Private**.|

### Gameplay

You are allowed to move your own pieces in the following directions: up, down, left and right (assuming you are not blocked by another friendly piece or the move does not take you out of bounds). In the game you may do this with the in-game command `<POS> <OPERATION>`.

## IMPORTANT: `termcolor`!

This program uses the `termcolor` module to display coloured and formatted text, so please ensure it's installed before running.

```bash
# MacOS/Windows
$ python3 -m pip install --upgrade termcolor

# Linux
$ sudo apt update
$ sudo apt install termcolor
```

Alternatively, you may also follow the **source installation** directions on `termcolor`'s [GitHub repository](https://github.com/termcolor/termcolor) (if you're into that).

> *Para kay Trish, sinta ko*
