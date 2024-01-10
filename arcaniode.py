import pygame,random
import time


BLACK = (0,0,0)
WHITE = (255,255,255)
ANCHO_PANTALLA = 700 
LARGO_PANTALLA = 900 



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((LARGO_PANTALLA, ANCHO_PANTALLA))
clock = pygame.time.Clock()
running = True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
pygame.display.set_caption("ARKANOID")                                          
font = pygame.font.Font(None, 36)

imagen_presentacion = pygame.transform.scale(pygame.image.load("img/arkanoid.png").convert(),(650,600))
imagen_gameover = pygame.transform.scale(pygame.image.load("img/gameover.png").convert(),(750,600))
imagen_ganaste = pygame.transform.scale(pygame.image.load("img/ganaste.png").convert(),(750,600))

#PADRES
class PowerUp(pygame.sprite.Sprite):

    def __init__(self,imagen,x,y,nombre): 
        super().__init__()   
        self.image = pygame.transform.scale(pygame.image.load(imagen).convert(),(x,y))
        self.rect = self.image.get_rect()          
        self.image.set_colorkey(WHITE)
        self.speed_y  = 15
        self.nombre = nombre      

    def posicionarPowerUp(self,x,y):
        self.rect.x = x
        self.rect.y = y
     

    def efecto(self,objeto):
         pass
    
    def moverPowerUp(self):
        self.rect.y += 2 

class Bloque(pygame.sprite.Sprite):  
    def __init__(self,fuerza,image):
        super().__init__()      
        self.fuerza = fuerza
        self.image = pygame.transform.scale(pygame.image.load(image).convert(),(50,20))
        self.rect = self.image.get_rect()        
  
class Pelota(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0):
         super().__init__()         
         self.velocidadx = 0
         self.velocidady = 0         
         self.image = pygame.transform.scale(pygame.image.load("img/pelota.png").convert(),(25,25))
         self.image.set_colorkey(BLACK)
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y

    def cambiarvelocidad(self,vX,vY):        
        self.velocidadx = vX
        self.velocidady = vY  
       
    def mover(self):
               
        self.rect.x += self.velocidadx
        self.rect.y += self.velocidady
          
class Paleta(pygame.sprite.Sprite):
    def __init__(self,imagen,x,y,px=0,py=0):  
        super().__init__()   
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.image = pygame.transform.scale(pygame.image.load(imagen).convert(),(x,y))
        self.image.set_colorkey(WHITE)        
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py 
        #Agregamos lista de Pelotas
        self.lista_pelotas = []      
        
    
    def cambiarvelocidad2(self,x):
       
        self.velocidad_x = x  
    
    def actualizarmovimientoDerecha(self):
        self.rect.x += self.velocidad_x
        juego.paleta_juego.rect.y = 620   # corresponde_juego.paleta 
    
    def actualizarmovimientoIzquierda(self):
        self.rect.x += -1*self.velocidad_x
        juego.paleta_juego.rect.y = 620   # corresponde_juego.paleta    
    
    def cambiarPaleta(self,imagen,x,y):
         self.image = pygame.transform.scale(pygame.image.load(imagen).convert(),(x,y))
         self.image.set_colorkey(WHITE)
    def generar_pelota(self,objeto=None):
        if objeto:
            self.lista_pelotas.append(objeto)          
            return objeto
        else:
            p = Pelota(self.rect.centerx-12,self.rect.centery-30)
            self.lista_pelotas.append(p)
            return p
    def tecla_especial(self,objeto):
        pass

class Paredes(pygame.sprite.Sprite):

    def __init__(self,imagen,x,y,px=0,py=0):
        super().__init__()                       
        self.image = pygame.transform.scale(pygame.image.load(imagen),(x,y))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK) 
        self.rect.x = px        
        self.rect.y = py


#HIJOS
class Laser(Pelota):
    def __init__(self, x=0 , y=0): #modifique los __ de ambos init, estaban con 1
        #self.rect.centerx,self.rect.centery
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("img/laser_tiros.png").convert(),(5,10))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.velocidady = 5

    def mover(self):
       
        self.rect.y -= self.velocidady
       
    


