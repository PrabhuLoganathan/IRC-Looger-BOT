##############################################################################
#   A simple IRC Bot used for loggin in txt-files according to date
#   Author:     Gaurav Mittal
#   License:    See LICENSE
##############################################################################
import socket , time, datetime

server = "irc.freenode.net" # Server
channel = "#channel-here" # Channel
botnick = "logger" # Your Logger (Bot) nick

def joinchan(chan): # Join Channel
    ircsock.send("JOIN "+ chan +"\n")
 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" : \n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel

def ping():
    ircsock.send("PONG :pingis\n")

while 1: #Endless Listening
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
    ircmsg = ircmsg.strip(':') # Cleaning up the incoming message
    filename = time.strftime("%d-%m-%Y")
    filename = (str)(filename)
    f = open(filename+".txt","a+")
    try:
        ircmsg_name = ircmsg.split("!")[0] # Getting the sender Name (rather the nick)
    except:
        ircmsg_name = "Error_Detected"
    try:
        ircmsg_request = ircmsg.split(" ")[1] # Getting the type of command sent by the nick
    except:
        ircmsg_request = " "
    time_cur = time.time()
    time_cur = datetime.datetime.fromtimestamp(time_cur).strftime('%Y-%m-%d %H:%M:%S') #Getting the time Stamp
    if ircmsg_request == "JOIN":
        message = time_cur+":\t-- "+ircmsg_name+" joined."
        print message
        f.write(message+"\n")
    elif ircmsg_request == "PRIVMSG":
        msg = ircmsg.split(" ")[3:]
        len_msg = len(msg)
        semi_msg = ""
        for i in range(len_msg-1):
            semi_msg += msg[i]+" "
        semi_msg += msg[len_msg-1]
        msg = semi_msg.split(":")[1:]
        len_msg = len(msg)
        final_msg = ""
        for i in range(len_msg-1):
            final_msg += msg[i]+":"
        final_msg += msg[len_msg-1]
        message = time_cur+":"+ircmsg_name+":"+final_msg
        f.write(message+"\n")
        print message # message sent
    elif ircmsg_request == "QUIT":
        message = time_cur+":\t-- "+ircmsg_name+" quit."    
        print message
        f.write(message+"\n")
    elif ircmsg_request == "NICK":
        message = time_cur+":\t-- "+ircmsg_name+" changed nick to "+ircmsg.split(" ")[2].split(":")[1]
        print message
        f.write(message+"\n")
    elif ircmsg.find("PING :") != -1:
        ping()
    else:
        f.write(ircmsg+"\n")
        print ircmsg
    f.close()
