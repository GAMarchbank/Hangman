import random
from flight_battle_work_templates import trial_game_field_two, trial_game_field_one, specific_card_dic_two
from copy import deepcopy


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


def computer_play_field_sorter(game_field):
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
        if game_field['R'][numbers + r_num]['on_map'] != False and game_field['L'][numbers + l_num]['on_map'] != False:
            try:
                specific_card_dic['L'] = {'card': game_field['L'][numbers + l_num]['card'], 'coordinate': numbers + l_num}
            except Exception:
                pass
            try:
                specific_card_dic['R'] = {'card': game_field['R'][numbers + r_num]['card'], 'coordinate': numbers + r_num}
            except Exception:
                pass
            specific_card_dic['on_map'] = True
        else:
            try:
                if game_field['L'][numbers + r_num]['on_map'] == False:
                    specific_card_dic['L'] = [{'card': game_field['L'][numbers + l_num]['card'], 'coordinate': numbers + l_num}, {'card': game_field['L'][numbers + l_num + 1]['card'], 'coordinate': numbers + l_num + 1}]
                    r_num -= 2
            except KeyError:
                pass
            try:
                if game_field['R'][numbers + r_num]['on_map'] == False:
                    specific_card_dic['R'] = [{'card': game_field['R'][numbers + r_num]['card'], 'coordinate': numbers + r_num}, {'card': game_field['R'][numbers + r_num + 1]['card'], 'coordinate': numbers + r_num + 1}]
                    l_num -= 2
            except KeyError:
                pass
            specific_card_dic['on_map'] = False
        if specific_card_dic != {'on_map': False}:
            card_list.append(specific_card_dic)
    return card_list

