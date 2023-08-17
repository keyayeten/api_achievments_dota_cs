import requests

FIVE_LAST = 2


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


def play_w_friends(player_id: int) -> int:
    """Get maximum of party size from 5 last matches."""

    return max([match["party_size"] for match in get_matches_list(player_id)])


def first_blood_time(player_id: int) -> int:
    """Get best first blood time from 5 last matches."""

    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    fb_timings = []
    for match in matches_list:
        match_id = match['match_id']
        match_url = f'https://www.opendota.com/api/matches/{match_id}'
        timing = requests.get(match_url).json()['first_blood_time']
        fb_timings.append(timing)

    return min(fb_timings)


def stacked_creeps(player_id: int) -> int:
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


def courier_kills(player_id: int) -> int:
    """Get best result of killed couriers."""
    url = f'https://www.opendota.com/api/players/{player_id}/matches/'
    matches_list = requests.get(url).json()[:FIVE_LAST]
    cour_kills = []
    for match in matches_list:
        match_id = match['match_id']
        match_url = f'https://www.opendota.com/api/matches/{match_id}'
        kills = requests.get(match_url).json().get('courier_kills', 0)
        cour_kills.append(kills)
    return max(cour_kills)


def count_runes_wise(player_id: int) -> int:
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


def deny_god(player_id: int) -> int:
    """Бог денаев"""
    matches_list = get_player_stats(player_id)
    denies = [match["denies"] for match in matches_list]
    return max(denies)


def aganim_purchase(player_id: int) -> int:
    """Покупка аганима"""
    return min([_safe_get(match["purchase_log"],
                          "Aganim_scepter")
                for match in get_player_stats(player_id)])


def first_blood_taken(player_id: int):
    return min([match["firstblood_claimed"]
                for match in get_player_stats(player_id)]) is not None


def get_twitch(player_id: int):
    pass


if __name__ == "__main__":
    print(aganim_purchase(279786838))
