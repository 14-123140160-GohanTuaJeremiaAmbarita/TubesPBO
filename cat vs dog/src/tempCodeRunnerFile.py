import pygame
import math
import random
import time

pygame.init()

# Inisialisasi clock
clock = pygame.time.Clock()

# Konfigurasi layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat vs Dog")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Physics
g = 0.5
max_power = 50
base_speed = 20
max_angle_offset = 20  # derajat

# Posisi pemain
player_pos = [50, HEIGHT - 50]

# Posisi musuh dan nyawa
lawan_pos = [600, HEIGHT - 60]
lawan_size = 40
musuh_darah = 30  # nyawa musuh

# Variabel projectile
projectile = None
power = 0
charging = False
charge_start_time = 0

# Wind
wind_angle_deg = 0
wind_strength = 0
last_wind_change = time.time()


def update_wind():
    global wind_angle_deg, wind_strength
    wind_angle_deg = random.uniform(0, 360)
    wind_strength = random.uniform(-3, 3)  # kekuatan wind antara -3 sampai 3
    global last_wind_change
    last_wind_change = time.time()


# Inisialisasi wind pertama
update_wind()

# Font
font = pygame.font.SysFont(None, 36)


# Fungsi gambar bar kekuatan
def draw_power_bar(surface, power):
    bar_width = 200
    bar_height = 20
    x = 10
    y = 50
    fill_width = (power / max_power) * bar_width
    pygame.draw.rect(surface, BLACK, (x, y, bar_width, bar_height), 2)
    pygame.draw.rect(surface, GREEN, (x, y, fill_width, bar_height))
    text = font.render(f"Power: {power:.1f}", True, BLACK)
    surface.blit(text, (x + bar_width + 10, y))


def get_effective_angle_offset(wind_deg, wind_strength):
    """
    Menghitung penyesuaian sudut berdasarkan arah dan kekuatan wind.
    Jika wind mengarah ke pemain (dengan dot positif), sudut berkurang.
    Jika menjauh, sudut bertambah.
    """
    rad = math.radians(wind_deg)
    wind_vec = (math.cos(rad), math.sin(rad))
    arah = (lawan_pos[0] - player_pos[0], lawan_pos[1] - player_pos[1])
    mag = math.hypot(*arah)
    dir_norm = (arah[0] / mag, arah[1] / mag)
    dot = wind_vec[0] * dir_norm[0] + wind_vec[1] * dir_norm[1]
    max_offset = 20  # maksimum offset sudut
    if dot > 0:
        offset = (
            -(wind_strength / 3) * max_offset
        )  # sesuaikan dengan rentang wind -3 sampai 3
    else:
        offset = (wind_strength / 3) * max_offset
    return offset


# Fungsi hitung sudut dari durasi klik
def calculate_angle_offset_from_duration(duration, max_duration=2.0):
    ratio = min(duration / max_duration, 1)
    return (ratio * 2 - 1) * max_angle_offset  # dari -20 sampai +20


# Fungsi buat projectile yang memperhitungkan wind
def create_projectile(angle_deg):
    global wind_angle_deg, wind_strength
    rad = math.radians(wind_angle_deg)
    wind_vec = (math.cos(rad), math.sin(rad))
    arah = (lawan_pos[0] - player_pos[0], lawan_pos[1] - player_pos[1])
    mag = math.hypot(*arah)
    dir_norm = (arah[0] / mag, arah[1] / mag)
    dot = wind_vec[0] * dir_norm[0] + wind_vec[1] * dir_norm[1]
    if dot > 0:
        speed_effect = 1 - (wind_strength / 10)
        if speed_effect < 0.2:
            speed_effect = 0.2
    else:
        speed_effect = 1 + (wind_strength / 10)
    speed_final = base_speed * speed_effect
    angle_rad = math.radians(angle_deg)
    vx = speed_final * math.cos(angle_rad)
    vy = -speed_final * math.sin(angle_rad)
    return {"x": player_pos[0], "y": player_pos[1], "vx": vx, "vy": vy}


# Fungsi gambarkan panah angin
def draw_wind_arrow(surface, wind_strength, wind_angle_deg):
    center_x, center_y = 750, 50
    length = 40
    if wind_strength > 0:
        # Panah ke kanan
        end_x = center_x + length
        end_y = center_y
    elif wind_strength < 0:
        # Panah ke kiri
        end_x = center_x - length
        end_y = center_y
    else:
        # Tidak ada panah
        return
    color = BLACK
    pygame.draw.line(surface, color, (center_x, center_y), (end_x, end_y), 4)
    # Tambahkan panah kecil di ujung
    arrow_size = 8
    if wind_strength > 0:
        pygame.draw.polygon(
            surface,
            color,
            [
                (end_x, end_y),
                (end_x - arrow_size, end_y - arrow_size / 2),
                (end_x - arrow_size, end_y + arrow_size / 2),
            ],
        )
    else:
        pygame.draw.polygon(
            surface,
            color,
            [
                (end_x, end_y),
                (end_x + arrow_size, end_y - arrow_size / 2),
                (end_x + arrow_size, end_y + arrow_size / 2),
            ],
        )


