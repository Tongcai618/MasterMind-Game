"""
    Tong Cai
    CS 5001
    2023 Fall
    Project 1
    Mastermind Game
"""
import random
import turtle
import time

# the default parameters
WIDTH = 750
HEIGHT = 750
SPEED = 1000
BUTTON_RADIUS = 26
MARBLE_RADIUS = 16
REG_RADIUS = 5
ROW_INTERVAL = 50
TITLE = "CS5001 MasterMind Code Game"
COLORS = ["red", "blue", "green", "yellow", "purple", "black"]
LEADERBOARD_PATH = "leaderboard.txt"
FONT = ("Arial", 18, "normal")

CONFIGURATION_PATH = "config.txt"


class MasterMindKernal:
    """ This class manages the comparison between secret code and a set of
    picked color of the game mastermind.

    Attributes:
        secret_code (list): A list representing the secret code, where each
                            element is a color.
        picked_colors (list): A list representing the colors picked by players,
                              where each element is a color.
    Methods:
        get_secret_code: Return the secret code.
        get_picked_colors: Return the picked colors.
        get_number_of_correct_position: Return the count of colors in the
                                        picked list that are in the correct
                                        position.
        get_number_of_wrong_position: Return the count of colors in the picked
                                      list that are in the wrong position.
        is_win: Check if the picked colors match the secret code exactly,
                indicating a win.
    """

    def __init__(self, secret_code: list, picked_colors: list) -> None:
        self.secret_code = secret_code
        self.picked_colors = picked_colors

    def get_secret_code(self) -> list:
        """ This method is to return the secret code.

        Returns:
            list: a list representing the secret code.
        """
        return self.secret_code

    def get_picked_colors(self) -> list:
        """ This method is to return the picked colors.

        Returns:
            list: a list representing the picked colors.
        """
        return self.picked_colors

    def get_number_of_correct_position(self) -> int:
        """ This method is to calculate the number of colors that
        exactly match the secret code.

        Returns:
            int: the number of picked colors that exactly match the secret
                 code.
        """
        number_of_correct_position = 0
        for position in range(len(self.picked_colors)):
            # the picked color is in the correct position
            if self.picked_colors[position] == self.secret_code[position]:
                number_of_correct_position += 1
        return number_of_correct_position

    def get_number_of_wrong_position(self) -> int:
        """ This method is to calculate the number of colors that are in
        secret code but not exactly in the correct position

        Returns:
            int: the number of picked colors that are members of secret
        code but in the wrong position
        """
        number_of_wrong_position = 0
        for position, picked_color in enumerate(self.picked_colors):
            # the picked color is in secret code but in the wrong position
            if (picked_color in self.secret_code) and (
                    picked_color != self.secret_code[position]):
                number_of_wrong_position += 1
        return number_of_wrong_position

    def is_win(self) -> bool:
        """ This method is to check if the picked colors exactly match the
        secret code.

        Returns:
            bool: if the picked colors exactly match the secret code.
        """
        if self.secret_code == self.picked_colors:
            return True
        return False


