from dynamicwidget import handlers


def widget_handler(rx):
    "Register widget generating function"
    def decorator(view):
        handlers.default.register(rx, view)
        return view

    return decorator
