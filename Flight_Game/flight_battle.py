import random


def game_field_gen():
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

if __name__ == '__main__':
    print(game_field_gen())