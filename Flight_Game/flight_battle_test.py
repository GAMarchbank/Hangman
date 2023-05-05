import unittest
import flight_battle
import random


class TestFlights(unittest.TestCase):
    
    def setUp(self):
        self.game_field_template = flight_battle.game_field_template_gen()
    
    def test_game_field_size(self):
        self.assertEqual(len(self.game_field_template), 16, 'The playfield is of the wrong size.')
    
    def test_game_field_cards(self):
        terrain_cards = ["['forest', 'forest']", "['forest', 'desert']", "['forest', 'mountains']", "['forest', 'fields']", "['forest', 'valley']", "['desert', 'forest']", "['desert', 'desert']", "['desert', 'mountains']", "['desert', 'fields']", "['desert', 'valley']", "['mountains', 'forest']", "['mountains', 'desert']", "['mountains', 'mountains']", "['mountains', 'fields']", "['mountains', 'valley']", "['fields', 'forest']", "['fields', 'desert']", "['fields', 'mountains']", "['fields', 'fields']", "['fields', 'valley']", "['valley', 'forest']", "['valley', 'desert']", "['valley', 'mountains']", "['valley', 'fields']", "['valley', 'valley']"]
        for cards in self.game_field_template:
            self.assertIn(str(self.game_field_template[cards]), terrain_cards, 'There are cards in the play field not in the deck.')
            
    def test_game_field_cards_duplicates(self):
        terrain_cards_dic = {"['forest', 'forest']": 2, "['forest', 'desert']": 2, "['forest', 'mountains']": 2, "['forest', 'fields']": 2, "['forest', 'valley']": 2, "['desert', 'forest']": 2, "['desert', 'desert']": 2, "['desert', 'mountains']": 2, "['desert', 'fields']": 2, "['desert', 'valley']": 2, "['mountains', 'forest']": 2, "['mountains', 'desert']": 2, "['mountains', 'mountains']": 2, "['mountains', 'fields']": 2, "['mountains', 'valley']": 2, "['fields', 'forest']": 2, "['fields', 'desert']": 2, "['fields', 'mountains']": 2, "['fields', 'fields']": 2, "['fields', 'valley']": 2, "['valley', 'forest']": 2, "['valley', 'desert']": 2, "['valley', 'mountains']": 2, "['valley', 'fields']": 2, "['valley', 'valley']": 2}
        for cards in self.game_field_template:
            terrain_cards_dic[str(self.game_field_template[cards])] -= 1
            self.assertNotEqual(terrain_cards_dic[str(self.game_field_template[cards])], -1, 'There are more then the allocated number of cards in the play field.')
    
    def test_game_field_cards_repeats(self):
        for cards in self.game_field_template:
            if cards == 1:
                pass
            else:
                num = 0
                while num < 2:
                    self.assertNotEqual(self.game_field_template[cards][num], self.game_field_template[cards-1][num],'Two of the same terrain types are next to each other.')
                    num += 1
    
    def test_game_field_transformer(self):
        self.game_field = flight_battle.game_field_transformer(self.game_field_template)
        for items in self.game_field['L']:
            self.assertEqual(self.game_field['L'][items]['card'], self.game_field_template[items][0], 'The left row of the game field does not match its template.')
            self.assertEqual(self.game_field['L'][items]['on_map'], True, "The left row of the game field contains cards that arn't located on the map.")
        for items in self.game_field['R']:
            self.assertEqual(self.game_field['R'][items]['card'], self.game_field_template[items][1], 'The right row of the game field does not match its template.')
            self.assertEqual(self.game_field['R'][items]['on_map'], True, "The right row of the game field contains cards that arn't located on the map.")
        
