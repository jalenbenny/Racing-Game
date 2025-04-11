import pygame
import random
#from utils import Chariot, ShieldPowerUp
from utils import Chariot, AIOpponent, ShieldPowerUp, SpeedBoost, PowerUp, Arrow
#from track_data import TRACK_DETAILS

WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)

#new
TRACK_DETAILS = { 
    "assets/colosseum_track.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        #right, left, top, bottom, middle
        "bounds": [pygame.Rect(850, 50, 750, 700), pygame.Rect(0, 50, 250, 700), pygame.Rect(80, 0, 750, 140), pygame.Rect(25, 775, 800, 50), pygame.Rect(450, 260, 200, 350)],
        "ai_path": [(500, 680), (670, 620), (700, 500), (720, 400), (700, 230), (500, 150), (360, 200), (300, 300), (300, 500), (400, 640)]
      
    },
    "assets/greektracks.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        # right, left, top, bottom, middle, upper right, upper left.
        "bounds": [pygame.Rect(850, 50, 750, 700), pygame.Rect(0, 50, 250, 700), pygame.Rect(80, 0, 750, 130), pygame.Rect(25, 750, 800, 50), pygame.Rect(450, 260, 210, 350), pygame.Rect(800, 50, 700, 300), pygame.Rect(0, 50, 300, 300)], 
        "ai_path": [(500, 680), (670, 620), (700, 550), (700, 500), (720, 400), (690, 230), (510, 155), (370, 200), (320, 300), (310, 500), (350, 590), (400, 640)]
    },
     "assets/modern_track.png": {
        "start": (460, 630),
        "finish": pygame.Rect(450, 550, 85, 20),
        #right, top, left, bottom, bottom right, inside top rec, middle inside rec, middle left inside, bottom inside horizontal rec, very bottom inside, rightside indent outside, leftside indent outside
        "bounds": [pygame.Rect(960, 0, 300, 800), pygame.Rect(0, 0, 1250, 50), pygame.Rect(0, 0, 350, 1250), pygame.Rect(0, 790, 980, 160), pygame.Rect(350, 555, 80, 300), pygame.Rect(480, 140, 350, 100), pygame.Rect(615, 250, 210, 180), pygame.Rect(480, 400, 180, 70), pygame.Rect(560, 480, 70, 230), pygame.Rect(630, 710, 200, 8), pygame.Rect(770, 520, 200, 120), pygame.Rect(340, 320, 160, 7)],
        "ai_path": [(460, 630), (480, 730), (810, 730), (865, 705), (820, 650), (690, 650), (690, 450), (880, 450), (880, 80), (400, 80), (400, 250), (450, 270), (500, 300), (450, 330), (400, 350), (400, 450), (450, 500)]
    },
    "assets/ancient_greece.png": {
        "start": (800, 300),
        "finish": pygame.Rect(540, 320, 50, 20),
        #right, top, left, bottom, bottom right corner, top right corner, top left corner, bottom left corner
        "bounds": [pygame.Rect(980, 150, 700, 500), pygame.Rect(0, 0, 980, 160), pygame.Rect(0, 0, 100, 800), pygame.Rect(0, 770, 980, 160), pygame.Rect(970, 650, 980, 160), pygame.Rect(950, 670, 980, 160), pygame.Rect(950, 710, 980, 160), pygame.Rect(900, 700, 980, 160), pygame.Rect(880, 250, 400, 55), pygame.Rect(810, 150, 400, 50), pygame.Rect(200, 160, 60, 50), pygame.Rect(100, 210, 60, 70), pygame.Rect(100, 280, 40, 40), pygame.Rect(100, 600, 30, 200), pygame.Rect(100, 680, 50, 200), pygame.Rect(100, 740, 140, 50), pygame.Rect(780, 740, 400, 50), pygame.Rect(785, 420, 80, 150), pygame.Rect(240, 450, 80, 160), pygame.Rect(260, 350, 75, 100), pygame.Rect(330, 260, 45, 100), pygame.Rect(350, 240, 380, 1), pygame.Rect(680, 260, 40, 60), pygame.Rect(490, 530, 120, 60), pygame.Rect(350, 675, 400, 1), pygame.Rect(680, 350, 13, 170)],    #, pygame.Rect(960, 660, 980, 160)
        "ai_path": [(800, 300), (750, 220), (730, 190), (700, 180), (550, 180), (350, 180), (280, 220), (220, 300), (150, 400), (130, 500), (180, 600), (330, 695), (700, 695), (850, 630), (890, 590), (900, 380), (800, 350), (720, 395), (700, 580), (620, 620), (450, 630), (340, 580), (340, 480), (430, 250), (500, 235), (620, 280), (510, 480)]
    }
    
}