class PaletaLaser(Paleta):
    #depende los parametros que le enviemos cuando lo invocamos entra al init correspondiente
    def __init__(self, imagen,x,y,px=0,py=0):    
        #Inicializar los atributos de la clase padre
        super().__init__("img/nave_misil.png",x,y,px,py)
        #Inicializo los atributos propios de la clase PaletaLaser
    
    def __init__(self, objeto):    
        #Inicializar los atributos de la clase padre
        super().__init__("img/nave_misil.png", objeto.rect.width,objeto.rect.height,objeto.rect.x,objeto.rect.y)
        self.lista_pelotas = objeto.lista_pelotas.copy()
        self.velocidad_x = 90
   

    def tecla_especial(self, objeto):          
        laser = Laser(self.rect.centerx  - 12, self.rect.centery - 30)
        self.lista_pelotas.append(laser)
        objeto.all_sprites_list.add(laser)
      

class PowerUpLaser(PowerUp):       
        def __init__(self):
            super().__init__("img/laser.png",40,20,"laser")          
         
      
        #modifique el efecto  
        def efecto(self, objeto):
            paleta_laser = PaletaLaser(objeto.paleta_juego)
            objeto.all_sprites_list.remove(objeto.paleta_juego)
            objeto.paleta_juego = paleta_laser
            objeto.all_sprites_list.add(paleta_laser)                    
    
class PowerUpReducir(PowerUp):
        def __init__(self):
          super().__init__("img/reducir.png",40,20,"reducir")

        def efecto(self,objeto):
            objeto = objeto.paleta_juego 
            objeto.image = pygame.transform.scale(pygame.image.load("img/nave_corta.png").convert(),(40,20))
            objeto.image.set_colorkey(WHITE)
            aux_x = objeto.rect.x
            aux_y = objeto.rect.y 
            objeto.rect = objeto.image.get_rect() 
            objeto.rect.x = aux_x
            objeto.rect.y = aux_y
            
              
class PowerUpExpandir(PowerUp):
    def __init__(self):
          super().__init__("img/expandir.png",40,20,"expandir")
    
    def efecto(self,objeto):                   
            objeto = objeto.paleta_juego
            objeto.image = pygame.transform.scale(pygame.image.load("img/nave_larga.png").convert(),(200,20))
            objeto.image.set_colorkey(WHITE)
            aux_x = objeto.rect.x
            aux_y = objeto.rect.y 
            objeto.rect = objeto.image.get_rect() 
            objeto.rect.x = aux_x
            objeto.rect.y = aux_y
            


class PowerUpMultiball(PowerUp):
    def __init__(self):
          super().__init__("img/multiball.png",40,20,"multiball")   

    def efecto(self,objeto):
           objeto = objeto.paleta_juego
           direcciones = [(-1,1),(1,1),(0,1),(1,-1),(-1,-1),(0,-1)]
           cantidad = len(objeto.lista_pelotas)
           for i in range(3-cantidad):
                nx = objeto.lista_pelotas[0].rect.centerx
                ny = objeto.lista_pelotas[0].rect.centery
                sx,sy=random.choice(direcciones)
             
                vx = objeto.lista_pelotas[0].velocidadx*sx
                vy = objeto.lista_pelotas[0].velocidady*sy
             
                p = Pelota(nx,ny)
                p.velocidadx=vx
                p.velocidady=vy

                objeto.lista_pelotas.append(p)                             
                juego.all_sprites_list.add(p) 

class PowerUpAumentarVelocidad(PowerUp):
        def __init__(self):
          super().__init__("img/rapido.png",40,20,"aumentar_velocidad")   
      
         
        def efecto(self,objeto):
            objeto = objeto.paleta_juego            
            objeto.velocidad_x= 150
            
class PowerUpReducirVelocidad(PowerUp):
        def __init__(self):
          super().__init__("img/lento.png",40,20,"reducir_velocidad")   
         
            
        def efecto(self,objeto=None):         
            objeto = objeto.paleta_juego
            objeto.velocidad_x= 20

