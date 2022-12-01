
# fancy-fencing
__Let the fight begin__

## Description
<p>
Welcome to the Facny Fencing Game. It aims to create a fencing game using python. This project initally was given in my Advanced Programming course. It was told we can add it to github and share it publicly. But from my side I choose to make it possible for other people willing to contribute to open source project to particiapte, learn and share thoughts and code, in order to improve it. The project subject can be found here. 
</p>

## Technologies
<p>
This program uses a variety of advanced coding concpets
* Object Oriented Programming
* Multithreading
* Sound
* Network Communication
* Keyboard Listener
</p>

<p>
Library used in this projects are:
    <table>
        <thead>
            <tr>
                <td>
                    Name
                </td>
                <td>
                    Objective
                </td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    os
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    json
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    threading
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    socket
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    pynput
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    time
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    re
                </td>
                <td>
                    Objective
                </td>
            </tr>
            <tr>
                <td>
                    pigar
                </td>
                <td>
                    Objective
                </td>
            </tr>
        </tbody>
    </table>
</p>

## Installation

### Requirements

*Please use Python3.10 to run this project to avoid compatibility issues. 
Highly recommended not to use on Macbook because of an issue existing with pynput module.
To use on Mac you will need to allow your terminal to have accessibility access.*

### Package Install

    pip3 install requirements.txt

### Running the program

    python3.10 ./main.py

## Usage
The game can be played in two mode. Either the two players are on the same machine, or they are on different machines connected on same network. When starting the program, users are presented with a scren showing the IP of the actual users and the other Menu.

> Menu image when the game is first launched
![Menu Image][menu-image]

> Game mode selection
![Game Selection][game-selection]

> Continue a saved game
![Saved Game][saved-game]

> Users actually playing
![Game Playing][game-playing]
    
### Command to play
<p>
Player 1:</br></br>

q => Move Left,</br>
d => Move Right,</br>
a => Jump Left,</br>
e => Jump Right,</br>
z => Attack,</br>
s => Block</br></br>

Player 2:</br></br>

Left Arrow => Move Left,</br>
Right Arrow => Move Right,</br>
l => Jump Left,</br>
m => Jump Right,</br>
o => Attack,</br>
p => Block</br>
</p>

## How to contribute?   
1. Fork the project
2. Make a pull request
3. Wait for it to get merged
4. And be happy to contribute there :-)

**Feel free to open Issues whenever possible. This is the very basic version, and we are looking forward to make it run as smooth as possible on every platform.**


[menu-image]: https://github.com/tiserge2/fancy-fency/blob/main/sc_game/menu.png?raw=true
[saved-game]: https://github.com/tiserge2/fancy-fency/blob/main/sc_game/saved_game.png?raw=true
[game-selection]: https://github.com/tiserge2/fancy-fency/blob/main/sc_game/game_selection.png?raw=true
[game-playing]: https://github.com/tiserge2/fancy-fency/blob/main/sc_game/game_playing.png?raw=true