import os
import re

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.attack_direction = None
        self.defend_direction = None
        self.previous_attack = None
        self.previous_defese = None
        self.stun = False
        self.hp = 1
        self.dmg = 1
    def move(self, moves,oponent_position):
        array = moves.split(',')
        direction = array[0]
        self.set_attack(array[1])
        self.set_defend(array[2])
        if direction == 'W':
            if self.position[0] == oponent_position[0] and self.position[1]+1 == oponent_position[1]:
               print(f"{self.name} foi bloqueado de andar para cima!")
            else:
                self.position = (self.position[0], max(0, self.position[1] - 1))     
        elif direction == 'S':
            if self.position[0] == oponent_position[0] and self.position[1]+1 == oponent_position[1]:
                print(f"{self.name} foi bloqueado de andar para baixo!")
            else:
                self.position = (self.position[0], min(4, self.position[1] + 1))  
        elif direction == 'A':
            if self.position[1] == oponent_position[1] and self.position[0]-1 == oponent_position[0]:
                print(f"{self.name} foi bloqueado de andar para esquerda!")
            else:
                self.position = (max(0, self.position[0] - 1), self.position[1])
        elif direction == 'D':
            if self.position[1] == oponent_position[1] and self.position[0]+1 == oponent_position[0]:
                print(f"{self.name} foi bloqueado de andar para direita!")
            else:
                self.position = (min(4, self.position[0] + 1), self.position[1])
        elif direction == 'Q':
            self.position = (self.position[0], self.position[1])
        elif direction == 'WD':
            self.position = (min(4, self.position[0] + 1), max(self.position[1]-1,0))
        elif direction == 'SD':
            self.position = (min(4, self.position[0] + 1), min(self.position[1]+1,4))
        elif direction == 'SA':
            self.position = (max(0, self.position[0] - 1), min(self.position[1]+1,4))
        elif direction == 'WA':
            self.position = (max(0, self.position[0] - 1), max(self.position[1]-1,0))

    def set_attack(self, direction):
        self.attack_direction = direction

    def set_defend(self, direction):
        self.defend_direction = direction

class Game:
    def __init__(self):
        self.board = [[None for _ in range(5)] for _ in range(5)]
        self.player1 = Player("Player 1", (0, 1))
        self.player2 = Player("Player 2", (0, 0))
        self.board[1][0] = self.player1#4,0
        self.board[0][0] = self.player2#0,4
        self.winner=None

    def display_board(self):
        for row in self.board:
            print(' | '.join(['P1' if p == self.player1 else 'P2' if p == self.player2 else ' ' for p in row]))
            print('-' * 13)

    def play_turn(self):
        if self.player1.previous_attack:
            print(f"Player 1 previous attack: {self.player1.previous_attack}")
        if self.player2.previous_attack:
            print(f"Player 2 previous attack: {self.player2.previous_attack}")
        if self.player1.previous_defese:
            print(f"Player 1 previous defese: {self.player1.previous_defese}")
        if self.player2.previous_defese:
            print(f"Player 1 previous defese: {self.player2.previous_defese}")

        print("\nEscolha sua movimentação,ataque e defesa, dividido por virgula.\n\n")
        self.player1.move(input("Jogador 1: ").upper(),self.player2.position)
        self.player2.move(input("Jogador 2: ").upper(),self.player1.position)

        self.battle()

        self.update_board()

        self.player1.previous_attack = self.player1.attack_direction
        self.player2.previous_attack = self.player2.attack_direction

        self.player1.previous_defese = self.player1.defend_direction
        self.player2.previous_defese = self.player2.defend_direction

        self.check_winner()
        if self.winner:
            print(f"{self.winner} wins!")
            return True
        return False
    def battle(self):
        #Dano recebido de baixo sem bloqueio
        if self.player1.attack_direction == 'W':
            if self.player2.position == (self.player1.position[0],self.player1.position[1]-1) and self.player2.defend_direction != 'S':
                self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction == 'W':
            if self.player1.position == (self.player2.position[0],self.player2.position[1]-1) and self.player1.defend_direction != 'S':
                self.player1.hp = self.player1.hp - self.player2.dmg  
        
         

    def update_board(self):
        self.board = [[None for _ in range(5)] for _ in range(5)]
        self.board[self.player1.position[1]][self.player1.position[0]] = self.player1
        self.board[self.player2.position[1]][self.player2.position[0]] = self.player2

    def check_winner(self):
        if self.player1.hp == 0:
            self.winner = self.player2.name
        elif self.player2.hp == 0:
            self.winner = self.player1.name
        else:
            return (False,"teste")
os.system('clear')
game = Game()
game.display_board()

while True:
    if game.play_turn():
        break
    game.display_board()
