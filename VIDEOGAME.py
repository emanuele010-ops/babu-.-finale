"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 800
WINDOW_TITLE = "RUNNING CHIKEN"
CAM_VEL = 100
SCROLL_SPEED = 50


class GameView(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()
    
        self.setup()

        self.direction = [0, 0]
         
        self.camera = arcade.Camera2D (position=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),zoom=1)
        self.cam_dir = [0, 0]
        self.score = 0

        self.score = 0
        self.high_score = 0

    def spawn_obstacle(self):

        obstacle = arcade.Sprite("./ostacles.png", scale=0.4)

        # posizione casuale orizzontale
        obstacle.center_x = random.randrange(50, WINDOW_WIDTH - 50)

        # spawn sopra la camera
        obstacle.center_y = self.sprite.center_y + WINDOW_HEIGHT

        self.obstacle_list.append(obstacle)


    def setup(self):
        
        self.sprite = arcade.Sprite("./pollo.png")
        
        self.obstacle_list = arcade.SpriteList("./ostacles.png")
        self.spawn_timer = 0

        self.sprite.center_x = 100
        self.sprite.center_y = 100
        self.sprite.scale_x = 0.35
        self.sprite.scale_y = 0.35

        
        self.background = arcade.load_texture("../sfondo.jpg")
        self.background_y = 0
        self.playerSpriteList.append(self.sprite)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        with self.camera.activate():

            cam_y = self.camera.position[1]

            # Trova il blocco di sfondo corrente
            base_y = (cam_y // WINDOW_HEIGHT) * WINDOW_HEIGHT

            for offset in (-1, 0, 1):
                arcade.draw_texture_rect(
                    self.background,
                    arcade.LBWH(
                        0,
                        base_y + offset * WINDOW_HEIGHT,
                        WINDOW_WIDTH,
                        WINDOW_HEIGHT
                    )
                )

            self.playerSpriteList.draw()
            self.obstacle_list.draw()



        arcade.draw_text(
    f"Ostacoli schivati: {self.score}",
    20,
    500,
    arcade.color.WHITE,
    20
)

        arcade.draw_text(
            f"Score: {self.score}",
            20,
            450,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"High Score: {self.high_score}",
            20,
            320,
            arcade.color.YELLOW,
            20
        )

                


                

    def on_update(self, delta_time):

        SPEED = 500
        HORIZONTAL_SPEED = 550

        # Movimento automatico verso l'alto
        self.sprite.center_y += SPEED * delta_time

        # Movimento destra/sinistra
        self.sprite.center_x += self.direction[0] * HORIZONTAL_SPEED * delta_time

        # Limiti dello schermo
        if self.sprite.left < 0:
            self.sprite.left = 0

        if self.sprite.right > WINDOW_WIDTH:
            self.sprite.right = WINDOW_WIDTH

        # Camera segue il player
        self.camera.position = (
            WINDOW_WIDTH / 2,
            self.sprite.center_y
        )

                # spawn ostacoli
        self.spawn_timer += delta_time

        if self.spawn_timer > 0.8:
            self.spawn_obstacle()
            print(len(self.obstacle_list))
            self.spawn_timer = 0

        # collisioni
        if arcade.check_for_collision_with_list(self.sprite, self.obstacle_list):
            if self.score > self.high_score:
                self.high_score = self.score
                print("GAME OVER")

                self.close()

        for obstacle in self.obstacle_list:
    
            # se l'ostacolo è sotto il player significa che è stato schivato
            if obstacle.center_y < self.sprite.center_y - 50:
                self.score += 1
                obstacle.remove_from_sprite_lists()   

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.RIGHT:
            self.direction[0] = 1
        if key == arcade.key.LEFT:
            self.direction[0] = -1

    def on_key_release(self, key, modifiers):

        if key == arcade.key.RIGHT:
            self.direction[0] = 0
        if key == arcade.key.LEFT:
            self.direction[0] = 0
    

        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    game = GameView(
        WINDOW_WIDTH, WINDOW_HEIGHT, "RUNNIG CHIKEN"
    )
    arcade.run()




if __name__ == "__main__":
    main()