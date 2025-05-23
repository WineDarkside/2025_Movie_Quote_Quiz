from tkinter import *
from functools import partial  # to prevent unwanted windows


# classes start here
class StartGame:
    """
    Initial Quiz interface (asks users how many question
    they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()
        self.start_frame.configure(bg="#EDE8D0")

        # Create play button...
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#333333", bg="#D0CEE2", text="Play", width=10,
                                  command=self.check_questions)
        self.play_button.grid(row=0, column=1)

    def check_questions(self):
        """
        Checks users have entered 1 or more questions for quiz
        """

        Play(10)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and takes across number of rounds to be played
        """
        Play(num_rounds)
        # Hide root window (ie: hide rounds choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the colour quest game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Movie Quotes", font=("Arial", "16", "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Hints", width=15, fg="#333333",
                                   bg="#FFF2CC", padx=10, pady=10, command=self.to_hints)
        self.hints_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)


class DisplayHints:
    """
    Displays hints for Colour Quest Game
    """
    def __init__(self, partner):
        # set dialogue box and background colour
        background = "#FFF2CC"
        self.hint_box = Toplevel()

        # disable hint button
        partner.hints_button.config(state=DISABLED)

        # if users press cross at top, closes hint and
        # 'releases' hint button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text="Hints",
                                        font=("Arial", "24", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "This quiz will show a quote and four " \
                    "movies. Your goal is to choose the correct " \
                    "movie the quote is from and collect points " \
                    "on the way.\n\n" \
                    "You expect to see movies with various " \
                    "genres like comedy, romance, horror etc.\n\n " \
                    "Make sure you choose the right movie\n\n" \
                    "Good luck!" \

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=300,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "18", "bold"),
                                     text="Close", bg="#FEDC85",
                                     fg="#333333",
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # list and loop to set background color on
        # everything except the buttons
        recolor_list = [self.hint_frame, self.hint_heading_label,
                        self.hint_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_hint(self, partner):
        """
        closes hint dialogue (and enables hint button)
        :param partner:
        :return:
        """
        # put hint button back to normal
        partner.hints_button.config(state=NORMAL)
        self.hint_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie Quotes")
    StartGame()
    root.mainloop()
