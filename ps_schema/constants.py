
all_collections = {
    # "all_filters": [
    #     { "filter_name": "source_types", "hidden": False },
    #     {
    #         "title": "Fechas",
    #         "component": "RangeDates", "hidden": False
    #     },
    #     {
    #         "title": "Editor", "field": "editor",
    #         "component": "UserSelect", "hidden": True,
    #     },
    #     {
    #         "title": "Revisor", "field": "reviewer",
    #         "component": "UserSelect", "hidden": True,
    #     },
    #     {
    #         "title": "Con archivos", "field": "has_files",
    #         "component": "TripleBooleanFilter", "hidden": True
    #     },
    # ],
    "ies": [
        {
            "snake_name": "institution",
            "name": "Institución",
            "plural_name": "Instituciones",
            "model_name": "Institution",
            "level": "category_subtype",
        },
        {
            "snake_name": "period",
            "name": "Periodo",
            "plural_name": "Periodos",
            "model_name": "Period",
            "level": "category_subtype",
        },
    ],
    "indicator": [
        {
            "snake_name": "axis",
            "name": "Eje",
            "plural_name": "Ejes",
            "model_name": "Axis",
            "level": "category_group",
        },
        {
            "snake_name": "component",
            "name": "Componente",
            "plural_name": "Componentes",
            "model_name": "Component",
            "level": "category_type",
        },
        {
            "snake_name": "observable",
            "name": "Observable",
            "plural_name": "Observables",
            "model_name": "Observable",
            "level": "category_subtype",
        },
        {
            "snake_name": "sector",
            "name": "Sector Poblacional",
            "plural_name": "Sectores Poblacionales",
            "model_name": "Sector",
            "level": "category_subtype",
        }
    ],
    "example": [
        {
            "snake_name": "feature",
            "name": "Característica a calificar",
            "plural_name": "Características a calificar",
            "model_name": "Feature",
            "level": "category_subtype",
        },
        {
            "snake_name": "good_practice",
            "name": "Buena práctica",
            "plural_name": "Buenas prácticas",
            "model_name": "GoodPractice",
            "level": "primary",
        },
    ],
    "question": [
        {
            "snake_name": "a_option",
            "model_name": "AOption",
            "level": "category_subtype",
        }
    ]

}

delete_collections = []
delete_filter_groups = ["project_types"]

all_available_actions = [
    "massive_delete",
    "merge",
    "massive_edit",
]


filter_groups = [
    {
        "key_name": "institutions",
        "name": "Institución",
        "plural_name": "Instituciones",
        "category_subtype": "institution",
    },
    {
        "key_name": "periods",
        "name": "Periodo",
        "plural_name": "Periodos",
        "category_subtype": "period",
    },
    {
        "key_name": "axes",
        "name": "Eje/Componentes",
        "plural_name": "Ejes y Componentes",
        "category_group": "axis",
        "category_type": "component",
        "category_subtype": "observable",
    },
    {
        "key_name": "sectors",
        "name": "Sector Poblacional",
        "plural_name": "Sectores Poblacionales",
        "category_subtype": "sector",
    },
    {
        "key_name": "features",
        "name": "Característica",
        "plural_name": "Características",
        "category_subtype": "feature",
    },
    {
        "key_name": "a_options",
        "name": "Opción de Respuesta Institucionalización",
        "plural_name": "Opciones de Respuesta Institucionalización",
        "category_subtype": "a_option",
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

