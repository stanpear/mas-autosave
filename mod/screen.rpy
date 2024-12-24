screen fom_autosave_screens__await(promise, pending_ui, complete_ui, error_ui):
    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)

    $ result = None
    $ error = None

    python:
        try:
            if promise.is_complete():
                result = promise.get()
        except Exception as e:
            error = e

    if not promise.is_complete():
        $ renpy.display.screen.use_screen(pending_ui)
    elif error is not None:
        $ renpy.display.screen.use_screen(error_ui, error)
    else:
        $ renpy.display.screen.use_screen(complete_ui, result)

screen fom_autosave_screens__confirm(**properties):
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")
    modal True
    zorder 200

    key "mas_game_menu" action NullAction()

    frame:
        vbox:
            align (0.5, 0.5)
            xfill True
            properties properties
            transclude
