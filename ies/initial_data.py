from .models import StatusControl


class InitStatus:
    def __init__(self):
        init_status = [
            # is_public, open_editor, is_deleted
            ("draft", "register", "Borrador",
                "blue", "edit_note", False, True, False, 8),
            ("created", "register", "Creado (para revisarse)",
                "green", "pending_actions", False, True, False, 6),
            ("need_changes", "register", "Requiere cambios",
                "orange", "new_releases", False, False, False, 2),
            ("need_new_checking", "register", "Requiere nueva revisión",
                "pink", "report_gmailerrorred", False, True, False, 4),
            ("approved", "register", "Aprobado",
                "green", "done_all", True, False, False, 16),
            ("discarded", "register", "Descartado",
                "red", "heart_broken", False, True, False, 10),
        ]
        order = -1
        for data in init_status:
            # name, group, public_name, color, icon, is_public,
            # open_editor, is_deleted = data
            name = data[0]
            group = data[1]
            public_name = data[2]
            color = data[3]
            icon = data[4]
            is_public = data[5]
            open_editor = data[6]
            is_deleted = data[7]
            try:
                priority = data[8]
            except IndexError:
                priority = 99
            try:
                description = data[9]
            except IndexError:
                description = None
            status, _ = StatusControl.objects.get_or_create(
                name=name
            )
            status.group = group
            status.public_name = public_name
            status.color = color
            status.icon = icon
            status.is_public = is_public
            order += 2
            if group == "register" and order < 20:
                order = 20
            if group == "location" and order < 40:
                order = 40
            status.order = order
            status.open_editor = open_editor
            status.is_deleted = is_deleted
            status.priority = priority
            status.description = description
            status.save()
