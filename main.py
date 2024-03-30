import pygame
import random
from math import sqrt

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
BROWN = (139,69,19)
SPECIAL_BLUE = (105,206,236)

car_colors = [RED,RED,ORANGE,YELLOW,YELLOW,BLUE,BLUE,BLUE,PURPLE,PINK]
obj_ls = []

WIDTH, HEIGHT = 450, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Rossy Croad")

img = pygame.image.load('chicken3.webp')
img = pygame.transform.scale(img, (40,40))
img_2 = pygame.transform.scale(img, (228,360))

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
		self.speed = int(2.0*sqrt(random.randint(9,60)))
		self.dir = random.getrandbits(1) #True is left to right, False is right to left
		self.car_width = random.randint(65,120)
		self.car_count = random.randint(2,4)
		self.start_offset = random.randint(0,(WIDTH+400)//self.car_count)
		for x in range(self.car_count):
			self.car_ls.append(Car((x*(WIDTH+400//self.car_count))+self.start_offset, 
													self.posy+5, 
						  							self.car_width, 
						  							self.speed,self.dir))
		obstacles.extend(self.car_ls)
				 
	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.car_ls)):
			self.car_ls[x].update(self.posy+5,xFac)

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.car_ls)):
			self.car_ls[x].manual_x(xFac)

class Car():
	def __init__(self,posx,posy,width,speed,dir):
		self.width = width
		self.height = 40
		self.posx = posx
		self.posy = posy
		self.dir = dir #True is left to right, False is right to left
		self.speed = speed
		self.color = random.choice(car_colors)
		self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
	
	def update(self,posy,xFac):
		self.posy = posy
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

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

class Field():
	def __init__(self, posy, val):
		self.tree_ls = []
		self.posy = posy
		self.posx = -200 + val*50
		self.color = LIGHT_GREEN
		for x in range(3):
			rand_val = random.randint(-200,WIDTH+350)
			self.tree_ls.append(Tree_Rock(rand_val - rand_val%50,self.posy))

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.tree_ls)):
			self.tree_ls[x].update(xFac,yFac)

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.tree_ls)):
			self.tree_ls[x].manual_x(xFac)

class Tree_Rock():
	def __init__(self,posx,posy):
		options = [GREEN,GREEN,GREEN,GREEN,GRAY]
		self.posx = posx
		self.posy = posy
		self.color = random.choice(options)

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx + 5, self.posy + 5, 40, 40)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx + 5, self.posy + 5, 40, 40)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		
class Water():
	def __init__(self, posy, val):
		self.width_options = []
		for x in range(2,4):
			self.width_options.append(50*x)
		self.log_ls = []
		self.posy = posy
		self.posx = -200 + val*50
		self.color = BLUE
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		self.speed = random.randint(2,4)
		self.dir = random.getrandbits(1) #True is left to right, False is right to left
		self.log_count = random.randint(5,9)
		self.start_offset = random.randint(0,(WIDTH+400)//self.log_count)
		for x in range(self.log_count):
			self.log_ls.append(Log((x*(WIDTH+400//self.log_count) + self.start_offset), 
													self.posy+10,
						  							random.choice(self.width_options), 
						  							self.speed,
													self.dir))

	def update(self,xFac,yFac):
		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.log_ls)):
			self.log_ls[x].update(xFac,self.posy+10)

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)
		for x in range(len(self.log_ls)):
			self.log_ls[x].manual_x(xFac)

class Log():
	def __init__(self,posx,posy,width,speed,dir):
		self.color = BROWN
		self.width = width
		self.height = 30
		self.posx = posx
		self.posy = posy
		self.dir = dir #True is left to right, False is right to left
		self.speed = speed
		self.Rect = (self.posx,self.posy,self.width,self.height)
		self.drawn = pygame.draw.rect(screen,self.color,self.Rect)
	
	def update(self,xFac,posy):
		if self.dir:
			self.posx += self.speed
		else:
			self.posx -= self.speed
		self.posx += xFac*50
		if self.posx < -200:
			self.posx = WIDTH+400 - self.width
		elif self.posx + self.width > WIDTH+400:
			self.posx = -200
		self.Rect = pygame.Rect(self.posx, posy, self.width, self.height)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

