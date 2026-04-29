import arcade
import random
import os
 
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 800
WINDOW_TITLE = "RUNNING PIGGEN"
 
FRAME_WIDTH = 64
FRAME_HEIGHT = 64
FRAME_COUNT = 8
FRAME_ROW = 0
FRAME_DURATION = 0.07
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 

# Stati del gioco
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"
 
 
class GameView(arcade.Window):
 
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()
 
        self.setup()
 
        self.direction = [0, 0]
        self.camera = arcade.Camera2D(position=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), zoom=1)
 
        self.score = 0
        self.high_score = 0
 
        self.base_speed = 500
        self.speed = self.base_speed
 
        self.boost_active = False
        self.boost_timer = 0
        self.obstacles_for_boost = 0
        self.ostacoli_contati = []
 
        self.state = STATE_MENU
 
        # Animazione personaggio
        self.run_textures = []
        self._load_run_textures()
        self.current_frame = 0
        self.frame_timer = 0.0
 
        # Animazione game over
        self.gameover_timer = 0.0
        self.gameover_duration = 3.0
        self.gameover_alpha = 0
        self.gameover_scale = 3.0
        self.show_restart_prompt = False
 
    def _load_run_textures(self):
        spritesheet = arcade.load_spritesheet(os.path.join(BASE_DIR, "run.png"))
        for i in range(FRAME_COUNT):
            texture = spritesheet.get_texture(
                arcade.LBWH(
                    i * FRAME_WIDTH,
                    FRAME_ROW * FRAME_HEIGHT,
                    width=FRAME_WIDTH,
                    height=FRAME_HEIGHT
                )
            )
            self.run_textures.append(texture)
 
    def spawn_obstacle(self):
        obstacle = arcade.Sprite(os.path.join(BASE_DIR, "ostacles.png"), scale=0.4)
        obstacle.center_x = random.randrange(50, WINDOW_WIDTH - 50)
        obstacle.center_y = self.sprite.center_y + WINDOW_HEIGHT
        obstacle.passed = False
        self.obstacle_list.append(obstacle)
 
    def setup(self):
        self.sprite = arcade.Sprite(scale=2.3)
        self.obstacle_list = arcade.SpriteList()
        self.spawn_timer = 0
        self.sprite.center_x = WINDOW_WIDTH / 2
        self.sprite.center_y = 100
        self.background = arcade.load_texture("./sfondo.jpg")
        self.playerSpriteList.append(self.sprite)
 
    def reset(self):
        self.score = 0
        self.sprite.center_x = WINDOW_WIDTH / 2
        self.sprite.center_y = 100
        self.obstacle_list.clear()
        self.spawn_timer = 0
        self.speed = self.base_speed
        self.boost_active = False
        self.boost_timer = 0
        self.obstacles_for_boost = 0
        self.ostacoli_contati = []
        self.current_frame = 0
        self.frame_timer = 0.0
 
    def start_gameover(self):
        self.state = STATE_GAMEOVER
        self.gameover_timer = 0.0
        self.gameover_alpha = 0
        self.gameover_scale = 3.0
        self.show_restart_prompt = False
 
    def on_draw(self):
        self.clear()
 
        # ---- MENU ----
        if self.state == STATE_MENU:
            arcade.draw_text(
                "RUNNING PIGGEN",
                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 80,
                arcade.color.YELLOW, 40,
                anchor_x="center", bold=True
            )
            arcade.draw_text(
                "Premi SPACE per iniziare",
                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                arcade.color.WHITE, 28,
                anchor_x="center"
            )
            arcade.draw_text(
                f"High Score: {self.high_score}",
                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60,
                arcade.color.YELLOW, 22,
                anchor_x="center"
            )
            return
 
        # ---- SFONDO E SPRITE ----
        with self.camera.activate():
            cam_y = self.camera.position[1]
            base_y = (cam_y // WINDOW_HEIGHT) * WINDOW_HEIGHT
            for offset in (-1, 0, 1):
                arcade.draw_texture_rect(
                    self.background,
                    arcade.LBWH(0, base_y + offset * WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
                )
            self.playerSpriteList.draw()
            self.obstacle_list.draw()
 
        arcade.draw_text(f"Score: {self.score}", 20, 750, arcade.color.WHITE, 20)
        arcade.draw_text(f"High Score: {self.high_score}", 20, 725, arcade.color.YELLOW, 20)
 
        # ---- OVERLAY GAME OVER ----
        if self.state == STATE_GAMEOVER:
 
            # Sfondo scuro semi-trasparente
            overlay_alpha = min(180, int(self.gameover_timer / self.gameover_duration * 180))
            arcade.draw_rect_filled(
                arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT),
                (0, 0, 0, overlay_alpha)
            )
 
            # Testo GAME OVER con fade in e zoom out
            alpha = min(255, self.gameover_alpha)
            scale = max(1.0, self.gameover_scale)
            font_size = min(int(55 * scale), 160)
 
            arcade.draw_text(
                "GAME OVER",
                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40,
                (220, 30, 30, alpha),
                font_size,
                anchor_x="center", anchor_y="center",
                bold=True
            )
 
            # Punteggio (appare dopo il testo principale)
            if self.gameover_alpha > 100:
                score_alpha = min(255, (self.gameover_alpha - 100) * 3)
                arcade.draw_text(
                    f"Punteggio: {self.score}",
                    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60,
                    (255, 255, 255, score_alpha),
                    26, anchor_x="center", bold=True
                )
                arcade.draw_text(
                    f"High Score: {self.high_score}",
                    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100,
                    (255, 215, 0, score_alpha),
                    22, anchor_x="center"
                )
 
            # Prompt lampeggiante dopo gameover_duration secondi
            if self.show_restart_prompt:
                blink = int(self.gameover_timer * 2) % 2 == 0
                if blink:
                    arcade.draw_text(
                        "Premi SPACE per riprovare",
                        WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 160,
                        arcade.color.WHITE,
                        22, anchor_x="center"
                    )
 
    def on_update(self, delta_time):
 
        # ---- AGGIORNAMENTO GAME OVER ----
        if self.state == STATE_GAMEOVER:
            self.gameover_timer += delta_time
            progress = min(1.0, self.gameover_timer / 0.8)
            self.gameover_alpha = int(progress * 255)
            self.gameover_scale = 3.0 - (2.0 * progress)  # zoom out: 3.0 → 1.0
            if self.gameover_timer >= self.gameover_duration:
                self.show_restart_prompt = True
            return
 
        if self.state != STATE_PLAYING:
            return
 
        HORIZONTAL_SPEED = 550
 
        # Animazione
        self.frame_timer += delta_time
        if self.frame_timer >= FRAME_DURATION:
            self.frame_timer = 0.0
            self.current_frame = (self.current_frame + 1) % FRAME_COUNT
        if self.run_textures:
            self.sprite.texture = self.run_textures[self.current_frame]
 
        self.sprite.center_y += self.speed * delta_time
        self.sprite.center_x += self.direction[0] * HORIZONTAL_SPEED * delta_time
 
        if self.sprite.left < 0:
            self.sprite.left = 0
        if self.sprite.right > WINDOW_WIDTH:
            self.sprite.right = WINDOW_WIDTH
 
        self.camera.position = (WINDOW_WIDTH / 2, self.sprite.center_y)
 
        self.spawn_timer += delta_time
        if self.spawn_timer > 0.8:
            self.spawn_obstacle()
            self.spawn_timer = 0
 
        for obstacle in self.obstacle_list:
            if not obstacle.passed and obstacle.center_y < self.sprite.center_y:
                obstacle.passed = True
                self.score += 1
 
                if not self.boost_active:
                    if obstacle not in self.ostacoli_contati:
                        self.obstacles_for_boost += 1
                        self.ostacoli_contati.append(obstacle)
 
                    if self.obstacles_for_boost >= 15:
                        self.boost_active = True
                        self.boost_timer = 5
                        self.speed = self.base_speed * 1.6
                        self.obstacles_for_boost = 0
 
            if self.score > self.high_score:
                self.high_score = self.score
 
            if obstacle.center_y < self.sprite.center_y - WINDOW_HEIGHT:
                obstacle.remove_from_sprite_lists()
 
        if arcade.check_for_collision_with_list(self.sprite, self.obstacle_list):
            self.start_gameover()
 
        if self.boost_active:
            self.boost_timer -= delta_time
            if self.boost_timer <= 0:
                self.boost_active = False
                self.speed = self.base_speed
 
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.state == STATE_MENU:
                self.state = STATE_PLAYING
            elif self.state == STATE_GAMEOVER and self.show_restart_prompt:
                self.reset()
                self.state = STATE_MENU
 
        if key == arcade.key.RIGHT:
            self.direction[0] = 1
        if key == arcade.key.LEFT:
            self.direction[0] = -1
 
    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.direction[0] = 0
        if key == arcade.key.LEFT:
            self.direction[0] = 0
 
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass
 
    def on_mouse_press(self, x, y, button, key_modifiers):
        pass
 
    def on_mouse_release(self, x, y, button, key_modifiers):
        pass
 
 
def main():
    game = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, "RUNNING PIGGEN")
    arcade.run()
 
 
if __name__ == "__main__":
    main()