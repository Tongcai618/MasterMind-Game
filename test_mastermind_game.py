
import unittest
# Importing all classes and functions from the game script
from mastermind_game import MasterMindKernal


class TestMastermindGame(unittest.TestCase):
    """
    Test suite for the Mastermind game excluding graphical components.
    """

    # def setUp(self):
    # """
    # Set up any necessary data or configurations needed before each test.
    # """
    # config = load_config(path='config.txt')
    # self.width = int(config["width"])
    # self.height = int(config["height"])
    # self.speed = int(config["speed"])
    # self.button_radius = int(config["button_radius"])
    # self.marble_radius = int(config["marble_radius"])
    # self.reg_radius = int(config["reg_radius"])
    # self.title = config["title"]
    # self.leaderboard_path = config["leaderboard_path"]
    # self.colors = config["colors"].replace(' ', '').split(',')
    # self.font = tuple(config['font'].replace(' ', '').split(','))
    # pass  # Implement any set up procedures if needed

    def tear_MasterMindKernal(self):
        """
        Test Class MasterMindKernal
        """
        # test the winning situation
        mmc = MasterMindKernal(
            secret_code=['yellow', 'blue', 'red', 'black'],
            picked_colors=['yellow', 'blue', 'red', 'black']
        )
        self.assertEqual(mmc.get_number_of_correct_position, 4)
        self.assertEqual(mmc.get_number_of_wrong_position, 0)
        self.assertEqual(mmc.is_win, True)
        # test other situation
        mmc = MasterMindKernal(
            secret_code=['yellow', 'blue', 'purple', 'black'],
            picked_colors=['yellow', 'blue', 'red', 'black']
        )
        self.assertEqual(mmc.get_number_of_correct_position, 3)
        self.assertEqual(mmc.get_number_of_wrong_position, 0)
        self.assertEqual(mmc.is_win, False)

        mmc = MasterMindKernal(
            secret_code=['yellow', 'blue', 'purple', 'black'],
            picked_colors=['yellow', 'red', 'blue', 'green']
        )
        self.assertEqual(mmc.get_number_of_correct_position, 1)
        self.assertEqual(mmc.get_number_of_wrong_position, 1)
        self.assertEqual(mmc.is_win, False)

        mmc = MasterMindKernal(
            secret_code=['yellow', 'blue', 'purple', 'black'],
            picked_colors=['blue', 'red', 'yellow', 'green']
        )
        self.assertEqual(mmc.get_number_of_correct_position, 0)
        self.assertEqual(mmc.get_number_of_wrong_position, 2)
        self.assertEqual(mmc.is_win, False)
        pass

    # def test_MasterMind(self):
    #     mm = MasterMind(
    #         width=self.width,
    #         height=self.height,
    #         title=self.title,
    #         speed=self.speed,
    #         button_radius=self.button_radius,
    #         marble_radius=self.marble_radius,
    #         reg_radius=self.reg_radius,
    #         colors=self.colors,
    #         leaderboard_path=self.leaderboard_path,
    #         font=self.font)
    #     pass


# This allows the test suite to be run from the command line
if __name__ == '__main__':
    unittest.main()
