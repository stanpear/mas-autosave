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
            properties dict(properties)
            transclude
