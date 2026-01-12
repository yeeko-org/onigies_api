from django.core.management.base import BaseCommand
from django.db import transaction
from indicator.models import Axis, Component, Observable
from decimal import Decimal


class Command(BaseCommand):
    help = "Carga los datos iniciales de Materias, Componentes y Observables"

    def handle(self, *args, **kwargs):
        # 1. Definición del diccionario de datos basado en tu referencia
        data = [
            {
                "number": 1,
                "name": "Igualdad de género",
                "components": [
                    {
                        "name": "Normas y políticas",
                        "observables": [
                            (1.1, "Proceso de armonización normativa"),
                            (
                                1.2,
                                "Norma principal de carácter general que integra la igualdad de género",
                            ),
                            (1.3, "Normas y disposiciones para la igualdad de género"),
                            (
                                1.4,
                                "Planeación institucional para la igualdad de género",
                            ),
                        ],
                    },
                    {
                        "name": "Estructuras organizacionales",
                        "observables": [
                            (1.5, "Estructuras para la igualdad de género"),
                            (1.6, "Principio de paridad de género en la normatividad"),
                            (1.7, "Integración paritaria"),
                        ],
                    },
                    {
                        "name": "Procesos y recursos institucionales",
                        "observables": [
                            (
                                1.8,
                                "Estadísticas y diagnósticos con perspectiva de género",
                            ),
                            (
                                1.9,
                                "Programas y actividades de sensibilización, concientización y capacitación en igualdad de género",
                            ),
                            (
                                1.10,
                                "Presupuestos institucionales para la igualdad de género",
                            ),
                            (
                                1.11,
                                "Evaluaciones en igualdad de género / características de los observables",
                            ),
                        ],
                    },
                    {
                        "name": "Procesos y recursos académicos",
                        "observables": [
                            (
                                1.12,
                                "Planes y programas de estudio, y asignaturas para la igualdad de género y con perspectiva de género (docencia)",
                            ),
                            (1.13, "Formación docente con perspectiva de género"),
                            (1.14, "Investigación académica con perspectiva de género"),
                            (
                                1.15,
                                "Mecanismos y criterios de evaluación y promoción académica (docencia e investigación) para la igualdad y no discriminación",
                            ),
                            (
                                1.16,
                                "Mecanismos y criterios de ingreso, permanencia y evaluación estudiantil para la igualdad y no discriminación",
                            ),
                            (
                                1.17,
                                "Evaluaciones académicas en materia de igualdad de género",
                            ),
                        ],
                    },
                ],
            },
            {
                "number": 2,
                "name": "Inclusión y no discriminación",
                "components": [
                    {
                        "name": "Normas y políticas institucionales y académicas",
                        "observables": [
                            (2.1, "Políticas institucionales para la inclusión"),
                            (
                                2.2,
                                "Políticas institucionales y académicas de inclusión y no discriminación",
                            ),
                            (
                                2.3,
                                "Mecanismos institucionales de reconocimiento de la diversidad sexo-genérica",
                            ),
                            (
                                2.4,
                                "Lenguaje incluyente, no discriminatorio y no sexista",
                            ),
                        ],
                    },
                    {
                        "name": "Procesos y recursos institucionales y académicos",
                        "observables": [
                            (
                                2.5,
                                "Programas y acciones institucionales de prevención primaria de la discriminación y la violencia",
                            ),
                            (
                                2.6,
                                "Programas y acciones institucionales de trabajo con hombres para la igualdad de género",
                            ),
                        ],
                    },
                ],
            },
            {
                "number": 3,
                "name": "Cuidados corresponsables",
                "components": [
                    {
                        "name": "Normas y políticas institucionales",
                        "observables": [
                            (
                                3.1,
                                "Políticas institucionales para la corresponsabilidad de los cuidados",
                            ),
                        ],
                    },
                    {
                        "name": "Procesos y recursos institucionales y académicos",
                        "observables": [
                            (
                                3.2,
                                "Licencias y permisos con perspectiva de género y de cuidados",
                            ),
                            (
                                3.3,
                                "Infraestructura para el acceso y ejercicio de cuidados en corresponsabilidad",
                            ),
                            (
                                3.4,
                                "Servicios para el acceso y ejercicio de cuidados en corresponsabilidad",
                            ),
                        ],
                    },
                ],
            },
            {
                "number": 4,
                "name": "Una vida libre de discriminaciones y violencias",
                "components": [
                    {
                        "name": "Normas y políticas institucionales",
                        "observables": [
                            (4.1, "Proceso de armonización normativa"),
                            (
                                4.2,
                                "Legislación para la atención de casos de discriminación / violencia basada en el género",
                            ),
                            (
                                4.3,
                                "Normas específicas para la atención de casos de discriminación / violencia basada en el género",
                            ),
                            (
                                4.4,
                                "Personas de primer contacto especializadas en materia de violencias de género",
                            ),
                            (
                                4.5,
                                "Políticas y medidas de prevención secundaria y terciaria de las discriminaciones / violencias basadas en el género enfocadas a las personas responsables de su ejercicio",
                            ),
                        ],
                    },
                    {
                        "name": "Estructuras institucionales",
                        "observables": [
                            (
                                4.6,
                                "Estructuras especializadas para la atención de casos de discriminación / violencia basadas en el género",
                            ),
                            (
                                4.7,
                                "Puestos especializados para la atención de casos de discriminación / violencias basadas en el género",
                            ),
                            (
                                4.8,
                                "Servicios especializados para la atención de casos de discriminación / violencia basadas en el género",
                            ),
                            (
                                4.9,
                                "Responsabilidades de actuación para atender casos de discriminación y violencia basada en el género",
                            ),
                        ],
                    },
                    {
                        "name": "Procesos y recursos institucionales",
                        "observables": [
                            (
                                4.10,
                                "Criterios de resolución y medidas de no repetición en el marco de la justicia restaurativa",
                            ),
                            (
                                4.11,
                                "Mecanismos de seguimiento de casos y cumplimiento de resoluciones",
                            ),
                            (
                                4.12,
                                "Documentación, sistematización de información y transparencia",
                            ),
                            (
                                4.13,
                                "Evaluación de atención de procedimientos formales (quejas o denuncias) de atención de casos de violencias de género.",
                            ),
                            (
                                4.14,
                                "Evaluación de atención de mecanismo de atención de las violencias por razones de género",
                            ),
                        ],
                    },
                ],
            },
        ]

        # 2. Lógica de inserción con transacción para asegurar integridad
        try:
            with transaction.atomic():
                for axis_data in data:
                    axis, created = Axis.objects.get_or_create(
                        order=axis_data["number"],
                        defaults={"name": axis_data["name"]}
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Eje creado: {axis.name}")
                        )

                    for comp_data in axis_data["components"]:
                        # Usamos get_or_create para componentes basándonos en nombre y eje
                        component, created = Component.objects.get_or_create(
                            name=comp_data["name"], axis=axis
                        )

                        for obs_num, obs_name in comp_data["observables"]:
                            observable, created = Observable.objects.get_or_create(
                                component=component,
                                number=Decimal(str(obs_num)),
                                defaults={"name": obs_name},
                            )

                self.stdout.write(self.style.SUCCESS("¡Datos cargados exitosamente!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante la carga: {str(e)}"))
