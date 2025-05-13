import pygame
from settings import WHITE, BLACK


class Obstacle(pygame.sprite.Sprite):
    """Kelas untuk membuat rintangan sebagai sprite"""

    def __init__(self, screen, x, y, width, height):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)  # Rintangan berwarna hitam
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Memperbarui posisi rintangan jika diperlukan"""
        # Rintangan ini tidak bergerak, jadi update tidak diperlukan, tetapi ini bisa ditambahkan jika perlu
        pass


class Level:
    """Kelas dasar untuk level dalam game"""

    def __init__(self, screen):
        self.screen = screen
        self.level_objects = pygame.sprite.Group()

        self.background = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height())
        )
        self.background.fill(WHITE)
        self.background_image = None

        self.level_rect = pygame.Rect(
            0, 0, self.screen.get_width(), self.screen.get_height()
        )

    def update(self):
        """Memperbarui status level dan objeknya"""
        self.level_objects.update()

    def draw(self):
        """Menggambar level ke layar"""
        self.screen.blit(self.background, (0, 0))
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))

        self.level_objects.draw(self.screen)

    def add_object(self, obj):
        """Menambahkan objek ke level"""
        self.level_objects.add(obj)

    def remove_object(self, obj):
        """Menghapus objek dari level"""
        self.level_objects.remove(obj)


class Level1(Level):
    """Level 1 dalam game"""

    def __init__(self, screen):
        super().__init__(screen)
        self.level_name = "Level 1"

        # Menambahkan musuh dan rintangan di level
        self.add_enemy()
        self.add_obstacle()

    def add_enemy(self):
        """Menambahkan musuh ke level"""
        from characters import Dog

        enemy = Dog(self.screen, x=400, y=300)
        self.add_object(enemy)

    def add_obstacle(self):
        """Menambahkan rintangan ke level"""
        obstacle = Obstacle(self.screen, x=300, y=350, width=100, height=30)
        self.add_object(obstacle)

    def update(self):
        """Memperbarui level dan objeknya"""
        super().update()
