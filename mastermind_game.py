"""
    Tong Cai
    CS 5001
    2023 Fall
    Project 1
    Mastermind Game
"""
from error_logger import ErrorLogger
from mastermind import Mastermind

# the default parameters
WIDTH = 750
HEIGHT = 750
SPEED = 1000
BUTTON_RADIUS = 26
MARBLE_RADIUS = 16
REG_RADIUS = 5
ROW_INTERVAL = 50
TITLE = "Mastermind Game"
COLORS = ["red", "blue", "green", "yellow", "purple", "black"]
LEADERBOARD_PATH = "leaderboard.txt"
FONT = ("Arial", 18, "normal")
FONT_COLOR = "blue"
CONFIGURATION_PATH = "config.txt"


"""
The functions below are used to create a Mastermind object and
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


def setup_Mastermind_config(path) -> Mastermind:
    """ This function create a Mastermind instance based on
    the configuration file or default values.

    Args:
        path (_type_): the path of the configuration file.

    Returns:
        Mastermind: a Mastermind instance that used to
                    play the Mastermind game.
    """
    try:
        # if the configuration file exists, load the configuration file
        config = load_config(path)
        # pass the configuration parameters to the Mastermind
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
        font_color = config['font_color']

        mastermind = Mastermind(
            width=width,
            height=height,
            title=title,
            speed=speed,
            button_radius=button_radius,
            marble_radius=marble_radius,
            reg_radius=reg_radius,
            colors=colors,
            leaderboard_path=leaderboard_path,
            font=font,
            font_color=font_color)

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
        font_color = FONT_COLOR

        mastermind = Mastermind(
            width=width,
            height=height,
            title=title,
            speed=speed,
            button_radius=button_radius,
            marble_radius=marble_radius,
            reg_radius=reg_radius,
            colors=colors,
            leaderboard_path=leaderboard_path,
            font=font,
            font_color=font_color)
        # raise the configuration file error
        mastermind.raise_config_error()
    # initilize the turtle UI window
    mastermind.initilize_turtle()
    return mastermind


def get_player_sign_in(Mastermind: Mastermind):
    """ This function is to let players sign in the game with
    their names.

    Args:
        Mastermind (Mastermind): a Mastermind object.
    """
    title = "Mastermind Game"
    prompt = "Enter your name: "
    Mastermind.pop_up_window(title=title,
                             prompt=prompt)


def create_Mastermind_ui(Mastermind: Mastermind):
    """ This function is to create the Mastermind user interface window.

    Args:
        Mastermind (Mastermind): a Mastermind object.
    """
    Mastermind.generate_frame()
    Mastermind.generate_check_button()
    Mastermind.generate_x_button()
    Mastermind.generate_quit_button()
    Mastermind.generate_marbles()
    Mastermind.generate_regs()
    Mastermind.generate_selections()
    Mastermind.generate_arrow()
    Mastermind.generate_leaderboard()


def start_game_play(Mastermind: Mastermind) -> None:
    """ This function start the game. At first, it will generate secret code,
    and then, it will allow players to play the game.

    Args:
        Mastermind (Mastermind): a Mastermind object.
    """
    Mastermind.generate_secret_code()
    Mastermind.play()


def run_game_maintenance(Mastermind: Mastermind) -> None:
    """ This function maint the running of the game.

    Args:
        Mastermind (Mastermind): a Mastermind obkect
    """
    Mastermind.maintain()


def game_exe():
    """ This function is to combine all functions above to create a mastermind
    instance, and run a complete game.
    """
    # initialize the game's configuration
    mastermind = setup_Mastermind_config(path=CONFIGURATION_PATH)
    # ask players to sign in the game
    get_player_sign_in(mastermind)
    # generate the game's UI
    create_Mastermind_ui(mastermind)
    # start playing the game
    start_game_play(mastermind)
    # maintain the game's running
    run_game_maintenance(mastermind)


def main():
    """ The main function deploys a logger to log any possible
    issue occurred in the game_exe function.
    """
    logger = ErrorLogger()
    logger.execute_and_log(game_exe)


if __name__ == "__main__":
    main()
