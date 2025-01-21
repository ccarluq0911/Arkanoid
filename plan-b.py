import pygame

import random

def movimientoYColisionesRectangulo(x):

    keyPressed = pygame.key.get_pressed()
    

    if (keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a]) and x>0:
        x -= vel
        
    elif (keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d]) and x<width-rect_width:
        x += vel
    return x
def movimientoYColisionesPelota(xb,yb,movx,movy):
    efectoNegativo = False
    xb=xb+movx
    yb=yb+movy
    if(xb>=width):
        movx=-movx
    if(xb<=0):
        movx=-movx
    if(yb<=0):
        movy=-movy
        efectoNegativo=True
    if(yb>=height):
        movy=-movy
        xb=310
        yb=240
        efectoNegativo=True
    return xb,yb,movx,movy,efectoNegativo
def generarBloques():
    filas = []
    
    bloque_y=0
    bloque_width= 60
    bloque_height = 15
    
    for x in range (0,5):
        bloque_x = 5
        
        columnas=[]
        
        for y in range(0,10):
            columnas.append((bloque_x,bloque_y,bloque_width,bloque_height,True))
            
            bloque_x = bloque_x + bloque_width + 10
            
        filas.append(columnas)
        
        bloque_y = bloque_y + bloque_height + 10
        
    return filas
def colisionesBloques(xb,yb,bloques):
    x = 0
    
    colision = False
    
    while (x < len(bloques) and not colision):
        
        y = 0
        columna = bloques [x]
        
        while y < len(columna) and not colision:
            
            bloque = columna[y]
            
            bloque_x = bloque[0]
            bloque_y = bloque[1]
            bloque_width = bloque[2]
            bloque_height = bloque[3]
            bloque_visible = bloque[4]
            
            if(bloque_visible and bloque_x < xb < bloque_x  + bloque_width) and (bloque_y < yb < bloque_y + bloque_height):
                
                columna[y] = (bloque_x,bloque_y,bloque_width,bloque_height,False)
                
                colision = True
            y = y +1
        x = x + 1
    return colision
   
    
def pintarBloques(bloques):
    
    for x in range(0,5):
        for y in range(0,10):
            verBloque = bloques [x][y][4]
            
            if verBloque:
                bloque_x=bloques [x][y][0]
                bloque_y=bloques [x][y][1]
                bloque_width=bloques [x][y][2]
                bloque_height=bloques [x][y][3]
                
                pygame.draw.rect(screen, (129, 184, 255), (bloque_x, bloque_y, bloque_width, bloque_height))
                
def efectos(efectoPositivo,efectoNegativo,ball_radio,ball_width,rect_width):
    if(efectoPositivo==True):
        numero = random.randint(1,2)
        if(numero==1):
            rect_width=rect_width+5
        if(numero==2):
            ball_radio=ball_radio+3
            ball_width=ball_width+3
    if(efectoNegativo==True):
        numero = random.randint(1,2)
        if(numero==1):
            rect_width=rect_width-8
        if(numero==2):
            ball_radio=ball_radio-4
            ball_radio=ball_radio-4
    if(ball_radio<4):
        ball_radio=2
    if(rect_width<20):
        rect_width=20
    if(ball_radio>20):
        ball_radio=20
    if(rect_width>200):
        rect_width=200
    return ball_radio,rect_width
            
width = 720
height = 480
vidas = 3
# 3 formas de definir los colores
red = pygame.Color('Red')

cyan = pygame.Color('cyan')
blue = pygame.Color(0,0,255) # ¿alpha?
green = (0, 255, 0)
white = (255,255,255)
black = (0,0,0)
pygame.init() # Inicializa el entorno de pygame
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Numero de vidas')
# coordenadas del cuadrado
x = 284
y = height-20
# coordenadas de la pelota
xb = 284
yb = 120
# tamaño del rectángulo
rect_width = 90
rect_height = 20
# tamaño de la pelota
ball_width = 50
ball_radio = 10
# velocidad de movimiento
vel = 0.5
movx = 0.2
movy = 0.2
derecha = False
izquierda = False
efectoNegativo = False
efectoPositivo = False

numero = random.randint(0,1)

if (numero==0):
    izquierda = True
elif(numero==1):
    derecha = True
    
if(derecha==True):
        movx=movx
else:
        movx=-movx

running = True
bloques=generarBloques()
while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
    keyPressed = pygame.key.get_pressed()
        
    if keyPressed[pygame.K_q]: # salimos con la tecla q

        running = False        
    x=movimientoYColisionesRectangulo(x)    
    xb,yb,movx,movy,efectoNegativo=movimientoYColisionesPelota(xb,yb,movx,movy)
    if(yb >= y and xb>=x and xb <= x+rect_width):
        numero = random.randint(0,1)
        if (numero==0):
            izquierda = True
        elif(numero==1):
            derecha = True
        if(izquierda==True):
            movx=-movx
            movy=movy
            izquierda=False
        elif(derecha == True):
            movy=-movy
            movx=movx
            derecha=False
    if colisionesBloques(xb,yb,bloques):
        movy=-movy
        efectoPositivo = True
        
    ball_radio,rect_width=efectos(efectoPositivo,efectoNegativo,ball_radio,ball_width,rect_width)
        
    
        
    efectoNegativo = False
    efectoPositivo = False
    screen.fill(black) # ponemos el fondo negro
        
    # después dibujamos el rectángulo
    
    pygame.draw.rect(screen, (255, 0, 0), (x, y, rect_width, rect_height))
    pygame.draw.circle( screen,  (0,0,255), (xb,yb), ball_radio )
    pintarBloques(bloques)
    pygame.display.set_caption('numero de vidas ',str (vidas))
    pygame.display.flip() # actualizamos la pantalla
        
pygame.quit()