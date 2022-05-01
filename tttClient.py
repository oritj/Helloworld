import socket
import pygame
import sys
from time import sleep
import os
import ast
import threading

data = ""

XorO = ""
width = 300
height = 300
radius = 30
color1 = pygame.Color(200,0,0)
color2 = pygame.Color(100,100,100)
middle_positions = [(50,50),(150,50),(250,50),(50,150),(150,150),(250,150),(50,250),(150,250),(250,250)]
    

IP = socket.gethostbyname(socket.gethostname())
PORT = 8820
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def send_to_server (client, data):
    client.send(data.encode(FORMAT))

def recv_from_server(client):
        data = client.recv(SIZE).decode(FORMAT)
        print("recieved data: " + data)
        return data
def quit (client): 
    send_to_server (client, "!DISCONNECT")
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    pygame.quit()
    print ("Bye")
    sys.exit()
    
def play_turn (temp, board, XorO):    
    x = temp[0]
    y = temp[1]
    temp_board = board
    legal_action = True
    print("play turn called with: " + str(temp))
    if (XorO == "X"):
        if x >=0 and x<=100 and y>=0 and y<=100:
            if temp_board[0] == "NULL":
                temp_board[0] = "X"
            else:
                legal_action = False
        elif x >=100 and x<=200 and y>=0 and y<=100:
            if temp_board[1] == "NULL":
                temp_board[1] = "X"
            else:
                legal_action = False
        elif x >=200 and x<=300 and y>=0 and y<=100:
            if temp_board[2] == "NULL":
                temp_board[2] = "X"
            else:
                legal_action = False
        elif x >=0 and x<=100 and y>=100 and y<=200:
            if temp_board[3] == "NULL":
                temp_board[3] = "X"
            else:
                legal_action = False
        elif x >=100 and x<=200 and y>=100 and y<=200:
            if temp_board[4] == "NULL":
                temp_board[4] = "X"
            else:
                legal_action = False
        elif x >=200 and x<=300 and y>=100 and y<=200:
            if temp_board[5] == "NULL":
                temp_board[5] = "X"
            else:
                legal_action = False
        elif x >=0 and x<=100 and y>=200 and y<=300:
            if temp_board[6] == "NULL":
                temp_board[6] = "X"
            else:
                legal_action = False
        elif x >=100 and x<=200 and y>=200 and y<=300:
            if temp_board[7] == "NULL":
                temp_board[7] = "X"
            else:
                legal_action = False
        elif x >=200 and x<=300 and y>=200 and y<=300:
            if temp_board[8] == "NULL":
                temp_board[8] = "X"
            else:
                legal_action = False
    elif (XorO == "O"):
        if x >=0 and x<=100 and y>=0 and y<=100:
            if temp_board[0] == "NULL":
                temp_board[0] = "O"
            else:
                legal_action = False
        elif x >=100 and x<=200 and y>=0 and y<=100:
            if temp_board[1] == "NULL":
                temp_board[1] = "O"
            else:
                legal_action = False
        elif x >=200 and x<=300 and y>=0 and y<=100:
            if temp_board[2] == "NULL":
                temp_board[2] = "O"
            else:
                legal_action = False
        elif x >=0 and x<=100 and y>=100 and y<=200:
            if temp_board[3] == "NULL":
                temp_board[3] = "O"
            else:
                legal_action = False
        elif x >=100 and x<=200 and y>=100 and y<=200:
            if temp_board[4] == "NULL":
                temp_board[4] = "O"
            else:
                legal_action = False
        elif x >=200 and x<=300 and y>=100 and y<=200:
            if temp_board[5] == "NULL":
                temp_board[5] = "O"
            else:
                legal_action = False
        elif x >=0 and x<=100 and y>=200 and y<=300:
            if temp_board[6] == "NULL":
                temp_board[6] = "O"
            else:
                legal_action = False
        elif x >=100 and x<=200 and y>=200 and y<=300:
            if temp_board[7] == "NULL":
                temp_board[7] = "O"
            else:
                legal_action = False
        elif x >=200 and x<=300 and y>=200 and y<=300:
            if temp_board[8] == "NULL":
                temp_board[8] = "O"
            else:
                legal_action = False
    return temp_board, legal_action
        
def win_check (board, surf):
    if (board[0] == board[1] and board[1] == board [2] and board[0] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(0,50), (300,50), 4)
        return (board[0])
    elif (board[3] == board[4] and board[4] == board [5] and board[3] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(0,150), (300,150), 4)
        return (board[3])
    elif (board[6] == board[7] and board[7] == board [8] and board[6] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(0,250), (300,250), 4)
        return (board[6])
    elif (board[0] == board[3] and board[3] == board [6] and board[0] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(50,0), (50,300), 4)
        return (board[0])
    elif (board[1] == board[4] and board[4] == board [7] and board[1] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(150,0), (150,300), 4)
        return (board[1])
    elif (board[2] == board[5] and board[5] == board [8] and board[2] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(250,0), (250,300), 4)
        return (board[2])
    elif (board[0] == board[4] and board[4] == board [8] and board[0] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(0,0), (300,300), 4)
        return (board[0])
    elif (board[6] == board[4] and board[4] == board [2] and board[6] != "NULL"):
        pygame.draw.line(surf,(255,255,255),(0,300), (300,0), 4)
        return (board[6])
    return False
    
