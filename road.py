# road.py
import pygame
import math

class Road:
    def __init__(self):
        self.scroll = 0
        self.road_width = 600  
        self.top_width = 200   
        self.lane_count = 3
        self.lane_width = self.road_width // self.lane_count
        

        self.road_color = (20, 20, 40)
        self.lane_color = (255, 100, 200) 
        self.edge_color = (200, 50, 150)   
        self.glow_color = (255, 100, 200)
        

        self.start_y = 350 
        self.end_y = 700    

        self.lane_positions = self.calculate_lane_positions()
        


        self.markings = []
        self.generate_markings()
    
    def calculate_lane_positions(self):
        road_left = (1200 - self.road_width) // 2
        positions = []
        for i in range(self.lane_count):
            center_x = road_left + (i + 0.5) * self.lane_width
            positions.append(center_x)
        return positions
    
    def generate_markings(self):
        self.markings = []
        for i in range(50):
            y = self.start_y + i * 15
            if y < self.end_y:
                self.markings.append(y)
    
    def update(self, speed):
        self.scroll += speed * 2
        for i in range(len(self.markings)):
            self.markings[i] += speed * 2
            if self.markings[i] > self.end_y:
                self.markings[i] = self.start_y - 20
    
    def get_lane_x(self, lane_index, y_pos):
        if lane_index < 0 or lane_index >= self.lane_count:
            return 600
        progress = (y_pos - self.start_y) / (self.end_y - self.start_y)
        progress = max(0, min(1, progress))
        road_width = self.top_width + (self.road_width - self.top_width) * progress
        lane_width = road_width / self.lane_count
        road_left = (1200 - road_width) // 2
        return road_left + (lane_index + 0.5) * lane_width
    
    def get_road_bounds(self, y_pos):
        progress = (y_pos - self.start_y) / (self.end_y - self.start_y)
        progress = max(0, min(1, progress))
        road_width = self.top_width + (self.road_width - self.top_width) * progress
        road_left = (1200 - road_width) // 2
        road_right = road_left + road_width
        return road_left, road_right
    
    def draw(self, screen):
        for y in range(int(self.start_y), int(self.end_y), 2):
            progress = (y - self.start_y) / (self.end_y - self.start_y)
            road_width = self.top_width + (self.road_width - self.top_width) * progress
            road_left = (1200 - road_width) // 2
            road_right = road_left + road_width
            color_factor = 0.5 + progress * 0.5
            color = (int(15 * color_factor), int(15 * color_factor), int(35 * color_factor))
            pygame.draw.line(screen, color, (road_left, y), (road_right, y), 2)
        for marking_y in self.markings:
            if self.start_y <= marking_y <= self.end_y:
                progress = (marking_y - self.start_y) / (self.end_y - self.start_y)
                road_width = self.top_width + (self.road_width - self.top_width) * progress
                road_left = (1200 - road_width) // 2
                
                for lane in range(1, self.lane_count):
                    lane_x = road_left + lane * (road_width / self.lane_count)
                    if int(marking_y / 20) % 2 == 0:
                        pygame.draw.line(screen, self.lane_color, 
                                       (lane_x, marking_y - 8), 
                                       (lane_x, marking_y + 8), 3)
        for y in range(int(self.start_y), int(self.end_y), 5):
            progress = (y - self.start_y) / (self.end_y - self.start_y)
            road_width = self.top_width + (self.road_width - self.top_width) * progress
            road_left = (1200 - road_width) // 2
            road_right = road_left + road_width
            pygame.draw.line(screen, self.edge_color, (road_left, y), (road_left, y+5), 3)
            pygame.draw.line(screen, self.edge_color, (road_right, y), (road_right, y+5), 3)
            if progress > 0.3:
                glow_alpha = int(30 * progress)
                glow_surf = pygame.Surface((10, 5), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.glow_color[:3], glow_alpha), (0, 0, 10, 5))
                screen.blit(glow_surf, (road_left - 5, y))
                screen.blit(glow_surf, (road_right - 5, y))
        glow_surf = pygame.Surface((self.road_width + 200, 100), pygame.SRCALPHA)
        for i in range(20):
            alpha = 10 - i // 2
            width = self.road_width + i * 20
            pygame.draw.ellipse(glow_surf, (255, 100, 200, alpha), 
                              ((glow_surf.get_width() - width) // 2, 0, width, 100))
        screen.blit(glow_surf, ((1200 - glow_surf.get_width()) // 2, self.start_y - 50))