#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 17:09:35 2021

@author: alessandro
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import random
import time

def accept_connections():
    """ Accept incoming client connection."""
    while True:
        # Player x is connected
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        
        # Info about the game
        send_msg(client, "Welcome on TriviaTavern! In this game you have to answer a few question as quickly as possible. ")
        send_msg(client, "The first to reach 5 wins. Good Luck! ")
        # Insert Player Name
        send_msg(client, " Please insert your name here: ")
        
        # Dictionary for client 
        clients_address[client] = client_address
        # Starting thread - one for each client
        Thread(target=client_manager, args=(client,)).start()

def client_manager(client):
    """Manage the connection with single client""" 
    # Name of client-player
    name = client.recv(BUFSIZ).decode("utf8")
    # Add information about player
    add_player(client)
    
    # Info about name and role of player
    send_msg(client, "Welcome %s! Digit {quit} to leave the chat. " % name)
    send_msg(client, "Your role is " + str(client_role[client]) + ". ")
    
    # Broadcast message where all are notified that user x is logged in
    user_login(client, name)
    
    # Select the number of player
    insert_num_player(client, name)
    
    # Preliminary_question
    preliminary_question(client, name)
    
    # Check if player are ready to start
    check_player_ready(client)
    
    # Start with question
    start_question(client, name)
    
    # Choose the winner
    find_winner(client)
    
    # Close client
    client_close(client, name)
    
def broadcast(msg, prefisso=""):  # prefix used for identify the name
    """Send broadcast message to each client"""
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)
        
def send_msg(client, text):
    """"Simplifies the sending function of a message
        %client -> the client that send the message
        %text ->  the text will be sent
    """
    client.send(bytes(str(text), "utf8"))

# ----------------------------------
# Function for client_manager
def add_player(client):
    """Add player info like role, initial score
        client -> current client
    """
    client_role[client] = role[random.randint(1, len(role))]
    if client_role[client] == "Wizard":  
        client_score[client] = 2
    if client_role[client] == "Berserk":  
        client_score[client] = -2
    if client_role[client] == "Paladin":  
        client_score[client] = 0
    if client_role[client] == "Cleric":  
        client_score[client] = -1
    if client_role[client] == "Thief":  
        client_score[client] = 1

def user_login(client, name):
    """Warn users that another user joined the chat
        client -> current client
        name -> name of current client
    """
    msg = "%s joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    # Update dictionary clients
    clients[client] = name

def insert_num_player(client, name): 
    """Only the first client can insert the number of player
        client -> current client
        name -> name of current client
    """
    global num_player
    global player_insert
    # Check if num_player was already insert
    if player_insert == False:
        send_msg(client, "Insert number of player:")
        temp = client.recv(BUFSIZ)
        # Check if is {quit}
        check_quit(temp, client, name)
        # Check if is a number
        num_player = check_number(client, temp, min_player, max_player)   
        # Now noone can reinsert number of player
        player_insert = True

def preliminary_question(client, name):
    """Assign first question to player, if he doesn't pass this, he lose the game
        client -> current client
        name -> name of current client
    """
    global num_player
    
    # Select option trap
    trap = random.randint(min_option, max_option)
    # Ask for the option
    send_msg(client, "You are sitting at a table in a tavern, the master asks you a question, you have " + str(max_option) + " choices ")
    send_msg(client, "Digit number between " + str(min_option) + " and " + str(max_option) + ": ")
    temp = client.recv(BUFSIZ)
    # Check if is {quit}
    check_quit(temp, client, name)
    # Check if it's between of this number
    preliminar_answer = check_number(client, temp, min_option, max_option)
    # Check if he fell into the trap
    if preliminar_answer == trap:
        send_msg(client, "You fell into the master's trap, you lost ")
        if num_player > 1:
            num_player -= 1
        client_close(client, name)
    else:
        send_msg(client, "You have been able to answer the master's question correctly, now you can challenge other players ")
    
def start_question(client, name):
    """Start to ask same question to all player
        client -> current client
        name -> name of current client
    """
    client_question_max = question_max
    client_question_index = 0
    
    while client_question_index != client_question_max and gameover == False:
        # Take random question, send to client and wait for answer
        single_question, single_answer = choose_question()
        send_msg(client, single_question)
        temp = client.recv(BUFSIZ)
        # Check if temp == {quit}, close client
        check_quit(temp, client, name)
        client_answer = temp
        # Check if is correct and add score
        state = check_answer(client, client_answer, single_answer, name)
        check_score(client, state)
        send_msg(client, clients[client] + " score: " + str(client_score[client]))
        client_question_index += 1

def choose_question():
    """Assign random question for the player """
    random_index_question = random.randint(1,len(question))
    single_question = question[random_index_question]
    single_answer = answer[random_index_question]
    return single_question, single_answer
   