class RaceScreen:
    def __init__(self, screen, track_image_path, selected_chariot, game_mode):
        self.screen = screen
        self.track_img = pygame.image.load(track_image_path)
        self.track_img = pygame.transform.scale(self.track_img, (1100, 850))
        self.selected_chariot = selected_chariot  # Store selected chariot

        self.game_mode = game_mode  # Store the mode

        self.falling_objects = []  # Objects in survival mode
        self.arrows = []  # Add this line to store arrows

        """
        # Apply chariot abilities
        if self.selected_chariot == "health":
            self.player_health = 120  # Default is 100
        elif self.selected_chariot == "speed":
            self.player_speed = 5.5  # Default is 5
        elif self.selected_chariot == "bullets":
            self.player_bullets = 2  # Default is 0
        """

        if track_image_path == "assets/modern_track.png":
            self.track_img = pygame.transform.scale(self.track_img, (1300, 850))


        # Ensure track details exist
        if track_image_path not in TRACK_DETAILS:
            raise ValueError(f"Track details not found for: {track_image_path}")

      
        self.track_data = TRACK_DETAILS[track_image_path] #new
        #self.player = Chariot(*self.track_data["start"])  # Spawn at track's start position
        self.start_pos = self.track_data["start"]
        self.finish_zone = self.track_data["finish"]
        self.track_bounds = self.track_data["bounds"]
        self.ai_path = self.track_data.get("ai_path", [])
       # self.player.laps = 0
        # Exit Button
        #newwwww
        self.player = Chariot(*self.start_pos, chariot_type=selected_chariot)

        #self.player = Chariot(*self.start_pos)
        self.ai_opponents = [AIOpponent(self.start_pos[0] + (i * 50), self.start_pos[1], self.ai_path, i) for i in range(4)]
        #self.ai_opponents = [AIOpponent(self.start_pos[0] + (i * 50), self.start_pos[1]) for i in range(4)]
        self.powerups = self.generate_powerups()

        self.exit_button = pygame.Rect(20, 720, 150, 50)
        self.font = pygame.font.Font(None, 36)

        
        if self.game_mode == "survival":
            self.obstacles = [
                pygame.Rect(random.randint(300,  800), random.randint(50, 1050), 40, 40)
                for _ in range(50)
            ]
        
    def spawn_falling_objects(self):
        """Spawn objects in survival mode."""
        if random.random() < 0.02:  # 2% chance per frame
            x = random.randint(50, 1000)
            self.falling_objects.append(pygame.Rect(x, 0, 30, 30))

    def move_falling_objects(self):
        """Move and detect collisions."""
        for obj in self.falling_objects[:]:
            obj.y += 5
            pygame.draw.rect(self.screen, RED, obj)
            if obj.y > 850:
                self.falling_objects.remove(obj)
            elif self.player.rect.colliderect(obj):
                if not self.player.shield_active:
                    self.player.health -= 10
                self.falling_objects.remove(obj)

    def spawn_arrows(self):
        """Spawn arrows from different sides in survival mode."""
        if random.random() < 0.01:  # 1% chance per frame
            # Randomly choose a direction
            direction = random.choice(["right", "left", "up", "down"])
            
            if direction == "right":
                x, y = 0, random.randint(100, 700)
            elif direction == "left":
                x, y = 1000, random.randint(100, 700)
            elif direction == "up":
                x, y = random.randint(100, 900), 800
            elif direction == "down":
                x, y = random.randint(100, 900), 0
                
            # Create and add the arrow
            arrow = Arrow(x, y, direction)
            self.arrows.append(arrow)

    def move_arrows(self):
        """Move arrows and check for collisions."""
        for arrow in self.arrows[:]:
            arrow.move()
            arrow.draw(self.screen)
            
            # Check for collision with player
            if self.player.rect.colliderect(arrow.rect):
                if not self.player.shield_active:
                    self.player.health -= 15  # More damage than regular obstacles
                self.arrows.remove(arrow)
            
            # Remove arrows that are off-screen
            elif arrow.is_off_screen(1000, 800):
                self.arrows.remove(arrow)


    def draw_exit_button(self):
        pygame.draw.rect(self.screen, RED, self.exit_button)
        text = self.font.render("Exit", True, WHITE)
        self.screen.blit(text, (self.exit_button.x + 50, self.exit_button.y + 10))
        


    def generate_powerups(self):
        powerups = []
        while len(powerups) < 3:
            x, y = random.randint(100, 900), random.randint(100, 700)
            # Ensure power-ups only spawn inside the track (not inside boundary areas)
            valid = all(not bound.collidepoint(x, y) for bound in self.track_bounds)

            if valid:
                powerups.append(random.choice([ShieldPowerUp(x, y), SpeedBoost(x, y)]))
        return powerups
    
    def draw_health_bar(self, surface, health):
        max_health = 100  # Assuming max health is 100
        bar_width = 200  # Total bar width
        bar_height = 20  # Height of the health bar
        x, y = 10, 10  # Top-right corner

        health_ratio = max(health / max_health, 0)  # Prevent negative health
        #pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))  # Red background
        pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * health_ratio, bar_height))  # Green foreground
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)  # White border



    def run_survival_mode(self):
        """Handles survival mode where player avoids obstacles for a time limit."""
        self.screen.blit(self.player, self.obstacles)

        # Spawn obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, RED, obstacle)

        # Check for collision with obstacles
        for obstacle in self.obstacles:
            if self.player_rect.colliderect(obstacle):
                self.player.health -= 10
                #return "lose"

        # If time runs out, player wins
        if self.player.health <= 0:
            return "lose"
        if self.player.laps >= 5:
            return "win"

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(30)
            self.screen.fill(WHITE)
            self.screen.blit(self.track_img, (0, 0))

            #if self.game_mode == "survival":
            #    self.run_survival_mode()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.collidepoint(event.pos):
                        return "exit"  # Go back to home screen
                

            keys = pygame.key.get_pressed()
            self.player.move(keys, self.track_bounds)
            #self.player.move(keys)
            self.player.check_collision(self.track_bounds) #new
    
            
            # AI Movement / new
            for ai in self.ai_opponents:
                ai.move(self.track_bounds)
            

            # Power-ups
            for powerup in self.powerups[:]:
                if self.player.rect.colliderect(powerup):
                    #self.player.activate_shield()
                    powerup.apply_effect(self.player) # new
                    self.powerups.remove(powerup)
                    #self.powerups.respawn(powerup)

            # Draw elements
            #self.player.draw(self.screen)
            #for powerup in self.powerups:
            #    powerup.draw(self.screen)

                # Draw Exit Button
            self.draw_exit_button()

            # Draw health bar
            self.draw_health_bar(self.screen, self.player.health)

            
            if self.game_mode == "survival":
                self.spawn_falling_objects()
                self.move_falling_objects()
                self.spawn_arrows()  # Add arrows in survival mode
                self.move_arrows()
                
                
                
                


            # Draw all elements / new
            self.player.draw(self.screen)
            for ai in self.ai_opponents:
                ai.draw(self.screen)

            for powerup in self.powerups: #new
                powerup.draw(self.screen)

            # Check lap completion / new
            if self.player.rect.colliderect(self.finish_zone):
                self.player.laps += 1
                print(f"Player Laps: {self.player.laps}")
              
            # Check if AI crosses the finish line
            for ai in self.ai_opponents:
                if ai.rect.colliderect(self.finish_zone):
                    ai.laps += 1
                    print(f"AI Laps: {ai.laps}")
            
            # Check game over conditions
            if self.player.health <= 0:
                print("Game Over! You lost!")
                return "lose"

            if self.player.laps >= 50:
            #NO /if self.player.rect.colliderect(self.finish_zone): #new
                print("Congratulations! You won!")
                return "win"
            
            
            for ai in self.ai_opponents:
                if ai.laps >= 55:
                    print("AI wins! You lost.")
                    return "lose"
            pygame.draw.rect(self.screen, (200, 0, 0), self.finish_zone) # new

            pygame.display.update()
