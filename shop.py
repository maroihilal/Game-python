import pygame
import json
import os

class Shop:
    def __init__(self):
        self.items = self.load_items()
        self.unlocked_items = []
        self.current_equipped = {}
        self.coins = 0
        
    def load_items(self):
        try:
            with open("save/shop_items.json", "r") as f:
                return json.load(f)
        except:
            items = {
                "outfits": [
                    {"id": 0, "name": "Classic", "price": 0, "color": "Pink"},
                    {"id": 1, "name": "Hoodie", "price": 100, "color": "Dark Pink"},
                    {"id": 2, "name": "Jacket", "price": 200, "color": "Blue"},
                    {"id": 3, "name": "Sportswear", "price": 300, "color": "Green"},
                    {"id": 4, "name": "Dress", "price": 400, "color": "Purple"},
                ],
                "shoes": [
                    {"id": 0, "name": "Sneakers", "price": 50},
                    {"id": 1, "name": "Boots", "price": 150},
                    {"id": 2, "name": "High Heels", "price": 200},
                ],
                "hairstyles": [
                    {"id": 0, "name": "Long Hair", "price": 0},
                    {"id": 1, "name": "Ponytail", "price": 100},
                    {"id": 2, "name": "Bun", "price": 150},
                    {"id": 3, "name": "Short Hair", "price": 200},
                ],
                "accessories": [
                    {"id": 0, "name": "None", "price": 0},
                    {"id": 1, "name": "Sunglasses", "price": 50},
                    {"id": 2, "name": "Necklace", "price": 75},
                    {"id": 3, "name": "Hat", "price": 100},
                ]
            }
            self.save_items(items)
            return items
    
    def save_items(self, items):
        os.makedirs("save", exist_ok=True)
        with open("save/shop_items.json", "w") as f:
            json.dump(items, f)
    
    def purchase_item(self, category, item_id, coins):
        if category in self.items:
            for item in self.items[category]:
                if item["id"] == item_id:
                    if coins >= item["price"]:
                        self.coins -= item["price"]
                        if "unlocked_" + category not in self.unlocked_items:
                            self.unlocked_items.append("unlocked_" + category)
                        return True
        return False
    
    def equip_item(self, category, item_id):
        self.current_equipped[category] = item_id
    
    def is_unlocked(self, category, item_id):
        return True

class ShopUI:
    def __init__(self, screen, shop):
        self.screen = screen
        self.shop = shop
        self.selected_category = "outfits"
        self.scroll_offset = 0
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.categories = ["outfits", "shoes", "hairstyles", "accessories"]
        self.category_positions = {}
        
    def draw(self, coins):

        self.screen.fill((10, 10, 30))

        title = self.font_large.render("SHOP", True, (255, 100, 200))
        title_rect = title.get_rect(center=(600, 60))
        self.screen.blit(title, title_rect)

        coins_text = self.font_medium.render(f"💰 {coins}", True, (255, 215, 0))
        coins_rect = coins_text.get_rect(center=(600, 120))
        self.screen.blit(coins_text, coins_rect)

        self.draw_categories()
        self.draw_items(coins)
        pygame.draw.rect(self.screen, (200, 50, 150), (1050, 20, 120, 50), border_radius=15)
        close_text = self.font_small.render("Close", True, (255, 255, 255))
        close_rect = close_text.get_rect(center=(1110, 45))
        self.screen.blit(close_text, close_rect)
    
    def draw_categories(self):
        y = 170
        x = 100
        for i, category in enumerate(self.categories):
            color = (200, 50, 150) if category == self.selected_category else (50, 50, 100)
            rect = pygame.Rect(x + i * 250, y, 200, 50)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            
            
            text = self.font_small.render(category.upper(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
            self.category_positions[category] = rect
    
    def draw_items(self, coins):
        items = self.shop.items.get(self.selected_category, [])
        
        y = 240
        for i, item in enumerate(items):
        
            x = 100 + (i % 4) * 250
            row = i // 4
            y_pos = y + row * 80
            
            is_unlocked = self.shop.is_unlocked(self.selected_category, item["id"])
            is_equipped = self.shop.current_equipped.get(self.selected_category) == item["id"]
            
            if is_equipped:
                color = (50, 150, 50)
            elif is_unlocked:
                color = (50, 50, 100)
            else:
                color = (40, 40, 40)
            
            rect = pygame.Rect(x, y_pos, 200, 60)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            
            
            name_text = self.font_small.render(item["name"], True, (255, 255, 255))
            self.screen.blit(name_text, (x + 10, y_pos + 5))
            
            if is_equipped:
                status = "EQUIPPED"
                status_color = (0, 255, 0)
            elif is_unlocked:
                status = "EQUIP"
                status_color = (100, 200, 255)
            else:
                status = f"{item['price']} coins"
                status_color = (255, 215, 0)
            
            status_text = self.font_small.render(status, True, status_color)
            self.screen.blit(status_text, (x + 10, y_pos + 30))

            item["rect"] = rect