import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


# helper functions go here
def get_quotes():
    """
    Retrieves movies quotes from csv file
    :return: list of quotes where each list item has the
    movie name and a score of +1
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
    Choose 4 movies from larger list ensuring that the movies are all different
    :return: list of the movies
    """

    all_quotes_list = get_quotes()
    movie_questions = []

    # loop until we have four different movies
    while len(movie_questions) < 4:
        potential_movies = random.choice(all_quotes_list)

        # Ensure the selected movie is unique (different)
        if potential_movies[2] not in movie_questions:
            movie_questions.append(potential_movies)

    return movie_questions


# classes start here
class StartGame:
    """
    Initial Game interface
    (asks users how many questions they would like to play)
    """

    def __init__(self):
        """
        Gets number of questions from user
        """
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # set background colour
        background = "#EDE8D0"

        # strings for labels
        intro_string = ("In each round you will be shown a quote and 4 different movies. "
                        "Your goal is to choose the correct movie the quote came from.")
        choose_string = "How many questions do you want to play?"

        # List of labels to be made (text | font| fg)
        start_labels_list = [
            ["Movie Quote Quiz", ("Times New Roman ", "18", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"],
        ]

        # Create labels and add them to the reference list
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
        self.entry_area_frame = Frame(self.start_frame,bg=background)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button
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
        Checks users have entered 1 or more questions
        """
        # Retrieve number of questions wanted
        questions_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold",))
        self.num_rounds_entry.config(bg="#FFFFFF")

        # error message for when user enters invalid number
        error = "Oops = Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is number above zero
        try:
            questions_wanted = int(questions_wanted)
            if questions_wanted > 0:
                # when users play a new quiz, they don't see an error message
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many questions do you want to play?")
                # Invoke Play Class (and take across number of rounds)
                Play(questions_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Movie Quote Quiz
    """

    def __init__(self, how_many):

        background = "#EDE8D0"

        # Integers / String Variables
        self.questions_played = IntVar()
        self.questions_played.set(0)

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.rounds_won = IntVar()

        # quote list and score list
        self.question_quotes_list = []
        self.all_scores_list = []

        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box, bg=background)
        self.quiz_frame.grid(padx=10, pady=10)

        self.all_high_score_list = []

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
                                    bg=background, wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.quote_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up buttons...
        self.movie_frame = Frame(self.quiz_frame, bg=background)
        self.movie_frame.grid(row=3)

        self.movie_button_ref = []

        # create four button in a 2 x2 grid
        for item in range(0, 4):
            self.movie_button = Button(self.movie_frame, font=("Arial", 12),
                                       text="Movie Name", bg="#FDFFD6", width=15, height=2, wraplength=160,
                                       command=partial(self.round_results, item))
            self.movie_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)
            self.movie_button_ref.append(self.movie_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame, bg=background)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg| command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Question", "#D0CEE2", self.new_question, 24, 5, None],
            [self.hints_stats_frame, "Help", "#FF8000", self.to_hints, 11, 0, 0],
            [self.hints_stats_frame, "Stats ", "#808080", self.to_stats, 11, 0, 1],
            [self.quiz_frame, "End", "#990000", self.close_play, 24, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hint_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.stats_button.config(state=DISABLED)

        # once interface has been created, invoke new
        # round function for first round
        self.new_question()

    def new_question(self):
        """
        Choose four movies and configure buttons with chosen movies
        """
        background = "#EDE8D0"

        # retrieve number of questions played, add one to it and configure heading
        questions_played = self.questions_played.get()
        questions_wanted = self.questions_wanted.get()

        # get question movies
        self.question_quotes_list = get_movie_options()

        # randomly choose a movie from the 4 to display its quote
        quote_movie = random.choice(self.question_quotes_list)
        self.quote_label.config(text=quote_movie[0], bg="#FFFFFF", font=("Arial", "14", "bold"))
        self.correct_movie = quote_movie[1]
        self.correct_score = int(quote_movie[2])

        # shuffle the 4 movie names and set them as button text
        movie_names = [movie[1] for movie in self.question_quotes_list]
        random.shuffle(movie_names)

        # from round_results changes the colors back to original color
        for count, button in enumerate(self.movie_button_ref):
            button.config(text=movie_names[count], state=NORMAL, pady=10, padx=10, bg="#FDFFD6")

        self.heading_label.config(text=f"Question {questions_played + 1} of {questions_wanted}", font=("Arial", "18", "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg=background)

        # Disable next button until a choice is made
        self.next_button.config(state=DISABLED)

    def to_hints(self):
        """
        Displays hints for playing quiz
        """
        # check we have played at least one round so that
        # stats button is not enabled in error.
        questions_played = self.questions_played.get()
        DisplayHints(self, questions_played)

    def round_results(self, user_choice):
        """
        Retrieves which buttons was pushed (index 0 -3 ), retrieves
        score updates results
        """
        # Enable stats button after at least one round has been played
        self.stats_button.config(state=NORMAL)

        # Add one to the number of questions played and retrieve
        # the number of questions won...
        questions_played = self.questions_played.get() + 1
        self.questions_played.set(questions_played)

        rounds_won = self.rounds_won.get()

        # alternate way to get button name. buttons have been scrambled
        movie_name = self.movie_button_ref[user_choice].cget('text')

        # Reset all button backgrounds to default
        for button in self.movie_button_ref:
            button.config(bg="#FDFFD6")

        # Check if the selected movie matches the correct one
        if movie_name == self.correct_movie:
            result_text = f"Success! {movie_name} earned you {self.correct_score} point"
            result_bg = "#D5E8D4"
            self.all_scores_list.append(self.correct_score)

            rounds_won += 1
            self.rounds_won.set(rounds_won)

            # selected button turns green (correct)
            self.movie_button_ref[user_choice].config(bg="#D5E8D4")

        else:
            result_text = f"Oops, wrong movie! The correct answer was {self.correct_movie}."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)
            self.all_high_score_list.append(self.correct_score)

            # selected button turns red (incorrect)
            self.movie_button_ref[user_choice].config(bg="#F8CECC")

            # Turn the correct movie button green
            for i, button in enumerate(self.movie_button_ref):
                if button.cget('text') == self.correct_movie:
                    button.config(bg="#D5E8D4")
                    break

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats & next buttons, disable movie buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if quiz is over
        questions_played = self.questions_played.get()
        questions_wanted = self.questions_wanted.get()

        if questions_played == questions_wanted:
            # work out success rate
            success_rate = rounds_won / questions_played * 100
            success_string = (f"Success Rate: "
                              f"{rounds_won} / {questions_played} "
                              f"({success_rate:.0f}%)")

            # Configure 'end of quiz' labels / buttons
            self.heading_label.config(text="End of Quiz")
            self.results_label.config(text=success_string)
            self.next_button.config(state=DISABLED, text="End of Quiz")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.movie_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # quiz / allow new quiz to start
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        """
        Retrieves everything we need to display the quiz / round statistics
        """
        # Important: retrieve number of rounds won as a number
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list,
                        self.all_high_score_list]

        DisplayStats(self, stats_bundle)


class DisplayHints:
    """
    Displays hints for Movie Quote QUiz
    """

    def __init__(self, partner, questions_played):
        self.questions_played = questions_played

        # set dialogue box and background colour
        background = "#FFF2CC"
        self.hint_box = Toplevel()

        # disable hint, stats and end game buttons to prevent users
        # from leaving a dialogue open and then going back to the questions dialogue
        partner.hint_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # if users press cross at top, closes hint and
        # 'releases' hint button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text="Help",
                                        font=("Arial", 24, "bold"))
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
                                     font=("Arial", 18, "bold"),
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
        partner.hint_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)

        # only enable stats button if we have
        # played at least one round
        if self.questions_played >= 1:
            partner.stats_button.config(state=NORMAL)

        self.hint_box.destroy()


