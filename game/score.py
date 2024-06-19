def calculate_score(word, round_wins):
    if word == round_wins:
        if word == 9:
            return 900
        else:
            return 50 + 50 * word
    elif round_wins == 0 and word != 0:
        return -500
    else:
        if round_wins > word:
            return 10 * max(round_wins, word)
        else:
            return 10 * min(round_wins, word)


def print_scores(players):
    print("\nScores:")
    for player in players:
        print(f"{player.name}: {player.score} points")

