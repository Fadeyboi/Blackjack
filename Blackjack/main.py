import random


class Card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

    def change_ace(self):
        self.value = 1


class Deck:
    def __init__(self):
        self.card_deck = []
        for suit in suits:
            for rank in ranks:
                self.card_deck.append(Card(suit, rank))

    def __str__(self):
        for i in self.card_deck:
            print(i)

    def __len__(self):
        return len(self.card_deck)

    def shuffle(self):
        random.shuffle(self.card_deck)

    def deal(self):
        return self.card_deck.pop()


class Player:
    def __init__(self, money):
        self.money = money

    def __str__(self):
        return f'Player has ${self.money}'

    def add_money(self, money):
        self.money += money * 2

    def remove_money(self, money):
        if self.money < money:
            print(f"Sorry, the amount you entered exceeds your funds, try again!\nCurrent balance ${self.money}\n")
            return True
        else:
            self.money -= money
            return False


def calculate_value(list):
    total = 0
    for item in list:
        total += item.value
    return total


def print_list(list):
    for item in list:
        print(f'{item}')


def check_value(list):
    value = calculate_value(list)
    if value > 21:
        return True
    else:
        return False


def check_for_ace(list):
    for item in list:
        if item.rank == 'Ace':
            return True
    return False


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

while True:
    try:
        starting_value = int(input("Welcome to Blackjack, how much money would you like to start with? \n>>>"))
    except:
        print("Sorry, the amount you entered is wrong, please try again.\n\n")
    else:
        break

player = Player(starting_value)
playing = True

while playing:
    betting_amount = eval(input("How much would you like to bet? \n>>>"))
    if player.remove_money(betting_amount):
        continue
    round_start = True
    while round_start:
        deck = Deck()
        deck.shuffle()
        player_hand = []
        dealer_hand = []
        player_hand.append(deck.deal())
        player_hand.append(deck.deal())
        dealer_hand.append(deck.deal())
        print(f'Dealer hands:\n<Hidden Card>\n{dealer_hand[0]}')
        dealer_hand_value = calculate_value(dealer_hand)
        print(f'Value: {dealer_hand_value}\n\n')
        print(f'Player hands:\n{player_hand[0]}\n{player_hand[1]}')
        player_hand_value = calculate_value(player_hand)
        print(f'Value: {player_hand_value}')

        game_over = True
        while player_hand_value <= 21 and game_over:
            while True:
                hit_or_stand = input("\n\nWould you like to hit or stand? h for hit/s for stand: ")
                if hit_or_stand == "h":
                    player_hand.append(deck.deal())
                    player_hand_value = calculate_value(player_hand)
                    # PLAYER HIT
                    if check_value(player_hand):
                        if check_for_ace(player_hand):
                            # CHECKED FOR ACE
                            for card in player_hand:
                                if card.rank == 'Ace':
                                    card.change_ace()
                            # END OF CHECK FOR ACE
                        else:  # LOSS, PLAYER BUSTED
                            dealer_hand.append(deck.deal())
                            dealer_hand_value = calculate_value(dealer_hand)
                            print('Dealer hands:')
                            print_list(dealer_hand)
                            print(f'Value: {dealer_hand_value}\n\n')
                            print('Player hands:')
                            print_list(player_hand)
                            print(f'Value: {player_hand_value}')
                            print("\n\nBusted! Dealer wins\n")
                            round_start = False
                            game_over = False
                            break
                    player_hand_value = calculate_value(player_hand)
                    print(f'Dealer hands:\n<Hidden Card>\n{dealer_hand[0]}')
                    print(f'Value: {dealer_hand_value}\n\n')
                    print('Player hands:')
                    print_list(player_hand)
                    print(f'Value: {player_hand_value}\n\n')
                elif hit_or_stand == "s":
                    while dealer_hand_value < player_hand_value and not check_value(dealer_hand):
                        dealer_hand.append(deck.deal())
                        dealer_hand_value = calculate_value(dealer_hand)
                        if dealer_hand_value > 21:
                            if check_for_ace(dealer_hand):
                                # CHECKED FOR ACE
                                for card in dealer_hand:
                                    if card.rank == 'Ace':
                                        card.change_ace()
                                        dealer_hand_value = calculate_value(dealer_hand)
                                # END OF CHECK FOR ACE
                    if dealer_hand_value > player_hand_value and not check_value(dealer_hand):
                        print('Dealer hands:')
                        print_list(dealer_hand)
                        print(f'Value: {dealer_hand_value}\n\n')
                        print('Player hands:')
                        print_list(player_hand)
                        print(f'Value: {player_hand_value}')
                        print("\n\nDealer hand value is bigger, dealer wins\n")
                        round_start = False
                        game_over = False
                        break
                    elif dealer_hand_value < player_hand_value:
                        print('Dealer hands:')
                        print_list(dealer_hand)
                        print(f'Value: {dealer_hand_value}\n\n')
                        print('Player hands:')
                        print_list(player_hand)
                        print(f'Value: {player_hand_value}')
                        print("\n\nPlayer hand value is bigger, player wins\n")
                        player.add_money(betting_amount)
                        round_start = False
                        game_over = False
                        break
                    elif check_value(dealer_hand):
                        print('Dealer hands:')
                        print_list(dealer_hand)
                        print(f'Value: {dealer_hand_value}\n\n')
                        print('Player hands:')
                        print_list(player_hand)
                        print(f'Value: {player_hand_value}')
                        print("\n\nDealer busted, player wins\n")
                        player.add_money(betting_amount)
                        round_start = False
                        game_over = False
                        break
                    else:
                        print('Dealer hands:')
                        print_list(dealer_hand)
                        print(f'Value: {dealer_hand_value}\n\n')
                        print('Player hands:')
                        print_list(player_hand)
                        print(f'Value: {player_hand_value}')
                        print("\n\nDraw!\n")
                        round_start = False
                        game_over = False
                        break
                else:
                    print("Wrong input, please try again\n\n")

    if player.money == 0:
        playing = False
        print("Sorry, your remaining balance is $0, thank you for playing!")
        break
    while True:
        condition = input(f"Would you like to continue playing? Your remaining balance is ${player.money} y/n\n>>>")
        if condition == "n":
            playing = False
            print(f'Thank you for playing!\nYour balance is {player.money}')
            break
        elif condition == "y":
            break
        else:
            print("Wrong input, please try again\n\n")