class Tracks():
	def __init__(self, posy, val):
		self.posy = posy
		self.posx = -200 + val*50
		self.color_val = random.randint(50,255)
		self.color = (self.color_val,self.color_val,self.color_val)
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def update(self,xFac,yFac):
		self.color_val -= 2
		if self.color_val < 0:
			self.color_val = 255
			self.color = RED
		elif self.color_val < 20:
			self.color = RED
		else:
			self.color = (self.color_val,self.color_val,self.color_val)

		self.posy += yFac * 50
		self.posx += xFac * 50
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

	def manual_x(self,xFac):
		self.posx += xFac
		self.Rect = pygame.Rect(self.posx, self.posy, WIDTH+400, 50)
		self.drawn = pygame.draw.rect(screen, self.color, self.Rect)

def global_x_update(obj_ls,x_diff,dir):
	for obj in obj_ls:
		if dir:
			obj.posx += x_diff
		else:
			obj.posx -= x_diff
	return obj_ls

def main():
	#setup
	running = True
	start = True
	was_log = False
	class_options = [Road,Road,Road,Field,Road,Field,Field,Field,Road,Tracks,Water,Water]
	player = pygame.Rect((WIDTH//2)-20,HEIGHT-95,40,40)
	total_left_right = 0
	score = 0
	x_offset = 0
	with open("best_score.txt","r") as f:
		file = f.read()
		if len(file) > 0:
			best_score = int(file.split("\n")[-2])
			former_best = best_score
		else:
			best_score = 0
			former_best = 0
	highest_score_this_round = 0
	time_since_move = 0
	#main loop
	while running:
		font = pygame.font.Font('freesansbold.ttf', 40)
		your_score_img = font.render(str(score), True, BLACK)
		font = pygame.font.Font('freesansbold.ttf', 15)
		best_score_img = font.render("Best: " + str(best_score), True, BLACK)
		
		if score > best_score:
			best_score = score
		if start:
			if score > best_score:
				best_score = score
			x_offset = 0
			highest_score_this_round = 0
			time_since_move = 0
			obstacles,obj_ls = [],[]

			screen.fill(SPECIAL_BLUE)

			screen.blit(img_2,((WIDTH//2)-114,200))

			font = pygame.font.Font('freesansbold.ttf', 15)
			your_score_img = font.render("Your Score: " + str(score), True, BLACK)

			text_rect_3 = your_score_img.get_rect(center=(int(WIDTH/2), 250))
			text_rect_4 = best_score_img.get_rect(center=(int(WIDTH/2), 275))

			font = pygame.font.Font('freesansbold.ttf', 60)
			title_screen = font.render("Rossy Croad",True,BLACK)
			text_rect_1 = title_screen.get_rect(center=(int(WIDTH/2), 125))

			font = pygame.font.Font('freesansbold.ttf', 20)
			press_to_play = font.render("Press any key to start",True,BLACK)
			text_rect_2 = press_to_play.get_rect(center=(int(WIDTH/2), 200))

			screen.blit(title_screen,text_rect_1)
			screen.blit(press_to_play,text_rect_2)
			if score != 0:
				screen.blit(your_score_img,text_rect_3)
			screen.blit(best_score_img,text_rect_4)
			score = 0
			total_left_right = 0
			for x in range(4):
				obj_ls.append(Field(HEIGHT-50-(50*x),0))
			while start and running:
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
					if event.type == pygame.KEYDOWN:
						start = False
						obstacles = []
				pygame.display.update()
				clock.tick(FPS)
		
		xFac=yFac=points_change=0
		was_x_off = x_offset
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					yFac += 1
					score += 1
					points_change -= 1
				if event.key == pygame.K_DOWN:
					yFac -= 1
					score -= 1
					points_change += 1
				if event.key == pygame.K_LEFT:
					total_left_right += 1
					x_offset -= 50
					xFac += 1
				if event.key == pygame.K_RIGHT:
					total_left_right -= 1
					x_offset += 50
					xFac -= 1
		
		if total_left_right == -5:
			total_left_right = -4
			xFac += 1
			x_offset -= 50
		elif total_left_right == 5:
			total_left_right = 4
			xFac -= 1
			x_offset += 50
		

		time_since_move += 1

		if score > highest_score_this_round:
			highest_score_this_round = score
			time_since_move = 0
		
		#Eagle waiting death
		if time_since_move > 100:
			start = True
			time_since_move = 0
			continue
		
		#Car death
		#for x in range(len(obstacles)):
			#if pygame.Rect.colliderect(player,obstacles[x].Rect):
				#start = True
				#break
		
		was_log = False
		collided = False
		for obj in obj_ls:
			#Train death
			if type(obj) == Tracks and obj.color == RED and pygame.Rect.colliderect(player,obj.Rect):
				start = True
				break
			#Log movements
			if type(obj) == Water and pygame.Rect.colliderect(player,obj.Rect):
				was_log = True
				for log in obj.log_ls:
					if pygame.Rect.colliderect(player,log.Rect):
						collided = True
						if log.dir:
							x_offset += log.speed
							for obj in obj_ls:
								obj.manual_x(-log.speed)
						else:
							x_offset -= log.speed
							for obj in obj_ls:
								obj.manual_x(log.speed)
						#break
				#Water fall in
				if not collided:
					start = True
		
		if not was_log:
			val = x_offset % 50
			for obj in obj_ls:
				obj.manual_x(val)
			temp = [abs(x_offset-(x_offset-val)),abs(x_offset-(x_offset-val+50))]
			if min(temp) == abs(x_offset-(x_offset-val)):
				x_offset -= val
			else:
				x_offset -= val + 50
		

		tree_list,tuple_ls  = [],[]
		for obj in obj_ls:
			obj.update(xFac,yFac)
			if type(obj) == Field:
				tree_list += obj.tree_ls

		for x in range(len(tree_list)):
			tuple_ls.append((tree_list[x].posx,tree_list[x].posy))
		if ((WIDTH//2)-25,HEIGHT-100) in tuple_ls:
			score += points_change
			x_offset = was_x_off
			for x in range(len(obj_ls)):
				obj_ls[x].update(-xFac,-yFac)
	

		if score < 0:
			score = 0
			x_offset = was_x_off
			for x in range(len(obj_ls)):
				obj_ls[x].update(-xFac,-yFac)

		total_left_right = -(round(x_offset/50))
		y_ls = []
		for x in range(len(obj_ls)):
			y_ls.append(obj_ls[x].posy)

		for x in range(0,HEIGHT,50):
			if x not in y_ls:
				choice = random.choice(class_options)
				if choice == Road:
					obj_ls.append(choice(x,total_left_right,obstacles))
				else:
					obj_ls.append(choice(x,total_left_right))

		#print(total_left_right, x_offset)
		#Log fell off map
		if abs(x_offset) > 200:
			start = True
			continue

		screen.blit(img,((WIDTH//2)-20-(5*xFac),HEIGHT-95-(5*yFac)))
		behind_scores_rect = pygame.Rect(0,0,100,60)
		pygame.draw.rect(screen, WHITE, behind_scores_rect)
		screen.blit(your_score_img,(0,0))
		screen.blit(best_score_img,(0,40))
		if not running:
			screen.fill(SPECIAL_BLUE)
		pygame.display.update()
		clock.tick(FPS)

	with open("best_score.txt","w") as f:
		f.write(str(max(score,best_score,former_best)) + "\n")	
	

if __name__ == "__main__":
	main()
	pygame.quit()