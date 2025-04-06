from game import *



volume = 1
mixer.music.load(get_asset_path('carrots.wav'))
mixer.music.play(-1)

#starting window loop
menu_loop = True
while menu_loop:
    mousex, mousey = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mousex, mousey, 1, 1)
    start_window.blit(main_menu.image, main_menu.rect)
    start_window.blit(new_button.image, new_button.rect)
    start_window.blit(load_button.image, load_button.rect)
    start_window.blit(exit_button.image, exit_button.rect)
    pygame.display.flip()

    #music
    
    for event in pygame.event.get():
        #if event.type == pygame.VIDEORESIZE:
             #width, height = event.w, event.h
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_button.rect.colliderect(mouse_rect):
                game = Game()
                game.start()

            elif load_button.rect.colliderect(mouse_rect):
                game = Game()
                game.load()
                game.start()

            elif exit_button.rect.colliderect(mouse_rect):
                pygame.quit()
                exit()