class DisplayStats:
    """
    Displays stats for Movie quote quiz
    """

    def __init__(self, partner, all_stats_info):
        # disable buttons to prevent program crashing
        partner.hint_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # extract information from master list...
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        # high_scores = all_stats_info[2]

        # sort user scores to find the high score...
        user_scores.sort()

        self.stats_box = Toplevel()

        # if users press the cross at the top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300)
        self.stats_frame.grid()

        # Math to populate Stats dialogue...
        questions_played = len(user_scores)

        success_rate = rounds_won / questions_played * 100
        total_score = sum(user_scores)
        max_possible = questions_played

        best_score = user_scores[-1]
        average_score = total_score / questions_played

        # strings for stats labels...

        success_string = f"Success Rate: {rounds_won} / {questions_played}" \
                         f" ({success_rate:.0f}%)"
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"
        average_score_string = f"Average Score: {average_score:.1f}"

        # Check if quiz is complete
        quiz_complete = (questions_played == partner.questions_wanted.get())

        if quiz_complete:
            # custom comment text and formatting
            if total_score == max_possible:
                comment_string = "Amazing! You got the \n" \
                                 "highest possible score!"
                comment_colour = "#D5E8D4"
            elif total_score == 0:
                comment_string = "Oops - You got all the question\n " \
                                 "wrong Try using the Help!"
                comment_colour = "#F8CECC"
                best_score_string = f"Best score: n/a"
            else:
                comment_string = ""
                comment_colour = "#F0F0F0"

        else:
            comment_string = "Quiz in progress...\nMore questions to come!"
            comment_colour = "#FFF2CC"

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

        self.dismiss_button = Button(self.stats_frame, font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#333333", fg="#FFFFFF",
                                     width=20, command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        # closes help dialogue (used by button and x at top od dialogue)

    def close_stats(self, partner):
        # put stats button back to normal
        partner.hint_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)

        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie Quote Quiz")

    StartGame()
    root.mainloop()
