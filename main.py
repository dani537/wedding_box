import pygame
from pygame import mixer
import math
import pandas as pd
import RPi.GPIO as GPIO
import random
from datetime import datetime

import aux_mail

pygame.init()


########
# GPIO #
########

# 1 - Blanc
button_pin1 = 17
# 2 - Vermell
button_pin2 = 23
# 3 - Blau
button_pin3 = 24
# 4 - Verd
button_pin4 = 16
# 5 - Groc
button_pin5 = 26
# 9 - Start
button_pin9 = 14

def push1(ev=None):
	global button_input
	button_input = 1
def push2(ev=None):
	global button_input
	button_input = 2
def push3(ev=None):
	global button_input
	button_input = 3
def push4(ev=None):
	global button_input
	button_input = 4
def push5(ev=None):
	global button_input
	button_input = 5
def push9(ev=None):
	global button_input
	button_input = 9

GPIO.setmode(GPIO.BCM)

GPIO.setup(button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin9, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(button_pin1, GPIO.FALLING, callback=push1)
GPIO.add_event_detect(button_pin2, GPIO.FALLING, callback=push2)
GPIO.add_event_detect(button_pin3, GPIO.FALLING, callback=push3)
GPIO.add_event_detect(button_pin4, GPIO.FALLING, callback=push4)
GPIO.add_event_detect(button_pin5, GPIO.FALLING, callback=push5)
GPIO.add_event_detect(button_pin9, GPIO.FALLING, callback=push9)

##############
# PARÀMETRES #
##############

# Llegim csv dels inputs
df = pd.read_csv("codes.txt")
print(df)
# Creació de la pantalla
width = 1024 # 1024 
height = 600
#screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Background
background = pygame.image.load('image/background.png')

# Música
mixer.music.load(f"music/background_music{random.randint(1,9)}.mp3")
mixer.music.set_volume(0.8)
mixer.music.play(-1)

# Títol i icona
pygame.display.set_caption('Wedding Box')
icon = pygame.image.load('image/heart.png')
pygame.display.set_icon(icon)

# Icona block
enemy_img_0 = pygame.image.load('image/block_gris.png')
enemy_img_1 = pygame.image.load('image/block_blanc.png')
enemy_img_2 = pygame.image.load('image/block_vermell.png')
enemy_img_3 = pygame.image.load('image/block_blau.png')
enemy_img_4 = pygame.image.load('image/block_verd.png')
enemy_img_5 = pygame.image.load('image/block_groc.png')
enemy_img_list = [enemy_img_0, enemy_img_1, enemy_img_2, enemy_img_3, enemy_img_4, enemy_img_5] 

#enemyX = 400 #random.randint(0, 800)
enemyX = [50, 250, 450, 650, 850]
enemyY = 30 #random.randint(50, 200)

# Quadre pausa
quadre_img = pygame.image.load('image/success.png')
quadre_game_over_img = pygame.image.load('image/game_over.png')

ample_quadre = 900 # Fiquem mida d'ample de la imatge en pixels
alt_quadre = 500 # Fiquem mida d'alt de la imatge en pixels
quadreX = (width - ample_quadre) / 2
quadreY = (height - alt_quadre) / 2

# Icona jugador
player_img = pygame.image.load('image/spaceship.png')
playerX = 50
playerY = 450
playerX_change = 0

# Icona bala
bullet_img = pygame.image.load('image/bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 8 # velocitat bala
bullet_state = 'ready' # state: si és ready, no podem veure la bala, si és fire, farà el tret

# Font del text
font1 = pygame.font.Font('font/GamePlayed.ttf', 50)
font2 = pygame.font.Font('font/GamePlayed.ttf', 70)
font3 = pygame.font.Font('font/ArialRoundedBolt.ttf', 20)
font4 = pygame.font.Font('font/WheatSmile.ttf', 20)

# Posicions del text
text1_height = ((height - alt_quadre) / 2) + 30
text2_height = text1_height + 60
text3_height = text1_height + 125
text4_height = ((height - alt_quadre) / 2) + alt_quadre - 25

# Imatges dels jocs-taula
taula01_img = pygame.image.load('image/taules/01.png')
taula02_img = pygame.image.load('image/taules/02.png')
taula03_img = pygame.image.load('image/taules/03.png')
taula04_img = pygame.image.load('image/taules/04.png')
taula05_img = pygame.image.load('image/taules/05.png')
taula06_img = pygame.image.load('image/taules/06.png')
taula07_img = pygame.image.load('image/taules/07.png')
taula08_img = pygame.image.load('image/taules/08.png')
taula09_img = pygame.image.load('image/taules/09.png')
taula10_img = pygame.image.load('image/taules/10.png')

taules_img = [taula01_img, taula02_img, taula03_img, taula04_img, taula05_img,
			  taula06_img, taula07_img, taula08_img, taula09_img, taula10_img]

ample_taula = 600
alt_taula = 200
taulaX = (width - ample_taula) / 2
taulaY = ((height - alt_taula) / 2) + 20

score     = 0
loop_song = 0
send_mail = 0
color     = None
colors    = []
id_colors = []
str_id_colors = ''
id_taula = 0
success_game = False
input_raw = 0
start_state = True
finalitzar_song = False

############
# Funcions #
############

def player(x,y):
	screen.blit(player_img, (x, y))

def enemy(x,y, n, l_blocks):
	color = l_blocks[n]
	if color == 'gris':
		enemy_img = enemy_img_0
	elif color == 'blanc':
		enemy_img = enemy_img_1
	elif color == 'vermell':
		enemy_img = enemy_img_2
	elif color == 'blau':
		enemy_img = enemy_img_3
	elif color == 'verd':
		enemy_img = enemy_img_4
	elif color == 'groc':
		enemy_img = enemy_img_5

	screen.blit(enemy_img, (x, y))

def quadre(quadreX, quadreY, id_taula, taulaX, taulaY, success_game):
	if success_game == True:
		screen.blit(quadre_img, (quadreX, quadreY))
		screen.blit(taules_img[id_taula - 1], (taulaX, taulaY))
	else:
		screen.blit(quadre_game_over_img, (quadreX, quadreY))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bullet_img, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
	if distance < 50:
		return True
	else:
		return False

def text(nom, salutacio, salutacio2, musica):

	text1 = font1.render(salutacio, True, (255, 255, 255))
	text1_rect = text1.get_rect(center=(width/2, text1_height))
	screen.blit(text1, text1_rect)

	text2 = font2.render(nom, True, (240, 116, 228))
	text2_rect = text2.get_rect(center=(width/2, text2_height))
	screen.blit(text2, text2_rect)

	text3 = font3.render(salutacio2, True, (255, 255, 255))
	text3_rect = text3.get_rect(center=(width/2, text3_height))
	screen.blit(text3, text3_rect)

	text4 = font4.render(musica, True, (255, 255, 255))
	text4_rect = text4.get_rect(center=(width/2, text4_height))
	screen.blit(text4, text4_rect)


########
# Loop #
########

# Game Loop
running = True
while running:
	#Variable input polsador
	if input_raw != 0:
		if finalitzar_song == True:
			button_input = 9
			input_raw = 0
			finalitzar_song = False
		else:
			button_input = input
			input_raw = 0
	else:
		button_input = input_raw

	#RGB
	screen.fill((255, 222, 239))
	#Background
	screen.blit(background, (0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# 1-BLANC
	if button_input == 1:
		if bullet_state == 'ready':
			bulletX = playerX
			fire_bullet(bulletX, bulletY)
			color = 'blanc'
			id_color = 1
			bulletSound = mixer.Sound("music/laser.wav")
			bulletSound.play()
	# 2-VERMELL
	if button_input == 2:
		if bullet_state == 'ready':	
			bulletX = playerX
			fire_bullet(bulletX, bulletY)
			color = 'vermell'
			id_color = 2
			bulletSound = mixer.Sound("music/laser.wav")
			bulletSound.play()
	# 3-BLAU
	if button_input == 3:
		if bullet_state == 'ready':	
			bulletX = playerX
			fire_bullet(bulletX, bulletY)
			color = 'blau'
			id_color = 3
			bulletSound = mixer.Sound("music/laser.wav")
			bulletSound.play()
	# 4-VERD
	if button_input == 4:
		if bullet_state == 'ready':	
			bulletX = playerX
			fire_bullet(bulletX, bulletY)
			color = 'verd'
			id_color = 4
			bulletSound = mixer.Sound("music/laser.wav")
			bulletSound.play()
	# 5-GROC
	if button_input == 5:
		if bullet_state == 'ready':	
			bulletX = playerX
			fire_bullet(bulletX, bulletY)
			color = 'groc'
			id_color = 5
			bulletSound = mixer.Sound("music/laser.wav")
			bulletSound.play()
	# 9-START
	if button_input == 9 and start_state == True:
		start_state = False
		click_moment = int(datetime.now().strftime("%H%M%S"))
		score = 0
		loop_song = 0
		send_mail = 0
		colors = []
		id_colors = []
		str_id_colors = ''
		mixer.music.unload()
		mixer.music.load(f"music/background_music{random.randint(1,9)}.mp3")
		mixer.music.set_volume(0.8)
		mixer.music.play(-1)

	# Col·lissió
	for n_enemyX in enemyX:
		collision = isCollision(n_enemyX, enemyY, bulletX, bulletY)
		if collision:
			explosionSound = mixer.Sound("music/explosion.wav")
			explosionSound.play()
			bulletY = playerY
			bullet_state = "ready"
			score+=1

			# Fem lògica dels blocks
			colors.append(color)
			id_colors.append(id_color)
			str_id_colors = str(str_id_colors) + str(id_color)
			#if score < 5:
			#	l_blocks = colors

	# Movimient de la bala
	if bulletY <= 0:
		bulletY = playerY
		bullet_state = 'ready'
	if bullet_state == 'fire':
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change
	
	# Estat del botó START
	if start_state == False:
		click_now = int(datetime.now().strftime("%H%M%S"))
		if (click_now - click_moment) > 2:
			start_state = True

	# Fixem la posició de la nau en funció de la puntuació
	if score < 5:
		playerX = enemyX[score]
	else:
		playerX = enemyX[4]

	# Introduïm dades per la nau espacial
	player(playerX, playerY)

	# Fem llista de blocks a carregar
	l_blocks = []
	while (len(colors) + len(l_blocks)) < 5:
		l_blocks.append('gris')
	l_blocks = colors + l_blocks

	# Introduïm dades pels blocks
	n = 0
	for n_enemyX in enemyX:
		enemy(n_enemyX, enemyY, n, l_blocks)
		n+=1

	# A partir d'score 5 fiquem el quadre de text
	if score >= 5:
		if loop_song == 0:
			try:
				success_game = True
				nom         = df.loc[df['codi'] == int(str_id_colors)]['nom'].reset_index(drop=True)[0]
				musica      = df.loc[df['codi'] == int(str_id_colors)]['musica'].reset_index(drop=True)[0]
				url_musica  = df.loc[df['codi'] == int(str_id_colors)]['url_musica'].reset_index(drop=True)[0]
				id_taula    = df.loc[df['codi'] == int(str_id_colors)]['id_taula'].reset_index(drop=True)[0]
				salutacio   = df.loc[df['codi'] == int(str_id_colors)]['salutacio'].reset_index(drop=True)[0]
				salutacio2  = df.loc[df['codi'] == int(str_id_colors)]['salutacio2'].reset_index(drop=True)[0]
				mail        = df.loc[df['codi'] == int(str_id_colors)]['mail'].reset_index(drop=True)[0]
				idioma      = df.loc[df['codi'] == int(str_id_colors)]['idioma'].reset_index(drop=True)[0]
				seconds     = df.loc[df['codi'] == int(str_id_colors)]['mp3_seconds'].reset_index(drop=True)[0]
				song_loops  = 1
			except:
				success_game = False
				url_musica   = 'game_over'
				seconds      = 10
				song_loops   = 1

			pygame.mixer.music.unload()
			pygame.mixer.music.load(f"music/songs/{url_musica}.mp3")
			pygame.mixer.music.set_volume(1)
			pygame.mixer.music.play(loops=song_loops)
			inici_song  = datetime.now()
			
			
			loop_song+=1

		now_song = datetime.now()
		delta_song = now_song - inici_song
		if (delta_song.total_seconds()) > seconds:
			input_raw = 9
			finalitzar_song = True
			
		quadre(quadreX, quadreY, id_taula, taulaX, taulaY, success_game)
		if success_game == True:
			text(nom, salutacio, salutacio2, musica)
	
	pygame.display.update()

	# Si s'ha encertat la combinació, s'enviarà un correu electrònic d'avís
	if (send_mail == 0) and (success_game == True) and (score >= 5):
		try:
			aux_mail.enviament_mail(mail, nom, salutacio, idioma, id_taula)
		except:
			print("Mail no enviat")
			pass
		send_mail+=1
