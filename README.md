# Bridg-It (Game of Gale)
Web implementation of GUI and AI for Brigd-It game with Python and SocketIO.
## Requirements
* `flask`
* `flask-socketio`
* `numpy`
* `eventlet`
## Run
Primarily, clone repository and go to application directory
```
git clone https://github.com/vvkin/knapsack-genetic/
cd bridg-it
```
Of course, you must have python installed on your computer.
Also you need a tool like pipenv.
To install it, just use pip
```
pip install pipenv
```
It's time to deal with requirements
```
pipenv install
pipenv shell
```
Finally, you are ready to run it
```
python game.py
```
After that just go to localhost:5000
## Rules
In that game you play against bot with different levels of difficulty. Rules are pretty simple — connect adjacent cells without intersection.
Your goal is to build connected line from one side to another. Of course, line direction depends on player color. Red player tries to build
horizontal line and can't connect cells on first and last rows, while blue player builds vertical line and can't connect cells on first and last
columns. The player who is the first to build such a line wins.
## Contributors
Vadym Kinchur, vvkin
