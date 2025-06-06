from tkinter import *
from functools import partial  # to prevent unwanted windows


class StartGame:
    """
    Initial Game interface (asks users how many rounds
    they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # set background colour
        background = "#EDE8D0"

        # strings for labels
        intro_string = ("In each round you will be shown a quote and 4 different movies. "
                        "Your goal is to choose the correct movie the quote came from.")

        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many questions do you want to play?"

        # List of labels to be made (text | font| fg)
        start_labels_list = [
            ["Movie Quote Quiz", ("Times New Roman ", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"],
        ]

        # Create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], bg=background,
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame, bg=background)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#333333", bg="#D0CEE2", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

        # list and loop to set background color on
        # everything except the buttons
        recolor_list = [self.start_frame]

        for item in recolor_list:
            item.config(bg=background)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold",))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops = Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error id necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Color Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of a {how_many}",
                                        font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour quest")
    StartGame()
    root.mainloop()
