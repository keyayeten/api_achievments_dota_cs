import requests


_URL_STATS = 'http://api.steampowered.com\
/ISteamUserStats/GetUserStatsForGame/v0002\
/?appid=730&key=8128F0A3C7915CF2962611FE8A92207A&steamid='
_KNIFE_INDEX = 9
_BERETAS_INDEX = 13
_INF_WIN_STAT = 32
_HEAD_KILL_STAT = 25
_TARGET_HEAD = 20


def knife_kill_task(cs_id, initial_value=None, **kwargs):
    knife_kill_stats = requests.get(
        _URL_STATS+str(cs_id)).json()["playerstats"][
            "stats"][_KNIFE_INDEX]['value']
    if initial_value:
        return knife_kill_stats > initial_value
    return knife_kill_stats


def beretas_stats(cs_id, initial_value=None, **kwargs):
    beret_kill_stats = requests.get(
        _URL_STATS+str(cs_id)).json()["playerstats"][
            "stats"][_BERETAS_INDEX]['value']
    if initial_value:
        return beret_kill_stats > initial_value
    return beret_kill_stats


def inferno_win_stats(cs_id, initial_value=None, **kwargs):
    inf_wins = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_INF_WIN_STAT]['value']
    if initial_value:
        return inf_wins > initial_value
    return inf_wins


def headshots_stats(cs_id, initial_value=None, first_val=0):
    headshots = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_HEAD_KILL_STAT]['value']

    return headshots, headshots >= first_val + _TARGET_HEAD


def steam_connected(cs_id, initial_value=None, **kwargs):
    pass
