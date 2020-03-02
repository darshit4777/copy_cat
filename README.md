# copy_cat

## Introduction
copy_cat is a pygame based ball-on-plate simulator. The user can use arrow keys to tilt the plate left or right or center it, in an effort to balance a rolling ping pong ball on a plate.</br>
</br>
The copy cat simulator was built for testing various control algorithms to solve a well known and interesting controls problem. Additionally its application can be extended to build Machine Learning models to control the plate.

## Installation
It is recommended that you create a virtual environment first. To do so, use `python3 -m venv <name of virtualenv>`
This will create a virtual environment. After that activate the virtual environment and clone this repository. 
To download the dependencies from the requirements.txt, just use `pip install -r requirements.txt`

## Usage
### Launching
Start the game using `python3 main.py` </br>

### Controls
Use the arrow keys to tilt the plate. As the plate tilts the ball will start rolling down the incline. Be careful! The ball speeds up quite fast!. </br> 

### Scoring
The aim is to center the ball on the plate and hold it for 2 seconds. If you do so, the game restarts with a randomised ball location and you gain a point. The game will restart if the ball falls off and you lose a point.
</br>

### Data collection for training algorithms
Press the `s` key to enter into the data collection mode aka 'SharinGan' mode. This will start tracking all your moves to CSV file. This gets stored in the `train_data` directory.</br>

### Machine Learning
Press the `m` key to analyse all your moves and let machine learning do the controlling. When a new game session is started, the program checks for any collected data. If any data is found it trains a Multi-Linear Regression model on the given data. On pressing the `m` key, the machine learning trained controller starts playing with the ball. The model will behave on the basis of the inputs given to it. In that it will try to emulate the user's playing style.</br>

### Automatic Conrol
The program now has built-in control modules for PID control and Binary (Bang-Bang Control). To activate PID control just press 'p' and to activate Binary control just press 'b'. To switch back to user control just press 'u'

## Enjoy !
