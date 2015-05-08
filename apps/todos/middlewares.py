from django.shortcuts import redirect

from todos.models import Todo


class TodoMiddleware(object):

    def process_view(self, request, view_func, *args):
        if request.session.get("impersonated_by", None) is not None:
            return
        if not request.user.is_authenticated():
            return
        todos = request.user.todos.all()
        todo = None
        depends = getattr(view_func, "todo_depends", None)
        if depends:
            for dependency in depends:
                try:
                    todo = todos.get(view_name=dependency)
                except Todo.DoesNotExist:
                    continue
                break
        if todo is None:
            # Only check ignore_todos when no dependencies
            if getattr(view_func, "ignore_todos", False):
                return
            if todos.count():
                todo = todos[0]
        if todo:
            return redirect("todos:" + todo.view_name)
