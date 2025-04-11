from game import *



mixer.music.load(get_asset_path('carrots.wav'))
mixer.music.play(-1)

def end():
	pygame.quit()
	exit()


#starting window loop
menu_loop = True
while menu_loop:
	mixer.music.set_volume(0)

	mousex, mousey = pygame.mouse.get_pos()
	mouse_rect = pygame.Rect(mousex, mousey, 1, 1)
	screen.blit(main_menu.image, main_menu.rect)
	screen.blit(new_button.image, new_button.rect)
	screen.blit(load_button.image, load_button.rect)
	screen.blit(exit_button.image, exit_button.rect)
	pygame.display.flip()
	keys = pygame.key.get_pressed()
	

	# music
	
	for event in pygame.event.get():
		#if event.type == pygame.VIDEORESIZE:
			 #width, height = event.w, event.h

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if new_button.rect.colliderect(mouse_rect):
				game = Game()

			elif load_button.rect.colliderect(mouse_rect):
				game = Game(load = True)

			elif exit_button.rect.colliderect(mouse_rect):
				end()

		elif event.type == pygame.QUIT or keys[pygame.K_q]:
			end()
