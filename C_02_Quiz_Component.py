from tkinter import *
from functools import partial  # to prevent unwanted windows


class StartGame:
    """
    Initial Quiz interface (asks users how many questions
    they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button...
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_questions)
        self.play_button.grid(row=0, column=1)

    def check_questions(self):
        """
        Checks users have entered 1 or more questions for quiz
        """

        Play(5)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:
    """
    Interface for playing the movie quote quiz
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font| background | row)
        play_labels_list = [
            ["Question # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            [" Choose a movie below from this quote. Good luck", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(item)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up buttons..
        self.movie_frame = Frame(self.quiz_frame)
        self.movie_frame.grid(row=3)

        # create four button in a 2 x2 grid
        for item in range(0, 4):
            self.movie_button = Button(self.movie_frame, font=("Arial", "12"),
                                       text="Movie name", width=15)
            self.movie_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)
        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg| command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Question", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats ", "#333333", "", 10, 0, 1],
            [self.quiz_frame, "End", "#990000", self.close_play, 21, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie Quote Quiz")
    StartGame()
    root.mainloop()