class PowerUpReducirVida(PowerUp):
        def __init__(self):
          super().__init__("img/restavida.png",40,20,"resta_vida") 

        #pasar la clase juego que contiene las vidas
        def efecto(self,objeto):
             objeto.vidas -= 1
             
class PowerUpAumentarVidas(PowerUp):
        def __init__(self):
          super().__init__("img/sumavida.png",40,20,"aumenta_vida") 
        
        def efecto(self,objeto):
             objeto.vidas += 1


class Juego:


    def __init__(self,x,y,puntos,vidas):
        self.x = x
        self.y = y
        self.puntos = puntos
        self.vidas = vidas
        self.pared_superior  =  Paredes("img/pared_superior_.png",900,20,0,0) 
        self.pared_izquierda = Paredes("img/pared_izquierda_.png",28,670,0,19) 
        self.pared_derecha   = Paredes("img/pared_derecha_.png",28,670,871,19)
        self.paleta_juego    = Paleta("img/nave2.png",100,20,400,620)         
        self.sprite_seleccionado = None
        

        
        #Generan los Sprites
        #Todos los Sprites
        self.all_sprites_list = pygame.sprite.Group()
        #Sprites de los Bloques
        self.bloque_listaSprite = pygame.sprite.Group()
        #Sprites de las paredes
        self.paredes_listaSprite = pygame.sprite.Group()
        #power ups
        self.bloque_PowerUps = pygame.sprite.Group()

        #PAREDES
        self.all_sprites_list.add(self.pared_superior)
        self.all_sprites_list.add(self.pared_izquierda)
        self.all_sprites_list.add(self.pared_derecha)
        self.paredes_listaSprite.add(self.pared_superior)
        self.paredes_listaSprite.add(self.pared_izquierda)  
        self.paredes_listaSprite.add(self.pared_derecha)  

        #PALETA
        self.all_sprites_list.add(self.paleta_juego)

        #PELOTA
        self.pelota = self.paleta_juego.generar_pelota() #esta bien llamar al objeto aca 
        self.all_sprites_list.add(self.pelota)
   
    def finJuego(self):
        pygame.quit()
         
         
    def actualizarVidas(self):
         self.vidas -=1
         return self.vidas   
           
    def actualizarPuntaje(self,puntaje):
        self.puntos += puntaje 

    def posicionamientodeBlocks(self):
        INICIO_X=100
        INICIO_Y=100
        SEPARACION_X=5
        SEPARACION_Y=21   
        
        
        lista_colores = ["img/bloque_amarillo.png","img/bloque_azul.png","img/bloque_gris.png", "img/bloque_naranja.png","img/bloque_rojo.png","img/bloque_verde.png","img/bloque_violeta.png"]
        lista_puntajes =[2,3,5,4,10,1,6]

        for j in range(7):       
            for i in range (13):
                    bloque = Bloque(lista_puntajes[j],lista_colores[j])                
                    bloque.rect.x =  INICIO_X+i*(bloque.rect.width + SEPARACION_X)
                    bloque.rect.y = INICIO_Y+SEPARACION_Y*(j+1)
                    juego.bloque_listaSprite.add(bloque)  
                    juego.all_sprites_list.add(bloque)
                
    def textoFinal(self):
        texto_presentacion = font.render("<<< Presione enter para volver a jugar o esc para salir >>>", True, (255, 255, 255))
        texto_presentacion_rect = texto_presentacion.get_rect()
        texto_presentacion_rect.topleft = (100, 550)      
        screen.blit(texto_presentacion, texto_presentacion_rect)

    #Juego ganado
    def juego_ganado_presentacion(self):
        screen.fill(BLACK)
        texto_ganaste = font.render("<<< FELICITACIONES - GANASTE  >>>", True, WHITE)
        texto_rect = texto_ganaste.get_rect()    
        texto_rect.topleft =  (200, 650)
        screen.blit(imagen_ganaste, (75, 20))
        screen.blit(texto_ganaste, texto_rect)
        pygame.display.flip()

