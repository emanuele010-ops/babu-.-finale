"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

WINDOW_WIDTH = 540
WINDOW_HEIGHT = 800
WINDOW_TITLE = "RUNNING CIKEN"
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
        


    def setup(self):
        
        self.sprite = arcade.Sprite("./pollo.png")

        self.sprite.center_x = 100
        self.sprite.center_y = 100
        self.sprite.scale_x = 0.35
        self.sprite.scale_y = 0.35

        
        self.background = arcade.load_texture("../sfondo.jpg")

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
            # per 3 volte, a partire da self.inizio_coordinate_sfondo
            arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0,-WINDOW_HEIGHT/2,WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0,WINDOW_HEIGHT/2,WINDOW_WIDTH, WINDOW_HEIGHT)
            )
                    
                    
            self.playerSpriteList.draw()

                


                # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # se la posizione del giocatore è "troppo in alto" rispetto alla posizione prec
            # imposto la coordinata di partenza di dove disegnare lo sfondo 
            # aggiorno l'ultima posizione
        

        print(self.camera.position)
        
        self.sprite.center_x += self.direction[0] * 7
        self.sprite.center_y += self.direction[1] * 7

        self.camera.position = (
            self.camera.position[0],
            self.sprite.center_y
        )

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.UP:
            self.direction[1] = 1
        if key == arcade.key.DOWN:
            self.direction[1] = -1
        if key == arcade.key.RIGHT:
            self.direction[0] = 1
        if key == arcade.key.LEFT:
            self.direction[0] = -1

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP:
            self.direction[1] = 0
        if key == arcade.key.DOWN:
            self.direction[1] = 0
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
        WINDOW_WIDTH, WINDOW_HEIGHT, "Il mio giochino"
    )
    arcade.run()




if __name__ == "__main__":
    main()