import pygame
from save import SettingsManager
from ui import Button, ToggleButton

class SettingsMenu:
    def __init__(self, screen, settings_manager, audio_manager):
        self.screen = screen
        self.settings = settings_manager
        self.audio = audio_manager
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.create_widgets()
        
    def create_widgets(self):
        self.music_slider = Slider(300, 220, 300, 20, 
                                   self.settings.get("music_volume", 0.7))
        self.sfx_slider = Slider(300, 290, 300, 20,
                                 self.settings.get("sfx_volume", 0.7))

        self.music_toggle = ToggleButton(300, 360, 60, 30,
                                        "Music", self.settings.get("music_on", True))
        self.sfx_toggle = ToggleButton(300, 420, 60, 30,
                                      "SFX", self.settings.get("sfx_on", True))
        self.particles_toggle = ToggleButton(300, 480, 60, 30,
                                            "Particles", self.settings.get("particles", True))

        self.back_button = Button(450, 560, 300, 60,
                                 "BACK", (200, 50, 150), (255, 100, 200))
    
    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.music_slider.update(mouse_pos)
        self.sfx_slider.update(mouse_pos)
        self.music_toggle.update(mouse_pos)
        self.sfx_toggle.update(mouse_pos)
        self.particles_toggle.update(mouse_pos)
        self.back_button.update(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.music_slider.handle_click(event)
                self.sfx_slider.handle_click(event)

                if self.music_toggle.hover:
                    self.music_toggle.toggle()
                    self.settings.set("music_on", self.music_toggle.state)
                    if not self.music_toggle.state:
                        self.audio.stop_music()
                    else:
                        pass
                
                if self.sfx_toggle.hover:
                    self.sfx_toggle.toggle()
                    self.settings.set("sfx_on", self.sfx_toggle.state)
                
                if self.particles_toggle.hover:
                    self.particles_toggle.toggle()
                    self.settings.set("particles", self.particles_toggle.state)

                if self.back_button.hover:
                    self.back_button.clicked = True
                    return "back"
        if self.music_toggle.state:
            self.settings.set("music_volume", self.music_slider.value)
            self.audio.set_music_volume(self.music_slider.value)

        if self.sfx_toggle.state:
            self.settings.set("sfx_volume", self.sfx_slider.value)
            self.audio.set_sfx_volume(self.sfx_slider.value)

        return None
    
    def draw(self):
        self.screen.fill((10, 10, 30))
        title = self.font_large.render("SETTINGS", True, (255, 100, 200))
        title_rect = title.get_rect(center=(600, 80))
        self.screen.blit(title, title_rect)
        self.draw_label("Music Volume", 300, 200)
        self.music_slider.draw(self.screen)
        self.draw_value_text(f"{int(self.music_slider.value * 100)}%", 620, 220)
        
        self.draw_label("SFX Volume", 300, 270)
        self.sfx_slider.draw(self.screen)
        self.draw_value_text(f"{int(self.sfx_slider.value * 100)}%", 620, 290)
        
        self.music_toggle.draw(self.screen, self.font_small)
        self.sfx_toggle.draw(self.screen, self.font_small)
        self.particles_toggle.draw(self.screen, self.font_small)

        self.back_button.draw(self.screen, self.font_medium)    
    def draw_label(self, text, x, y):
        label = self.font_small.render(text, True, (200, 200, 200))
        self.screen.blit(label, (x, y))
    
    def draw_value_text(self, text, x, y):
        value = self.font_small.render(text, True, (255, 255, 255))
        self.screen.blit(value, (x, y))

class Slider:
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.dragging = False
        self.handle_radius = 10
    def update(self, mouse_pos):

        if self.dragging:
            relative_x = max(0, min(mouse_pos[0] - self.rect.x, self.rect.width))
            self.value = relative_x / self.rect.width
    
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 80), self.rect, border_radius=5)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, 
                                self.rect.width * self.value, self.rect.height)
        pygame.draw.rect(screen, (200, 50, 150), fill_rect, border_radius=5)
        handle_x = self.rect.x + self.rect.width * self.value
        pygame.draw.circle(screen, (255, 100, 200), 
                          (int(handle_x), self.rect.centery), 
                          self.handle_radius)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(handle_x), self.rect.centery), 
                          self.handle_radius, 2)