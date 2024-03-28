import pygame
import random

pygame.init()
#RGB color stuff
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
LIGHT_GREEN = (75,255,75)
RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (200,200,200)
obj_ls = []
obstacles = []

WIDTH, HEIGHT = 450, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Rossy Croad")

img = pygame.image.load('chicken.jpg')
img = pygame.transform.scale(img, (40,40))

clock = pygame.time.Clock() 
FPS = 60

class Row:
	def __init__(self,posy,color):
		self.posy = posy
		self.posx = -200
		self.color = color
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
	
	def update(self,yFac,xFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		if self.posx < -400:
			self.posx = -400
		if self.posx > 0:
			self.posx
		self.Rect = pygame.Rect(0, self.posy, WIDTH, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

class Road():
	def __init__(self, posy, val):
		self.posy = posy
		self.posx = -200
		self.color = BLACK
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(0, self.posy, WIDTH, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

class Field():
	def __init__(self, posy, val):
		self.tree_ls = []
		self.posy = posy
		self.posx = -200 + val*50
		self.color = LIGHT_GREEN
		for x in range(3):
			rand_val = random.randint(-200,WIDTH+350)
			self.tree_ls.append(Tree(rand_val - rand_val%50,self.posy))

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.tree_ls)):
			self.tree_ls[x].update(xFac,yFac)


class Tree():
	def __init__(self,posx,posy):
		self.posx = posx
		self.posy = posy
		self.Rect = pygame.Rect(self.posx, self.posy, 50, 50)

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, 50, 50)
		self.drawn = pygame.draw.rect(screen, GREEN, self.Rect)
		

class Water():
	def __init__(self, posy, val):
		self.posy = posy
		self.posx = -200 + val*50
		self.color = BLUE
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

class Tracks():
	def __init__(self, posy, val):
		self.posy = posy
		self.posx = -200 + val*50
		self.color = GRAY
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)


def main():
	#setup
	running = True
	start = True
	class_options = [Road,Field,Field,Field,Road,Water,Tracks]
	player = pygame.Rect((WIDTH//2)-20,HEIGHT-45,40,40)
	total_left_right = 0

	#main loop
	while running:
		if start:
			while start and running:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
					if event.type == pygame.KEYDOWN:
						start = False
		xFac,yFac=0,0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					yFac += 1
				if event.key == pygame.K_DOWN:
					yFac -= 1
				if event.key == pygame.K_LEFT:
					total_left_right += 1
					xFac += 1
				if event.key == pygame.K_RIGHT:
					total_left_right -= 1
					xFac -= 1
		if total_left_right == -5:
			total_left_right = -4
			xFac += 1
		elif total_left_right == 5:
			total_left_right = 4
			xFac -= 1
		y_ls = []
		for x in range(len(obj_ls)):
			y_ls.append(obj_ls[x].posy)

		for x in range(0,HEIGHT-50,50):
			if x not in y_ls:
				obj_ls.append(random.choice(class_options)(x,total_left_right))
		
		for x in range(len(obj_ls)):
			obj_ls[x].update(xFac,yFac)
		
		player_drawn = pygame.draw.rect(screen,WHITE,player)
		screen.blit(img,((WIDTH//2)-20,HEIGHT-45))
		pygame.display.update()
		clock.tick(FPS)
					
	

if __name__ == "__main__":
	main()
	pygame.quit()