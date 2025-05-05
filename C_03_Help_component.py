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

        self.heading_label = Label(self.game_frame, text="Colour Quest", font=("Arial", "16", "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Hints", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_hints)
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
        background = "#ffe6cc"
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
                                        font=("Arial", "14", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "The score for each colour relates to it's hexadecimal code.\n\n" \
                    "Remember, the hex code for the white is #FFFFFF - which is teh best " \
                    "possible score.\n\n" \
                    "The hex code for black is #000000 which is the worst possible score.\n\n" \
                    "The first score in the code is red, so if you had to choose" \
                    "between red (#FF0000), green (#00FF00) and blue (#0000FF), then" \
                    "red would be the best choice.\n\n" \
                    "Good luck!" \

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
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
    root.title("Colour quest")
    StartGame()
    root.mainloop()