class MasterMind:
    """
    This class creates and manages the UI of MasterMind and runs the game.

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
    """

    def __init__(self, width: int, height: int, title: str,
                 speed: int, button_radius: int, marble_radius: int,
                 reg_radius: int, colors: list,
                 leaderboard_path: str, font: tuple) -> None:
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
        # initialize the result of the game
        self.is_win = False
        # set the width and height of quit button
        self.quit_button_width = 58
        self.quit_button_height = 29

    def initilize_turtle(self):
        """ This function is to initilize Turtle and Screen to
        establish the foundation of the turtle UI window.
        """
        # initialize the self.turtle
        self.turtle = turtle.Turtle()
        self.turtle.speed(self.speed)
        self.turtle.hideturtle()

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
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.pendown()
        self.turtle.circle(radius=radius)

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
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.pendown()
        # draw the border
        self.turtle.circle(radius=radius)
        # fill the circle
        self.turtle.color(color)
        self.turtle.begin_fill()
        self.turtle.circle(radius=radius)
        self.turtle.end_fill()
        # set back the original color
        self.turtle.color("black")

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
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.pendown()
        # set the pensize to 5
        self.turtle.pensize(5)
        self.turtle.color(color)
        # draw the rectangle
        for _ in range(2):
            self.turtle.forward(width)
            self.turtle.right(90)
            self.turtle.forward(height)
            self.turtle.right(90)
        # set back the pensize to 1
        self.turtle.pensize(1)
        # set back the color to black
        self.turtle.color('black')

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
                            color="blue")
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

    def generate_hints(self) -> list[list[dict]]:
        """ This method is to generate the hints circle.

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
        hint_radius = self.reg_radius  # is 5
        self.hints_coordinate = []
        # draw the hints circles and store their coordinates
        for row in range(1, row_number + 1):
            group = []
            for index in range(1, index_number + 1):
                x = initial_x + index * index_interval
                y = initial_y - row * self.row_interval
                self.draw_circle(x=x,
                                 y=y,
                                 radius=hint_radius)
                group.append({'x': x, 'y': y})

            for index in range(1, index_number + 1):
                x = initial_x + index * index_interval
                y = initial_y - row * self.row_interval - 20
                self.draw_circle(x=x,
                                 y=y,
                                 radius=hint_radius)
                group.append({'x': x, 'y': y})
            self.hints_coordinate.append(group)

        return self.hints_coordinate

    def generate_leaderboard(self) -> None:
        """ This method is to generate the leaderboard, consisting the list of
        players who got the best performance before.
        """
        initial_x = 0.15 * self.width
        initial_y = 0.40 * self.height
        text = "Leaders: "
        color = "blue"
        font = self.font
        # write the intial line of the leaderboard
        self.display_text(x=initial_x, y=initial_y, color=color,
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
            # adjust the y-coordinate for each subsequent leader to be 50px
            # lower on the leader board
            y = initial_y - ((rank + 1) * self.row_interval)
            self.display_text(x=x, y=y,
                              color="blue", font=font,
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
        path = "Mastermind_Starter_code/checkbutton.gif"
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
        path = "Mastermind_Starter_code/xbutton.gif"
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
        path = "Mastermind_Starter_code/quit.gif"
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
        arrow = "Mastermind_Starter_code/arrow_symbol.gif"
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
                               color=self.turtle.screen.bgcolor())
        # redraw the border
        self.draw_circle(x=x, y=y, radius=radius)

    def light_up_hints(self, nums_correct_position: int,
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
            x = self.hints_coordinate[self.round][index]['x']
            y = self.hints_coordinate[self.round][index]['y']
            radius = self.reg_radius
            color = "black"
            self.draw_solid_circle(x, y, radius=radius, color=color)
            index += 1
            nums_correct_position -= 1
        # light up the black regs for number of color in wrong position
        while nums_wrong_position > 0:
            x = self.hints_coordinate[self.round][index]['x']
            y = self.hints_coordinate[self.round][index]['y']
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
        pen.color(color)
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
                Call the function self.loss().
            3. Move to the next round:
                Clear the self.selction_stack, increase self.round by 1.
        """
        # use the last result to light up the hint to prompt players
        last_round_result = MasterMindKernal(
            secret_code=self.secret_code,
            picked_colors=self.selection_stack)
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
            2. Loss:
                The player loses the game.
            """
            self.loss()
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
        path = "Mastermind_Starter_code/quitmsg.gif"
        self.draw_image(x=x, y=y, path=path)
        # after 3 seconds, close the screen
        self.screen.onscreenclick(None)
        time.sleep(2)
        self.screen.bye()

    def win(self):
        """ This method is to function the condition that the player won.
        """
        x = 0
        y = 0
        path = "Mastermind_Starter_code/winner.gif"
        # pop up the winner.gif window
        self.draw_image(x=x, y=y, path=path)
        self.to_leaderboard(self.name)
        # end the onscreenclick
        self.screen.onscreenclick(None)
        time.sleep(2)
        self.screen.bye()

    def loss(self):
        """ This method is to function the condition that the player lost.
        """
        # pop up the lose.gif window
        x = 0
        y = 0
        path = "Mastermind_Starter_code/Lose.gif"
        self.screen.onscreenclick(None)
        self.draw_image(x=x, y=y, path=path)
        time.sleep(2)
        self.pop_up_window(title="Secret Code: ",
                           prompt=f"{self.secret_code[0]} "
                           f"{self.secret_code[1]} "
                           f"{self.secret_code[2]} "
                           f"{self.secret_code[3]} ")
        self.screen.bye()

    def proceed_to_next_round(self, last_result: MasterMindKernal):
        """ This method is to proceed the game to the next round.
        To proceed the next round, this method will light up the hints of
        last round. After that, this method will increase self.round by 1, and
        clear the self.selection_stack for the next round's selection. Finally,
        this method will recover all selections in the selection area and move
        the arrow to the next round's position.

        Args:
            last_result (MasterMindKernal): the hints of last game, which
                contains the number of color int he correct position and
                the number of color in the wrong position.
        """
        # if the guess are not correct, prompt the hints
        self.light_up_hints(nums_correct_position=(
            last_result.get_number_of_correct_position()),
            nums_wrong_position=(
            last_result.get_number_of_wrong_position()))
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
        path = "Mastermind_Starter_code/leaderboard_error.gif"
        self.draw_image(x=x, y=y, path=path)

    def raise_config_error(self):
        """ This method is to raise a file error when the configuration
        file was not found.
        """
        x = 0.27 * self.width
        y = -0.2 * self.height
        path = 'Mastermind_Starter_code/file_error.gif'
        self.draw_image(x=x, y=y, path=path)

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
                if color not in self.selection_stack and (
                    (self.selections_coordinate[color]['x'] -
                     self.marble_radius) < x < (
                        self.selections_coordinate[color]['x'] +
                        self.marble_radius)) and (
                    (self.selections_coordinate[color]['y'] -
                     self.marble_radius) < y < (
                        self.selections_coordinate[color]['y'] +
                        self.marble_radius)):
                    # activate the selection button
                    self.click_selection_button(color=color)
            """
            # 2. X: they can cancel their selections
            """
            if ((  # click the x button
                ((self.x_button_coordinate['x']) -
                 self.button_radius < x < (
                    self.x_button_coordinate['x'] +
                    self.button_radius)) and (
                    (self.x_button_coordinate['y']) -
                    self.button_radius < y < (
                    self.x_button_coordinate['y'] +
                    self.button_radius)))):
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
            if ((  # click the x button
                ((self.x_button_coordinate['x']) -
                 self.button_radius < x < (
                    self.x_button_coordinate['x'] +
                    self.button_radius)) and (
                    (self.x_button_coordinate['y']) -
                    self.button_radius < y < (
                    self.x_button_coordinate['y'] +
                    self.button_radius)))):
                self.click_x_button()
            """
            # 2. CHECK: they can check their choice
            """
            if (  # click the check button
                ((self.check_button_coordinate['x']) -
                 self.button_radius < x < (
                    self.check_button_coordinate['x'] +
                    self.button_radius)) and (
                    (self.check_button_coordinate['y']) -
                    self.button_radius < y < (
                        self.check_button_coordinate['y'] +
                        self.button_radius))):
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


"""
The functions below are used to create a MasterMind object and
call its methods to run and maintain the game.
"""


def load_config(path: str) -> dict:
    """ This function loads the configuration file.

    Args:
        path (str): the path of the configuration file.

    Returns:
        dict: a dict of configuration for the game.
    """
    config_dict = {}
    with open(file=path, mode='r') as config:
        for param in config:
            # remove "\n"
            param = param.replace("\n", '')
            param_name, param_value = param.split('=')
            # strip the param_name and param_value
            param_name = param_name.strip(' ')
            param_value = param_value.strip(' ')
            # store name and value in config_dict
            config_dict[param_name] = param_value
    return config_dict


def setup_mastermind_config(path) -> MasterMind:
    """ This function create a MasterMind instance based on
    the configuration file or default values.

    Args:
        path (_type_): the path of the configuration file.

    Returns:
        MasterMind: a MasterMind instance that used to
                    play the Mastermind game.
    """
    try:
        # if the configuration file exists, load the configuration file
        config = load_config(path)
        # pass the configuration parameters to the mastermind
        width = int(config["width"])
        height = int(config["height"])
        speed = int(config["speed"])
        button_radius = int(config["button_radius"])
        marble_radius = int(config["marble_radius"])
        reg_radius = int(config["reg_radius"])
        title = config["title"]
        leaderboard_path = config["leaderboard_path"]
        colors = config["colors"].replace(' ', '').split(',')
        font = tuple(config['font'].replace(' ', '').split(','))

        mastermind = MasterMind(
            width=width,
            height=height,
            title=title,
            speed=speed,
            button_radius=button_radius,
            marble_radius=marble_radius,
            reg_radius=reg_radius,
            colors=colors,
            leaderboard_path=leaderboard_path,
            font=font)

    except FileNotFoundError:
        # if the configuration file does't exist, load the default parameters
        width = WIDTH
        height = HEIGHT
        speed = SPEED
        button_radius = BUTTON_RADIUS
        marble_radius = MARBLE_RADIUS
        reg_radius = REG_RADIUS
        title = TITLE
        colors = COLORS
        leaderboard_path = LEADERBOARD_PATH
        font = FONT

        mastermind = MasterMind(
            width=width,
            height=height,
            title=title,
            speed=speed,
            button_radius=button_radius,
            marble_radius=marble_radius,
            reg_radius=reg_radius,
            colors=colors,
            leaderboard_path=leaderboard_path,
            font=font)
        # raise the configuration file error
        mastermind.raise_config_error()
    # initilize the turtle UI window
    mastermind.initilize_turtle()
    return mastermind


def get_player_sign_in(mastermind: MasterMind):
    """ This function is to let players sign in the game with
    their names.

    Args:
        mastermind (MasterMind): a mastermind object.
    """
    title = "CS 5001 MasterMind"
    prompt = "Enter your name: "
    mastermind.pop_up_window(title=title,
                             prompt=prompt)


def create_mastermind_ui(mastermind: MasterMind):
    """ This function is to create the mastermind user interface window.

    Args:
        mastermind (MasterMind): a mastermind object.
    """
    mastermind.generate_frame()
    mastermind.generate_check_button()
    mastermind.generate_x_button()
    mastermind.generate_quit_button()
    mastermind.generate_marbles()
    mastermind.generate_hints()
    mastermind.generate_selections()
    mastermind.generate_arrow()
    mastermind.generate_leaderboard()


def start_game_play(mastermind: MasterMind) -> None:
    """ This function start the game. At first, it will generate secret code,
    and then, it will allow players to play the game.

    Args:
        mastermind (MasterMind): a mastermind object.
    """
    mastermind.generate_secret_code()
    mastermind.play()


def run_game_maintenance(mastermind: MasterMind) -> None:
    """ This function maint the running of the game.

    Args:
        mastermind (MasterMind): a mastermind obkect
    """
    mastermind.maintain()


def main():
    # initialize the game's configuration
    mastermind = setup_mastermind_config(path=CONFIGURATION_PATH)
    # ask players to sign in the game
    get_player_sign_in(mastermind)
    # generate the game's UI
    create_mastermind_ui(mastermind)
    # start playing the game
    start_game_play(mastermind)
    # maintain the game's running
    run_game_maintenance(mastermind)


if __name__ == "__main__":
    main()
