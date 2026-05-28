import pygame
import sys
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 900, 700
FPS = 60
CIRCLE_RADIUS = 70
CIRCLE_SPEED = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
LIGHT_GRAY = (180, 180, 180)
ACCENT = (80, 200, 255)
ACCENT_HOVER = (120, 220, 255)
RED = (255, 80, 80)
GREEN = (80, 220, 120)
DARK_BG = (25, 25, 35)
PANEL_BG = (35, 35, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Attention")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("segoeui", 56, bold=True)
font_medium = pygame.font.SysFont("segoeui", 32)
font_small = pygame.font.SysFont("segoeui", 24)
font_timer = pygame.font.SysFont("consolas", 40, bold=True)


class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        label = font_medium.render(self.text, True, WHITE)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Circle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * CIRCLE_SPEED
        self.vy = math.sin(angle) * CIRCLE_SPEED

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - CIRCLE_RADIUS <= 0:
            self.x = CIRCLE_RADIUS
            self.vx = abs(self.vx)
            self._randomize_bounce("left")
        elif self.x + CIRCLE_RADIUS >= WIDTH:
            self.x = WIDTH - CIRCLE_RADIUS
            self.vx = -abs(self.vx)
            self._randomize_bounce("right")

        if self.y - CIRCLE_RADIUS <= 50:
            self.y = 50 + CIRCLE_RADIUS
            self.vy = abs(self.vy)
            self._randomize_bounce("top")
        elif self.y + CIRCLE_RADIUS >= HEIGHT:
            self.y = HEIGHT - CIRCLE_RADIUS
            self.vy = -abs(self.vy)
            self._randomize_bounce("bottom")

    def _randomize_bounce(self, wall):
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        angle = math.atan2(self.vy, self.vx)
        angle += random.uniform(-0.5, 0.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        if wall in ("left", "right"):
            if wall == "left":
                self.vx = abs(self.vx)
            else:
                self.vx = -abs(self.vx)
        if wall in ("top", "bottom"):
            if wall == "top":
                self.vy = abs(self.vy)
            else:
                self.vy = -abs(self.vy)

    def draw(self, surface, tracking):
        color = GREEN if tracking else ACCENT
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), CIRCLE_RADIUS)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), CIRCLE_RADIUS, 2)

    def contains_point(self, px, py):
        dist = math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2)
        return dist <= CIRCLE_RADIUS