def find_winner(client):
    """Find max score, if there are more than one max score, print a draw, without any name, 
        otherwise print the name of player with max score
        client -> current client
    """
    global max_player_name
    global gameover
    max_score = 0
    draw = False
    gameover = True
    # Find Max score
    for pkey in client_score:
        if max_score < client_score[pkey]:
            max_score = client_score[pkey]
            max_player_name = clients[pkey] 
        elif max_score == client_score[pkey] and len(client_score) != 1:
            draw = True
    if draw:
        broadcast(bytes("The game finish with a draw!", "utf8"))
    else:
        broadcast(bytes("The winner is: " + max_player_name + " with " + str(max_score) + " points!", "utf8"))

def client_close(client, name):
    """Close client and print to all that user left the chat
        client -> current client
        name -> name of current client
    """
    send_msg(client, "Exit ...")
    client.close()
    del clients[client]
    del client_role[client]
    del client_score[client]
    del clients_address[client]
    broadcast(bytes("%s has left chat." % name, "utf8"))
       
# ----------------------------------
# Check function

def check_number(client, num, min, max):
    """Check if temp is a number between min and max, if is not will have to be reinserted. 
        Type of num -> bytes.
        Return an integer
        client -> current client
        num -> number to check
        min -> min range
        max -> max range
    """
    while True:
        try:
            # Convert it into integer
            temp = int(num)
            if temp >= min and temp <= max:
                break
            else:
                send_msg(client, "Please, insert a number between " + str(min) + " and " + str(max) + ": ")
                num= client.recv(BUFSIZ)
        except ValueError:
            send_msg(client, "Please, insert a number between " + str(min) + " and " + str(max) + ": ")
            num = client.recv(BUFSIZ)              
    return temp

def check_player_ready(client):
    """Check if the current clients connected are the same as number player previously insert
        client -> current client
     """
    while len(clients) != num_player:
        if len(clients) < num_player:
            send_msg(client, "Waiting for other player...")
        else:   
            send_msg(client, "Too much player connected!, please someone leave the chat")
        time.sleep(5)  
    send_msg(client, "Game can start, good luck!")

def check_answer(client, client_answer, single_answer, name):
    """Check if answer is correct, return True if is correct, false otherwise
        client -> current client
        client_answer -> answer of client
        single_answer -> right answer of question
        name -> name of current client
    """
    if client_answer == bytes(str(single_answer), "utf8"):
        send_msg(client, "Correct! The player: %s has earned one point. " % name)
        return True
    else:
        send_msg(client, "Wrong! The player: %s has lost one point. " % name)
        return False

def check_score(client, state):
    """Check score of player, if state is true add one point, if it's false remove one point
        client -> current client
        state -> If is true client earned one point, otherwise lost one
    """
    if state:
        client_score[client] += 1
    else:
        client_score[client] -= 1 
        
def check_quit(string, client, name):
    """Check if string is equal {quit}.
        string -> string to check
        client -> current client
        name -> name of current client
    """
    if string == bytes("{quit}", "utf8"):
        client_close(client, name)

# ----------------------------------

# Player variable
clients = {}
clients_address = {} 
client_answer = {} 
client_score = {} 
client_role = {} 
role = {1 : "Wizard", 2 : "Berserk", 3 : "Paladin", 4 : "Cleric", 5 : "Thief"}

# Player setup
player_insert = False
num_player = 1
min_player = 1
max_player = 5
max_player_name = "null"

# Game state
gameover = False

# Option setup
min_option = 1
max_option = 3

# Question variable
question_max = 5
question = {1 : "What is the name of the track reserved for auto-mobile competitions in general? ", 
            2 : "What was the name of the magic sword that, according to legend, gave King Arthur the Kingdom? ",
            3 : "If it's cold you take it by the neck. What's this? ",
            4 : "He has teeth and yet he does not eat. What is that? ",
            5 : "He was defeated at Waterloo ",
            6 : "How many toes do dogs have forelegs? (Insert number) ",
            7 : "Water boils at 212 degrees on which temperature scale? ",
            8 : "Which Australian marsupial enjoys eating eucalyptus leaves? ",
            9 : "What is one quarter of 1,000? (Insert number) ",
            10 : "When did the French Revolution end? (Insert number)",
            11 : "Which ocean surrounds the Maldives? ",
            12 : "Which Russian town suffered an infamous nuclear disaster in 1986? ",
            13 : "Name this stringless fictional character created by Carlo Collodi over one hundred years ago. ",
            14 : "What is another word for lexicon? ",
            15 : "What is the seventh planet from the sun? "}
answer = {1 : "Autodromo",
            2 : "Excalibur" ,
            3 : "Scarf",
            4 : "Comb",
            5 : "Napoleone", 
            6 : "5",
            7 : "Fahrenheit",
            8 : "Koala",
            9 : "250",
            10 : "1799",
            11 : "Indian Ocean",
            12 : "Chernobyl",
            13 : "Pinocchio",
            14 : "Dictionary",
            15 : "Uranus"}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting connections...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()