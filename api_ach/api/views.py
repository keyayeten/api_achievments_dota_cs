# import datetime
from django.http import JsonResponse
from trackers import dota_st, cs_st
from django.http import Http404
# from django.shortcuts import get_object_or_404
# from django.views.decorators.http import require_GET
# from django.views.decorators.csrf import csrf_exempt
# from .models import User


TASKS = {
    'dota821248': (dota_st.get_twitch, None),
    'dota512001': (dota_st.play_w_friends, 1),
    'dota258052': (dota_st.deny_god, 20),
    'dota522247': (dota_st.aganim_purchase, None),
    'dota737288': (dota_st.first_blood_time, None),



    'cs768009': (cs_st.steam_connected, None),
    'cs643082': (cs_st.knife_kill_task, 1),
    'cs516108': (cs_st.beretas_stats, 3),
    'cs725004': (cs_st.inferno_win_stats, None),
    'cs256012': (cs_st.headshots_stats, 20),
}


def update_tasks(request):
    par_task_id = request.GET.get("par_task_id")
    id = int(request.GET.get('id'))
    try:
        method, target_progress = TASKS[par_task_id]
    except KeyError:
        raise Http404("Такого задания нет")

    first_val = int(request.GET.get('first_value'))
    if first_val:
        current_progress, is_completed = method(id,
                                                first_val=first_val)
    else:
        current_progress, is_completed = method(id)

    return JsonResponse({'new_value': current_progress,
                         'is_completed': is_completed,
                         'target_progress': target_progress})


# @csrf_exempt
# def manage_user(request):
#     if request.method == 'POST':
#         data = request.POST.get('data')
#     if not data:
#         return JsonResponse({'message': 'Invalid request'}, status=400)
#     try:
#         users = []
#         for item in data:
#             task_id = item.get('task_id')
#             user_id = item.get('user_id')
#             cs_id = item.get('cs_id')
#             dota_id = item.get('dota_id')
#             winline_id = user_id
#             current_task = task_id

#             user, created = User.objects.get_or_create(winline_id=winline_id)
#             user.current_task = current_task
#             user.steam_id = cs_id
#             user.dota_id = dota_id
#             user.save()
#             users.append(user)

#         return JsonResponse({'message': 'updated successfully'},
#                             status=201)
#     except Exception as e:
#         return JsonResponse({'message': str(e)}, status=500)

#     return JsonResponse({'message': 'Invalid request method'},
#                         status=405)


# @require_GET
# def get_user_tasks(request):

#     users = User.objects.all()

#     user_tasks = []

#     for user in users:

#         task_id = user.current_task

#         if task_id:
#             value = TASKS[task_id](user.dota_id)
#             is_completed = value is bool

#             task = {
#                 'task_id': task_id,
#                 'value': value,
#                 'is_completed': is_completed,
#                 'last_update': datetime.datetime.now(),
#             }

#             user_tasks.append(task)

#     return JsonResponse(user_tasks, safe=False)
