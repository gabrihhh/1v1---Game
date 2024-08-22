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
    def verifica_input(self,str):
        validacao = 0
        array = str.split(',')
        if len(array) == 3:
            validacao += 1
        if array[0] == "Q" or array[0] == "W" or array[0] == "A" or array[0] == "S" or array[0] == "D" or array[0] == "WA" or array[0] == "WD" or array[0] == "SA" or array[0] == "SD":
             validacao += 1
        if array[1] == "Q" or array[1] == "W" or array[1] == "A" or array[1] == "S" or array[1] == "D" or array[1] == "WA" or array[1] == "WD" or array[1] == "SA" or array[1] == "SD":
             validacao += 1  
        if array[2] == "Q" or array[2] == "W" or array[2] == "A" or array[2] == "S" or array[2] == "D" or array[2] == "WA" or array[2] == "WD" or array[2] == "SA" or array[2] == "SD":
             validacao += 1
            
        if validacao == 4:
            return True
        else:
            return False
    def play_turn(self):
        if self.winner:
            print(f"{self.winner} wins!")
            return True


        if self.player1.previous_attack:
            print(f"Player 1\n ultimo ataque: {self.player1.previous_attack}")
        if self.player1.previous_defese:
            print(f" ultima defesa: {self.player1.previous_defese}")
        if self.player2.previous_attack:
            print(f"Player 2\n ultimo ataque: {self.player2.previous_attack}")
        if self.player2.previous_defese:
            print(f" ultima defesa: {self.player2.previous_defese}")

        print("\nEscolha sua movimentação,ataque e defesa, dividido por virgula.\n\n")

        while True:
            keydownPlayer1 = input("Jogador 1: ").upper()
            if self.verifica_input(keydownPlayer1):
                break
            else:
                print("A Letra escolhida não se refere a nenhum tipo de movimentação, tente novamente.")

        while True:
            keydownPlayer2 = input("Jogador 2: ").upper()
            if self.verifica_input(keydownPlayer2):
                break
            else:
                print("A Letra escolhida não se refere a nenhum tipo de movimentação, tente novamente.")

        self.player1.move(keydownPlayer1,self.player2.position)
        self.player2.move(keydownPlayer2,self.player1.position)

        self.update_board()
        
        self.player1.previous_attack = self.player1.attack_direction
        self.player2.previous_attack = self.player2.attack_direction

        self.player1.previous_defese = self.player1.defend_direction
        self.player2.previous_defese = self.player2.defend_direction

        return False
    #função feita para construção de lógica de combate
    def battle(self):
        #Dano para cima
        if self.player1.attack_direction == 'W':
            if self.player2.position == (self.player1.position[0],self.player1.position[1]-1):
                if self.player2.defend_direction == 'S':
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction == 'W':
            if self.player1.position == (self.player2.position[0],self.player2.position[1]-1):
                if self.player1.defend_direction == 'S':
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg  

        #Dano para baixo
        if self.player1.attack_direction == 'S':
            if self.player2 == (self.player1.position[0],self.player1.position[1]+1):
                if self.player2.defend_direction == 'W':
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction == 'S':
            if self.player1 == (self.player2.position[0],self.player2.position[1]+1):
                if self.player1.defend_direction == 'W':
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg  
        #Dano para esquerda
        if self.player1.attack_direction=="A":
            if self.player2.position == (self.player1.position[0]-1,self.player1.position[1]):
                if self.player2.defend_direction == "D":
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg

        if self.player2.attack_direction=="A":
            if self.player1.position == (self.player2.position[0]-1,self.player2.position[1]):
                if self.player1.defend_direction == "D":
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg
        
        #Dano para direita
        if self.player1.attack_direction=="D":
            if self.player2.position == (self.player1.position[0]+1,self.player1.position[1]):
                if self.player2.defend_direction == "A":
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction=="D":
            if self.player1.position == (self.player2.position[0]+1,self.player2.position[1]):
                if self.player1.defend_direction == "A":
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg
        
        #Dano para Cima Esquerda
        if self.player1.attack_direction=="WA":
            if self.player2.position == (self.player1.position[0]-1,self.player1.position[1]-1):
                if self.player2.defend_direction == "SD":
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction=="WA":
            if self.player1.position == (self.player2.position[0]-1,self.player2.position[1]-1):
                if self.player1.defend_direction == "SD":
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg
         #Dano para Baixo Esquerda
        if self.player1.attack_direction=="SA":
            if self.player2.position == (self.player1.position[0]-1,self.player1.position[1]+1):
                if self.player2.defend_direction == "WD":
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction=="SA":
            if self.player1.position == (self.player2.position[0]-1,self.player2.position[1]+1):
                if self.player1.defend_direction == "WD":
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg
         #Dano para Cima Direita
        if self.player1.attack_direction=="WD":
            if self.player2.position == (self.player1.position[0]+1,self.player1.position[1]-1):
                if self.player2.defend_direction == "SA":
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction=="WD":
            if self.player1.position == (self.player2.position[0]+1,self.player2.position[1]-1):
                if self.player1.defend_direction == "SA":
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
                    self.player1.hp = self.player1.hp - self.player2.dmg
         #Dano para Baixo Direita
        if self.player1.attack_direction=="WD":
            if self.player2.position == (self.player1.position[0]+1,self.player1.position[1]+1):
                if self.player2.defend_direction == "WA":
                    print(f"{self.player2.name} bloqueou!")
                else:
                    print(f"{self.player2.name} tomou um hit!")
                    self.player2.hp = self.player2.hp - self.player1.dmg
        if self.player2.attack_direction=="WD":
            if self.player1.position == (self.player2.position[0]+1,self.player2.position[1]+1):
                if self.player1.defend_direction == "WA":
                    print(f"{self.player1.name} bloqueou!")
                else:
                    print(f"{self.player1.name} tomou um hit!")
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
game = Game()
game.display_board()

while True:
    if game.play_turn():
        break
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    game.display_board()
    game.battle()
    game.check_winner()