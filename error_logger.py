from datetime import date


class ErrorLogger:

    def __init__(self) -> None:
        """ Construct all necessary attributes for ErrorLogger object.
        """
        self.day = date.today()

    def execute_and_log(self, fun) -> None:
        """ This method is to execute a function and log errors from
        this function.

        Args:
            fun: a particular function need to be executed and logged.
        """
        try:
            # execute the function
            fun()
        except Exception as e:
            # if any error is raised
            with open(file="mastermind_errors.err", mode='a') as error_file:
                error_file.write(f"{self.day}: \n")
                error_file.write(f"Exception occurred: {e}\n\n")
