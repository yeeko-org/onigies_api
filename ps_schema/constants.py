
all_collections = {
    "source": [
        {
            "snake_name": "note",
            "name": "Nota Final",
            "plural_name": "Notas Finales",
            "model_name": "Note",
            "level": "primary",
            "color": "deep-purple",
            "icon": "news",
            "all_filters": [
                {"filter_name": "source_types", "hidden": False},
                {
                    "title": "Fechas",
                    "component": "RangeDates", "hidden": False
                },
                {
                    "title": "Editor", "field": "editor",
                    "component": "UserSelect", "hidden": True,
                },
                {
                    "title": "Revisor", "field": "reviewer",
                    "component": "UserSelect", "hidden": True,
                },
                {
                    "title": "Con archivos", "field": "has_files",
                    "component": "TripleBooleanFilter", "hidden": True
                },
            ],
        },
        {
            "snake_name": "source",
            "name": "Fuente de información",
            "plural_name": "Fuentes de información",
            "model_name": "Source",
            "level": "category_subtype",
        },
        {
            "snake_name": "mention",
            "name": "Mención de proyecto en nota",
            "plural_name": "Menciones de proyectos en notas",
            "model_name": "Mention",
            "level": "relational",
        },
    ],

}

delete_collections = ["event_subtype"]

all_available_actions = [
    "massive_delete",
    "merge",
    "massive_edit",
]


filter_groups = [
    {
        "key_name": "project_types",
        "name": "Clasificación de Proyecto",
        "short_name": "Clasif. de Proyecto",
        "plural_name": "Clasificaciones de Proyecto",
        "main_collection": "project-project",
        "category_type": "project-extractivism_type",
        "category_subtype": "project-megaproject_type",
        "addl_config": {
            "subtype_is_autocomplete": True,
            "open_search": True
        },
    },

]


def send_many_requests():
    import requests
    import json
    import time

    error_ids = [2107]
    # 2075
    all_ids = [
        2107, 2005, 1902, 1896, 1833, 1832, 1737, 1571, 1501,
        1450, 1405, 1270, 797, 760, 718, 49]
    url = "https://ocsa.ibero.mx/api/rpc/approve_draft"
    headers = {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoib2Nzd2ViYWRtaW4iLCJlbWFpbCI6InNlYmFzdGlhbi5vbHZlcmFAaWJlcm8ubXgifQ.boDDaOPQXa9Q3LMohHXQvuw85fR5rEKPcMxr4nqzGms'
    }

    for elem_id in all_ids:
        payload = {'_id': elem_id}
        with requests.Session() as session:
            response = session.post(
                url, headers=headers, data=json.dumps(payload))
            if response.text:
                print(f"elem_id: {elem_id} | response: {response.text}")
        time.sleep(35)


def model_fields():
    from django.apps import apps
    my_model = apps.get_model("source", "Note")
    fields = my_model._meta.get_fields()
    for field in fields:
        try:
            print(field.default)
            print(type(field.default))
        except AttributeError:
            pass

