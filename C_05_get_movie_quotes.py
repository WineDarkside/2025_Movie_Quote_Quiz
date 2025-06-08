import csv
import random


def round_ans(val):
    """
    rounds numbers to nearest integer
    :param val: number to be rounded
    :RETURN: rounded number (an integer)
    """

    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# Retrieve quotes from csv file and put them in a list
file = open("00_movie_quotes_hex.csv", "r")
all_quotes = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_quotes.pop(0)

movie_questions = []
movie_scores = []

# loop until we have four movies with different scores...
while len(movie_questions) < 4:
    potential_movies = random.choice(all_quotes)

    # get teh score and check it's not a duplicate
    if potential_movies[2] not in movie_scores:
        movie_questions.append(potential_movies)
        # make score an integer and add it to the list of scores
        movie_scores.append(int(potential_movies[2]))

print(movie_questions)
print(movie_scores)

# find target score (median)
int_scores = [int(x) for x in movie_scores]
int_scores.sort()

median = (int_scores[1] + int_scores[2]) / 2
median = round_ans(median)
print("median:", median)
