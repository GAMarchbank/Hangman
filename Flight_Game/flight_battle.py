import random


def game_field_template_gen():
    scene_types = ['forest', 'desert', 'mountains', 'fields', 'valley']
    output_lst = []
    for items in scene_types:
        num = 0
        while num < 5:
            output_lst.append([items, scene_types[num]])
            num += 1
    out_dic = {}
    num = 1
    output_lst += output_lst
    while num < 17:
        card_check = True
        card_choice = random.choice(output_lst)
        if num != 1:
            for nums in range(0,2):
                if card_choice[nums] == out_dic[num-1][nums]:
                    card_check = False
        if card_check == False:
            continue
        output_lst.remove(card_choice)
        out_dic[num] = card_choice
        num += 1
    return out_dic

def game_field_transformer(template):
    out_dic = {}
    for items in template:
        out_dic[items] = {'L': template[items][0], 'R': template[items][1]}
    return out_dic


def deck_shuffle(terrain_trick):
    if terrain_trick == 'trick':
        deck_template = ['swap/pickup', 'shift/rotate', 'forwards/backwards', 'add/remove']
        num_check = 3
    elif terrain_trick == 'terrain':
        deck_template = ['fields', 'mountains', 'forest', 'valley', 'desert']
        num_check = 9
    deck = []
    for cards in deck_template:
        num = 1
        while num != num_check:
            deck.append(cards)
            num += 1
    out_deck = []
    while len(deck) != 0:
        card = random.choice(deck)
        out_deck.append(card)
        deck.remove(card)
    return out_deck

class Players:
    def __init__(self, is_human, l_r):
        self.is_human = is_human
        trick_deck = deck_shuffle('trick') 
        terrain_deck = deck_shuffle('terrain')
        self.trick_deck = trick_deck
        self.terrain_deck = terrain_deck
        self.hand = []
        if l_r == 'L':
            self.location = {'side': 'L', 'coordinate': 0}
        else:
            self.location = {'side': 'R', 'coordinate': 0}
    
    def return_hand(self):
        return self.hand
    
    def return_trick_deck(self):
        return self.trick_deck
    
    def return_terrain_deck(self):
        return self.terrain_deck    
    
    def return_location(self):
        return self.location 
    
    def draw_terrain_card(self):
        card = self.terrain_deck[0]
        self.terrain_deck.remove(card)
        return card
    
    def draw_trick_card(self):
        card = self.trick_deck[0]
        self.trick_deck.remove(card)
        return card
    
    def computer_cards_draw(self, number_of_cards_drawn):
        drawn_cards = []
        while number_of_cards_drawn != 0:
            if len(self.trick_deck) != 0:
                if len(self.terrain_deck) == 0:
                    self.terrain_deck = deck_shuffle('terrain')
                    continue
                card_choice = random.choice(['trick', 'terrain', 'terrain', 'terrain'])
            else:
                card_choice = 'terrain'
            if card_choice == 'trick':
                drawn_cards.append(self.draw_trick_card())
            else:
                drawn_cards.append(self.draw_terrain_card())
            number_of_cards_drawn -= 1
        return drawn_cards
    
    # add human 
    def new_game_create_hand(self):
        if self.is_human == False:
            self.hand = self.computer_cards_draw(7)
    
    # add human 
    def end_turn_draw_new_cards(self, current_hand):
        if self.is_human == False:
            current_hand.append(self.computer_cards_draw(3))
            self.hand = current_hand
            
    # add human 
    def discard_cards(self, current_hand):
        if self.is_human == False:
            if len(current_hand) > 7:
                while len(current_hand) > 7:
                    card = random.choice(current_hand)
                    current_hand.remove(card)
            self.hand = current_hand
    
    # add human
    def make_move(self, game_field):
        if self.is_human == False:
            previous_card = None
            while True:
                if game_field[self.location['coordinate'] + 1][self.location['side']] == previous_card:
                    self.location['coordinate'] += 1
                elif game_field[self.location['coordinate'] + 1][self.location['side']] in self.hand:
                    self.location['coordinate'] += 1
                    previous_card = game_field[self.location['coordinate']][self.location['side']]
                    self.hand.remove(previous_card)
                else:
                    return False
                    
    
            

if __name__ == '__main__':
    computer = Players(False, 'L')
    game_field_template = game_field_template_gen()
    game_field = game_field_transformer(game_field_template)
    print(game_field)
    