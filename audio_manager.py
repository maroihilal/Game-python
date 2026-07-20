import pygame
import os
from typing import Dict, Optional

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_files = {
            'jump': 'jump.mp3',
            'coin': 'coin.mp3',
            'button_click': 'button_click.mp3',
            'game_over': 'game_over.mp3',
            'pause': 'pause.mp3',
            'resume': 'resume.mp3',
            'obstacle_hit': 'obstacle_hit.mp3',
            'powerup': 'powerup.mp3',
        }
        
        self.music_files = {
            'menu': 'menu_music.mp3',
            'gameplay': 'gameplay_music.mp3',
        }
        
        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self.current_music: Optional[str] = None
        self.music_loaded: bool = False
        self._music_volume = 0.7
        self._sfx_volume = 0.7
        
        self.load_all_sounds()
        
    def load_all_sounds(self):
        print("🎵 Loading audio files...")
        print("-" * 40)
        for name, filename in self.sound_files.items():
            self.load_sound(name, filename)
        for name, filename in self.music_files.items():
            self.load_music(name, filename)
        print("-" * 40)
        print("✅ Audio loading complete!")
        
    def load_sound(self, name: str, filename: str) -> Optional[pygame.mixer.Sound]:
        path = os.path.join("assets", "sounds", filename)
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self._sfx_volume)
                self.sounds[name] = sound
                print(f"  ✅ Loaded: {filename}")
                return sound
            else:
                self.sounds[name] = None
                print(f"  ⚠️  Warning: Sound file not found: {path}")
                return None
        except Exception as e:
            self.sounds[name] = None
            print(f"  ❌ Error loading {filename}: {e}")
            return None
    
    def load_music(self, name: str, filename: str) -> bool:
        path = os.path.join("assets", "sounds", filename)
        
        try:
            if os.path.exists(path):
                self.sounds[f"music_{name}"] = path
                print(f"  ✅ Loaded music: {filename}")
                return True
            else:
                self.sounds[f"music_{name}"] = None
                print(f"  ⚠️  Warning: Music file not found: {path}")
                return False
        except Exception as e:
            self.sounds[f"music_{name}"] = None
            print(f"  ❌ Error loading music {filename}: {e}")
            return False
    
    def play_sound(self, name: str) -> bool:
        if name not in self.sounds:
            print(f"⚠️  Sound '{name}' not found")
            return False
        
        sound = self.sounds[name]
        if sound:
            try:
                sound.play()
                return True
            except Exception as e:
                print(f"❌ Error playing sound '{name}': {e}")
                return False
        return False
    
    def play_music(self, name: str, loop: bool = True) -> bool:
        """Play background music"""
        music_key = f"music_{name}"
        
        if music_key not in self.sounds:
            print(f"⚠️  Music '{name}' not found")
            return False
        
        music_path = self.sounds[music_key]
        if music_path:
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self._music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = name
                self.music_loaded = True
                return True
            except Exception as e:
                print(f"❌ Error playing music '{name}': {e}")
                return False
        return False
    
    def stop_music(self):
        try:
            pygame.mixer.music.stop()
            self.music_loaded = False
            return True
        except:
            return False
    
    def pause_music(self):
        try:
            pygame.mixer.music.pause()
            return True
        except:
            return False
    
    def unpause_music(self):
        try:
            pygame.mixer.music.unpause()
            return True
        except:
            return False
    
    def set_music_volume(self, volume: float):
        self._music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self._music_volume)
        except:
            pass
    
    def set_sfx_volume(self, volume: float):
        self._sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound and isinstance(sound, pygame.mixer.Sound):
                try:
                    sound.set_volume(self._sfx_volume)
                except:
                    pass
    
    def get_music_volume(self) -> float:
        return self._music_volume
    
    def get_sfx_volume(self) -> float:
        return self._sfx_volume
    
    def is_music_playing(self) -> bool:
        try:
            return pygame.mixer.music.get_busy()
        except:
            return False
    
    def stop_all(self):
        try:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        except:
            pass
    
    def play_jump(self):
        self.play_sound('jump')
    
    def play_coin(self):
        self.play_sound('coin')
    
    def play_click(self):
        self.play_sound('button_click')
    
    def play_game_over(self):
        self.play_sound('game_over')
    
    def play_pause(self):
        self.play_sound('pause')
    
    def play_resume(self):
        self.play_sound('resume')
    
    def play_obstacle_hit(self):
        self.play_sound('obstacle_hit')
    
    def play_powerup(self):
        self.play_sound('powerup')
    
    def play_menu_music(self):
        self.play_music('menu')

    def play_gameplay_music(self):
        self.play_music('gameplay')