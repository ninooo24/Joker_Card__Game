from score import calculate_score


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.word = 0
        self.round_wins = 0
        self.score = 0
        self.bonus = False

    def show_initial_cards(self):
        print(f"\n{self.name}'s initial cards: {[(card.rank, card.suit) for card in self.hand[:3]]}")

    def choose_trump_or_no_trump(self):
        while True:
            try:
                choice = input(f"{self.name}, choose a trump suit or 'no' for no trump: ").lower()
                if choice == 'no':
                    return None
                for card in self.hand[:3]:
                    if card.suit.lower() == choice:
                        return card.suit
                raise ValueError("Please choose a valid suit or 'no'.")
            except ValueError as e:
                print(e)

    def choose_word(self, exclude=None):
        while True:
            word = int(input(f"{self.name}, enter your word (0-9): "))
            if 0 <= word <= 9 and (exclude is None or word != exclude):
                self.word = word
                return word

    def play_card(self, played_cards, trump_suit):
        lead_suit = played_cards[0].suit if played_cards else None
        while True:
            print(f"\n{self.name}'s hand: {[(card.rank, card.suit) for card in self.hand]}")
            try:
                index = int(input(f"{self.name}, play a card by index: "))
                if 0 <= index < len(self.hand):
                    chosen_card = self.hand[index]
                    if chosen_card.rank == "Joker":
                        lead_suit = input("Choose lead suit: ")
                    if self.can_play_card(chosen_card, lead_suit, trump_suit):
                        return self.hand.pop(index)
                    else:
                        print("You must follow the suit ")
            except (ValueError, IndexError):
                print("Please choose the valid index.")

    def can_play_card(self, card, lead_suit, trump_suit):
        if lead_suit is None:
            return True
        if card.suit == lead_suit:
            return True
        if card.suit == trump_suit or card.rank == 'Joker':
            return True
        if any(c.suit == lead_suit for c in self.hand):
            return False
        return True

    def add_round_win(self):
        self.round_wins += 1

    def calculate_score(self):
        self.score += calculate_score(self.word, self.round_wins)
        self.round_wins = 0

    def bonus(self):
        if self.round_wins == 4:
            self.bonus = True


