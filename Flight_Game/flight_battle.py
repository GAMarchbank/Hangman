import random
from flight_battle_work_templates import trial_game_field_two


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
    out_dic = {'L': {}, 'R': {}}
    for items in template:
        out_dic['L'][items] = {'card': template[items][0], 'on_map': True}
        out_dic['R'][items] = {'card': template[items][1], 'on_map': True}
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

# maybe think about refigering this with unque code numbers for each card. might be an easier way of doing what im trying to do  
def computer_play_field_sorter(game_field):
    card_dupe_slip = False
    r_num = len(game_field['R'])
    l_num = len(game_field['L'])
    if r_num > l_num:
        out_num = r_num
    else:
        out_num = l_num
    l_num = 0
    r_num = 0
    card_list = []
    for numbers in range(1, out_num+1):
        specific_card_dic = {}
        if game_field['R'][numbers + r_num]['on_map'] == False or game_field['L'][numbers + l_num]['on_map'] == False:
            
            try:
                if game_field['R'][numbers + r_num]['on_map'] == True:
                    specific_card_dic['R'] = {'card': game_field['R'][numbers + r_num]['card'], 'coordinate': numbers + r_num}
                else:
                    specific_card_dic['R'] = [{'card': game_field['R'][numbers + r_num]['card'], 'coordinate': numbers + r_num}, {'card': game_field['R'][numbers + r_num + 1]['card'], 'coordinate': numbers + r_num + 1}]
                    r_num += 2
            except Exception:
                pass
            try:
                if game_field['L'][numbers + l_num]['on_map'] == True:
                    specific_card_dic['L'] = {'card': game_field['L'][numbers + l_num]['card'], 'coordinate': numbers + l_num}
                else:
                    specific_card_dic['L'] = [{'card': game_field['L'][numbers + l_num]['card'], 'coordinate': numbers + l_num}, {'card': game_field['L'][numbers + l_num + 1]['card'], 'coordinate': numbers + l_num + 1}]
                    l_num += 2
            except Exception:
                pass
        card_list.append(specific_card_dic)
    return card_list

class Players:
    def __init__(self, is_human, l_r):
        self.is_human = is_human
        trick_deck = deck_shuffle('trick') 
        terrain_deck = deck_shuffle('terrain')
        self.trick_deck = trick_deck
        self.terrain_deck = terrain_deck
        self.hand = []
        self.l_r = l_r
        if l_r == 'L':
            self.location = {'side': 'L', 'coordinate': 0}
        else:
            self.location = {'side': 'R', 'coordinate': 0}
        self.test_check = False
        
    def set_test(self):
        self.test_check = True
    
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
    def end_turn_draw_new_cards(self):
        if self.is_human == False:
            self.hand.append(self.computer_cards_draw(3))
            
    # add human 
    def discard_cards(self, current_hand):
        if self.is_human == False:
            if len(current_hand) > 7:
                while len(current_hand) > 7:
                    card = random.choice(current_hand)
                    current_hand.remove(card)
            self.hand = current_hand
    
    def computer_trick_card_selectors(self, game_field, enemy_location):
        while True:
            trick_card_selector_list =[]
            if 'swap/pickup' in self.hand:
                trick_card_selector_list.append({'move': 'pickup', 'card': 'swap/pickup'})
                if self.l_r == self.location['side']:
                    pass
                    # this is gonna be really hard. possibly worth thinking this through fully before i make any further moves. 
                else:
                    pass
                if self.l_r != enemy_location['side']:
                    pass
                else:
                    pass
                    
            if 'shift/rotate' in self.hand:
                pass
            if 'forwards/backwards' in self.hand:
                pass
            if 'add/remove' in self.hand:
                pass
            break
        return game_field

    # add human
    def make_move(self, game_field, enemy_location):
        if self.is_human == False:
            previous_card = None
            trick_card_check = False
            if self.test_check == True:
                cards_used = 0
            while True:
                while True:
                    if game_field[self.location['side']][self.location['coordinate'] + 1]['card'] == previous_card:
                        self.location['coordinate'] += 1
                    elif game_field[self.location['side']][self.location['coordinate'] + 1]['card'] in self.hand:
                        self.location['coordinate'] += 1
                        previous_card = game_field[self.location['side']][self.location['coordinate']]['card']
                        self.hand.remove(previous_card)
                        cards_used += 1
                    else:
                        if trick_card_check == True:
                            if self.test_check == True:
                                return cards_used
                            else:
                                return False
                        else:
                            break
                game_field = self.computer_trick_card_selectors(game_field, enemy_location) 
                trick_card_check = True
            
            
            
            

if __name__ == '__main__':
    # computer = Players(False, 'L')
    # game_field_template = game_field_template_gen()
    # game_field = game_field_transformer(game_field_template)
    game_field = computer_play_field_sorter(trial_game_field_two)
    print(game_field)
    