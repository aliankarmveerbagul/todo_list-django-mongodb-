from bson import ObjectId
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import db_list, db_register, db_status, db
from datetime import datetime, timedelta
from functools import wraps
from django.http import HttpRequest


def get_cookie(cookie_name):

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if isinstance(request, HttpRequest):
                cookie_value = request.COOKIES.get(cookie_name)
                data = db.uid.find_one({'uid':ObjectId(cookie_value)})
                if data is None:
                    messages.error(request,"Please Login, found to be not registered ")
                    return redirect('todo_app:login')
                else:
                    return view_func(request, *args, **kwargs)

        return wrapper

    return decorator




def register(request):
    if request.method == "POST":
        storage = {'email': request.POST.get("email"), 'name': request.POST.get("name"),
                   'password': request.POST.get("password"), 'user_creation_time': datetime.now()}
        db_register.insert_one(storage)
        messages.success(request, "You Have Been Registered Successfully!")
        return redirect('todo_app:login')
    else:
        return render(request, 'todo_app/register.html')


def login(request):
    if request.method == "POST":
        cred = {'email': request.POST.get('email'), 'password': request.POST.get('password')}
        find_db = db_register.find_one({'email': cred['email']})
        if find_db is None:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('todo_app:login')
        elif find_db['password'] == cred['password']:
            messages.success(request, "You Have Been Logged In!")
            uid = find_db['_id']
            # Set cookie
            response = redirect('todo_app:home', uid=uid)
            response.set_cookie('uid', uid,
                                expires=datetime.now() + timedelta(days=30))  # Set cookie expiration as required
            db.uid.insert_one({'uid': uid, 'logintime': datetime.now()})

            return response
        else:
            messages.error(request, "Your given Credentials doesn't match")
            return redirect('todo_app:login')

    return render(request, 'todo_app/login.html')


