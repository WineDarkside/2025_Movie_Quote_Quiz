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
    movie_scores.sort()
    median = (movie_scores[1] + movie_scores[2]) / 2
    median = round_ans(median)

    return movie_questions, median


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


class Play:
    """
    Interface for playing the movie Quest Game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = IntVar()

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
        self.quiz_frame.configure(bg="#EDE8D0")

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font| background | row)
        play_labels_list = [
            ["Question # of #", ("Arial", "16", "bold"), None, 0],
            ["Movie Quote", body_font, None, 1],

            ["Choose a movie below. Good Luck.", body_font, "#F0F0F0", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg="#EDE8D0", wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.quote_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up buttons..
        self.movie_frame = Frame(self.quiz_frame)
        self.movie_frame.grid(row=3)
        self.movie_frame.configure(bg="#EDE8D0")

        self.movie_button_ref = []

        # create four button in a 2 x2 grid
        for item in range(0, 4):
            self.movie_button = Button(self.movie_frame, font=("Arial", "12"),
                                       text="Movie Name", width=15, height=2, wraplength=160,
                                       command=partial(self.round_results, item))
            self.movie_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)
            self.movie_button_ref.append(self.movie_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)
        self.hints_stats_frame.configure(bg="#EDE8D0")

        # List for buttons (frame | text | bg| command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Question", "#D0CEE2", self.new_question, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.hint_button, 10, 0, 0],
            [self.hints_stats_frame, "Stats ", "#6A6868", "", 10, 0, 1],
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
        buttons with chosen movies
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.questions_played.get()
        rounds_played += 1
        self.questions_played.set(rounds_played)

        rounds_wanted = self.questions_wanted.get()

        # get rounds movies and median score.
        self.question_quotes_list, median = get_movie_options()

        # set target as median (for later comparison)
        self.target_score.set(median)

        # randomly choose a movie from the 4 to display its quote
        quote_movie = random.choice(self.question_quotes_list)
        self.quote_label.config(text=quote_movie[0], bg="#D5E8D4", font=("Arial", "14", "bold"))
        self.correct_movie = quote_movie[1]
        self.correct_score = int(quote_movie[2])

        # shuffle the 4 movie names and set them as button text
        movie_names = [movie[1] for movie in self.question_quotes_list]
        random.shuffle(movie_names)

        for count, button in enumerate(self.movie_button_ref):
            button.config(text=movie_names[count], state=NORMAL, pady=10, padx=10)

        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.results_label.config(text=f"{'=' * 7}", bg="#EDE8D0")

        self.next_button.config(state=DISABLED)

    def hint_button(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)

    def round_results(self, user_choice):
        """
        Retrieves which buttons was pushed (index 0 -3 ), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """

        # Get user score and movie bases in button press...
        score = int(self.question_quotes_list[user_choice][2])

        # alternate way to get button name. Good for it buttons have been scrambled
        movie_name = self.movie_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()
        self.all_medians_list.append(target)

        # Check if the selected movie matches the correct one
        if movie_name == self.correct_movie:
            if self.correct_score >= target:
                result_text = f"Success! {movie_name} earned you {self.correct_score} points"
                result_bg = "#D5E8D4"
                self.all_scores_list.append(self.correct_score)
            else:
                result_text = f"Oops, correct movie was {self.correct_movie}."
                result_bg = "#F8CECC"
                self.all_scores_list.append(0)
        else:
            result_text = f"Oops, wrong movie! The correct answer was {self.correct_movie}."
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


class DisplayHints:
    """
    Displays hints for Colour Quest Game
    """
    def __init__(self, partner):
        # set dialogue box and background colour
        background = "#FFF2CC"
        self.hint_box = Toplevel()

        # disable hint button
        partner.hint_button.config(state=DISABLED)

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
    root.title("Movie Quote Quiz")
    StartGame()
    root.mainloop()
