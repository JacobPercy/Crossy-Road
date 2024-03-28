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
YELLOW = (255,255,0)
ORANGE = (255,160,16)
PINK = (255,96,208)
PURPLE = (160,32,255)

car_colors = [RED,RED,RED,RED,ORANGE,YELLOW,YELLOW,BLUE,BLUE,PURPLE,PINK]
obj_ls = []

WIDTH, HEIGHT = 450, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Rossy Croad")

img = pygame.image.load('chicken.jpg')
img = pygame.transform.scale(img, (40,40))

clock = pygame.time.Clock() 
FPS = 15

class Road():
	def __init__(self, posy, val, obstacles):
		self.car_ls = []
		self.posx = -200 + val*50
		self.posy = posy
		self.color = BLACK
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		self.speed = random.randint(4,8)
		self.dir = random.getrandbits(1) #True is left to right, False is right to left
		self.car_color = RED
		self.car_width = random.randint(40,130)
		self.car_count = random.randint(2,3)
		self.start_offset = random.randint(0,(WIDTH+400)//self.car_count)
		for x in range(self.car_count):
			self.car_ls.append(Car(x*(WIDTH+400//self.car_count),self.posy+5,self.car_width,self.speed,self.dir,self.car_color))
		obstacles.extend(self.car_ls)
				 
	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.car_ls)):
			self.car_ls[x].update(self.posy+5,xFac)

class Car():
	def __init__(self,posx,posy,width,speed,dir,color):
		self.width = width
		self.height = 40
		self.posx = posx
		self.posy = posy
		self.dir = dir #True is left to right, False is right to left
		self.speed = speed
		self.color = random.choice(car_colors)
		self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
	
	def update(self,posy,xFac):
		if self.dir:
			self.posx += self.speed
		else:
			self.posx -= self.speed
		self.posx += xFac*50
		if self.posx < -200:
			self.posx = WIDTH+400 #-self.width-(-200 - self.posx)
		elif self.posx - self.width > WIDTH+400:
			self.posx = -200
		self.Rect = pygame.Rect(self.posx, posy, self.width, self.height)
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

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx + 5, self.posy + 5, 40, 40)
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
def reset_game():
	return [],[]


def main():
	#setup
	
	obstacles = []
	running = True
	start = True
	class_options = [Road,Field,Field,Field,Road,Tracks]
	player = pygame.Rect((WIDTH//2)-20,HEIGHT-95,40,40)
	total_left_right = 0
	points = 0
	
	

	#main loop
	while running:
		if start:
			screen.fill(BLACK)
			obstacles,obj_ls = reset_game()
			points = 0
			total_left_right = 0
			while start and running:
				screen.fill(BLACK)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
					if event.type == pygame.KEYDOWN:
						start = False
						obstacles = []
				pygame.display.update()
				clock.tick(FPS)
		
		xFac,yFac,points_change=0,0,0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					yFac += 1
					points += 1
					points_change -= 1
				if event.key == pygame.K_DOWN:
					yFac -= 1
					points -= 1
					points_change += 1
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
				choice = random.choice(class_options)
				if choice == Road:
					obj_ls.append(choice(x,total_left_right,obstacles))
				else:
					obj_ls.append(choice(x,total_left_right))
		
		tree_list = []
		tuple_ls = []
		for x in range(len(obj_ls)):
			obj_ls[x].update(xFac,yFac)
			if type(obj_ls[x]) == Field:
				tree_list += obj_ls[x].tree_ls

		for x in range(len(tree_list)):
			tuple_ls.append((tree_list[x].posx,tree_list[x].posy))
		if ((WIDTH//2)-25,HEIGHT-100) in tuple_ls:
			points += points_change
			for x in range(len(obj_ls)):
				obj_ls[x].update(-xFac,-yFac)

		for x in range(len(obstacles)):
			if pygame.Rect.colliderect(player,obstacles[x].Rect):
				start = True
				break

		screen.blit(img,((WIDTH//2)-20-(5*xFac),HEIGHT-95-(5*yFac)))
		if not running:
			screen.fill(BLACK)
		print(points)
		pygame.display.update()
		clock.tick(FPS)
					
	

if __name__ == "__main__":
	main()
	pygame.quit()