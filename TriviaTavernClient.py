#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 17:10:10 2021

@author: alessandro
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt


def receive():
    """It manages the receipt of message"""
    while True:
        try:
            # When it's called it listens for messages that arrive on the socket
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # Display the message list on the screen and make sure that the cursor is visible at the end of the same
            msg_list.insert(tkt.END, msg)
            # In case of an error it is likely that the client has left the chat.

        except OSError:  
            break

def send(event=None):
    """ It manages the sending of messages"""
    # Events are passed by binders
    msg = my_msg.get()
    # Clear the input box
    my_msg.set("")
    # Send message on socket
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        window.quit()

def on_closing(event=None):
    """It's invoked when the chat window is closed. """
    my_msg.set("{quit}")
    send()
    window.destroy()

window = tkt.Tk()
window.title("TriviaTavern")

# Create the frame for message
messages_frame = tkt.Frame(window)
# Create variable to save input string
my_msg = tkt.StringVar()
# Indicate to the user where he should write his messages
my_msg.set("Write here:")
# Create scrollbar to navigate on previously message
scrollbar_y = tkt.Scrollbar(messages_frame)
scrollbar_x = tkt.Scrollbar(messages_frame, orient='horizontal')

# Next part is for message box
msg_list = tkt.Listbox(messages_frame, height=20, width=130, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
scrollbar_y.pack(side=tkt.RIGHT, fill=tkt.Y)
scrollbar_x.pack(side=tkt.BOTTOM, fill=tkt.X)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

# Create the input field and associate it with the string variable
entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
# Create the enter key and associate it with the send function
send_button = tkt.Button(window, text="Enter", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

#----Server connection----
HOST = input('Insert host server: ')
PORT = input('Insert door host server: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
# Start execution window chat
tkt.mainloop()