def computer_ai_swap_card_sorter(computer_intergrated_game_field, l_r, location):
    if l_r == 'L':
        oppostion = 'R'
    else:
        oppostion = 'L'
    select_path = False
    this_user_cards_ahead = []
    other_side_addition_list = []
    for sides in [l_r, oppostion]:
        if location['side'] != l_r and sides == l_r:
            pass
        else:
            for items in computer_intergrated_game_field:
                try:
                    check = items[sides]
                except KeyError:
                    pass
                else:
                    if location['side'] == l_r and sides != l_r:
                        if type(items[sides]) == list:
                            for item in items[sides]:
                                item['sides'] = sides
                                other_side_addition_list.append(item)
                        else:
                            items[sides]['side'] = sides
                            other_side_addition_list.append(items[sides])
                    else:
                        if type(items[sides]) == list:
                            for item in items[sides]:
                                if l_r == location['side']:
                                    if item['coordinate'] > location['coordinate']:
                                        item['side'] = sides
                                        this_user_cards_ahead.append(item)
                                else:
                                    if item['coordinate'] < location['coordinate']:
                                        item['side'] = sides
                                        this_user_cards_ahead.append(item)  
                                        select_path = True   
                        else:
                            if l_r == location['side']:
                                if items[sides]['coordinate'] > location['coordinate']:
                                    items[sides]['side'] = sides
                                    this_user_cards_ahead.append(items[sides])
                            else:
                                if items[sides]['coordinate'] < location['coordinate']:
                                    items[sides]['side'] = sides
                                    this_user_cards_ahead.append(items[sides])    
                                    select_path = True                                 
    if len(other_side_addition_list) != 0:
        for items in reversed(other_side_addition_list):
            this_user_cards_ahead.append(items)
    if select_path == True:
        this_user_cards_ahead = list(reversed(this_user_cards_ahead))
    return this_user_cards_ahead

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
        
    def test_settings(self, test_setting, finness = None):
        if test_setting == 'location':
            if finness == None:
                self.location = {'side': self.l_r, 'coordinate': 7}
            else:
                self.location = finness

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
    
    def computer_swap_decision_maker(self, computer_intergrated_game_field, enemy_location, decide):
        computer_ahead = computer_ai_swap_card_sorter(computer_intergrated_game_field, self.l_r, self.location)    
        if self.l_r == 'L':
            op_l_r = 'R'
        else:
            op_l_r = 'L'
        opp_ahead = computer_ai_swap_card_sorter(computer_intergrated_game_field, op_l_r, enemy_location)
        temp_collated_list = []
        for items in computer_ahead:
            if items in opp_ahead:
                opp_ahead.remove(items)
                temp_collated_list.append(items)
        for items in temp_collated_list:
            if items in computer_ahead:
                computer_ahead.remove(items)
        if len(computer_ahead) == 0 and len(opp_ahead) == 0:
            return False
        cards_to_be_moved = []
        move_choice = False
        for cards in computer_ahead:
            if computer_ahead.index(cards) != 0 and computer_ahead.index(cards) != len(computer_ahead)-1:
                if computer_ahead[computer_ahead.index(cards)-1]['card'] == computer_ahead[computer_ahead.index(cards)+1]['card']:
                    cards_to_be_moved.append([cards, computer_ahead[computer_ahead.index(cards)+1]['card']])
        if len(cards_to_be_moved) != 0:
            move_choice = random.choice(cards_to_be_moved)
        op_cards_to_be_moved = []
        op_move_choice = False
        for cards in opp_ahead:
            card_check = False
            if opp_ahead.index(cards) != 0:
                if cards['card'] == opp_ahead[opp_ahead.index(cards)-1]['card']:
                    card_check = True
            if opp_ahead.index(cards) != len(opp_ahead)-1:
                if cards ['card'] == opp_ahead[opp_ahead.index(cards)+1]['card']:
                    if card_check == True:
                        op_move_choice = cards
                    card_check = True
            if card_check == True:
                op_cards_to_be_moved.append([cards, cards['card']])
        if len(op_cards_to_be_moved) != 0:
            op_move_choice = random.choice(op_cards_to_be_moved)
        same_card_check = False
        if move_choice != False and op_move_choice != False:
            for cards in computer_intergrated_game_field:
                for sides in ['L', 'R']:
                    try:
                        cards[sides] 
                    except KeyError:
                        pass
                    else:
                        if type(cards[sides]) == list:
                            check_num = 0
                            if ({'card': move_choice[0]['card'], 'coordinate': move_choice[0]['coordinate']} in cards[sides]) and sides == move_choice[0]['side']:
                                check_num += 1
                                check_num +=1
                            if check_num == 2: 
                                same_card_check = True
                        else:
                            if (cards[sides]['card'] == move_choice[0]['card'] and cards[sides]['coordinate'] == move_choice[0]['coordinate']) and sides == move_choice[0]['side']:
                                if (cards[sides]['card'] == op_move_choice[0]['card'] and cards[sides]['coordinate'] == op_move_choice[0]['coordinate']) and sides == op_move_choice[0]['side']:
                                    same_card_check = True
        un_swappable_cards_pile = deepcopy(computer_ahead)
        swap_card_lst = []
        for cards in opp_ahead:
            if cards in un_swappable_cards_pile:
                pass
            else:
                un_swappable_cards_pile.append(cards)
        for cards in computer_intergrated_game_field:
            for sides in ['L', 'R']:
                if sides == 'L':
                    other_side = 'R'
                else:
                    other_side = 'L'
                try:
                    cards[sides]
                except KeyError:
                    pass
                else:
                    if type(cards[sides]) == list:
                        if ({'card': cards[sides][0]['card'], 'coordinate': cards[sides][0]['coordinate'], 'side': sides} not in un_swappable_cards_pile) and ({'card': cards[sides][1]['card'], 'coordinate': cards[sides][1]['coordinate'], 'side': other_side} not in un_swappable_cards_pile):
                            if cards not in swap_card_lst:
                                swap_card_lst.append(cards) 
                    elif ({'card': cards[sides]['card'], 'coordinate': cards[sides]['coordinate'], 'side': sides} not in un_swappable_cards_pile) and ({'card': cards[other_side]['card'], 'coordinate': cards[other_side]['coordinate'], 'side': other_side} not in un_swappable_cards_pile): 
                        if cards not in swap_card_lst:
                            swap_card_lst.append(cards)
        selected_card_to_swap = None                   
        while True:
            if selected_card_to_swap == None:
                if same_card_check == True:
                    for cards in swap_card_lst:
                        try:
                            cards[move_choice[0]['side']]
                        except KeyError:
                            pass
                        else:
                            if type(cards[move_choice[0]['side']]) == list:
                                if (cards[move_choice[0]['side']][0]['card'] == move_choice[1] and cards[move_choice[0]['side']][1]['card'] == op_move_choice[1]) or (cards[move_choice[0]['side']][1]['card'] == move_choice[1] and cards[move_choice[0]['side']][0]['card'] == move_choice[1]):
                                    selected_card_to_swap = [cards, move_choice]
                                    break
                            elif cards[move_choice[0]['side']]['card'] == move_choice[1] and cards[op_move_choice[0]['side']]['card'] == op_move_choice[1]:
                                selected_card_to_swap = [cards, move_choice]
                                break
                    same_card_check = False
                    continue
                elif same_card_check == False and (move_choice != False or op_move_choice != False):
                    choice_list = []
                    if move_choice != False:
                        choice_list.append(move_choice)
                    if op_move_choice != False:
                        choice_list.append(op_move_choice)
                    move = random.choice(choice_list)
                    for cards in swap_card_lst:
                        try:
                            cards[move[0]['side']]
                        except KeyError:
                            pass
                        else:
                            if type(cards[move[0]['side']]) == list:
                                if cards[move[0]['side']][0]['card'] == move[1] or cards[move[0]['side']][1]['card'] == move[1]:
                                    selected_card_to_swap = [cards, move]
                                    break
                            elif cards[move[0]['side']]['card'] == move[1]:
                                selected_card_to_swap = [cards, move]
                                break
                    if move == move_choice:
                        move_choice = False
                    elif move == op_move_choice:
                        op_move_choice = False
                    continue
                else:
                    selected_card_to_swap = None
                    break
            else:
                break
        if selected_card_to_swap != None:
            if decide == False:
                whole_card = None
                for cards in computer_intergrated_game_field:
                    try:
                        cards[selected_card_to_swap[1][0]['side']]
                    except KeyError:
                        pass
                    else:
                        if type(cards[selected_card_to_swap[1][0]['side']]) == list:
                            if (cards[selected_card_to_swap[1][0]['side']][0]['card'] == selected_card_to_swap[1][0]['card'] and cards[selected_card_to_swap[1][0]['side']][0]['coordinate'] == selected_card_to_swap[1][0]['coordinate']) or (cards[selected_card_to_swap[1][0]['side']][1]['card'] == selected_card_to_swap[1][0]['card'] and cards[selected_card_to_swap[1][0]['side']][1]['coordinate'] == selected_card_to_swap[1][0]['coordinate']):
                                whole_card = cards
                        else:
                            if cards[selected_card_to_swap[1][0]['side']]['card'] == selected_card_to_swap[1][0]['card']:
                                whole_card = cards
                if whole_card != None:
                    selected_card_to_swap = [selected_card_to_swap[0], whole_card]
                    return selected_card_to_swap 
                return False
            else:
                return True
        else:
            return False   
     
    # turn necessary sections of the above function into independent functions so you can call apon them here to make this simpler to write. 
    def computer_shift_decision_maker(self, game_field, op_location, decide):
        pass
    
    def computer_trick_card_selectors(self, game_field, enemy_location):
        while True:
            computer_intergrated_game_field = computer_play_field_sorter(game_field)
            trick_card_selector_list =[]
            if 'swap/pickup' in self.hand:
                trick_card_selector_list.append({'move': 'pickup', 'card': 'swap/pickup', 'action': None})
                swap_card = self.computer_swap_decision_maker(computer_intergrated_game_field, enemy_location, False)
                if swap_card != False:
                    trick_card_selector_list.append({'move': 'swap', 'card': 'swap/pickup', 'action': swap_card})
            if 'shift/rotate' in self.hand:
                
                pass
            if 'forwards/backwards' in self.hand:
                pass
            if 'add/remove' in self.hand:
                pass
            break
        return game_field

    # add human, change this so it runs one card at a time, and returns the value of the card its played. 
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
    lits = []
    computer = Players(False, 'L')
    op_computer = Players(False, 'R')
    computer.new_game_create_hand()
    op_computer.new_game_create_hand()
    computer.test_settings('location', {'side': 'L', 'coordinate': 3})
    op_computer.test_settings('location', {'side': 'R', 'coordinate': 3})
    game_field_two = computer_play_field_sorter(trial_game_field_two)
    game_field_one = computer_play_field_sorter(trial_game_field_one)
    computer.computer_swap_decision_maker(game_field_one, op_computer.return_location(), True)
    computer.computer_swap_decision_maker(game_field_two, op_computer.return_location(), True)
    