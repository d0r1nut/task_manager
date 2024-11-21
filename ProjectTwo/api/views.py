from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse

from api.helper import check_token

# Create your views here.

def signup(request):
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/users/signup'

        data = { 
            'email': request.POST['email'],
            'name': request.POST['name'],
            'password': request.POST['password'],
            'expiresInMins': 30,
        }

        response = requests.post(url, json=data)

        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/users/login'

        data = { 
            'email': request.POST['email'],
            'password': request.POST['password'],
            'expiresInMins': 30,
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            request.session['token'] = response.json().get('token')
        request.session['user'] = response.json().get('logged_user')
        login_data = response.json()
        return redirect('index')

    return render(request, 'login.html')

def logout(request):

    request.session.flush()

    return redirect('index')

def get_user_data(request):

    if not check_token(request):
        return redirect('login')
    
    url = 'http://127.0.0.1:5000/users/all'

    token = request.session.get('token')
    headers = {
        'x-access-token': token
    }
    response = requests.get(url, headers=headers)

    user_data = response.json()

    return JsonResponse(user_data)

def get_all_tasks_created_by(request):

    if not check_token(request):
        return redirect('login')
    
    url = "http://127.0.0.1:5000/tasks/createdby"
    request.session['where'] = 'createdby'
    response = requests.get(url, headers={'x-access-token': request.session.get('token')})

    user = request.session.get('user')
    tasks = response.json().get('tasks')

    return render(request, 'all_tasks.html', {'tasks': tasks, 'created_by': True, 'user': request.session.get('user')})

def get_all_tasks_assigned_to(request):

    
    if not check_token(request):
        return redirect('login')

    url = "http://127.0.0.1:5000/tasks/assignedto"
    request.session['where'] = 'assignedto'

    response = requests.get(url, headers={'x-access-token': request.session.get('token')})
    user = request.session.get('user')
    tasks = response.json().get('tasks')

    return render(request, 'all_tasks.html', {'tasks': tasks, 'created_by': False, 'user': request.session.get('user')})


def add_task(request):

    if not check_token(request):
        return redirect('login')

    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/tasks/add'
        data = {
            "description": request.POST['description'],
            "assignedToUid": request.POST['assignedToUid']
        }
        response = requests.post(url, json=data, headers={'x-access-token': request.session.get('token')})
        task_data = response.json()
        return redirect('get_all_tasks_created_by')
    get_users = requests.get('http://127.0.0.1:5000/users/all', headers={'x-access-token': request.session.get('token')})
    
    users = get_users.json()
    print(users)
    return render(request, 'task_form.html', {'users': users['users'], 'user': request.session.get('user')})

def edit_task(request, task_id):

    if not check_token(request):
        return redirect('login')
    
    if request.method == 'POST':
        url = f'http://127.0.0.1:5000/tasks/{task_id}'

        data = {
            'data': {
                'description': request.POST['description'],
                'done': request.POST['done']
            }
        }
        response = requests.patch(url, json=data, headers={'x-access-token': request.session.get('token')})
        update_data = response.json()
        if request.session.get('where') == 'createdby':
            next = 'get_all_tasks_created_by'
        elif request.session.get('where') == 'assignedto':
            next = 'get_all_tasks_assigned_to'
        return redirect(next)
    url = f'http://127.0.0.1:5000/tasks/{task_id}'
    response = requests.get(url, headers={'x-access-token': request.session.get('token')})
    task = response.json()
    return render(request, 'task_form.html', {'task_id': task_id, 'task': task, 'user': request.session.get('user')})

def delete_task(request, task_id):

    if not check_token(request):
        return redirect('login')
    
    if request.method == 'POST':
        url = f'http://127.0.0.1:5000/tasks/{task_id}'
        response = requests.delete(url, headers={'x-access-token': request.session.get('token')})
        if request.session.get('where') == 'createdby':
            next = 'get_all_tasks_created_by'
        elif request.session.get('where') == 'assignedto':
            next = 'get_all_tasks_assigned_to'
        return redirect(next)
    return render(request, 'delete_task.html', {'task_id': task_id, 'user': request.session.get('user')}) 

def index(request):
    if request.session.get('user') == None:
        user = { 'name': '' }
        request.session['user'] = user
    return render(request, 'index.html', {'user': request.session.get('user')})