#instancia de los objetos      
juego = Juego(ANCHO_PANTALLA,LARGO_PANTALLA,0,3)
#inicializar variables
vidas = 3
puntos = 0
text_font = pygame.font.SysFont("Arial",30)
MOVIMIENTO = 90 



#Booleano 
pelota_moverInicial = False #activar movimeinto pelota 
primer_lanzamiento_pelota = False #para que s emueva la pelota con la paleta 
soundgameover=False
sound_presentacion=False
juegoIniciado=True
random_sprite = False
#chequeo si la pelota se encuentra en la zona de juego
pelota_existe = True
powerup_laser_activo = False
#bandera para que no se rompa cuando esta en el game over y se precione por error el espacio 
activa_gameOver = False
#presentacion Ganaste
juego_ganado = False

sound_ganaste_ = True
gameover = True


#sonidos
sound_ball = pygame.mixer.Sound("mp3/laser5.ogg.opus")
sound_gameover = pygame.mixer.Sound("mp3/gameover.mp3")
sound_gameover2 = pygame.mixer.Sound("mp3/gameover1.mp3")
sound_presentacion = pygame.mixer.Sound("mp3/arkanoid.mp3")
sound_ganaste = pygame.mixer.Sound("mp3/audio_ganaste.wav")
sound_perdervida = pygame.mixer.Sound("mp3/tntt.ogg.opus")
sound_perdervida2 = pygame.mixer.Sound("mp3/SnapSave.ogg.opus")

#BLOQUES
juego.posicionamientodeBlocks()


#imagen
screen.blit(imagen_presentacion, (100, 20))
sound_presentacion.play()


#txt
texto = font.render("Presione espacio para iniciar partida", True, (255, 255, 255))
text_rect = texto.get_rect()
text_rect.center = (400,600)
screen.blit(texto, text_rect)


pygame.display.flip()
tiempo_inicial = time.time()
espera = True





#While para la presentacion. 
while espera:
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            espera = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                espera = False
                sound_presentacion.stop()
            tiempo_actual = time.time()
            if tiempo_actual - tiempo_inicial >= 20:
                espera = False
                sound_presentacion.stop()


#inicializo la velocidad de la paleta 
juego.paleta_juego.cambiarvelocidad2(MOVIMIENTO)

