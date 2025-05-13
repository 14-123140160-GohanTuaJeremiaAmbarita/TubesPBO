import pygame
from settings import WHITE, BLACK


class Character(pygame.sprite.Sprite):
    """Kelas dasar untuk karakter (kucing dan anjing)"""

    def __init__(self, screen, x, y, speed=5, health=100):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.velocity = [0, 0]  # Kecepatan (horizontal, vertikal)

        self.image = pygame.Surface((50, 50))  # Gambar karakter (placeholder)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """Memperbarui posisi karakter"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.rect.x = max(
            0, min(self.rect.x, self.screen.get_width() - self.rect.width)
        )
        self.rect.y = max(
            0, min(self.rect.y, self.screen.get_height() - self.rect.height)
        )

    def move(self, dx, dy):
        """Menggerakkan karakter"""
        self.velocity = [dx * self.speed, dy * self.speed]

    def stop(self):
        """Menghentikan pergerakan karakter"""
        self.velocity = [0, 0]

    def take_damage(self, amount):
        """Mengurangi HP karakter"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        """Menangani kematian karakter"""
        print(f"{self.__class__.__name__} has died.")

    def draw(self):
        """Menggambar karakter ke layar"""
        self.screen.blit(self.image, self.rect)


class Cat(Character):
    """Karakter kucing"""

    def __init__(self, screen, x=100, y=100, speed=6, health=100):
        super().__init__(screen, x, y, speed, health)
        self.image.fill((255, 0, 0))  # Warna merah untuk kucing
        self.attack_power = 10

    def attack(self):
        """Serangan kucing"""
        print("Cat attacks with claws!")


class Dog(Character):
    """Karakter anjing"""

    def __init__(self, screen, x=200, y=100, speed=5, health=120):
        super().__init__(screen, x, y, speed, health)
        self.image.fill((0, 0, 255))  # Warna biru untuk anjing
        self.attack_power = 15

    def attack(self):
        """Serangan anjing"""
        print("Dog attacks with bite!")
