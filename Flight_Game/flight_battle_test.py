import unittest
import flight_battle


class TestFlights(unittest.TestCase):
    
    def setUp(self):
        self.game_field = flight_battle.game_field_gen()
    
    def test_game_field_size(self):
        self.assertEqual(len(self.game_field), 16, 'The playfield is of the wrong size.')
    
    def test_game_field_cards(self):
        terrain_cards = ["['forest', 'forest']", "['forest', 'desert']", "['forest', 'mountains']", "['forest', 'fields']", "['forest', 'valley']", "['desert', 'forest']", "['desert', 'desert']", "['desert', 'mountains']", "['desert', 'fields']", "['desert', 'valley']", "['mountains', 'forest']", "['mountains', 'desert']", "['mountains', 'mountains']", "['mountains', 'fields']", "['mountains', 'valley']", "['fields', 'forest']", "['fields', 'desert']", "['fields', 'mountains']", "['fields', 'fields']", "['fields', 'valley']", "['valley', 'forest']", "['valley', 'desert']", "['valley', 'mountains']", "['valley', 'fields']", "['valley', 'valley']"]
        for cards in self.game_field:
            self.assertIn(str(self.game_field[cards]), terrain_cards, 'There are cards in the play field not in the deck.')
            
    def test_game_field_cards_duplicates(self):
        terrain_cards_dic = {"['forest', 'forest']": 2, "['forest', 'desert']": 2, "['forest', 'mountains']": 2, "['forest', 'fields']": 2, "['forest', 'valley']": 2, "['desert', 'forest']": 2, "['desert', 'desert']": 2, "['desert', 'mountains']": 2, "['desert', 'fields']": 2, "['desert', 'valley']": 2, "['mountains', 'forest']": 2, "['mountains', 'desert']": 2, "['mountains', 'mountains']": 2, "['mountains', 'fields']": 2, "['mountains', 'valley']": 2, "['fields', 'forest']": 2, "['fields', 'desert']": 2, "['fields', 'mountains']": 2, "['fields', 'fields']": 2, "['fields', 'valley']": 2, "['valley', 'forest']": 2, "['valley', 'desert']": 2, "['valley', 'mountains']": 2, "['valley', 'fields']": 2, "['valley', 'valley']": 2}
        for cards in self.game_field:
            terrain_cards_dic[str(self.game_field[cards])] -= 1
            self.assertNotEqual(terrain_cards_dic[str(self.game_field[cards])], -1, 'There are more then the allocated number of cards in the play field.')
    
    def test_game_field_cards_repeats(self):
        for cards in self.game_field:
            if cards == 1:
                pass
            else:
                num = 0
                while num < 2:
                    self.assertNotEqual(self.game_field[cards][num], self.game_field[cards-1][num],'Two of the same terrain types are next to each other.')
                    num += 1
        
        
if __name__ == '__main__':
    unittest.main()