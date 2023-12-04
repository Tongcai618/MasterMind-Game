import turtle
import random
import time
import math
from src.mastermind_kernal import MastermindKernal


class Mastermind:
    """
    This class creates and manages the UI of Mastermind and runs the game.

    Attributes:
        width (int): The width of the UI window.
        height (int): The height of the UI window.
        title (str): The title of the UI window.
        speed (int): The speed of the turtle that creates the UI window.
        button_radius (int): The radius of the button (check_button, X_button).
        marble_radius (int): The radius of the big circles in the UI windows.
        reg_radius (int): The radius of the small circles in the UI window.
        row_interval (int): The vertical interval of each row, representing
                            different rounds in the game.
        colors (list): The constant list of colors for generating secret code 
                       and for players to pick from.
        leaderboard_path (str): Path to the leaderboard file.
        font (tuple): The font settings for text in the game.
        font_color (str): The font's color for text in the game.

    Methods:
        initilize_turtle(self):
            Initializes Turtle and Screen to establish the foundation of the
            turtle UI window.

        draw_circle(self, x: int, y: int, radius: int) -> None:
            Draws an unfilled circle given its center coordinates (x, y) and
            radius.

        draw_solid_circle(self, x: int, y: int, radius: int,
                          color: str) -> None:
            Draws a filled circle given its center coordinates (x, y), radius,
            and color.

        draw_rectangle(self, x: int, y: int, width: int, height: int,
                       color: str):
            Draws an unfilled rectangle given the top-left coordinate (x, y),
            width, height, and line color.

        draw_image(self, x: int, y: int, path: str) -> dict:
            Imports and draws an image given its coordinates (x, y) and file
            path. Returns the image's coordinates.

        generate_secret_code(self) -> list[str]:
            Randomly generates and returns a secret code consisting of a list
            of colors.

        generate_frame(self):
            Generates three rectangle frames on the UI window.

        generate_marbles(self) -> list[list[dict]]:
            Generates marble circles and returns a list of coordinates for
            each marble.

        generate_regs(self) -> list[list[dict]]:
            Generates hint circles and returns a list of coordinates for each
            reg.

        generate_leaderboard(self) -> None:
            Generates the leaderboard displaying the best performing players.

        generate_selections(self) -> dict[dict]:
            Generates a selection area of colored circles and returns a
            dictionary of their coordinates.

        generate_check_button(self) -> dict[str:int]:
            Generates a check button and returns its center coordinates.

        generate_x_button(self) -> dict[str:int]:
            Generates an X button for canceling selections and returns its
            center coordinates.

        generate_quit_button(self) -> dict[str:int]:
            Generates a quit button and returns its center coordinates.

        generate_arrow(self) -> dict[str:int]:
            Generates an arrow to indicate the current round and returns its
            center coordinates.

        pop_up_window(self, title: str, prompt: str) -> str:
            Generates a pop-up window for user input and returns the entered
            text.

        remove_solid_circle(self, x: int, y: int, radius: int) -> None:
            Removes a solid circle's color, reverting it to the background
            color, but preserves its border.

        light_up_regs(self, nums_correct_position: int,
                            nums_wrong_position: int):
            Lights up the regs based on the number of colors in the correct
            and wrong positions.

        read_leaderboard(self, path: str) -> list[tuple[int, str]]:
            Reads the leaderboard file and converts it into a sorted list of
            tuples, each containing a player's score and name, sorted in
            ascending order of scores.

        to_leaderboard(self, text: str) -> None:
            Writes the current player's name and score to the leaderboard file.

        display_text(self, x: int, y: int, color: str,
                     font: tuple, text: str) -> None:
            Displays specified text at given coordinates on the game UI with
            the specified color and font.

        remove_selected_circle_color(self, color: str) -> None:
            Removes the color of a selected circle in the selection area.

        recover_selected_circle_color(self, color: str) -> None:
            Recovers the color of a selected circle in the selection area.

        move_arrow(self, distance: int) -> None:
            Moves the arrow a specific distance to indicate the current round.

        click_selection_button(self, color: str) -> None:
            Handles the action after clicking a specific color circle in the
            selection area.

        click_x_button(self) -> None:
            Handles the action of clicking the X button, used to cancel the
            last selection.

        click_check_button(self) -> None:
            Handles the action of clicking the check button, used to confirm
            selections and proceed in the game.

        click_quit_button(self) -> None:
            Handles the action of clicking the quit button, used to exit the
            game.

        win(self) -> None:
            Executes the sequence of events when the player wins the game.

        lose(self) -> None:
            Executes the sequence of events when the player loses the game.

        proceed_to_next_round(self, last_result: MasterMindKernal) -> None:
            Proceeds the game to the next round based on the last round's
            result.

        raise_leaderboard_error(self) -> None:
            Raises an error if the leaderboard file is not found.

        raise_config_error(self) -> None:
            Raises an error if the configuration file is not found.

        click(self, x: int, y: int) -> None:
            Sets the response to a click event in the game.

        play(self) -> None:
            Activates the onclick function, enabling user interaction with the
            game's UI.

        maintain(self) -> None:
            Maintains the UI window, keeping the game window responsive.
    """

    def __init__(self, width: int, height: int, title: str,
                 speed: int, button_radius: int, marble_radius: int,
                 reg_radius: int, colors: list,
                 leaderboard_path: str, font: tuple,
                 font_color: str) -> None:
        """
        Constructs all the necessary attributes for the Mastermind object.

        Args:
            width (int): The width of the UI window.
            height (int): The height of the UI window.
            title (str): The title of the UI window.
            speed (int): The speed of the turtle that creates the UI window.
            button_radius (int): The radius of the button (check_button,
                                 X_button).
            marble_radius (int): The radius of the big circles in the UI 
                                 windows.
            reg_radius (int): The radius of the small circles in the UI window.
            row_interval (int): The vertical interval of each row, representing
                                different rounds in the game.
            colors (list): The constant list of colors for generating secret 
                           code and for players to pick from.
            leaderboard_path (str): Path to the leaderboard file.
            font (tuple): The font settings for text in the game.
        """
        self.width = width
        self.height = height
        self.title = title
        self.button_radius = button_radius
        self.marble_radius = marble_radius
        self.reg_radius = reg_radius
        self.row_interval = self.height * 0.07
        self.speed = speed
        self.colors = colors
        # create a stack to store players' selections at each round
        self.selection_stack = []
        # self.round indicates the current playing round (0-9), starting by 0
        self.round = 0
        self.last_round = 9
        # We have 10 rows
        self.row_number = self.last_round + 1
        # the path of the leaderboard.txt
        self.leaderboard_path = leaderboard_path
        # the font of the text
        self.font = font
        self.font_color = font_color
        # initialize the result of the game
        self.is_win = False
        # set the width and height of quit button
        self.quit_button_width = 58
        self.quit_button_height = 29

    def initilize_turtle(self):
        """ This function is to initilize Screen to
        establish the foundation of the turtle UI window.
        """
        # initialize the self.screen
        self.screen = turtle.Screen()
        self.screen.title(self.title)
        self.screen.setup(width=self.width, height=self.height)

    def draw_circle(self, x: int, y: int, radius: int) -> None:
        """ This method is to draw a unfilled circle given
        its center's coordinate x, y and radius.

        Args:
            x (int): the x-coordinate of the circle's cetner.
            y (int): the y-coordinate of the circle's center.
            radius (int): the radius of the circle.
        """
        pen = turtle.Turtle()
        pen.speed(self.speed)
        pen.hideturtle()
        pen.penup()
        pen.setpos(x, y)
        pen.pendown()
        pen.circle(radius=radius)

    def draw_solid_circle(self, x: int, y: int,
                          radius: int, color: str) -> None:
        """ This method is to draw a filled circle given
        its center's coordinate x, y, radius and color.

        Args:
            x (int): The x-coordinate of the circle's center.
            y (int): the y-coordinate of the circle's center.
            radius (int): the radius of the circle.
            color (str): the color of the circle.
        """
        pen = turtle.Turtle()
        pen.speed(self.speed)
        pen.hideturtle()
        pen.penup()
        pen.setpos(x, y)
        pen.pendown()
        # draw the border
        pen.circle(radius=radius)
        # fill the circle
        pen.color(color)
        pen.begin_fill()
        pen.circle(radius=radius)
        pen.end_fill()

    def draw_rectangle(self, x: int, y: int,
                       width: int, height: int, color: str):
        """ This method is to draw an unfilled rectangle.

        Args:
            x (int): the x-coordinate of the left-top starting point
                     of the rectangle.
            y (int): the y-coordinate of the left-top starting point
                     of the rectangle.
            width (int): the width of the rectangle.
            height (int): the height of the rectangle.
            color (str): the color of the rectangle's line.
        """
        pen = turtle.Turtle()
        pen.speed(self.speed)
        pen.hideturtle()
        pen.penup()
        pen.setpos(x, y)
        pen.pendown()
        # set the pensize to 5
        pen.pensize(5)
        pen.color(color)
        # draw the rectangle
        for _ in range(2):
            pen.forward(width)
            pen.right(90)
            pen.forward(height)
            pen.right(90)

    def draw_image(self, x: int, y: int, path: str) -> dict:
        """ This method is to import image from its path and draw the image
        given by its x-coordinate and y-coordinate.

        Args:
            x (int): the x-coordinate of the image.
            y (int): the y-coordinate of the image
            path (str): the path of the image.

        Return:
            dict: the coordinates of the image like:
                  {'x': 300, 'y': 200}
        """
        image = turtle.Turtle()
        image.speed(self.speed)
        # add the path of the image
        self.screen.addshape(path)
        image.penup()
        # store the coordinate of the image
        image_coordinate = {'x': x, 'y': y}
        image.setpos(image_coordinate['x'],
                     image_coordinate['y'])
        image.pendown()
        image.shape(path)

        return image_coordinate

    def generate_secret_code(self) -> list[str]:
        """ This method is to generate secret code. It will randomly
        choose 4 colors out of 6 to return a secret code list.

        Returns:
            list[str]: a secret code list consists of 4 colors.
        """
        self.secret_code = self.colors[:]
        self.secret_code.pop(random.randint(0, len(self.secret_code) - 1))
        self.secret_code.pop(random.randint(0, len(self.secret_code) - 1))
        return self.secret_code

    def generate_frame(self):
        """
            This method is to generate 3 rectangle frames on the UI window.
        """
        # draw the left-top frame
        self.draw_rectangle(x=(-0.46 * self.width),
                            y=(0.46 * self.height),
                            width=0.56 * self.width,
                            height=0.78 * self.height,
                            color="black")
        # draw the right-top frame
        self.draw_rectangle(x=(0.12 * self.width),
                            y=(0.46 * self.height),
                            width=0.3 * self.width,
                            height=0.78 * self.height,
                            color=self.font_color)
        # draw the bottom frame
        self.draw_rectangle(x=(-0.46 * self.width),
                            y=(-0.33 * self.height),
                            width=0.9 * self.width,
                            height=0.13 * self.height,
                            color="black")

    def generate_marbles(self) -> list[list[dict]]:
        """ This method is to generate the marbles circle.

        Returns:
            list[list[dict]]: a list of the coordinate of each marble circle:
        [
            [
                {'x': -282, 'y': 275}, {'x': -239, 'y': 275},
                {'x': -296, 'y': 275}, {'x': -153, 'y': 275}
            ], ......,
            [
                {'x': -282, 'y': -175}, {'x': -239, 'y': -175},
                {'x': -296, 'y': -175}, {'x': -153, 'y': -175}
            ]
        ]
        """
        initial_x = -0.43 * self.width
        initial_y = 0.43 * self.height
        row_number = self.row_number
        index_number = 4
        index_interval = 0.057 * self.height
        marble_radius = self.marble_radius
        # marbles_center is to save the x, y position of each marbles
        self.marbles_coordinate = []
        for row in range(1, row_number + 1):
            group = []
            for index in range(1, index_number + 1):
                x = initial_x + index * index_interval
                y = initial_y - row * self.row_interval
                self.draw_circle(x=x,
                                 y=y,
                                 radius=marble_radius)
                group.append({'x': x, 'y': y})
            self.marbles_coordinate.append(group)
        return self.marbles_coordinate

    def generate_regs(self) -> list[list[dict]]:
        """ This method is to generate the regs to prompt hints.

        Returns:
            list[list[dict]]: a list of the coordinate of each hint circle:
        [
            [
                {'x': -35, 'y': 295}, {'x': -20, 'y': 295},
                {'x': -35, 'y': 275}, {'x': -20, 'y': 275}
            ], ......,
            [
                {'x': -35, 'y': -155}, {'x': -20, 'y': -155},
                {'x': -35, 'y': -175}, {'x': -20, 'y': -175}
            ]
        ]
        """
        initial_x = -0.06 * self.width
        initial_y = 0.46 * self.height
        row_number = self.row_number
        index_number = 2
        index_interval = 0.02 * self.width
        reg_radius = self.reg_radius  # is 5
        self.regs_coordinate = []
        # draw the regs and store their coordinates
        for row in range(1, row_number + 1):
            # for each row, we use a group to save their coordinate
            group = []
            for index in range(1, index_number + 1):
                x = initial_x + index * index_interval
                y = initial_y - row * self.row_interval
                self.draw_circle(x=x,
                                 y=y,
                                 radius=reg_radius)
                group.append({'x': x, 'y': y})

            for index in range(1, index_number + 1):
                x = initial_x + index * index_interval
                y = initial_y - row * self.row_interval - 20
                self.draw_circle(x=x,
                                 y=y,
                                 radius=reg_radius)
                group.append({'x': x, 'y': y})
            self.regs_coordinate.append(group)

        return self.regs_coordinate

    def generate_leaderboard(self) -> None:
        """ This method is to generate the leaderboard, consisting the list of
        players who got the best performance before.
        """
        initial_x = 0.15 * self.width
        initial_y = 0.40 * self.height
        text = "Leaders: "
        font_color = self.font_color
        font = self.font
        # write the intial line of the leaderboard
        self.display_text(x=initial_x, y=initial_y, color=font_color,
                          font=font, text=text)
        # read the leaders_list
        try:
            leaders_list = self.read_leaderboard(path=self.leaderboard_path)
        except FileNotFoundError:
            # if cannot find the leaderboard.txt, display the leaderboard error
            self.raise_leaderboard_error()
            leaders_list = []

        for rank, leader in enumerate(leaders_list):
            x = initial_x
            # adjust the y-coordinate for each subseq
            # ent leader to be 50px
            # lower on the leader board
            y = initial_y - ((rank + 1) * self.row_interval)
            self.display_text(x=x, y=y,
                              color=self.font_color, font=font,
                              text=f"{leader[0]}: {leader[1]}")

    def generate_selections(self) -> dict[dict]:
        """ This method is to generate the selection area consisting of
        a line of circles. This method creates and positions a series of
        colored circles, storing their coordinates in a dictionary.

        Returns:
            dict[dict]: a list that contain the coordinate for
                        each selection' circle:
        {
           "red": {'x': -275, 'y':-300},
           "blue": {'x': -230, 'y': -300}, ......,
           "purple": {'x': -95, 'y': -300},
           "black": {'x': -50, 'y': -300}
        }
        """
        initial_x = -0.37 * self.width
        initial_y = -0.4 * self.height
        index_interval = 0.06 * self.width
        selections_radius = self.marble_radius
        # save the selections' coordinates by dict
        self.selections_coordinate = {}
        for index, color in enumerate(self.colors):
            x = initial_x + index * index_interval
            y = initial_y
            self.draw_solid_circle(x=x,
                                   y=y,
                                   radius=selections_radius,
                                   color=color)
            self.selections_coordinate[color] = {'x': x, 'y': y}

        return self.selections_coordinate

    def generate_check_button(self) -> dict[str:int]:
        """ This method is to generate a check button for players to check
        their selections at each round of the game.

        Returns:
            dict[str:int]: the coordinate of the center of the check button.
        """
        x = 0.026 * self.width
        y = -0.4 * self.height
        path = "src/checkbutton.gif"
        self.check_button_coordinate = self.draw_image(x=x, y=y,
                                                       path=path)
        return self.check_button_coordinate

    def generate_x_button(self) -> dict[str:int]:
        """ This method is to generate an X button for players to cancel
        their selections from the last-in-first-out order.

        Returns:
            dict[str:int]: the coordinate of the center of the X button
        """
        x = 0.13 * self.width
        y = -0.4 * self.height
        path = "src/xbutton.gif"
        self.x_button_coordinate = self.draw_image(x=x, y=y,
                                                   path=path)

        return self.x_button_coordinate

    def generate_quit_button(self) -> dict[str:int]:
        """ This method is to generate a quit button for players to
        quit the game.

        Returns:
            dict: the coordinate of the center of the button.
        """
        # set the width and height of quit button
        self.quit_button_width = 58
        self.quit_button_height = 29
        # set the coordinates and path of quit button
        x = 0.30 * self.width
        y = -0.4 * self.height
        path = "src/quit.gif"
        self.quit_button_coordinate = self.draw_image(x=x,
                                                      y=y,
                                                      path=path)
        return self.quit_button_coordinate

    def generate_arrow(self) -> dict[str:int]:
        """ This method is to generate a arrow to indicate the current round 
        of the game.

        Returns:
            dict[str:int]: the coordinate of the center of the arrow
        """
        initial_x = -0.43 * self.width
        initial_y = 0.39 * self.height

        self.arrow = turtle.Turtle()
        self.arrow.speed(self.speed)
        arrow = "src/arrow_symbol.gif"
        self.screen.addshape(arrow)
        self.arrow.penup()
        self.arrow_coordinate = {'x': initial_x,
                                 'y': initial_y}
        self.arrow.setpos(self.arrow_coordinate['x'],
                          self.arrow_coordinate['y'])
        self.arrow.right(90)
        self.arrow.shape(arrow)

        return self.arrow_coordinate

    def pop_up_window(self, title: str, prompt: str) -> str:
        """ This method is to generate a pop up window for users to enter
        their names. Their names and records will be stored based on their
        performances.

        Args:
            title (str): the title of the pop-up window.
            prompt (str): the text that users input.

        Returns:
            str: the text that users input.
        """
        self.name = self.screen.textinput(title=title,
                                          prompt=prompt)
        return self.name

    def remove_solid_circle(self, x: int, y: int, radius: int) -> None:
        """ This method is to remove a solid cirle's color with the
        background color but preserve its border.

        Args:
            x (int): The x-coordinate of the circle's center.
            y (int): The y-coordinate of the circle's center.
            radius (int): the radius of the circle.
        """
        # fill white color
        self.draw_solid_circle(x=x, y=y, radius=radius,
                               color=self.screen.bgcolor())
        # redraw the border
        self.draw_circle(x=x, y=y, radius=radius)

    def light_up_regs(self, nums_correct_position: int,
                      nums_wrong_position: int):
        """ This method is to light up the hints at each round of the game,
        given the number of colors in correct position and number of color in
        wrong position. Red pegs meant a correct color but out of position,
        black pegs meant a correct color in the correct position.

        Args:
            nums_correct_position (int): the number of red pegs.
            nums_wrong_position (int): the number of black pegs.
        """
        # define the index of hints, the index will increase from 0 to 3
        index = 0
        # light up the red pegs for number of color in correct position
        while nums_correct_position > 0:
            x = self.regs_coordinate[self.round][index]['x']
            y = self.regs_coordinate[self.round][index]['y']
            radius = self.reg_radius
            color = "black"
            self.draw_solid_circle(x, y, radius=radius, color=color)
            index += 1
            nums_correct_position -= 1
        # light up the black regs for number of color in wrong position
        while nums_wrong_position > 0:
            x = self.regs_coordinate[self.round][index]['x']
            y = self.regs_coordinate[self.round][index]['y']
            radius = self.reg_radius
            color = "red"
            self.draw_solid_circle(x, y, radius=radius, color=color)
            index += 1
            nums_wrong_position -= 1

    def read_leaderboard(self, path) -> list[tuple[int:str]]:
        """ This method is to read the leaderboard.txt file and convert the
        text to a list with tuple elements. After that, this method will
        sort the leader list based on ascending order.

            i.e. [(3, "Tong Cai"), (5, "Jenny Yi"), ......]

        Returns:
            list[tuple[int:str]]: a list consists of tuple elements. Each
                                  element is a tuple with scores and name.
        """
        leaders_list = []
        # open the leaderboard.txt
        with open(path, 'r') as leaders:
            if leaders is None:
                return []
            for leader in leaders:
                if ":" in leader:
                    scores, name = leader.split(':')
                    # drop any "\n" and space around name
                    name = name.replace("\n", "").strip(' ')
                    leaders_list.append(tuple([int(scores), name]))
        # sort the leaders list with ascending order
        sorted_leaders_list = sorted(leaders_list, key=lambda x: x[0])
        # only display the top 5 players
        sorted_leaders_list = sorted_leaders_list[0:5]

        return sorted_leaders_list

    def to_leaderboard(self, text: str):
        """ This method is to save the current player's name and its scores.
        The text will be saved like: "5: Tong Cai", "3: Jenny Yi"......

        Args:
            text (str): the text to be saved into leaderboard.txt.
        """
        with open(self.leaderboard_path, 'a') as file:
            file.write(f"{self.round + 1}: {text}\n")

    def display_text(self, x: int, y: int, color: str,
                     font: tuple, text: str) -> None:
        """ This method is to display specified text given its coordinate,
        color, and font on the leaderboard area.

        Args:
            x (int): the x-coordinate of the text.
            y (int): the y-coordinate of the text.
            color (str): the color of the text.
            font (tuple): the font of the text.
            text (str): the text needed to be written.
        """
        pen = turtle.Turtle()
        pen.hideturtle()
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        # choose the text's color
        pen.color(color)
        # choose the font
        pen.write(text, font=font)

    def remove_selected_circle_color(self, color: str):
        """ This method is to remove the circle's color of the
        selected circle in the selection area.

        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]

        Args:
            color (str): the color of the selected selection circles that
                         need to be removed.

        """
        initial_x = -0.37 * self.width
        initial_y = -0.4 * self.height
        index_interval = 0.06 * self.width
        selections_radius = self.marble_radius
        color = color
        index = self.colors.index(color)
        self.remove_solid_circle(x=initial_x + index * index_interval,
                                 y=initial_y,
                                 radius=selections_radius)

    def recover_selected_circle_color(self, color: str):
        """ This method is to recover the circle's color of the selected
        circle in the selection area.

        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]

        Args:
            color (str): the color of the selected selection circles that
                         need to be recovered

        """
        initial_x = -0.37 * self.width
        initial_y = -0.4 * self.height
        index_interval = 0.06 * self.width
        selections_radius = self.marble_radius
        color = color
        index = self.colors.index(color)
        self.draw_solid_circle(x=initial_x + index * index_interval,
                               y=initial_y,
                               radius=selections_radius,
                               color=color)

    def move_arrow(self, distance: int):
        """ This method is to move the arrow given a specific distance.

        Args:
            distance (int): the distance of moving.
        """
        self.arrow.forward(distance=distance)

    def click_selection_button(self, color: str) -> None:
        """ This method is to react after clicking a specific color circle.
        1. Append the color into the selection_stack.
        2. Remove the color from selection area.
        3. Draw a solid color circlein the display area.

        Args:
            color (str): the color that was selected by the players
        """
        # click the color circle
        self.selection_stack.append(color)
        # remove the color of the selected circle
        self.remove_selected_circle_color(color=color)
        # draw the selected solid circle
        self.draw_solid_circle(x=self.marbles_coordinate[self.round][
            len(self.selection_stack) - 1]['x'],
            y=self.marbles_coordinate[self.round][
            len(self.selection_stack) - 1]['y'],
            radius=self.marble_radius,
            color=color)

    def click_x_button(self):
        """ This method is to handle the action of clicking X button.
        """
        # if the selection stack is over 0, we can pop the stack
        if len(self.selection_stack) > 0:
            # pop out the selected color
            self.cancelled_color = self.selection_stack.pop()
            self.recover_selected_circle_color(color=self.cancelled_color)
            # remove the selected marble's color
            self.remove_solid_circle(x=(
                self.marbles_coordinate[self.round][
                    len(self.selection_stack)]
                ['x']),
                y=(self.marbles_coordinate[self.round][
                    len(self.selection_stack)]
                   ['y']),
                radius=self.marble_radius)

    def click_check_button(self):
        """ This method is to handle the action of clicking check button.
        If the players win, if will return a True.

        The check button has 3 situations.
            1. Win:
                Call the function self.win().
            2. Loss:
                Call the function self.lose().
            3. Move to the next round:
                Clear the self.selction_stack, increase self.round by 1.
        """
        # use the last result to light up the hint to prompt players
        last_round_result = MastermindKernal(
            secret_code=self.secret_code,
            picked_colors=self.selection_stack
        )
        # to check whether the player win the game
        self.is_win = last_round_result.is_win()
        # if the guess are correct, the users win
        if self.is_win is True:
            """
            1. Win:
                The player wins the game.
            """
            self.win()
        elif (self.is_win is False) and (self.round == self.last_round):
            """
            2. Lose:
                The player loses the game.
            """
            self.lose()
        """
        3. Move to the next round:
            Clear the self.selction_stack, increase self.round by 1.
        """
        self.proceed_to_next_round(last_result=last_round_result)

    def click_quit_button(self) -> None:
        """ This method is to handle the action of clicking
        the quit button.
        """
        # pop up the quit.gif window
        x = 0
        y = 0
        path = "src/quitmsg.gif"
        self.draw_image(x=x, y=y, path=path)
        # after 2 seconds, close the screen
        self.screen.onscreenclick(None)
        time.sleep(2)
        self.screen.bye()

    def win(self):
        """ This method is to function the condition that the player won.
        """
        x = 0
        y = 0
        path = "src/winner.gif"
        # pop up the winner.gif window
        self.draw_image(x=x, y=y, path=path)
        self.to_leaderboard(self.name)
        # after 2 seconds, end the onscreenclick
        self.screen.onscreenclick(None)
        time.sleep(2)
        self.screen.bye()

    def lose(self):
        """ This method is to function the condition that the player lost.
        """
        # pop up the lose.gif window
        x = 0
        y = 0
        path = "src/Lose.gif"
        self.draw_image(x=x, y=y, path=path)
        self.screen.onscreenclick(None)
        time.sleep(2)
        self.pop_up_window(title="Secret Code: ",
                           prompt=f"{self.secret_code[0]} "
                           f"{self.secret_code[1]} "
                           f"{self.secret_code[2]} "
                           f"{self.secret_code[3]} ")
        self.screen.bye()

    def proceed_to_next_round(self, last_result: MastermindKernal):
        """ This method is to proceed the game to the next round.
        To proceed the next round, this method will light up the hints of
        last round. After that, this method will increase self.round by 1, and
        clear the self.selection_stack for the next round's selection. Finally,
        this method will recover all selections in the selection area and move
        the arrow to the next round's position.

        Args:
            last_result (MastermindKernal): the hints of last game, which
                contains the number of color int he correct position and
                the number of color in the wrong position.
        """
        # if the guess are not correct, prompt the hints
        self.light_up_regs(
            nums_correct_position=(
                last_result.get_number_of_correct_position()
            ),
            nums_wrong_position=(
                last_result.get_number_of_wrong_position()
            )
        )
        # go into the next round
        self.round += 1
        self.selection_stack = []
        # regain all selections
        self.generate_selections()
        # move the arrow
        self.move_arrow(distance=self.row_interval)

    def raise_leaderboard_error(self) -> None:
        """ This method is to raise a leaderboard error
        when the leaderboard file was not found.
        """
        x = 0.27 * self.width
        y = 0.33 * self.height
        path = "src/leaderboard_error.gif"
        self.draw_image(x=x, y=y, path=path)

    def raise_config_error(self):
        """ This method is to raise a file error when the configuration
        file was not found.
        """
        x = 0.27 * self.width
        y = -0.2 * self.height
        path = 'src/file_error.gif'
        self.draw_image(x=x, y=y, path=path)

    def is_within_circular_button_area(self, x: int, y: int,
                                       center_x: int, center_y: int,
                                       radius: int) -> bool:
        """ This method is to check a point is within the area of
        a circular button.

        Args:
            x (int): The x-coordinate of the point to check.
            y (int): The y-coordinate of the point to check.
            center_x (int): The x-coordinate of the button's center.
            center_y (int): The y-coordinate of the button's center.
            radius (int): The radius of the circular button.

        Returns:
            bool: True if the point is within the button's area,
                  False otherwise.
        """
        if math.sqrt(
            (x - center_x) ** 2 + (y - center_y) ** 2
        ) < radius:
            return True
        return False

    def click(self, x: int, y: int) -> None:
        """ This method is to set the click's reaction

        Args:
            x (int): the x-coordinate of one clicking
            y (int): the y-coordinate of one clicking
        """
        if (((  # click the quit button
             self.quit_button_coordinate['x'] -
             self.quit_button_width) < x < (
                 self.quit_button_coordinate['x'] +
                 self.quit_button_width) and (
            self.quit_button_coordinate['y'] -
            self.quit_button_height) < y < (
                 self.quit_button_coordinate['y'] +
                 self.quit_button_height
        ))):
            self.click_quit_button()

        """
        Condition 1:
            If players have selected less or equal to 4 colors,
        they have 2 choices:
                1. S: they can select more colors
                2. X: they can cancel their selections
        """

        """
        # 1. S: they can select more colors
        """
        if len(self.selection_stack) < 4:
            for color in self.colors:
                if (
                    color not in self.selection_stack
                ) and (
                    self.is_within_circular_button_area(
                        x=x,
                        y=y,
                        center_x=self.selections_coordinate[color]['x'],
                        center_y=self.selections_coordinate[color]['y'],
                        radius=self.marble_radius
                    )
                ):
                    # activate the selection button
                    self.click_selection_button(color=color)
            """
            # 2. X: they can cancel their selections
            """
            if self.is_within_circular_button_area(
                x=x,
                y=y,
                center_x=self.x_button_coordinate['x'],
                center_y=self.x_button_coordinate['y'],
                radius=self.button_radius
            ):
                # when selection_stack is not empty, selection can be canceled
                self.click_x_button()

        """
        Condition 2:
            If players have already selected 4 selections,
        they have 2 choices:
                1. X: they can cancel their selection
                2. CHECK: they can check their selections
        """
        if len(self.selection_stack) == 4:
            """
            # 1. X: they can cancel their selections
            """
            if self.is_within_circular_button_area(
                x=x,
                y=y,
                center_x=self.x_button_coordinate['x'],
                center_y=self.x_button_coordinate['y'],
                radius=self.button_radius
            ):
                self.click_x_button()
            """
            # 2. CHECK: they can check their choice
            """
            if self.is_within_circular_button_area(
                x=x,
                y=y,
                center_x=self.check_button_coordinate['x'],
                center_y=self.check_button_coordinate['y'],
                radius=self.button_radius
            ):
                self.click_check_button()

    def play(self) -> None:
        """ This method is to activate the onclick function, which allows
        users to click the UI to play the game
        """
        self.screen.onclick(fun=self.click)

    def maintain(self) -> None:
        """ This method is to maintain the turtle UI
        """
        self.screen.mainloop()
