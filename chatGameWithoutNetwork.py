#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 11:48:02 2021

@author: alessandro
"""
import random

# Function to add player
def add_player(player_index):
    player[player_index] = input("Insert name of player: ")
    player_role[player_index] = role[random.randint(1, len(role))]
    player_score[player_index] = 0

# Function to assign first question to player, if he doesn't pass this, he lose the game
def preliminary_question():
    trap = random.randint(1, 3)
    preliminar_answer = int(input("Insert number between 1 and 3: "))
    if preliminar_answer == trap:
        print("Sorry, you lose the game.\n")
        return True

# Function to assign question to player
def choose_question():
    random_index_question = random.randint(1,6)
    single_question = question[random_index_question]
    single_answer = answer[random_index_question]
    return single_question, single_answer

# Check if answer is correct, return True if is correct, false otherwise
def check_answer(player_index, player_answer, single_answer):
    if player_answer == single_answer:
        print("Correct! The player: " + player[player_index] + " has earned one point. ")
        return True
    else:
        print("Wrong! The player: " + player[player_index] + " has lost one point. ")
        return False
        
# Check score of player, if state is true add one point, if it's false remove one point
def check_score(player_index, state):
    if state:
        player_score[player_index] += 1
    else:
        player_score[player_index] -= 1

# Find max score, if there are more than one max score, print a draw, without any name, otherwise print the name of player with max score
def find_winner():
    max_score = 0
    draw = False
    for pkey in player_score:
        if max_score < player_score[pkey]:
            max_score = player_score[pkey]
            max_player_name = player[pkey] 
        elif max_score == player_score[pkey] and len(player_score) != 1:
            draw = True
    if draw:
        print("The game finish with a draw!")
    else:
        print("The winner is: " + max_player_name + " with " + str(max_score) + " points!")
    
# Main 
def start():
    print("Welcome on ChatGame!")
    print("To win you have to answer at five question, good luck!")
    
    question_index = 0
    num_player = int(input("Insert number of player: "))
    
    for player_index in range(num_player):
        add_player(player_index)
    
    print("\nReady for the game:\n")
    # Preliminary_question Block, remove player from dictionary
    player_removed = 0
    new_player_index = 0
    temp_player = {}
    temp_player_score = {}
    
    for player_index in range(num_player):
        print(player[player_index] + ":")
        state = preliminary_question()  
        if state:
            player.pop(player_index)
            player_score.pop(player_index)
            player_removed += 1
                
    for player_index in range(num_player):
        if player_index in player:
            temp_player[new_player_index] = player[player_index]
            temp_player_score[new_player_index] = player_score[player_index]
            new_player_index +=1
    
    player.clear()

    for elem in temp_player:
        player[elem] = temp_player[elem]
        player_score[elem] = temp_player_score[elem]
        
    num_player -= player_removed
    
    # Loop game, run until question are the same as question_max
    if len(player) != 0:
        while question_index != question_max:
            quest, ans = choose_question()
            print("\n" + quest)
            for player_index in range(num_player):
                player_answer[player_index] = input("Player " + player[player_index] + " reply: ")
                state = check_answer(player_index, player_answer[player_index], ans)
                check_score(player_index, state)
                print(player[player_index] + " score: " + str(player_score[player_index]))
            question_index += 1
        # Game is finish, calculate the winner
        print("\nGame is over!")
        find_winner()

    
# Player variable
player = {}
player_answer = {}
player_score = {}
player_role = {}
role = {1 : "Wizard", 2 : "Berserk", 3 : "Paladin", 4 : "Cleric", 5 : "Thief"}

# Question variable
question_max = 5
question = {1 : "Che nome ha la pista riservata alle competizioni auto-mobilistiche in genere? ", 
           2 : "Come si chiamava la spada magica che secondo la leggenda procurò a Re Artù il Regno? ",
           3 : "Se fa freddo si prende per il collo. Cos'è? ",
           4 : "Ha i denti eppure non mangia. Che cos'è? ",
           5 : "Fu sconfitto a Waterloo ",
           6 : "Quante dita hanno le zampe anteriori dei Cani? (Inserisci il numero) "}
answer = {1 : "Autodromo",
            2 : "Excalibur" ,
            3 : "Sciarpa",
            4 : "Pettine",
            5 : "Napoleone", 
            6 : "5"}

start()