class TestPlayersDecks(unittest.TestCase):
    def setUp(self):
        self.user = flight_battle.Players(True, 'L')
        self.second_user = flight_battle.Players(True, 'L')
    
    def test_return_terrain_deck_number(self):
        self.assertEqual(len(self.user.return_terrain_deck()), 40, 'There are too many cards in the terrain deck.')
    
    def test_return_location(self):
        self.assertEqual(self.user.return_location()['side'], 'L', 'The player is returned on the wrong side.')
        self.assertEqual(self.user.return_location()['coordinate'], 0, 'The uses does not start at the start of the play field.')
        
    def test_return_terrain_deck_repeats(self):
        terrain_deck_dic = {'forest': 8, 'fields': 8, 'desert': 8, 'mountains': 8, 'valley': 8}
        for cards in self.user.return_terrain_deck():
            terrain_deck_dic[cards] -= 1
            self.assertNotEqual(terrain_deck_dic[cards], -1, 'There are too many of one type of card in the terrain deck.')
    
    def test_return_terrain_deck_shuffle(self): 
        self.assertNotEqual(self.user.return_terrain_deck(), self.second_user.return_terrain_deck(), 'There is a small chance the decks have returned the same. Run the test again, if it fails again there is an error with shuffling.')
    
    def test_return_trick_deck_number(self):
        self.assertEqual(len(self.user.return_trick_deck()), 8, 'There are too many cards in the trick deck.')
        
    def test_return_trick_deck_repeats(self):
        trick_deck_dic = {'swap/pickup': 2, 'shift/rotate': 2, 'forwards/backwards': 2, 'add/remove': 2}
        for cards in self.user.return_trick_deck():
            trick_deck_dic[cards] -= 1
            self.assertNotEqual(trick_deck_dic[cards], -1, 'There are too many type of one card in the trick deck.')  
    
    def test_return_trick_deck_shuffle(self): 
        self.assertNotEqual(self.user.return_trick_deck(), self.second_user.return_trick_deck(), 'There is a chance the decks have returned equal. Run the test again and if it fails there is an error in shuffling.')  
        
    def test_terrain_draw(self):
        terrain_deck_template = ['forest', 'fields', 'mountains', 'desert', 'valley']
        self.assertIn(self.user.draw_terrain_card(), terrain_deck_template, 'The card drawn is not in the terrain deck.')
    
    def test_trick_draw(self):
        trick_deck_template = ['swap/pickup', 'shift/rotate', 'forwards/backwards', 'add/remove']
        self.assertIn(self.user.draw_trick_card(), trick_deck_template, 'The card drawn is not in the terrain deck.')
        
    def test_trick_draw_deck_removal(self):
        card = self.user.draw_trick_card()
        self.assertEqual(len(self.user.return_trick_deck()), 7, "After drawing a trickcard a card wasn't removed from the deck.")
        
    def test_trick_draw_deck_removal_specific(self):
        card = self.user.draw_trick_card()
        trick_deck_dic = {'swap/pickup': 2, 'shift/rotate': 2, 'forwards/backwards': 2, 'add/remove': 2}
        trick_deck_dic[card] -= 1
        for cards in self.user.return_trick_deck():
            trick_deck_dic[cards] -= 1
            self.assertNotEqual(trick_deck_dic[cards], -1, 'The specific drawn trick card was not removed from the deck.')
    
    def test_terrain_draw_deck_removal(self):
        card = self.user.draw_terrain_card()
        self.assertEqual(len(self.user.return_terrain_deck()), 39, 'A card was not removed from the terrain deck after a card was drawn.')
    
    def test_terrain_draw_deck_removal_specific(self):
        card = self.user.draw_terrain_card()
        terrain_deck_dic = {'forest': 8, 'fields': 8, 'desert': 8, 'mountains': 8, 'valley': 8}
        terrain_deck_dic[card] -= 1
        for cards in self.user.return_terrain_deck():
            terrain_deck_dic[cards] -= 1
            self.assertNotEqual(terrain_deck_dic[cards], -1, 'The specific drawn terrain card was not removed from the deck.')

class ComputerPlayFunctions(unittest.TestCase):
    def setUp(self):
        self.op_computer = flight_battle.Players(False, 'R')
        self.computer = flight_battle.Players(False, 'L')
        self.game_field_template = flight_battle.game_field_template_gen()
        self.game_field = flight_battle.game_field_transformer(self.game_field_template)
        self.computer.new_game_create_hand()
        self.computer_hand = self.computer.return_hand()
    
    def test_computer_hand_size(self):
        self.assertEqual(len(self.computer_hand), 7, 'Computer hand generated is of the incorrect size.')
    
    def test_computer_draws_and_discards_cards(self):
        orginal_hand_size = len(self.computer_hand)
        self.computer.end_turn_draw_new_cards()
        self.computer_hand = self.computer.return_hand()
        self.assertGreater(len(self.computer_hand), orginal_hand_size, 'The computers hand has not increased in size.')
        self.computer.discard_cards(self.computer_hand)
        self.computer_hand = self.computer.return_hand()
        self.assertEqual(len(self.computer_hand), 7, 'The computer has not discarded cards enough cards.')
        
    def test_computer_make_all_available_terrain_moves_and_use_cards(self):
        self.computer.set_test()
        hand_num = len(self.computer.return_hand())
        cards_used = self.computer.make_move(self.game_field, self.op_computer.return_location())
        next_coordinate_num = self.computer.return_location()['coordinate'] + 1
        self.assertNotIn(self.game_field[self.computer.return_location()['side']][next_coordinate_num]['card'], self.computer_hand, 'The computer has not played all of its availble terrain cards.')
        self.assertEqual(len(self.computer.return_hand()), hand_num - cards_used, 'The computer has not discarded all played cards.')

