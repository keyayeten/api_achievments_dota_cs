import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import User
from trackers import dota_st, cs_st

TASKS = {
    "0001": dota_st.get_twitch,
    "0002": dota_st.play_w_friends,
    "0003": dota_st.deny_god,
    "0004": dota_st.aganim_purchase,
    "0005": dota_st.first_blood_taken,



    "1000": cs_st.steam_connected,
    "2000": cs_st.knife_kill_task,
    "3000": cs_st.beretas_stats,
    "4000": cs_st.inferno_win_stats,
    "5000": cs_st.headshots_stats,
}


@csrf_exempt
def manage_user(request):
    if request.method == 'POST':
        data = request.POST.get('data')
    if not data:
        return JsonResponse({'message': 'Invalid request'}, status=400)
    try:
        users = []
        for item in data:
            task_id = item.get('task_id')
            user_id = item.get('user_id')
            cs_id = item.get('cs_id')
            dota_id = item.get('dota_id')
            winline_id = user_id
            current_task = task_id

            user, created = User.objects.get_or_create(winline_id=winline_id)
            user.current_task = current_task
            user.steam_id = cs_id
            user.dota_id = dota_id
            user.save()
            users.append(user)

        return JsonResponse({'message': 'Users created/updated successfully'},
                            status=201)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method'},
                        status=405)


@require_GET
def get_user_tasks(request):

    users = User.objects.all()

    user_tasks = []

    for user in users:

        task_id = user.current_task

        if task_id:
            value = TASKS[task_id](user.dota_id)
            is_completed = value is bool

            task = {
                'task_id': task_id,
                'value': value,
                'is_completed': is_completed,
                'last_update': datetime.datetime.now(),
            }

            user_tasks.append(task)

    return JsonResponse(user_tasks, safe=False)
