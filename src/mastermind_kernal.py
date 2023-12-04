class MastermindKernal:
    """ This class manages the comparison between secret code and a set of
    picked color of the game Mastermind.

    Attributes:
        secret_code (list): A list representing the secret code, where each
                            element is a color.
        picked_colors (list): A list representing the colors picked by players,
                              where each element is a color.
    Methods:
        get_secret_code() -> list:
            Return the secret code.

        get_picked_colors() -> list:
            Return the picked colors.

        get_number_of_correct_position() -> int:
            Return the count of colors in the picked list that are in the
            correct position.

        get_number_of_wrong_position() -> int:
            Return the count of colors in the picked list that are in the
            wrong position.

        is_win() -> bool: 
            Check if the picked colors match the secret code
            exactly, indicating a win.
    """

    def __init__(self, secret_code: list, picked_colors: list) -> None:
        """ Construct all the necessary attributes for MastermindKernal object.

        Args:
            secret_code (list): A list representing the secret code, where each
                                element is a color.
            picked_colors (list): A list representing the colors picked by 
                                  players, where each element is a color.
        """
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
