import random
from deck import Deck
from player import Player
from score import calculate_score, print_scores


class JokerGame:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.current_dealer_index = -1
        self.trump_suit = None

    def start_game(self):
        self.get_player_names()
        self.choose_dealer()
        self.show_player_order()
        for i in range(4):
            self.play_four()
            self.print_four_scores()

        self.print_final_scores()
        for player in self.players:
            if player.bonus:
                print(f"\n{self.players[player].name} has bonus points.")

    def get_player_names(self):
        for i in range(4):
            name = input(f"Enter the name of player {i + 1}: ")
            self.players.append(Player(name))

    def choose_dealer(self):
        self.current_dealer_index = random.randint(0, 3)
        print(f"\n{self.players[self.current_dealer_index].name} is the first dealer.")
        print(f"\n{self.players[(self.current_dealer_index + 1) % 4].name} is choosing the trump.")

    def show_player_order(self):
        print()
        print("Player order:")
        for i in range(4):
            player_index = (self.current_dealer_index + 1 + i) % 4
            print(f"{i + 1}. {self.players[player_index].name}")

    def play_four(self):
        for _ in range(4):
            self.deck.shuffle()
            self.deal_cards()
            self.choose_trump()
            self.collect_words()
            self.play_rounds()
            self.calculate_round_scores()
            self.current_dealer_index = (self.current_dealer_index + 1) % 4

    def deal_cards(self):
        self.deck.reset()
        self.deck.shuffle()
        for player in self.players:
            player.hand = self.deck.deal_hand()

    def choose_trump(self):
        first_player = self.players[(self.current_dealer_index + 1) % 4]
        first_player.show_initial_cards()
        self.trump_suit = first_player.choose_trump_or_no_trump()
        print(f"Trump suit is {self.trump_suit} ")

    def collect_words(self):
        total_word = 0
        for i in range(4):
            player = self.players[(self.current_dealer_index + 1 + i) % 4]
            print(f"\n{player.name}'s cards: {[(card.rank, card.suit) for card in player.hand]}")
            if i == 3:
                player_word = player.choose_word(exclude=9 - total_word)
            else:
                player_word = player.choose_word()
                total_word += player_word

    def play_rounds(self):
        start_player_index = (self.current_dealer_index + 1) % 4
        for i in range(9):
            start_player_index = self.play_single_round(start_player_index)

    def play_single_round(self, start_player_index):
        played_cards = []
        for i in range(4):
            player_index = (start_player_index + i) % 4
            player = self.players[player_index]
            played_cards.append(player.play_card(played_cards, self.trump_suit))
        winner_index = self.determine_winner(played_cards, start_player_index)
        print(f"\n{self.players[winner_index].name} wins this round.")
        self.players[winner_index].add_round_win()
        return winner_index

    def determine_winner(self, played_cards, start_player_index):
        highest_card = played_cards[0]
        highest_player = 0
        for i, card in enumerate(played_cards):
            if card.beats(highest_card, self.trump_suit):
                highest_card = card
                highest_player = i
        return (start_player_index + highest_player) % 4

    def calculate_round_scores(self):
        for player in self.players:
            player.calculate_score()

    def print_final_scores(self):
        print_scores(self.players)
        winner = max(self.players, key=lambda player: player.score)
        print(f"\nThe winner of the game is: {winner.name}")

    def print_four_scores(self):
        print("\nScores after this Four:")
        for player in self.players:
            print(f"{player.name}: {player.score} points")


if __name__ == "__main__":
    game = JokerGame()
    game.start_game()
