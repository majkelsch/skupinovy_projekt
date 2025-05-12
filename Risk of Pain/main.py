import pygame as pg

pg.init()


clock = pg.time.Clock()
fps = 60

screen_size = (800, 600)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Risk of Pain")

camera_offset_x = 0
camera_offset_y = 0

x = 0
y = 0






running = True
while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False

	clock.tick(fps)
	screen.fill((0, 0, 0))
	



	
	pg.draw.circle(screen, (255, 255, 255), (400+camera_offset_x, 300+camera_offset_y), 50)
	pg.draw.rect(screen, (255, 0, 0), (400+x+camera_offset_x, 300+y+camera_offset_y, 50, 50))
	keys = pg.key.get_pressed()
	if keys[pg.K_a]:
		x += 5
	if keys[pg.K_d]:
		x -= 5
	if keys[pg.K_w]:
		y += 5
	if keys[pg.K_s]:
		y -= 5

	mouse_x, mouse_y = pg.mouse.get_pos()
	mouse_vector_x = -(mouse_x - (screen_size[0] / 2))
	mouse_vector_y = -(mouse_y - (screen_size[1] / 2))
	camera_offset_x = mouse_vector_x // 2
	camera_offset_y = mouse_vector_y // 2
	
	



	pg.display.flip()
pg.quit()