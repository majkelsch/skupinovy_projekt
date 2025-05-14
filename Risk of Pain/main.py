import pygame as pg

pg.init()

clock = pg.time.Clock()
fps = 120

useDynamicCamera = False
camera_offset_x = 0
camera_offset_y = 0

screen_size = (800, 600)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Risk of Pain")

class Player(pg.sprite.Sprite):

	def __init__(self):
		super().__init__()
		self.image = pg.Surface((50, 50))
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)

		self.speed = 5
		self.x = 0
		self.y = 0

	def dynamic_camera(self):
		mouse_x, mouse_y = pg.mouse.get_pos()

		mouse_vector_x = -(mouse_x - (screen_size[0] // 2))
		mouse_vector_y = -(mouse_y - (screen_size[1] // 2))

		camera_offset_x = mouse_vector_x // 3
		camera_offset_y = mouse_vector_y // 3

		self.rect.center = (screen_size[0] // 2 + camera_offset_x, screen_size[1] // 2 + camera_offset_y)	

	def static_camera(self):
		self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)

	def player_movement(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_LSHIFT]:
			player_speed = 5
		else:
			player_speed = 2

		if keys[pg.K_a]:
			self.x += player_speed
		if keys[pg.K_d]:
			self.x -= player_speed
		if keys[pg.K_w]:
			self.y += player_speed
		if keys[pg.K_s]:
			self.y -= player_speed

	def update(self):
		if useDynamicCamera:
			self.dynamic_camera()
		else:
			self.static_camera()

		self.player_movement()

class StaticObject(pg.sprite.Sprite):
	def __init__(self, x:int, y:int, width:int, height:int, hasCollider:bool, color=(0, 0, 0)):
		super().__init__()
		self.image = pg.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.center = (x, y)
		self.hasCollider = hasCollider

	def dynamic_camera(self):
		mouse_x, mouse_y = pg.mouse.get_pos()
		mouse_vector_x = -(mouse_x - (screen_size[0] // 2))
		mouse_vector_y = -(mouse_y - (screen_size[1] // 2))
		camera_offset_x = mouse_vector_x // 3
		camera_offset_y = mouse_vector_y // 3
		self.rect.center = (player.x+self.x+camera_offset_x, player.y+self.y+camera_offset_y)


	def static_camera(self):
		self.rect.center = (player.x+self.x, player.y+self.y)

	def update(self):
		if self.hasCollider:
			self.check_collision()

		if useDynamicCamera:
			self.dynamic_camera()
		else:
			self.static_camera()

	def check_collision(self):
		if pg.sprite.collide_rect(self, player):
			# Get where colision happened
			collision_rect = self.rect.clip(player.rect)
			# Stop player from moving (stop world movement because player is standing still)
			if collision_rect.width > collision_rect.height:
				if player.rect.centery < self.rect.centery:
					player.y += collision_rect.height
				else:
					player.y -= collision_rect.height
			else:
				if player.rect.centerx < self.rect.centerx:
					player.x += collision_rect.width
				else:
					player.x -= collision_rect.width
		

player = Player()
static_object = StaticObject(400, 0, 300, 50, True, (255, 0, 0))
static_object2 = StaticObject(800, 0, 300, 25, False, (0, 255, 0))
all_sprites = pg.sprite.Group()

all_sprites.add(static_object)
all_sprites.add(static_object2)
all_sprites.add(player)


running = True
while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False

	
	screen.fill((0, 0, 0))


	all_sprites.draw(screen)
	all_sprites.update()

	
	



	pg.display.flip()
	clock.tick(fps)
pg.quit()