class test_ai_game_field_sorter(unittest.TestCase):
    def setUp(self):
        self.trial_game_field_one = {'L': {
      1: {'card': 'forest', 'on_map': True}, 2: {'card': 'fields', 'on_map': True}, 
       3: {'card': 'valley', 'on_map': True}, 4: {'card': 'fields', 'on_map': True}, 
       5: {'card': 'desert', 'on_map': True}, 6: {'card': 'forest', 'on_map': True}, 
       7: {'card': 'desert', 'on_map': True}, 8: {'card': 'forest', 'on_map': True},
       9: {'card': 'valley', 'on_map': True}, 10: {'card': 'fields', 'on_map': True}, 
       11: {'card': 'valley', 'on_map': True}, 12: {'card': 'forest', 'on_map': True}, 
       13: {'card': 'mountains', 'on_map': True}, 14: {'card': 'fields', 'on_map': True}, 
       15: {'card': 'mountains', 'on_map': True}, 16: {'card': 'desert', 'on_map': True}}, 
 'R': {1: {'card': 'desert', 'on_map': True}, 2: {'card': 'mountains', 'on_map': True}, 
       3: {'card': 'desert', 'on_map': True}, 4: {'card': 'forest', 'on_map': True}, 
       5: {'card': 'valley', 'on_map': True}, 6: {'card': 'forest', 'on_map': True}, 
       7: {'card': 'valley', 'on_map': True}, 8: {'card': 'forest', 'on_map': True}, 
       9: {'card': 'valley', 'on_map': True}, 10: {'card': 'mountains', 'on_map': True},
       11: {'card': 'desert', 'on_map': True}, 12: {'card': 'mountains', 'on_map': True},
       13: {'card': 'forest', 'on_map': True}, 14: {'card': 'fields', 'on_map': True}, 
       15: {'card': 'mountains', 'on_map': True}, 16: {'card': 'forest', 'on_map': True}}}
        self.trial_game_field_two = {'L': {
      1: {'card': 'forest', 'on_map': True}, 2: {'card': 'fields', 'on_map': True}, 
       3: {'card': 'valley', 'on_map': False}, 4: {'card': 'fields', 'on_map': False}, 
       5: {'card': 'desert', 'on_map': True}, 6: {'card': 'forest', 'on_map': True}, 
       7: {'card': 'desert', 'on_map': True}, 8: {'card': 'forest', 'on_map': True},
       9: {'card': 'valley', 'on_map': True}, 10: {'card': 'fields', 'on_map': True}, 
       11: {'card': 'valley', 'on_map': True}, 12: {'card': 'forest', 'on_map': True}, 
       13: {'card': 'mountains', 'on_map': True}, 14: {'card': 'fields', 'on_map': True}, 
       15: {'card': 'mountains', 'on_map': True}, 16: {'card': 'desert', 'on_map': True}}, 
       17: {'card': 'valley', 'on_map': True}, 18: {'card': 'fields', 'on_map': True},
 'R': {1: {'card': 'desert', 'on_map': True}, 2: {'card': 'mountains', 'on_map': True}, 
       3: {'card': 'desert', 'on_map': True}, 4: {'card': 'forest', 'on_map': True}, 
       5: {'card': 'valley', 'on_map': True}, 6: {'card': 'forest', 'on_map': True}, 
       7: {'card': 'valley', 'on_map': True}, 8: {'card': 'forest', 'on_map': True}, 
       9: {'card': 'valley', 'on_map': True}, 10: {'card': 'mountains', 'on_map': True},
       11: {'card': 'desert', 'on_map': True}, 12: {'card': 'mountains', 'on_map': True},
       13: {'card': 'forest', 'on_map': True}, 14: {'card': 'fields', 'on_map': True}, 
       15: {'card': 'mountains', 'on_map': True}, 16: {'card': 'forest', 'on_map': True}}}
    
    def test_game_field_sorter(self):
        game_field_one_sorted = [{'L': {'card': 'forest', 'coordinate': 1} , 'R': {'card': 'desert', 'coordinate': 1}},
                     {'L': {'card': 'fields', 'coordinate': 2} , 'R': {'card': 'mountains', 'coordinate': 2}},
                     {'L': {'card': 'valley', 'coordinate': 3} , 'R': {'card': 'desert', 'coordinate': 3}},
                     {'L': {'card': 'fields', 'coordinate': 4} , 'R': {'card': 'forest', 'coordinate': 4}},
                     {'L': {'card': 'desert', 'coordinate': 5} , 'R': {'card': 'valley', 'coordinate': 5}},
                     {'L': {'card': 'forest', 'coordinate': 6} , 'R': {'card': 'forest', 'coordinate': 6}},
                     {'L': {'card': 'desert', 'coordinate': 7} , 'R': {'card': 'valley', 'coordinate': 7}},
                     {'L': {'card': 'forest', 'coordinate': 8} , 'R': {'card': 'forest', 'coordinate': 8}},
                     {'L': {'card': 'valley', 'coordinate': 9} , 'R': {'card': 'valley', 'coordinate': 9}},
                     {'L': {'card': 'fields', 'coordinate': 10} , 'R': {'card': 'mountains', 'coordinate': 10}},
                     {'L': {'card': 'valley', 'coordinate': 11} , 'R': {'card': 'desert', 'coordinate': 11}},
                     {'L': {'card': 'forest', 'coordinate': 12} , 'R': {'card': 'mountains', 'coordinate': 12}},
                     {'L': {'card': 'mountains', 'coordinate': 13} , 'R': {'card': 'forest', 'coordinate': 13}},
                     {'L': {'card': 'fields', 'coordinate': 14} , 'R': {'card': 'fields', 'coordinate': 14}},
                     {'L': {'card': 'mountains', 'coordinate': 15} , 'R': {'card': 'mountains', 'coordinate': 15}},
                     {'L': {'card': 'desert', 'coordinate': 16} , 'R': {'card': 'forest', 'coordinate': 16}}]
        new = flight_battle.computer_play_field_sorter(self.trial_game_field_one)
        self.assertEqual(new, game_field_one_sorted, 'The game field does not match the template.')
        
    def test_game_field_sorter_with_added_cards(self):
        game_field_two_sorter = [{'L': {'card': 'forest', 'coordinate': 1} , 'R': {'card': 'desert', 'coordinate': 1}},
                     {'L': {'card': 'fields', 'coordinate': 2} , 'R': {'card': 'mountains', 'coordinate': 2}},
                     {'L': [{'card': 'forest', 'coordinate': 3}, {'card': 'forest', 'coordinate': 4}]},
                     {'L': {'card': 'valley', 'coordinate': 5} , 'R': {'card': 'desert', 'coordinate': 3}},
                     {'L': {'card': 'fields', 'coordinate': 6} , 'R': {'card': 'forest', 'coordinate': 4}},
                     {'L': {'card': 'desert', 'coordinate': 7} , 'R': {'card': 'valley', 'coordinate': 5}},
                     {'L': {'card': 'forest', 'coordinate': 8} , 'R': {'card': 'forest', 'coordinate': 6}},
                     {'L': {'card': 'desert', 'coordinate': 9} , 'R': {'card': 'valley', 'coordinate': 7}},
                     {'L': {'card': 'forest', 'coordinate': 10} , 'R': {'card': 'forest', 'coordinate': 8}},
                     {'L': {'card': 'valley', 'coordinate': 11} , 'R': {'card': 'valley', 'coordinate': 9}},
                     {'L': {'card': 'fields', 'coordinate': 12} , 'R': {'card': 'mountains', 'coordinate': 10}},
                     {'L': {'card': 'valley', 'coordinate': 13} , 'R': {'card': 'desert', 'coordinate': 11}},
                     {'L': {'card': 'forest', 'coordinate': 14} , 'R': {'card': 'mountains', 'coordinate': 12}},
                     {'L': {'card': 'mountains', 'coordinate': 15} , 'R': {'card': 'forest', 'coordinate': 13}},
                     {'L': {'card': 'fields', 'coordinate': 16} , 'R': {'card': 'fields', 'coordinate': 14}},
                     {'L': {'card': 'mountains', 'coordinate': 17} , 'R': {'card': 'mountains', 'coordinate': 15}},
                     {'L': {'card': 'desert', 'coordinate': 18} , 'R': {'card': 'forest', 'coordinate': 16}}]
        new = flight_battle.computer_play_field_sorter(self.trial_game_field_two)
        self.assertEqual(new, game_field_two_sorter, 'The game field with added cards does not match the template.')

if __name__ == '__main__':
    unittest.main()