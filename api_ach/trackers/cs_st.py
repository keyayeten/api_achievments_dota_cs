import requests


_URL_STATS = 'http://api.steampowered.com\
/ISteamUserStats/GetUserStatsForGame/v0002\
/?appid=730&key=8128F0A3C7915CF2962611FE8A92207A&steamid='
_KNIFE_INDEX = 9
_BERETAS_INDEX = 13
_INF_WIN_STAT = 32
_HEAD_KILL_STAT = 25
_TARGET_HEAD = 20
_BOMBS_DEF_INDX = 4
_BOMBS_PLN_INDX = 3
_HEG_KILLS_INDX = 10
_MOLLY_KILLS_INDX = 171


def knife_kill_task(cs_id, initial_value=None,
                    first_val=float('inf'),
                    **kwargs):
    knife_kill_stats = requests.get(
        _URL_STATS+str(cs_id)).json()["playerstats"][
            "stats"][_KNIFE_INDEX]['value']
    try:
        return knife_kill_stats, knife_kill_stats > first_val
    except TypeError:
        return knife_kill_stats, False


def beretas_stats(cs_id, initial_value=None, first_val=float('inf'), **kwargs):
    beret_kill_stats = requests.get(
        _URL_STATS+str(cs_id)).json()["playerstats"][
            "stats"][_BERETAS_INDEX]['value']
    try:
        return beret_kill_stats, beret_kill_stats > first_val
    except TypeError:
        return beret_kill_stats, False


def inferno_win_stats(cs_id, initial_value=None,
                      first_val=float('inf'),
                      **kwargs):
    inf_wins = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_INF_WIN_STAT]['value']
    try:
        return inf_wins, inf_wins > first_val
    except TypeError:
        return inf_wins, False


def headshots_stats(cs_id, initial_value=None, first_val=float('inf')):
    headshots = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_HEAD_KILL_STAT]['value']
    try:
        return headshots, headshots >= first_val + _TARGET_HEAD
    except TypeError:
        return headshots, False


def steam_connected(cs_id, initial_value=None, **kwargs):
    return 1, True


def defusing_bombs(cs_id, initial_value=10, first_val=float('inf')):
    defused = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_BOMBS_DEF_INDX]['value']
    try:
        return defused, defused >= first_val + initial_value
    except TypeError:
        return defused, False


def planting_bombs(cs_id, initial_value=10, first_val=float('inf')):
    planted = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_BOMBS_PLN_INDX]['value']
    try:
        return planted, planted >= first_val + initial_value
    except TypeError:
        return planted, False


def heg_kills(cs_id, initial_value=10, first_val=float('inf')):
    kills = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_HEG_KILLS_INDX]['value']
    try:
        return kills, kills >= first_val + initial_value
    except TypeError:
        return kills, False


def molly_kills(cs_id, initial_value=3, first_val=float('inf')):
    kills = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_MOLLY_KILLS_INDX]['value']
    try:
        return kills, kills >= first_val + initial_value
    except TypeError:
        return kills, False


def cache_plays(cs_id, initial_value=3, first_val=float('inf')):
    wins = requests.get(
        _URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_MOLLY_KILLS_INDX]['value']
    try:
        return wins, wins >= first_val + initial_value
    except TypeError:
        return wins, False


def cs_acc(cs_id):
    try:
        requests.get(_URL_STATS+str(cs_id)).json()[
            "playerstats"]["stats"][_MOLLY_KILLS_INDX]['value']
        return True
    except KeyError:
        return False
