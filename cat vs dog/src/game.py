import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from characters import Cat, Dog
from src.levels import Level1
from src.hud import HUD


class GameLoop:
    """Loop utama permainan"""

    def __init__(self):
        pygame.init()

        # Setup layar game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cat vs Dog")

        # Membuat objek level, karakter, dan HUD
        self.level = Level1(self.screen)
        self.cat = Cat(self.screen)
        self.dog = Dog(self.screen)
        self.hud = HUD(self.screen)

        # Timer
        self.timer = Timer(countdown_time=60)  # 60 detik per level

        # Clock untuk pengaturan FPS
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        """Menangani input pengguna"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Memperbarui status permainan"""
        self.cat.update()
        self.dog.update()
        self.level.update()
        self.hud.update()

        # Terapkan gravitasi dan gerakan
        apply_gravity(self.cat)
        apply_gravity(self.dog)
        move_character(self.cat)
        move_character(self.dog)

        # Perbarui timer
        self.timer.update()

    def draw(self):
        """Menggambar level dan objek di layar"""
        self.level.draw()
        self.cat.draw()
        self.dog.draw()
        self.hud.draw()

        # Gambar timer di layar
        font = pygame.font.Font(None, 36)
        timer_text = font.render(
            f"Time Left: {max(0, 60 - int(self.timer.elapsed_time))}", True, WHITE
        )
        self.screen.blit(timer_text, (10, 10))

        pygame.display.update()

    def run(self):
        """Game loop utama"""
        while self.running:
            self.handle_events()  # Menangani event
            self.update()  # Memperbarui status
            self.draw()  # Menggambar elemen ke layar
            self.clock.tick(60)  # Menetapkan frame rate ke 60 FPS

        pygame.quit()  # Keluar dari permainan


# --- Fungsionalitas Tambahan ---
def check_collision(rect1, rect2):
    """Memeriksa tabrakan antara dua objek"""
    return rect1.colliderect(rect2)


def apply_gravity(character, gravity=0.5):
    """Menambahkan gravitasi pada karakter"""
    character.velocity[1] += gravity


def move_character(character):
    """Menggerakkan karakter"""
    character.rect.x += character.velocity[0]
    character.rect.y += character.velocity[1]


class Timer:
    def __init__(self, countdown_time):
        """Inisialisasi timer hitung mundur"""
        self.start_time = pygame.time.get_ticks()  # Waktu mulai dalam milidetik
        self.countdown_time = countdown_time  # Hitung mundur dalam detik
        self.elapsed_time = 0

    def update(self):
        """Memperbarui waktu berlalu"""
        self.elapsed_time = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000  # Hitung dalam detik

    def is_time_up(self):
        """Memeriksa apakah waktu habis"""
        return self.elapsed_time >= self.countdown_time