# Loop utama
start_time_wind = time.time()

game_over = False  # Pastikan variabel ini didefinisikan

while True:
    dt = clock.tick(60)
    screen.fill(WHITE)

    # Ganti wind setiap 10 detik
    if time.time() - last_wind_change > 10:
        update_wind()
    if time.time() - start_time_wind > 10:
        update_wind()
        start_time_wind = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Tambahkan input spasi jika menang untuk keluar
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    charging = True
                    charge_start_time = pygame.time.get_ticks()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and charging:
                    charging = False
                    hold_time = (pygame.time.get_ticks() - charge_start_time) / 1000
                    if hold_time > 2.0:
                        hold_time = 2.0
                    # Hitung offset sudut dari wind
                    angle_offset = get_effective_angle_offset(
                        wind_angle_deg, wind_strength
                    )
                    # Hitung sudut akhir
                    base_angle = calculate_angle_offset_from_duration(hold_time)
                    final_angle = base_angle + angle_offset
                    # Batasi sudut -20 sampai +20
                    if final_angle > 20:
                        final_angle = 20
                    elif final_angle < -20:
                        final_angle = -20
                    projectile = create_projectile(final_angle)

    # Update power saat menahan
    if charging:
        hold_time = (pygame.time.get_ticks() - charge_start_time) / 1000
        if hold_time > 2.0:
            hold_time = 2.0
        power = min(hold_time * 25, max_power)
        current_angle = calculate_angle_offset_from_duration(hold_time)
    else:
        current_angle = 0

    # Gambar pemain dan musuh
    pygame.draw.rect(screen, BLUE, (player_pos[0] - 10, player_pos[1], 20, 20))
    pygame.draw.rect(
        screen, YELLOW, (lawan_pos[0], lawan_pos[1], lawan_size, lawan_size)
    )

    # Gambar bar darah musuh
    bar_width = 100
    bar_height = 10
    bar_x = lawan_pos[0]
    bar_y = lawan_pos[1] - 15
    darah_ratio = musuh_darah / 30
    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width * darah_ratio, bar_height))

    # Gambar projectile jika ada
    if projectile:
        projectile["x"] += projectile["vx"]
        projectile["y"] += projectile["vy"]
        projectile["vy"] += g
        pygame.draw.circle(screen, RED, (int(projectile["x"]), int(projectile["y"])), 8)
        # Hapus jika keluar layar
        if (
            projectile["x"] > WIDTH
            or projectile["x"] < 0
            or projectile["y"] > HEIGHT
            or projectile["y"] < 0
        ):
            projectile = None
        # Deteksi tabrakan
        rect_lawan = pygame.Rect(lawan_pos[0], lawan_pos[1], lawan_size, lawan_size)
        if projectile and rect_lawan.collidepoint(projectile["x"], projectile["y"]):
            musuh_darah -= 10
            projectile = None
            if musuh_darah <= 0:
                # Menang: tampil pesan dan tunggu spasi untuk keluar
                game_over = True

    # Gambar bar kekuatan
    draw_power_bar(screen, power)

    # Tampilkan info
    sudut_text = font.render(f"Sudut: {current_angle:.1f}°", True, BLACK)
    screen.blit(sudut_text, (10, 80))
    # Tampilkan arah angin
    draw_wind_arrow(screen, wind_strength, wind_angle_deg)
    wind_dir_text = font.render(f"Wind Dir: {wind_angle_deg:.1f}°", True, BLACK)
    wind_str_text = font.render(f"Wind Str: {wind_strength:.2f}", True, BLACK)
    screen.blit(wind_dir_text, (10, 140))
    screen.blit(wind_str_text, (10, 170))
    # Tampilkan durasi tahan
    if not game_over:
        durasi = 0
        if charging:
            durasi = (pygame.time.get_ticks() - charge_start_time) / 1000
            if durasi > 2.0:
                durasi = 2.0
        durasi_text = font.render(f"Tahan: {durasi:.2f}s", True, BLACK)
        screen.blit(durasi_text, (10, 110))
    else:
        # Pesan kemenangan
        msg = font.render("You Win! Press SPACE ", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        # Tunggu spasi untuk keluar

    pygame.display.flip()
