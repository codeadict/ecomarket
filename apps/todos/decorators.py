from functools import partial, wraps

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required


def ignore_todos(view_func):
    """Do not allow TodoMiddleware to redirect for this view"""
    view_func.ignore_todos = True
    return view_func


def todo_depends(name):
    def inner(view_func, name):
        if not hasattr(view_func, "todo_depends"):
            view_func.todo_depends = []
        view_func.todo_depends.append(name)
        return view_func
    return partial(inner, name=name)


def todo_function(view_func_or_name):
    def inner(view_func, name):
        if hasattr(view_func, "as_view"):
            view_func = view_func.as_view()
        @wraps(view_func)
        def wrapper(request, **kwargs):
            if not request.user.todos.filter(view_name=name).count():
                return redirect("home")
            return view_func(request, **kwargs)
        return ignore_todos(login_required(wrapper))
    if isinstance(view_func_or_name, basestring):
        return partial(inner, name=view_func_or_name)
    return inner(view_func_or_name, view_func_or_name.__name__)
