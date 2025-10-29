# Video Demo

# Game Display

<img width="499" height="621" alt="image" src="https://github.com/user-attachments/assets/2e8369cb-eda3-440a-8026-18ef9af9d29f" />

Strawberries will appear from all directions during gameplay.

<img width="496" height="620" alt="image" src="https://github.com/user-attachments/assets/a5ae4d8d-bea1-46f7-9421-d4724e2d5843" />

Items will drop during gameplay.


<img width="497" height="619" alt="image" src="https://github.com/user-attachments/assets/7204a25b-d8da-4ac1-9cef-7d7119f8a903" />

Collecting items triggers additional effects, such as changing the bullets to a double shot.



# Overview
This is a 2D vertical scrolling shooter game developed using Python and Pygame, themed "Strawberries are Delicious." Players control a cat (spaceship) moving across the screen, shooting falling strawberries while avoiding collisions to protect their health points.

# Game Mechanics
| Feature | Description |
| :--- | :--- |
| **Player Controls** | - Use WASD to move the cat<br>- Spacebar to shoot bullets |
| **Enemies** | Strawberries (enemies) randomly spawn from the top of the screen, rotate, and drift left/right while falling |
| **Bullet System** | - Normal single-shot (consumes ammo)<br>- Can obtain double-shot power-up (lasts 5 seconds) |
| **Health Bar (Red)** | - Lose health when hit by strawberries<br>- Game over when health reaches zero |
| **Ammo Bar (Green)** | - Each bullet consumes 10 points<br>- Slowly regenerates over time |
| **Power-up System** | Chance to drop when shooting down strawberries:<br>• **Meat**: Activates double-shot firing<br>• **Save**: Restores 15 health points |
| **Scoring System** | - Score points for shooting down strawberries (calculated based on strawberry size) |
| **Increasing Difficulty** | - Current code has logic to increase strawberry count and speed when score >= 500 / 2000<br>- Not working due to variable scope issues |


