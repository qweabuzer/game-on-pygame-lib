import pygame
import math
from PIL import Image, ImageFilter
from pygame.locals import *
from settings import player_sens


sens = player_sens

def run_menu():
    global sens
    sc = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption(" ")

    pygame.mixer.music.load("music/menu.mp3")
    pygame.mixer.music.play(-1)  # -1 означает зацикливание воспроизведения

    background_image = pygame.image.load("img/menu1.jpg")
    background_image = pygame.transform.scale(background_image, (1200, 800))
    background_rect = background_image.get_rect()

    background_surface = pygame.Surface(sc.get_size())
    background_surface.blit(background_image, (0, 0))

    # Преобразование изображения фона в объект PIL.Image
    pil_image = Image.fromarray(pygame.surfarray.array3d(background_image))

    blur_radius = 2
    blurred_pil_image = pil_image.filter(ImageFilter.GaussianBlur(blur_radius))
    blurred_pil_image = blurred_pil_image.rotate(270, expand=True)

    # Преобразование размытого изображения обратно в объект Pygame.Surface
    blurred_background_surface = pygame.image.fromstring(blurred_pil_image.tobytes(), blurred_pil_image.size,
                                                         blurred_pil_image.mode)

    background_x = 0
    background_y = 0

    clock = pygame.time.Clock()

    font_path = "fonts/font1.ttf"
    font_size = 48
    font_size_main = 179
    font = pygame.font.Font(font_path, font_size)
    font_main = pygame.font.Font(font_path, font_size_main)
    base_color = (0, 0, 0)
    color_range = (255, 0, 0)
    angle = 0

    button_color_normal = (0, 0, 0)
    button_color_hover = (255, 255, 255)
    text_color_normal = (255, 255, 255)
    text_color_hover = (0, 0, 0)


    button_texts = ["Play", "Options", "Exit"]
    button_texts_opt = ["Change sens ˆ", "Change sens ˇ", "Music off", "Music on", "Esc"]
    button_width = 200
    button_height = 50

    # Расчет позиции кнопок по центру экрана по оси X
    screen_width = sc.get_width()
    screen_height = sc.get_height()
    button_x = screen_width // 2 - button_width // 2


    button_spacing = 20
    total_button_height = button_height * len(button_texts)
    total_spacing = button_spacing * (len(button_texts) - 1)
    buttons_start_y = (screen_height - total_button_height - total_spacing) // 2


    menu_active = True
    is_settings_open = False


    while menu_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_settings_open:
                    for i, text in enumerate(button_texts_opt):
                        button_y = buttons_start_y + (button_height + button_spacing) * i
                        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            if text == "Esc":
                                is_settings_open = False
                            elif text == "Change sens ˆ":
                                sens += 0.002
                            elif text == "Change sens ˇ":
                                sens -= 0.002
                                if sens < 0:
                                    sens = 0.000666
                            elif text == "Music off":
                                pygame.mixer.music.pause()
                            elif text == "Music on":
                                pygame.mixer.music.unpause()


                else:
                    for i, text in enumerate(button_texts):
                        button_y = buttons_start_y + (button_height + button_spacing) * i
                        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            if text == "Exit":
                                pygame.quit()
                                return
                            elif text == "Play":
                                pygame.mixer.music.stop()
                                pygame.mouse.set_visible(False)
                                return 1
                            elif text == "Options":
                                is_settings_open = True

        mouse_pos = pygame.mouse.get_pos()
        background_x -= 1

        if background_x <= -background_rect.width:
            background_x = 0

        sc.blit(blurred_background_surface, (background_x, background_y))
        sc.blit(blurred_background_surface, (background_x + background_rect.width, background_y))

        r = base_color[0] + int(math.sin(angle) * color_range[0])
        g = base_color[1] + int(math.sin(angle + 2 * math.pi / 3) * color_range[1])
        b = base_color[2] + int(math.sin(angle + 4 * math.pi / 3) * color_range[2])

        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))


        title_text = font_main.render("Eternal DooM", True, (r, g, b))

        if not is_settings_open:
            for i, text in enumerate(button_texts):
                button_y = buttons_start_y + (button_height + button_spacing) * i

                button_surface = pygame.Surface((button_width, button_height))

                # Проверка, находится ли курсор над кнопкой
                if button_x <= mouse_pos[0] <= button_x + button_width and \
                        button_y <= mouse_pos[1] <= button_y + button_height:
                    text_color = text_color_hover
                    button_surface.fill(button_color_hover)
                else:
                    text_color = text_color_normal
                    button_surface.fill(button_color_normal)

                pygame.draw.rect(button_surface, (0, 0, 0), button_surface.get_rect(), 3)  # ramka

                text_surface = font.render(text, True, text_color)

                title_x_main = sc.get_width() // 2 - title_text.get_width() // 2  # title

                text_x = button_width // 2 - text_surface.get_width() // 2  # buttons
                text_y = button_height // 2 - text_surface.get_height() // 2

                button_surface.blit(text_surface, (text_x, text_y))
                sc.blit(title_text, (title_x_main, 50))
                sc.blit(button_surface, (button_x, button_y))

        if is_settings_open:
            for i, text in enumerate(button_texts_opt):
                button2_y = buttons_start_y + (button_height + button_spacing) * i

                button2_surface = pygame.Surface((button_width, button_height))

                sensitivity_button_rect = pygame.Rect(button_x, button2_y, button_width,
                                                      button_height)
                pygame.draw.rect(sc, button_color_normal, sensitivity_button_rect)

                if button_x <= mouse_pos[0] <= button_x + button_width and \
                        button2_y <= mouse_pos[1] <= button2_y + button_height:
                    text_color = text_color_hover
                    pygame.draw.rect(sc, button_color_hover, sensitivity_button_rect)
                    button2_surface.fill(button_color_hover)
                else:
                    text_color = text_color_normal
                    button2_surface.fill(button_color_normal)

                pygame.draw.rect(button2_surface, (0, 0, 0), button2_surface.get_rect(), 3)  # ramka

                text_surface = font.render(text, True, text_color)

                title_x_main = sc.get_width() // 2 - title_text.get_width() // 2  # title
                text_x = button_width // 2 - text_surface.get_width() // 2  # buttons
                text_y = button_height // 2 - text_surface.get_height() // 2

                button2_surface.blit(text_surface, (text_x, text_y))
                sc.blit(button2_surface, (button_x, button2_y))
                sc.blit(title_text, (title_x_main, 50))


        pygame.display.flip()
        clock.tick(60)
        angle += 0.02


def get_sens():
    print(sens)
    return sens
