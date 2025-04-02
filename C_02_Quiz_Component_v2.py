import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


# helper functions go here
def get_quotes():
    """
    Retrieves movies quotes from csv file
    :return: list of quotes which where each list item has the
    movie name, associated score and foreground movie for the text
    """

    # Retrieve quotes from csv file and put them in a list
    file = open("00_movie_quotes_hex.csv", "r")
    all_quotes = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_quotes.pop(0)

    return all_quotes


def get_movie_options():
    """
    Choose four movies from larger list ensuring that teh scores are all different
    :return: list of the movies and score to beat (median of scores)
    """

    all_quotes_list = get_quotes()
    movie_questions = []
    movie_scores = []

    # loop until we have four movies with scores...
    while len(movie_questions) < 4:
        potential_movies = random.choice(all_quotes_list)

        # movie scores are being read as a string
        # change them to an integer to compare / when adding to score list
        if potential_movies[2] not in movie_scores:
            movie_questions.append(potential_movies)
            # make score an integer and add it to the list of scores
            movie_scores.append(int(potential_movies[2]))

    # get median score / target score
    # movie_scores.sort()
    # median = (movie_scores[1] + movie_scores[2]) / 2
    # median = round_ans(median)

    return movie_questions # , median


def round_ans(val):
    """
    rounds numbers to nearest integer
    :param val: number to be rounded
    :RETURN: rounded number (an integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


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

        # Create play button...
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#005708", text="Play", width=10,
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
    Interface for playing the movie Quest Game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        # self.target_score = IntVar()

        # rounds played - start with zero
        self.questions_played = IntVar()
        self.questions_played.set(0)

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        # movie list and score list
        self.question_quotes_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font| background | row)
        play_labels_list = [
            ["Question # of #", ("Arial", "16", "bold"), None, 0],
            ["Quote", body_font, None, 1],
            ["Score to beat:", body_font, "#FFF2CC", 2],
            ["Choose a movie below. Good Luck.", body_font, "#D5E8D4", 3],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.quote_label = play_labels_ref[1]  
        # self.target_label = play_labels_ref[2]
        self.results_label = play_labels_ref[4]

        # set up buttons..
        self.movie_frame = Frame(self.quiz_frame)
        self.movie_frame.grid(row=3)

        self.movie_button_ref = []
        self.movie_button_list = []

        # create four button in a 2 x2 grid
        for item in range(0, 4):
            self.movie_button = Button(self.movie_frame, font=("Arial", "12"),
                                       text="Movie Name", width=15, wraplength=150,
                                       command=partial(self.round_results, item))
            self.movie_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)
            self.movie_button_ref.append(self.movie_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg| command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Question", "#0057D8", self.new_question, 21, 5, None],
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

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # once interface has been created, invoke new
        # round function for first round
        self.new_question()

    def new_question(self):
        """
        Choose four movies, works our median for score to beat. Confiqures
        buttons with chosen movie
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.questions_played.get()
        rounds_played += 1
        self.questions_played.set(rounds_played)

        rounds_wanted = self.questions_wanted.get()

        # get rounds movies and median score.
        self.question_quotes_list, median = get_movie_options()

        # set target as median (for later comparison)
        # self.target_score.set(median)

        # Set the quote above the buttons
        self.quote_label.config(text=self.question_quotes_list[0][0])

        # Update heading, and score to beat labels. "hide" results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        # self.target_label.config(text=f"Target score: {median}", font=("Arial", "14", "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # configure buttons using foreground and background movie from list
        # enable movie buttons (disabled at the end of hte last round)
        for count, button in enumerate(self.movie_button_ref):
            movie_name = self.question_quotes_list[count][1]  # Get movie title
            button.config(text=movie_name, state=NORMAL, pady=10, padx=10)

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which buttons was pushed (index 0 -3 ), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """

        # Get user score and movie quote in button press...
        score = int(self.question_quotes_list[user_choice][2])

        # alternate way to get button name. Good for it buttons have been scrambled
        movie_name = self.movie_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        # target = self.target_score.get()
        # self.all_medians_list.append(target)

        if movie_name >= score:
            result_text = f"Success! {movie_name} was correct,+{score} points"
            result_bg = "#828366"
            self.all_scores_list.append(score)
        else:
            result_text = f"Oops {movie_name} was incorrect ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats & next buttons, disable movie buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        questions_played = self.questions_played.get()
        questions_wanted = self.questions_wanted.get()

        if questions_played == questions_wanted:
            self.next_button.config(state=DISABLED, text="Game over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.movie_button_ref:
            item.config(state=DISABLED)

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
