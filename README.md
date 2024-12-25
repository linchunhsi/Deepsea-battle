#  "Deepsea Battle": A Python Fighting game

![contribution](https://img.shields.io/badge/contributions-welcome-blue)
![python](https://img.shields.io/badge/Python-3.9_or_later-green)
![pillow](https://img.shields.io/badge/Pillow-9.0_or_later-green)

Welcome to Ocean fight, an interesting and exciting game for fun and relax This README provides a comprehensive overview of the project, including its features, usage, architecture, development process, references, and enhancements. 

## (1) 程式的功能 Features

Deepsea battle provides the following functionalities:

- **Earn points**:defeat enemies and earn points
- **Changing game stage**:game stage changes
- **Increasing difficulty**:as the game stage moves on , the difficulty increases
- **Replay the game**:restart the game by pressing "R" when the game ends 
- **Control character**:hold wasd keys to move the character
- **Control weapon**:drag and release the mouse to decide power and direction of weapon
- **Dynamic background**:the background changes over time
- **Health bar**:visible health bar 

## (2) 使用方式 Usage

Follow these steps to play Deepsea Battle:

To play Deepsea Battle, follow these steps:
1.download all the files and put them in a folder
2.open vscode 
3.open the folder you create and make sure everything in the folder is downloaded
4.install pygame
```bash
pip install pygame
```
5.run game.py

## (3) 遊玩方式 How to play
1.move the character by pressing w,a,s,d 
2.drag your mouse to decide the direction and power ,release your mouse to shoot your weapon
3.hit the enemy to get point
4.game stage changes according to score
5.your heath decreases when you are hit by enemy
6.eat food to heal
7.game over when player health is zero or score is over 5000
8.press 'R' to play again if you want ,press 'ESC' to leave the game

## (4) 程式的架構 Program Architecture

The project is organized as follows:

```
DeepSeaBattle/
├── game/
│   ├── __init__.py                 # Initialize the game package
│   ├── main.py                     # Main game logic and entry point
│   ├── player_shoot.py                   # Player-related functionality
│   ├── enemy_shoot.py
│   ├── enemy_spawn.py                  # Enemy logic and spawning
│   ├── player_bullet.py
│   ├── enemy_bullet.py              # Projectile (spear) handling
│   ├── background.py               # Dynamic background functionality
│   ├── hud.py                      # Heads-up display (HUD) and health bar
│   ├── settings.py                 # Constants and configuration
├── assets/                        # Images for characters, background, etc.
│   ├── images/                     
└── README.md                       # Documentation about the game

```

- **Core Components**:
  - `update_bullet.py`: show the motion of player's bullet and check collision with enemy.
  - `update_enemy_bullet.py`: show the motion of enemies' bullets and check collision with player.

## (4) 開發過程 Development Process

The development Deepsea Battle followed these steps:

1. **Ideation and Planning**: Decided to create a game.Ask ChatGpt for topic and make it interesting
2. **Implementation**: Ask ChatGpt for program structure .Complete the fundamental functions.
3. **Testing**: Run the game.Sometimes the game crashes or doesn't work as expected
4. **Fixing the code**:Look for error.If error not found , ask Chatgpt
4. **Enhancements**: Add additional feature

## (5) 參考資料來源 References

1. A game : the archer 2
2. ChatGPT - Assisted with documentation and architectural structuring of the project.

## (6) 程式修改或增強的內容 Contributions and Enhancement

The following modifications and enhancements were added to the project:
### Enhancements:
1. Make the motion projectile motion
2. Make the background dynamic 
3. Load image of player,enemy,bullets
4. Enhance difficulty

### Unique Contributions:
1. Add start screen and end screen.
2. Add game stage 
3. Add food for healing
4. Add health bar on characters
5. Add water resistance on player bullet

### further modifications:
1. More objects:
2. Add water resistance on enemy bullet
3. Add item that has special effect
4. Record highest score
5. Able to play with people other than computer
6. Allow enemy bullet to exsist after enemy is gone
We encourage further modifications and look forward to community contributions to improve PyMemeMaker further.

