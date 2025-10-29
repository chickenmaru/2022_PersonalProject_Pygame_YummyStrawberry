# Video Demo

# Game Display


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