#bucle del juego  
while running: 
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
           
            #EVENTOS TECLADO        
            if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_LEFT and activa_gameOver==False:  #tecla FLECHA IZQUIERDA                    
                        juego.paleta_juego.actualizarmovimientoIzquierda() 
                        if not pelota_moverInicial: #se incorporo el booleano para que solamente 
                            #la pelota se mueva con la paleta cuando no se haya tocado el space
                            juego.pelota.rect.x = juego.paleta_juego.rect.centerx-10
                            if pelota_existe == False: #Mueve la pelota junto a la paleta en el primer lanzamiento despues de morir
                                p.rect.x = juego.paleta_juego.rect.centerx-10 

                    elif event.key == pygame.K_RIGHT and activa_gameOver==False:  #tecla FLECHA DERECHA  
                        juego.paleta_juego.actualizarmovimientoDerecha()                            
                        if not pelota_moverInicial:
                            juego.pelota.rect.x = juego.paleta_juego.rect.centerx-10
                            if pelota_existe == False: #Mueve la pelota junto a la paleta en el primer lanzamiento despues de morir
                                p.rect.x = juego.paleta_juego.rect.centerx-10 

                    elif event.key == pygame.K_SPACE and juegoIniciado and activa_gameOver==False:                            
                            juego.pelota.cambiarvelocidad(5,-5)
                            if pelota_existe == False:                                
                                p.cambiarvelocidad(5,-5)  
                            primer_lanzamiento_pelota = True  #para que se mueva la pelota con la paleta    
                            pelota_moverInicial = True                                   
                            juegoIniciado=False
                            gameover=True                     
                            sound_ganaste_ = True
                    
                    elif event.key == pygame.K_SPACE and activa_gameOver==False:                   
                        juego.paleta_juego.tecla_especial(juego)                         
                        primer_lanzamiento_pelota = True  #para que se mueva la pelota con la paleta    
                        pelota_moverInicial = True                                   
                        juegoIniciado=False
                    elif event.key == pygame.K_ESCAPE:
                         juego.finJuego()
                    elif event.key == pygame.K_RETURN: 
                        activa_gameOver=False                               
                        juego = Juego(ANCHO_PANTALLA,LARGO_PANTALLA,0,3)  
                        juego.posicionamientodeBlocks()                                                    
                        juego.paleta_juego.cambiarvelocidad2(MOVIMIENTO)
                        running = True
                        #a la segunda vez que perdes tira un error en la linea 611 moverpowerup
                        

                           
              

    #limites con las paredes  
    if juego.paleta_juego.rect.x > ((LARGO_PANTALLA - (juego.pared_derecha.rect.width)) - juego.paleta_juego.rect.width):
        juego.paleta_juego.rect.x = (LARGO_PANTALLA - (juego.pared_derecha.rect.width)) - juego.paleta_juego.rect.width
        if pelota_moverInicial == False:
            juego.pelota.rect.x = juego.paleta_juego.rect.centerx 
            if pelota_existe == False:
                p.rect.x = juego.paleta_juego.rect.centerx 
    if juego.paleta_juego.rect.x < juego.pared_izquierda.rect.x:
        juego.paleta_juego.rect.x = juego.pared_izquierda.rect.width
        if pelota_moverInicial == False:
            juego.pelota.rect.x = juego.paleta_juego.rect.centerx 
            if pelota_existe == False:
                p.rect.x = juego.paleta_juego.rect.centerx 

    # Bucle del juego    
    if pelota_moverInicial:   
        # Actualizar la posición de la pelota
        for pelota in juego.paleta_juego.lista_pelotas:
                pelota.mover()                   
                prueba=juego.paleta_juego.lista_pelotas
                if pelota.rect.colliderect(juego.pared_superior.rect): 
                    pelota.velocidady *= -1            
                if pelota.rect.colliderect(juego.pared_izquierda.rect):  
                    pelota.velocidadx *= -1
                    pelota.velocidady *= 1   
                if pelota.rect.colliderect(juego.pared_derecha.rect): 
                    pelota.velocidadx *= -1
                    pelota.velocidady *= 1                
                if pelota.rect.colliderect(juego.paleta_juego.rect): 
                    pelota.velocidadx *= 1
                    pelota.velocidady *= -1                    
                if pelota.rect.y > 750 and soundgameover==False:
                       
                     #elimino objeto pelota
                    if len(juego.paleta_juego.lista_pelotas)>1:                                
                                if type(juego.paleta_juego.lista_pelotas[1]) == Laser:                                           
                                        juego.all_sprites_list.remove(juego.paleta_juego.lista_pelotas[0:])
                                        tam_paleta_lista = len(juego.paleta_juego.lista_pelotas)                                 
                                        for x in range (tam_paleta_lista):                                             
                                            juego.paleta_juego.lista_pelotas.remove(juego.paleta_juego.lista_pelotas[0])
                                else: #soy multiball
                                     pelota.kill()
                                     juego.paleta_juego.lista_pelotas.remove(pelota)                                       
                    else:
                        pelota.kill()
                        juego.paleta_juego.lista_pelotas.remove(pelota)
                   
                    
                    
                    if len(juego.paleta_juego.lista_pelotas)==0:    
                        if juego.vidas > 0:
                            random_sound = random.randint(0,2)
                            if random_sound==1:
                                sound_perdervida.play()
                                sound_perdervida.set_volume(0.3)
                            elif random_sound==0 or random_sound==2:
                                sound_perdervida2.play() 
                                sound_perdervida2.set_volume(0.3)                                                    
                            juego.actualizarVidas()
                            juego.paleta_juego.kill() 
                            juego.paleta_juego = Paleta("img/nave2.png",100,20,400,620)                           
                            juego.all_sprites_list.add(juego.paleta_juego)                             
                            p = juego.paleta_juego.generar_pelota()                            
                            juego.all_sprites_list.add(p)                                                      
                            if random_sprite:
                                juego.sprite_seleccionado.kill()
                            pelota_existe = False
                            primer_lanzamiento_pelota = False   
                            juegoIniciado=True                             
                            juego.paleta_juego.cambiarvelocidad2(MOVIMIENTO)
                            pelota_moverInicial = False #se coloca porque cuando se pierde la vida sigue entrando al mover de la Pelota
                        else:
                            sound_gameover.play()
                            soundgameover=True 
                            juegoIniciado=True
                            pelota_moverInicial = False
                                    
                #Colisiones con los bloques
                colls = pygame.sprite.spritecollide(pelota, juego.bloque_listaSprite,True)       
                if colls != []:
                    for bloque in colls:                  
                        bloque.remove()
                        sound_ball.play()
                        fuerzaBloque = bloque.fuerza                                  
                        juego.actualizarPuntaje(fuerzaBloque)
                        random_powerup = random.randint(1,8) #si es True, es el valor de la derecha
                                                
                        if random_powerup == 1 and random_sprite==False:
                            random_sprite = True                            
                            juego.sprite_seleccionado = PowerUpExpandir()           
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY) 
                            juego.all_sprites_list.add(juego.sprite_seleccionado)
                            
                        if random_powerup == 2 and random_sprite==False:
                            random_sprite = True                            
                            juego.sprite_seleccionado = PowerUpReducir()        
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY) 
                            juego.all_sprites_list.add(juego.sprite_seleccionado)                               
                        if random_powerup == 3 and random_sprite==False:
                            random_sprite = True                            
                            if len(juego.paleta_juego.lista_pelotas) == 1:
                                juego.sprite_seleccionado = PowerUpMultiball()        
                                posicionX = bloque.rect.x                    
                                posicionY = bloque.rect.y                                                
                                juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY) 
                                juego.all_sprites_list.add(juego.sprite_seleccionado)                           
                        if random_powerup == 4 and random_sprite==False:
                            random_sprite = True                           
                            juego.sprite_seleccionado = PowerUpReducirVelocidad()        
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY) 
                            juego.all_sprites_list.add(juego.sprite_seleccionado) 
                        if random_powerup == 5 and random_sprite==False:
                            random_sprite = True                             
                            juego.sprite_seleccionado = PowerUpAumentarVelocidad()       
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY)  
                            juego.all_sprites_list.add(juego.sprite_seleccionado)
                        if random_powerup == 6 and random_sprite==False:
                            random_sprite = True                            
                            juego.sprite_seleccionado = PowerUpAumentarVidas()        
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY)  
                            juego.all_sprites_list.add(juego.sprite_seleccionado)
                        if random_powerup == 7 and random_sprite==False:
                            random_sprite = True                             
                            juego.sprite_seleccionado = PowerUpReducirVida()        
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY)
                            juego.all_sprites_list.add(juego.sprite_seleccionado)
                        if random_powerup == 8 and random_sprite==False:
                            random_sprite = True                             
                            juego.sprite_seleccionado = PowerUpLaser()        
                            posicionX = bloque.rect.x                    
                            posicionY = bloque.rect.y                     
                            juego.sprite_seleccionado.posicionarPowerUp(posicionX,posicionY)
                            juego.all_sprites_list.add(juego.sprite_seleccionado)                          
                          
                                                                               
                        pelota.velocidady *= -1                      
                        rand = random.randint(0,1)
                        if rand:
                            pelota.velocidadx *= -1 

                        
                        if len(juego.bloque_listaSprite) == 0:
                            juego_ganado = True           
               
                #actualiza los sprits
                juego.all_sprites_list.update() 
                

                

        #choco a un bloque y sale un power up 
        if random_sprite:            
            juego.sprite_seleccionado.moverPowerUp()
            if juego.paleta_juego.rect.colliderect(juego.sprite_seleccionado.rect): 
                        if len(juego.paleta_juego.lista_pelotas)>1: #laser o multiball
                            juego.all_sprites_list.remove(juego.paleta_juego.lista_pelotas[1:])
                            tam_paleta_lista = len(juego.paleta_juego.lista_pelotas)
                            print( tam_paleta_lista )                                     
                            for x in range (tam_paleta_lista-1):
                                if type(juego.paleta_juego.lista_pelotas[1]) == Laser:                                                                            
                                    juego.paleta_juego.lista_pelotas.remove(juego.paleta_juego.lista_pelotas[1])
                                elif type(juego.paleta_juego.lista_pelotas[1]) == Pelota: 
                                    juego.paleta_juego.lista_pelotas.remove(juego.paleta_juego.lista_pelotas[1])                                         
                        paleta_actual = juego.paleta_juego.lista_pelotas.copy() #hace copia de lista de pelotas                                           
                        paleta_actual_x = juego.paleta_juego.rect.x #hace copia de posicionX
                        juego.paleta_juego.kill() 
                        juego.paleta_juego = Paleta("img/nave2.png",100,20,400,620)
                        juego.paleta_juego.rect.x = paleta_actual_x   #vuelve asignar valores PosicionX
                        juego.paleta_juego.lista_pelotas = paleta_actual #vuelve asignar valores lista pelota                       
                        juego.paleta_juego.cambiarvelocidad2(MOVIMIENTO)                       
                        juego.all_sprites_list.add(juego.paleta_juego)                                                                            
                        juego.sprite_seleccionado.efecto(juego)                       
                        juego.all_sprites_list.update() #se agrego para que actualice la lista                                    
                        juego.sprite_seleccionado.kill()
                        random_sprite = False                    
                               
            elif juego.sprite_seleccionado.rect.y > 750:                    
                    juego.sprite_seleccionado.kill()
                    random_sprite = False 
    
    screen.fill(BLACK)
    
    for pelota in juego.paleta_juego.lista_pelotas:
        if isinstance(pelota, Laser):
            if pelota.rect.colliderect(bloque.rect):
                juego.paleta_juego.lista_pelotas.remove(pelota)
                juego.all_sprites_list.remove(pelota)
            elif pelota.rect.colliderect (juego.pared_superior.rect):
                juego.paleta_juego.lista_pelotas.remove(pelota)
                juego.all_sprites_list.remove(pelota)
    juego.all_sprites_list.draw(screen)    

     
        
    #dibujo textos en pantalla
    texto_puntaje = font.render("Puntaje: {}".format(juego.puntos), True, (255, 255, 255))    
    texto_rect = texto_puntaje.get_rect()
    texto_rect.topleft = (700, 650)
    texto_vidas = font.render("Vidas: {}".format(juego.vidas), True, (255, 255, 255))
    texto_vidas_rect = texto_vidas.get_rect()
    texto_vidas_rect.topleft = (50, 650)
    screen.blit(texto_puntaje, texto_rect) 
    screen.blit(texto_vidas, texto_vidas_rect) 

    if juego_ganado:
        juego.juego_ganado_presentacion()       
        sound_ball.stop() 
        sound_perdervida.stop()
        sound_perdervida2.stop()
        activa_gameOver = True
        if sound_ganaste_ :            
            sound_ganaste_ = False
            sound_ganaste.play() 
            sound_ganaste.set_volume(0.1) 

       
        
    if juego.vidas == 0 :       
        screen.blit(imagen_gameover, (75, 20))
        juego.paleta_juego.kill()
        juego.sprite_seleccionado.kill()
        random_sprite = False
        juego.all_sprites_list.empty()       
        texto_presentacion = font.render("<<< Presione enter para volver a jugar o esc para salir >>>", True, (255, 255, 255))
        texto_presentacion_rect = texto_presentacion.get_rect()
        texto_presentacion_rect.topleft = (100, 550)      
        screen.blit(texto_presentacion, texto_presentacion_rect)
        
        if gameover == True:
            sound_gameover.play()         
            gameover=False
    
        
    

    # Actualiza pantalla -  the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.   
    clock.tick(60)

