import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import User
from trackers import dota_st

TASKS = {
    "0001": dota_st.get_twitch,
    "0002": dota_st.play_w_friends,
    "0003": dota_st.deny_god,
    "0004": dota_st.aganim_purchase,
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
            winline_id = user_id
            current_task = task_id

            user, created = User.objects.get_or_create(winline_id=winline_id)
            user.current_task = current_task
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
            is_completed = value.get('is_completed')

            task = {
                'task_id': task_id,
                'value': value,
                'is_completed': is_completed,
                'last_update': datetime.datetime.now(),
            }

            user_tasks.append(task)

    return JsonResponse(user_tasks, safe=False)