@get_cookie('uid')
def home(request, uid):
    if uid:
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_id = uid
        user_name = user_cred['name']
        data_task = db_list.find({'user_id': ObjectId(user_id)})
        data_status = db_status.find(({'user_id': ObjectId(user_id)}))
        task_list = list(data_task)
        task_status = list(data_status)
        for i in task_list:
            i.update({"task_id": i['_id']})
            i.pop("_id")
        return render(request, 'todo_app/home.html',
                      {'task_list': task_list, 'task_status': task_status, 'uid': uid, 'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def add_task(request, uid):
    if uid:
        if request.method == "POST":
            storage = {'task_title': request.POST.get('task_title'), 'task_desc': request.POST.get('task_desc'),
                       'task_comm': request.POST.get('task_comm'), 'task_status': request.POST.get('task_status'),
                       'creation_task_time': datetime.now(), 'user_id': ObjectId(uid)}
            db_list.insert_one(storage)
            messages.success(request, "Your Data has been added Successfully")
            return redirect('todo_app:home', uid=uid)
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        opt_list = db_status.find({'user_id': ObjectId(uid)})
        uid = uid
        return render(request, 'todo_app/add_task.html', {'opt_list': opt_list, 'uid': uid, 'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def edit_task(request, id, uid):
    if uid:
        if request.method == "POST":
            storage = {'task_title': request.POST.get('task_title'), 'task_desc': request.POST.get('task_desc'),
                       'task_comm': request.POST.get('task_comm'), 'task_status': request.POST.get('task_status'),
                       'updated_task_time ': datetime.now()}
            db_list.update_one({"_id": ObjectId(id)}, {"$set": storage})
            messages.success(request, "Yor data hase been updated")
            return redirect('todo_app:home', uid=uid)
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        opt_list = db_status.find({'user_id': ObjectId(uid)})
        f_data = db_list.find_one({"_id": ObjectId(id)})
        user_name = user_cred['name']
        obj = id
        uid = uid
        return render(request, 'todo_app/edit_task.html',
                      {'data': f_data, 'opt_list': opt_list, 'obj': obj, 'uid': uid, 'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def delete(request, id, uid):
    if uid:
        uid = uid
        db_list.delete_one({"_id": ObjectId(id)})
        messages.success(request, "Your Task Has Been Deleted")
        return redirect('todo_app:home', uid=uid)
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def views_task(request, id, uid):
    if uid:
        data = db_list.find_one({"_id": ObjectId(id)})
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        uid = uid
        obj = id
        data.update({"task_id": str(data['_id'])})
        data.pop("_id")
        return render(request, 'todo_app/views_task.html', {'data': data, 'obj': obj, 'uid': uid, 'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def home_status(request, uid):
    if uid:
        data_status = db_status.find({'user_id': ObjectId(uid)})
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        data_s_list = list(data_status)
        for i in data_s_list:
            i.update({"task_id": i['_id']})
            i.pop("_id")
        return render(request, 'todo_app/view_stat_home.html',
                      {'data_s_list': data_s_list, 'uid': uid, 'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def add_status(request, uid):
    if uid:
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        if request.method == "POST":
            storage = {'t_status': request.POST.get('t_status'), 'user_id': ObjectId(uid),
                       'task_creation_time': datetime.now(), 'user_name': user_name}
            db_status.insert_one(storage)
            messages.success(request, "Your task has been added successfully")
            return redirect('todo_app:home', uid=uid)

        return render(request, 'todo_app/add_status.html', {'uid': uid, 'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def task_status_del(request, id, stat, uid):
    if uid:
        db_status.delete_one({"_id": ObjectId(id)})
        db_list.delete_many({"task_status": stat})
        messages.success(request, "Your Status  Has Been Deleted")
        uid = uid
        return redirect('todo_app:home_status', uid=uid)
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def task_status_edit(request, id, uid, stat):
    if uid:
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        if request.method == "POST":
            storage = {'t_status': request.POST.get('t_status'), 'user_id': user_cred['_id'],
                       'task_update_time': datetime.now()}
            db_status.update_one({"_id": ObjectId(id)}, {'$set': storage})
            db_list.update_many({'task_status': stat}, {'$set': {"task_status": storage['t_status']}})
            messages.success(request, "Yor data hase been updated")
            return redirect('todo_app:home', uid=uid)
        data = db_status.find_one({"_id": ObjectId(id)})
        stat = data['t_status']
        kid = data['_id']
        return render(request, 'todo_app/task_status_edit.html',
                      {'data': data, 'uid': user_cred['_id'], 'uname': user_name, 'kid': kid, 'stat': stat})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def filter_hours(request, flt, uid):
    if uid:
        if flt == "LastH":
            time = datetime.now()
            delta = timedelta(hours=1)
            t_time = time - delta
            stime = "1 Hour"
        elif flt == "Last2H":
            time = datetime.now()
            delta = timedelta(hours=2)
            t_time = time - delta
            stime = "2 Hour"
        elif flt == "Last3H":
            time = datetime.now()
            delta = timedelta(hours=3)
            t_time = time - delta
            stime = "3 Hour"
        elif flt == "Last12H":
            time = datetime.now()
            delta = timedelta(hours=12)
            t_time = time - delta
            stime = "12 Hour"
        elif flt == "Last24H":
            time = datetime.now()
            delta = timedelta(hours=24)
            t_time = time - delta
            stime = "24 Hour"
        data_task = db_list.find({"creation_task_time": {"$gte": t_time, "$lte": time}})
        data_status = db_status.find(({'user_id': ObjectId(uid)}))
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        task_list = list(data_task)
        task_status = list(data_status)
        for i in task_list:
            i.update({"task_id": i['_id']})
            i.pop("_id")
        return render(request, 'todo_app/filter_home.html',
                      {'task_list': task_list, 'task_status': task_status, 'time': stime, 'uid': uid,
                       'uname': user_name})
    else:
        return redirect('todo_app:login')

@get_cookie('uid')
def filter_task(request, flt, uid):
    if uid:
        data_task = db_list.find({'task_status': flt})
        data_status = db_status.find(({'user_id': ObjectId(uid)}))
        user_cred = db_register.find_one({'_id': ObjectId(uid)})
        user_name = user_cred['name']
        task_list = list(data_task)
        task_status = list(data_status)
        task_name = flt
        for i in task_list:
            i.update({"task_id": i['_id']})
            i.pop("_id")
        return render(request, 'todo_app/filter_task.html',
                      {'task_list': task_list, 'task_status': task_status, 'uid': uid, 'uname': user_name,
                       'task_name': task_name})
    else:
        return redirect('todo_app:login')





