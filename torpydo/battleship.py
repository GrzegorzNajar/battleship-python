import random
import os
import colorama
import platform

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
from torpydo.telemetryclient import TelemetryClient

import sys

print("Starting")

myFleet = []
enemyFleet = []

def main():
    # TelemetryClient.init()
    # TelemetryClient.trackEvent('ApplicationStarted', {'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()

    start_game()

def start_game():
    global myFleet, enemyFleet
    # clear the screen
    if(platform.system().lower()=="windows"):
        cmd='cls'
    else:
        cmd='clear'   
    os.system(cmd)
    print(r'''
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
   |      _  /
   |     /_\
    \    \_/
     """"""""''')

    while True:
        print()
        print("=====================================")
        print()
        print("Player, it's your turn, \nYour ships: " + str(myFleet) + "\nEnemy ships number: " + str(len(enemyFleet)) )
        if (len(myFleet) == 0):
            print("You Lost Game")
            exit(0)

        if (len(enemyFleet) == 0):
            print("You Won Game")
            exit(0)

        print("Please position your hit (Game board has size from A to H and 1 to 8)")

        position = parse_position(input(Fore.GREEN + "Enter coordinates for your shot :"))
        print(Fore.BLACK)
        is_hit = GameController.check_is_hit(enemyFleet, position)
        if is_hit:
            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''')
            print(Fore.BLACK)

        print(Fore.RED + str(position) + " Yeah ! Nice hit !" if is_hit else Fore.BLUE + str(position) +  " Miss")
        print(Fore.BLACK)
        TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

        print()
        print("-------------------------------------")
        print()

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print()
        if is_hit:
            rest = Fore.RED + "hit" + Fore.BLACK + " your ship"
        else:
            rest = Fore.BLUE + 'Miss'
        print(f"Computer shoot in {str(position)} and " + rest)

        print(Fore.BLACK)
        TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})
        if is_hit:
            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''')
            print(Fore.BLACK)

def parse_position(inp: str):
    while not((len(inp) == 2) and (ord(inp.upper()[:1]) in range(ord('A'), ord('H') + 1)) and (inp[1:].isnumeric())):
        print(Fore.RED + 'Wrong input')
        inp = input(Fore.BLACK + "try again:")

    letter = Letter[inp.upper()[:1]]
    number = int(inp[1:])
    position = Position(letter, number)

    return Position(letter, number)

def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position

def initialize_game():
    initialize_myFleet()

    initialize_enemyFleet()

def initialize_myFleet():
    global myFleet

    myFleet = GameController.initialize_ships()

    print("Please position your fleet (Game board has size from A to H and 1 to 8) :")
    j=0

    for ship in myFleet:
        print()
        print(f"Please enter the positions for the {ship.name} (size: {ship.size})")
        j+=1

        if len(sys.argv) > 1 and sys.argv[1] == '-demo':
            for i in range(ship.size):
                position_input = Position(Letter(j),i+1)
                ship.positions.append(position_input)
                TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})
        else:
            for i in range(ship.size):
                position_input = parse_position(input(Fore.GREEN + f"Enter position {i+1} of {ship.size} (i.e A3):"))
                ship.positions.append(position_input)
                TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})
            print(Fore.BLACK + "Your ships: " + str(myFleet) )

def initialize_enemyFleet():
    global enemyFleet

    enemyFleet = GameController.initialize_ships()

    enemyFleet[0].positions.append(Position(Letter.B, 4))
    enemyFleet[0].positions.append(Position(Letter.B, 5))
    enemyFleet[0].positions.append(Position(Letter.B, 6))
    enemyFleet[0].positions.append(Position(Letter.B, 7))
    enemyFleet[0].positions.append(Position(Letter.B, 8))

    enemyFleet[1].positions.append(Position(Letter.E, 6))
    enemyFleet[1].positions.append(Position(Letter.E, 7))
    enemyFleet[1].positions.append(Position(Letter.E, 8))
    enemyFleet[1].positions.append(Position(Letter.E, 9))

    enemyFleet[2].positions.append(Position(Letter.A, 3))
    enemyFleet[2].positions.append(Position(Letter.B, 3))
    enemyFleet[2].positions.append(Position(Letter.C, 3))

    enemyFleet[3].positions.append(Position(Letter.F, 8))
    enemyFleet[3].positions.append(Position(Letter.G, 8))
    enemyFleet[3].positions.append(Position(Letter.H, 8))

    enemyFleet[4].positions.append(Position(Letter.C, 5))
    enemyFleet[4].positions.append(Position(Letter.C, 6))

if __name__ == '__main__':
    main()
