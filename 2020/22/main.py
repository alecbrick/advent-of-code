from utils.input import read_batches


def parse_player(lines):
    return [int(n) for n in lines[1:]]


def play_war(player_1, player_2):
    while len(player_1) > 0 and len(player_2) > 0:
        card_1 = player_1.pop(0)
        card_2 = player_2.pop(0)
        if card_1 > card_2:
            player_1 += [card_1, card_2]
        elif card_2 > card_1:
            player_2 += [card_2, card_1]
        else:
            raise ValueError("wat")
    if player_1:
        return player_1
    else:
        return player_2


def play_recursive_war(player_1, player_2, game_history, game=1):
    original_hashable_state = (tuple(player_1), tuple(player_2))
    if original_hashable_state in game_history:
        if game_history[original_hashable_state] == 1:
            return player_1, []
        else:
            return [], player_2
    rounds = set()
    while len(player_1) > 0 and len(player_2) > 0:
        hashable_state = (tuple(player_1), tuple(player_2))
        if hashable_state in rounds:
            game_history[original_hashable_state] = 1
            return player_1, []
        rounds.add(hashable_state)
        card_1 = player_1.pop(0)
        card_2 = player_2.pop(0)
        if len(player_1) >= card_1 and len(player_2) >= card_2:
            recursive_deck_1 = player_1[:card_1]
            recursive_deck_2 = player_2[:card_2]
            end_player_1, end_player_2 = play_recursive_war(recursive_deck_1, recursive_deck_2, game_history, game + 1)
            if end_player_1:
                player_1 += [card_1, card_2]
            else:
                player_2 += [card_2, card_1]
        else:
            if card_1 > card_2:
                player_1 += [card_1, card_2]
            elif card_2 > card_1:
                player_2 += [card_2, card_1]
            else:
                raise ValueError("aaa")
    if player_1:
        game_history[original_hashable_state] = 1
    else:
        game_history[original_hashable_state] = 2
    return player_1, player_2


def main():
    batches = read_batches("input.txt")
    player_1, player_2 = parse_player(batches[0]), parse_player(batches[1])
    end_player_1, end_player_2 = play_recursive_war(player_1, player_2, {})
    if end_player_1:
        winning_deck = end_player_1
    else:
        winning_deck = end_player_2

    total = 0
    for i, val in enumerate(reversed(winning_deck)):
        total += (i + 1) * val
    print(total)


if __name__ == "__main__":
    main()
