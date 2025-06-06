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
    Interface for playing the Movie quote quiz
    """

    def __init__(self, how_many):
        self.rounds_won = IntVar()

        # Lists for stats component

        # Highest Score Test Data
        self.all_scores_list = [1, 1, 1, 1, 1]
        self.all_high_score_list = [1, 1, 1, 1, 1]
        self.rounds_won.set(5)

        # Lowest Score Test Data
        # self.all_scores_list = [0, 0, 0, 0, 0]
        # self.all_high_score_list = [1, 1, 1, 1, 1]
        # self.rounds_won.set(0)

        # Random Score Test Data...
        # self.all_scores_list = [1, 0, 1, 1, 0]
        # self.all_high_score_list = [1, 1, 1, 1, 1]
        # self.rounds_won.set(3)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Movie Quote Quiz", font=("Arial", "16", "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#6A6868", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """
        # Important: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list,
                        self.all_high_score_list]

        DisplayStats(self, stats_bundle)


class DisplayStats:
    """
    Displays stats for Movie quote quiz
    """

    def __init__(self, partner, all_stats_info):
        # extract information from master list...
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        high_scores = all_stats_info[2]

        # sort user scores to find the high score...
        user_scores.sort()

        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # if users press the cross at the top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300)
        self.stats_frame.grid()

        # Math to populate Stats dialogue...
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # strings for stats labels...

        success_string = f"Success Rate: {rounds_won} / {rounds_played}" \
                         f" ({success_rate:.0f}%)"
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"
        average_score_string = f"Average Score: {average_score:.1f}"

        # custom comment text and formatting
        if total_score == max_possible:
            comment_string = "Amazing! You got the \n" \
                             "highest possible score!"
            comment_colour = "#D5E8D4"
        elif total_score == 0:
            comment_string = "Oops - You got all the question\n " \
                             "wrong Try using the hints!"
            comment_colour = "#F8CECC"
            best_score_string = f"Best score: n/a"
        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")

        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, normal_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Highlight comment label
        stats_label_ref_list[4].config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#333333", fg="#FFFFFF",
                                     width=20, command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        # closes help dialogue (used by button and x at top od dialogue)

    def close_stats(self, partner):
        # put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie quote quiz")
    StartGame()
    root.mainloop()
