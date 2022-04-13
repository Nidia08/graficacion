from shutil import move
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

w,h = 950,650
#Bandera de inicio
start = False

#Movimiento
mov_y = 0
time = 0
diagonal = 0
move_map = 0

#multiplicador para el movimiento del carro
mov = 0

#funcion para dibujar y redibujar el carro 
def drawCar():
    colors = [1,88/255,88/255]
    glColor3f(colors[0],colors[1],colors[2])
    glBegin(GL_QUADS)
    xleft = w/2-50+mov;
    xright = w/2+50+mov;
    glVertex2d(xleft,150)#top izquierda
    glVertex2d(xright,150)#top derecha
    glVertex2d(xright,50)#bottom derecha
    glVertex2d(xleft,50)#bottom izquierda
    glEnd()

def keyPressed ( key, x, y ):
    global start, mov_y, time, diagonal, move_map, mov, xright, xleft

    if key == b'a':
        if (mov >= -155):
            mov += -10
            drawCar()

    if key == b'd':
        if (mov <= 155):
            mov += 10
            drawCar()

    if key == b'\x1b':
        glutLeaveMainLoop()  
    if key == b' ':
        start = True
        mov_y = 0
        time = 0
        diagonal = 0
        move_map = 0
        mov = 0
    

def keyUp ( key, x, y):
    global flag_left, flag_down, flag_right, flag_up, mov

    if key == b'\x1b':
        glutLeaveMainLoop()

def polygon(xc,yc,R,l,r,g,b):
    angle = 2*3.141592/l
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    for i in range(l):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()

#--------------------------------------Fondo--------------------------------------#
def draw_speedway(diagonal):
    global w,h

    glColor3f(0.1,0,0.1)
    glBegin(GL_QUADS)
    glVertex2f(int(w/4) - diagonal, 0)
    glVertex2f(int(w/4)*3 - diagonal, 0)
    glColor3f(0,0.5,1)
    glVertex2f(int(w/4)*3 + diagonal, h)
    glVertex2f(int(w/4) + diagonal, h)
    glEnd()
    
    if diagonal != 0: #If para mover las diagonales
        lines(0, diagonal*0.2, -diagonal) 
        lines(int(h/4), diagonal*0.2, -diagonal*0.3)
        lines(int(h/2), diagonal*0.2, diagonal*0.3)
        lines(int(h/4)*3, diagonal*0.2, diagonal)
    else: 
        lines(0, 0, 0) 
        lines(int(h/4), 0, 0)
        lines(int(h/2), 0, 0)
        lines(int(h/4)*3, 0, 0)


def lines(pos_y, inc, pos_x):
    global mov_y, w, h
    lines_coord=[[int(w/32)*20 - inc, int(h/16)], 
                [int(w/32)*21 -10 - inc, int(h/16)], 
                [int(w/32)*21 -10 + inc, int(h/4)], 
                [int(w/32)*20 + inc, int(h/4)],
                [int(w/32)*12 - inc, int(h/16)],
                [int(w/32)*13 -10 - inc, int(h/16)],
                [int(w/32)*13 -10 + inc, int(h/4)],
                [int(w/32) *12 + inc, int(h/4)]]
    glColor3f(0.5,0.5,0.5)
    glBegin(GL_QUADS)
    for i in range(len(lines_coord)):
        if lines_coord[i][1] + mov_y > 0:
            glVertex2d(lines_coord[i][0] + pos_x, lines_coord[i][1] + pos_y + mov_y)
        else:
            glVertex2d(lines_coord[i][0] + pos_x, lines_coord[i][1] + pos_y)
            mov_y = 0
    glEnd()

def draw_map(move_map): 
    glBegin(GL_QUADS)
    glColor3f(0.1,0.1,0.1)
    glVertex2d(0,0)
    glColor3f(0.5,0.5,0.5)
    glVertex2d(int(w/10),0)
    glVertex2d(int(w/10),h)
    glColor3f(0.1,0.1,0.1)
    glVertex2d(0,h)
    glEnd()

    move_map = 0 if int(w/20)-15 + move_map == h else polygon(int(w/20),int(w/20)-15 + move_map,int(w/20)-15,32,1,0,0)
    
#---------------------------------------------------------------------------------#

#------------------------------------TIMERS---------------------------------------#
def timer_move(value): #Timer para mover las lineas de la carretera, la pista, y el mapa (bola roja)
    global mov_y, start, time, diagonal, h, move_map
    if start:
        time_map = (h-int(w/20)-15)/1020 #Variable para incrementar la posicion en y del mapa
        if time < 1020:
            time += 1
            move_map += time_map
        if time < 150:
            mov_y -= 1      
        elif time < 200:
            mov_y -= 4
        elif time < 285:
            mov_y -= 8
        elif time < 800: 
            mov_y -= 16
            if time < 370:
                twist = True
                diagonal += 0.5
            elif time < 565:
                diagonal -= 0.5 
            elif time < 760:
                diagonal += 0.4 if diagonal < 0 else 0
        else:
            if time < 1000:
                mov_y -= 8
            elif time < 1020:
                mov_y -= 4
            elif time == 1020:
                mov_y = 0
                start = False
        glutPostRedisplay()
    glutTimerFunc(20, timer_move, 1)
#---------------------------------------------------------------------------------#

def init():
    glClearColor ( 0, 0, 0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def reshape(width, height):
    global w, h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def display():
    global diagonal, move_map
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()
    
    #---------------------DIBUJAR AQUI------------------------#
    draw_speedway(int(diagonal))
    draw_map(int(move_map))
    drawCar()
    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp = 0

def main():
    glutInit (  )
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( w, h )
    glutInitWindowPosition( 0, 0 )
    
    glutCreateWindow( "Game" )
    glutDisplayFunc (display)
    glutIdleFunc ( animate )
    glutReshapeFunc ( reshape )
    glutKeyboardFunc( keyPressed )
    glutKeyboardUpFunc( keyUp )
    init()

    timer_move(0)

    glutMainLoop()

print("Presiona Escape para cerrar.")
print("Presiona Espacio para iniciar.")
main()