def drawXO (board, surf):
    for i in range (9):
        if (board[i]== "X"):
            current_pose_x = middle_positions[i][0]
            current_pose_y = middle_positions[i][1]
            pygame.draw.line(surf,color1,(current_pose_x-30,current_pose_y-30),(current_pose_x+30,current_pose_y+30),4)
            pygame.draw.line(surf,color1,(current_pose_x-30,current_pose_y+30),(current_pose_x+30,current_pose_y-30),4)
        if (board[i]== "O"):
            pygame.draw.circle(surf,color1,middle_positions[i],30)
            
def recv_with_thread (client,SIZE,FORMAT):
    print(client)
    data1 = client.recv(SIZE).decode(FORMAT)
    print("thread recieved data: " + data1)
    global data
    data = data1

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print (f"[CONNTCTED] client connected to server at {IP}:{PORT}")
    
    connected = True
    firstMSG = True
    
    turn = 1
    board = ["NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"]
    global data
    
    final_msg = "its a tie!"
    
    try:
        while connected:
            while firstMSG:
                msg = client.recv(SIZE).decode(FORMAT)
                if (msg != ""):
                    msg.capitalize()
                    XorO = msg
                    print ("Playing " + XorO)
                    firstMSG = False
            pygame.init()
            surf = pygame.display.set_mode((width,height))
            pygame.display.set_caption(XorO)
            font = pygame.font.Font('freesansbold.ttf', 32)
            font2 = pygame.font.Font('freesansbold.ttf', 12)
        
            while (turn <= 9):
                if ((XorO == "X" and (turn%2) == 1) or (XorO == "O" and (turn%2) == 0)):
                    print("not my turn")
                    waiting = True
                    thread = threading.Thread(target = recv_with_thread, args = (client,SIZE,FORMAT))
                    thread.start()
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit(client)
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    quit(client)
                                else:
                                    print ("invalid command")
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                print("not your turn!")
                        surf.fill(color2) 
                        pygame.draw.line(surf,(255,255,255),(0,100), (300,100), 4)
                        pygame.draw.line(surf,(255,255,255),(100,0), (100,300), 4)
                        pygame.draw.line(surf,(255,255,255),(0,200), (300,200), 4)
                        pygame.draw.line(surf,(255,255,255),(200,0), (200,300), 4)
                        drawXO(board, surf)
                        pygame.display.update()
                        if (data != ""): 
                            print(board)
                            board = ast.literal_eval(data)
                            waiting = False
                            thread_is_running = False
                            turn +=1
                            data = ""
                            break
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit(client)
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                quit(client)
                            else:
                                print ("invalid command")
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            position = pygame.mouse.get_pos()
                            mouseX = position[0]
                            mouseY = position[1]
                            temp_mouse_pos = (mouseX,mouseY)
                            print("current mouse (X,Y):" + str(temp_mouse_pos))
                            temp_board, legal_action = play_turn(temp_mouse_pos, board, XorO)
                            print(temp_board)
                            if (legal_action == False):
                                print("the tile you have selected is already caught")
                            else:
                                board = temp_board
                                print(board)
                                send_to_server(client, str(board))
                                turn+=1
                
                surf.fill(color2)    
                pygame.draw.line(surf,(255,255,255),(0,100), (300,100), 4)
                pygame.draw.line(surf,(255,255,255),(0,200), (300,200), 4)
                pygame.draw.line(surf,(255,255,255),(100,0), (100,300), 4)
                pygame.draw.line(surf,(255,255,255),(200,0), (200,300), 4)
                drawXO(board, surf)
                if (win_check(board, surf) != False):
                    winner = win_check(board, surf)
                    if (winner == XorO):
                        final_msg = "You win!"
                    else:
                        final_msg = "You lose"
                    turn = 10
                    break
                pygame.display.update()
                    
            pygame.display.update()
            sleep(1)
            wait_for_response = True
            while (wait_for_response):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit(client)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            quit(client)
                        else:
                            wait_for_response = False
                            break
                surf.fill(color2)
                top_msg = font.render(final_msg , True , color1)
                play_again_msg = font2.render("To quit, press Q. For another match, press any key." , True , color1)
                surf.blit(top_msg, (80,150))
                surf.blit(play_again_msg,(1, 200))
                pygame.display.update()
            send_to_server(client, "DONE")
            final_msg = ""
            firstMSG = True
            turn = 1
            board = ["NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"]
            pygame.quit()
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        quit(client)
if __name__ == "__main__":
    main()