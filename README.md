# Hungry Birby-chan

`Hungry Birby-chan` is a Flappy Bird style arcade game built with `Python` and `Pygame`. Guide Birby-chan through pipes, collect apples to raise your score, and survive as the game speeds up.

## Features

- Flappy Bird inspired gameplay with a pixel-art presentation
- Animated bird, rainbow trail, and sparkle boost effects
- Multiple background themes: `noon`, `sunset`, `night`, and `sunrise`
- Settings menu for theme selection, volume, difficulty scaling, and dynamic obstacles
- Pause menu and retry flow
- Special flipped mode triggered by yellow apples

## Project Structure

```text
flappy_bird/
|- main.py
|- config.py
|- requirements.txt
|- assets/
|- src/
```

## Requirements

- `Python 3.10+`
- `pip`
- `pygame`

## Installation

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Install dependencies:

```bash
pip install pygame
```

If you prefer, you can also save that dependency into `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

## How To Boot Up The Game

From the project root, run:

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

## Controls

- `Space` or `Up Arrow`: flap / boost upward
- `Esc`: pause the game during a run
- `Enter` or `Esc` in pause menu: continue the game
- `R`: retry after game over
- `Esc` on game over screen: return to menu
- `Mouse`: interact with menu buttons, toggles, and volume slider

## Tutorial

### Starting the game

1. Launch the game with `python main.py`.
2. On the main menu, click `Play Game`.
3. Use `Space` or `Up Arrow` to keep Birby-chan in the air.

### Basic gameplay

- Fly through the gaps between pipes.
- Avoid touching pipes, the ceiling, or the ground.
- Collect apples to increase your score.
- The game ends if you collide with an obstacle or fly out of bounds.

### Pause and retry

- Press `Esc` during gameplay to open the pause menu.
- Choose `Continue` to resume or `Back to Menu` to leave the run.
- After losing, press `R` to retry instantly.

### Settings

From the `Settings` screen, you can adjust:

- `Difficulty Scaling`: when enabled, the scroll speed ramps up over time
- `Theme`: cycle between different background themes
- `Dynamic Obstacles`: enables vertically moving pipes
- `Volume`: change music volume or mute sound

### Special flipped mode

- A yellow apple appears after you reach certain score milestones.
- Collecting it flips gravity and changes the feel of the run.
- Collect the next yellow apple to return to normal gravity.

## Assets Used

### Fonts

- Press Start 2P: https://fonts.google.com/specimen/Press+Start+2P
- VT323: https://fonts.google.com/specimen/VT323?preview.script=Latn&query=vt3

### Backgrounds

- Sky with clouds background: https://craftpix.net/freebies/free-sky-with-clouds-background-pixel-art-set/?num=1&count=186&sq=parallax%20backgrounds%20cloud&pos=11
- Moon pixel background: https://craftpix.net/freebies/free-moon-pixel-game-backgrounds/?num=1&count=182&sq=parallax%20backgrounds%20moon&pos=2

### Character

- Fat Bird sprite: https://orizho.itch.io/fat-bird-character

## Notes

- Make sure all files inside `assets/` stay in their expected folders, otherwise the game may fail to load images, audio, or fonts.
- The project currently uses `pygame` directly and launches from `main.py`.
