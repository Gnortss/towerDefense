# Tower Defense

Really basic tower defense in python using PyGame


## Initial setup for Pycharm

- Create new project in Pycharm named *towerDefense*
- Add git repository *git@github.com:Gnortss/towerDefense.git*
- Make sure your project interpreter is *Python 3.7+ in virtualenv*
- Open terminal and go into towerDefense virtualenv and install requirements:
    ```
    pip install -r requirements.txt
    ```

## Game

It starts at level selection. It can only display 8 levels. You can click on a level and it will start.
Level will automatically end when you either finish all waves or run out of lives.

#### Controls
 - **1** - Basic tower
 - **2** - Basic trap
 - **P** - toggle pause/unpause
 - **ESC** - Quit the game
 
#### Custom levels
You can create your level by copying *levels/level01.json* and customizing it to your liking.
Number of waves or enemies is not limited.