def draw_timer_bar(surface, track_time, tracking):
    pygame.draw.rect(surface, PANEL_BG, (0, 0, WIDTH, 50))
    pygame.draw.line(surface, GRAY, (0, 50), (WIDTH, 50), 2)

    time_str = f"{track_time:.2f}s"
    color = GREEN if tracking else WHITE
    timer_surf = font_timer.render(time_str, True, color)
    timer_rect = timer_surf.get_rect(center=(WIDTH // 2, 25))
    surface.blit(timer_surf, timer_rect)

    if tracking:
        label = font_small.render("TRACKING", True, GREEN)
    else:
        label = font_small.render("NOT TRACKING", True, RED)
    surface.blit(label, (15, 13))

    best_label = font_small.render("Hold click on the circle", True, LIGHT_GRAY)
    surface.blit(best_label, (WIDTH - best_label.get_width() - 15, 13))


def menu_screen():
    btn_start = Button("Start", WIDTH // 2 - 100, 350, 200, 55, GRAY, ACCENT)
    btn_exit = Button("Exit", WIDTH // 2 - 100, 430, 200, 55, GRAY, RED)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_start.clicked(mouse_pos):
                    return "instructions"
                if btn_exit.clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        btn_start.update(mouse_pos)
        btn_exit.update(mouse_pos)

        screen.fill(DARK_BG)

        title = font_large.render("Circle Attention", True, ACCENT)
        title_rect = title.get_rect(center=(WIDTH // 2, 200))
        screen.blit(title, title_rect)

        subtitle = font_small.render("Test your tracking skills", True, LIGHT_GRAY)
        sub_rect = subtitle.get_rect(center=(WIDTH // 2, 270))
        screen.blit(subtitle, sub_rect)

        btn_start.draw(screen)
        btn_exit.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def instructions_screen():
    btn_play = Button("Play", WIDTH // 2 - 100, 520, 200, 55, GRAY, GREEN)

    lines = [
        "A circle will bounce around the screen.",
        "Click and hold on the circle to start tracking.",
        "Keep your cursor on the circle while holding the button.",
        "The timer counts how long you can track it.",
        "Try to keep your streak going as long as possible!",
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.clicked(mouse_pos):
                    return "game"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_RETURN:
                    return "game"

        btn_play.update(mouse_pos)

        screen.fill(DARK_BG)

        title = font_large.render("How to Play", True, ACCENT)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)

        for i, line in enumerate(lines):
            text = font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, 220 + i * 45))
            screen.blit(text, text_rect)

        esc_hint = font_small.render("Press ESC to return to menu", True, LIGHT_GRAY)
        esc_rect = esc_hint.get_rect(center=(WIDTH // 2, 620))
        screen.blit(esc_hint, esc_rect)

        btn_play.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def pause_screen(attempts):
    btn_resume = Button("Resume", WIDTH // 2 - 100, 550, 200, 55, GRAY, GREEN)
    btn_menu = Button("Main Menu", WIDTH // 2 - 100, 620, 200, 55, GRAY, RED)

    scroll_offset = 0
    max_visible = 10

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_resume.clicked(mouse_pos):
                    return "resume"
                if btn_menu.clicked(mouse_pos):
                    return "menu"
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset = max(0, min(scroll_offset - event.y, max(0, len(attempts) - max_visible)))

        btn_resume.update(mouse_pos)
        btn_menu.update(mouse_pos)

        screen.fill(DARK_BG)

        title = font_large.render("Paused", True, ACCENT)
        title_rect = title.get_rect(center=(WIDTH // 2, 60))
        screen.blit(title, title_rect)

        header = font_medium.render("Tracking Attempts", True, WHITE)
        header_rect = header.get_rect(center=(WIDTH // 2, 130))
        screen.blit(header, header_rect)

        sorted_attempts = sorted(attempts, reverse=True)

        if not sorted_attempts:
            no_data = font_small.render("No attempts yet", True, LIGHT_GRAY)
            no_rect = no_data.get_rect(center=(WIDTH // 2, 200))
            screen.blit(no_data, no_rect)
        else:
            list_y = 170
            visible = sorted_attempts[scroll_offset:scroll_offset + max_visible]
            for i, t in enumerate(visible):
                idx = scroll_offset + i + 1
                row_rect = pygame.Rect(WIDTH // 2 - 200, list_y + i * 36, 400, 32)
                bg_color = PANEL_BG if i % 2 == 0 else GRAY
                pygame.draw.rect(screen, bg_color, row_rect, border_radius=5)
                entry = font_small.render(f"#{idx:>3}    {t:.2f}s", True, WHITE)
                entry_rect = entry.get_rect(center=row_rect.center)
                screen.blit(entry, entry_rect)

            if len(attempts) > max_visible:
                hint = font_small.render(f"Scroll to see more ({len(attempts)} total)", True, LIGHT_GRAY)
                hint_rect = hint.get_rect(center=(WIDTH // 2, list_y + max_visible * 36 + 10))
                screen.blit(hint, hint_rect)

        btn_resume.draw(screen)
        btn_menu.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def game_screen():
    circle = Circle()
    track_time = 0.0
    tracking = False
    last_time = None
    attempts = []

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if tracking and track_time > 0:
                    attempts.append(track_time)
                    track_time = 0.0
                    tracking = False
                    last_time = None
                result = pause_screen(attempts)
                if result == "menu":
                    return "menu"

        on_circle = circle.contains_point(*mouse_pos)
        now = time.perf_counter()

        if mouse_pressed and on_circle:
            if not tracking:
                tracking = True
                last_time = now
            else:
                track_time += now - last_time
                last_time = now
        else:
            if tracking:
                attempts.append(track_time)
                track_time = 0.0
                tracking = False
                last_time = None

        circle.update()

        screen.fill(DARK_BG)
        draw_timer_bar(screen, track_time, tracking)
        circle.draw(screen, tracking)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    state = "menu"
    while True:
        if state == "menu":
            state = menu_screen()
        elif state == "instructions":
            state = instructions_screen()
        elif state == "game":
            state = game_screen()


if __name__ == "__main__":
    main()
