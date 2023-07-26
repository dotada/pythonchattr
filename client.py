# pylint: disable=missing-module-docstring, invalid-name
import socket
import threading
import sys
import ssl
import tkinter as tk
from queue import Queue

root = tk.Tk()
root.title("Deja's python chatroom")
root.minsize(800, 600)
text_box = tk.Entry(root)
text_box.grid(row=1, column=0, sticky="we")
read_only_text = tk.Text(root, state=tk.DISABLED)
read_only_text.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

def get_data():
    """
    Receives data from a socket connection and puts it into the message queue.

    Returns:
        None
    """
    try:
        while True:
            data = s.recv(2000)
            if data != b'':
                message_queue.put(data.decode())
            else:
                pass
    except ConnectionAbortedError:
        sys.exit(0)

def process_messages():
    """
    Processes the messages in the message queue and updates the read-only text box.

    Returns:
        None
    """
    while True:
        message = message_queue.get()
        root.after(0, lambda: update_read_only_text(message))
        message_queue.task_done()

def update_read_only_text(data):
    """
    Updates the read-only text box with the received message.

    Parameters:
        data (str): The received message.

    Returns:
        None
    """
    read_only_text.config(state=tk.NORMAL)
    read_only_text.insert(tk.END, data + '\n')
    read_only_text.config(state=tk.DISABLED)

def send_data(event=None):
    """
    Reads input from the text box and sends it over a socket connection.

    This function is called when the user presses the Enter key or clicks a send button.
    It reads the input from the text box and sends the data over a socket connection.

    Parameters:
        event (tkinter.Event): The event object (optional).

    Returns:
        None
    """
    try:
        data = text_box.get()
        if data.strip() == 'dc':
            s.send(data.strip().encode())
            s.close()
            sys.exit(0)
        if len(data) <= 2000:
            s.send(data.encode())
            text_box.delete(0, tk.END)
        else:
            print("Message too long.")
    except ConnectionAbortedError:
        sys.exit(0)

def on_enter(event):
    """
    Calls the send_data function when the Enter key is pressed.

    Parameters:
        event (tkinter.Event): The event object.

    Returns:
        None
    """
    send_data()

s = socket.socket()
ssl_context = ssl.create_default_context()
s = ssl_context.wrap_socket(s, server_hostname='chat.dejacraft.cf')
port = 666
s.connect(('chat.dejacraft.cf', port))

# Bind the send_data function to the Enter key event
root.bind('<Return>', on_enter)

message_queue = Queue()

try:
    t2 = threading.Thread(target=send_data)
    t2.start()
    t3 = threading.Thread(target=get_data)
    t3.start()
    t4 = threading.Thread(target=process_messages)
    t4.start()
    root.mainloop()  # Start the main event loop
except ConnectionAbortedError:
    sys.exit(0)
