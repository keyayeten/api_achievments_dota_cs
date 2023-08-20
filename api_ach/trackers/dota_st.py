import requests

FIVE_LAST = 1
_ITEM_RADIANCE_ID = 250
_ITEM_AGANIM_ID = 141
_UNIVERSAL_MIN_ID = 91
_UNIVERSAL_MAX_ID = 123


def get_player_stats(player_id: int) -> list:
    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    result = []
    for match in matches_list:
        match_id = match['match_id']
        match_url = f'https://www.opendota.com/api/matches/{match_id}'
        for player in requests.get(match_url).json()["players"]:
            if player["account_id"] == player_id:
                result.append(player)
    return result


def get_matches_list(player_id: int) -> list:
    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    return matches_list


def _get_object_or_null(_dict: dict, quest: str) -> int:
    result = _dict.get(quest, 0)
    if result:
        return result
    return 0


def _safe_get(_obj: dict, quest: str):
    if _obj is None:
        return 0
    return _obj.get(quest, 0)


def play_w_friends(player_id: int, initial_value=1, **kwargs) -> int:
    """Get maximum of party size from 5 last matches."""
    value = max([match["party_size"] for match in get_matches_list(player_id)])
    return value, value > initial_value if value else False


def first_blood_time(player_id: int, initial_value=0, **kwargs) -> int:
    """Get best first blood time from 5 last matches."""

    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    fb_timings = []
    for match in matches_list:
        match_id = match['match_id']
        match_url = f'https://www.opendota.com/api/matches/{match_id}'
        timing = requests.get(match_url).json()['first_blood_time']
        fb_timings.append(timing)
    res = min(fb_timings)
    return res, res == 0 and first_blood_taken(player_id=player_id)


def stacked_creeps(player_id: int, **kwargs) -> int:
    """Get best result of stacked creeps."""
    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    stacks_creeps = []
    for match in matches_list:
        match_id = match['match_id']
        match_url = f'https://www.opendota.com/api/matches/{match_id}'
        stacked = requests.get(match_url).json().get('creeps_stacked', 0)
        stacks_creeps.append(stacked)

    return max(stacks_creeps)


def count_runes_wise(player_id: int, **kwargs) -> int:
    """Get best result of taken runes of wise."""
    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    runes_taken = []
    for match in matches_list:
        match_id = match['match_id']
        match_url = f'https://www.opendota.com/api/matches/{match_id}'
        taken = requests.get(match_url).json().get('runes', None)
        if taken:
            runes_taken.append(taken.get("8", 0))
        else:
            runes_taken.append(0)
    return max(runes_taken)


def deny_god(player_id: int, **kwargs) -> int:
    """Бог денаев"""
    matches_list = get_player_stats(player_id)
    denies = [match["denies"] for match in matches_list]
    res = max(denies)
    return res, res >= 20


def aganim_purchase(player_id: int, **kwargs) -> int:
    """Покупка аганима"""
    return None, any([_is_agaganim_in([stat["item_0"],
                                       stat["item_1"],
                                       stat["item_2"],
                                       stat["item_3"],
                                       stat["item_4"],
                                       stat["item_5"]])
                     for stat in get_player_stats(player_id)])


def first_blood_taken(player_id: int, **kwargs):
    return min([match["firstblood_claimed"]
                for match in get_player_stats(player_id)]) is not None


def get_twitch(player_id: int):
    pass


def _is_radiance_in(item_list: list):
    return _ITEM_RADIANCE_ID in item_list


def _is_agaganim_in(item_list: list):
    return _ITEM_AGANIM_ID in item_list


def wraith_radiance(player_id: int, **kwargs):
    return None, any([_is_radiance_in([stat["item_0"],
                                       stat["item_1"],
                                       stat["item_2"],
                                       stat["item_3"],
                                       stat["item_4"],
                                       stat["item_5"]])
                     for stat in get_player_stats(player_id)])


def three_universal(player_id: int, initial_value=3, first_value=0):
    heroes = [hero["hero_id"]
              for hero in get_player_stats(player_id)[:FIVE_LAST]]

    if _universal_count(heroes):
        return first_value + 1, first_value + 1 >= initial_value
    return first_value, False


def _universal_count(ids: int):
    return len(list(filter(
        lambda hero:  _UNIVERSAL_MAX_ID >= hero >= _UNIVERSAL_MIN_ID,
        ids)))


def ten_stacks(player_id: int, initial_value=10, **kwargs):
    res = max([stack["creeps_stacked"]
               for stack in get_player_stats(player_id)])
    if res:
        return res, res >= initial_value
    return None, False


def _is_winner(stats):
    return stats['win'] == 1


def deep_late(player_id: int, initial_value=60, **kwargs):
    result = max(stat["duration"] // 60
                 for stat in get_player_stats(player_id) if _is_winner(stat))
    return result, result >= initial_value


def courier_kills(player_id: int, initial_value=3, **kwargs):
    result = max(stat["courier_kills"]
                 for stat in get_player_stats(player_id) if _is_winner(stat))
    if result:
        return result, result >= initial_value
    return result, False


def dota_acc(player_id):
    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    return requests.get(url) is not None


if __name__ == "__main__":
    # print(aganim_purchase(279786838))

    # url = 'https://www.opendota.com/api/players/279786838/matches/'
    # matches_list = requests.get(url).json()[:FIVE_LAST]
    # fb_timings = []
    # for match in matches_list:
    #     match_id = match['match_id']
    #     match_url = f'https://www.opendota.com/api/matches/{match_id}'
    #     timing = requests.get(match_url).json()['first_blood_time']
    #     fb_timings.append(timing)
    # print(min(fb_timings))
    # print(first_blood_time(279786838))
    # print(wraith_radiance(279786838))
    # print(three_universal(279786838))
    # print(ten_stacks(279786838))
    # print(deep_late(279786838))
    print(dota_acc(279786838))
