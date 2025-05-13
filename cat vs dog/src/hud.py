import pygame


class HUD:
    """Tampilan antarmuka pengguna (HUD) untuk menampilkan status"""

    def __init__(self, screen):
        self.screen = screen

    def update(self):
        """Memperbarui elemen HUD"""
        pass

    def draw(self):
        """Menggambar elemen HUD ke layar"""
        font = pygame.font.Font(None, 36)
        text = font.render("Health: 100", True, (255, 255, 255))  # Menampilkan HP
        self.screen.blit(text, (10, 40))  # Menampilkan HP di posisi (10, 40)
