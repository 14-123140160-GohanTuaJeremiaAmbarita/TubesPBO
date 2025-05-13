import pygame


# Fungsi untuk menampilkan menu utama
def main_menu(screen, width, height, game_loop):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Arial", 24)

    title = font.render("Cat vs Dog", True, (0, 0, 0))
    play_button = font.render("Play Game", True, (0, 0, 255))
    quit_button = font.render("Quit", True, (255, 0, 0))

    screen.blit(title, (width // 2 - title.get_width() // 2, 100))
    screen.blit(play_button, (width // 2 - play_button.get_width() // 2, 200))
    screen.blit(quit_button, (width // 2 - quit_button.get_width() // 2, 250))

    pygame.display.flip()

    # Menunggu input pengguna
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Klik kiri untuk memulai permainan
                    game_loop("1vs1")
                    waiting = False


# Fungsi untuk memulai permainan
def start_game(screen, width, height, game_loop):
    main_menu(screen, width, height, game_loop)
