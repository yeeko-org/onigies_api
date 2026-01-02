from .models import Feature, FeatureOption


class InitStatus:
    def __init__(self):

        init_features = [
            {
                'name': 'Es novedosa',
                'complement': 'Es innovadora o poco común',
                'description': 'La práctica es novedosa en el contexto '
                               'de la institución o región.',
                'reason_text': 'Explica por qué consideras que esta'
                               ' práctica es innovadora.',
                'options': [
                    {'name': 'Nada novedosa', 'value': 0},
                    {'name': 'Poco novedosa', 'value': 1},
                    {'name': 'Medianamente novedosa', 'value': 2},
                    {'name': 'Muy novedosa', 'value': 3},
                    {'name': 'Totalmente novedosa', 'value': 4},
                ],
            },
            {
                'name': 'Es relevante',
                'complement': 'Es un tema de la agenda de igualdad de género',
                'description': 'La práctica aborda temas importantes '
                               'relacionados con la igualdad de género.',
                'reason_text': 'Explica la relevancia de la práctica en '
                               'el contexto de igualdad de género.',
                'options': [
                    {'name': 'Nada relevante', 'value': 0},
                    {'name': 'Poco relevante', 'value': 1},
                    {'name': 'Medianamente relevante', 'value': 2},
                    {'name': 'Muy relevante', 'value': 3},
                    {'name': 'Totalmente relevante', 'value': 4},
                ],
            },
            {
                'name': 'Tiene amplia cobertura',
                'complement': 'Abarca un porcentaje significativo',
                'description': 'La práctica alcanza a un gran número '
                               'de personas dentro de la institución.',
                'reason_text': 'Describe cómo la práctica logra una '
                               'amplia cobertura.',
                'options': [
                    {'name': 'Cobertura muy baja', 'value': 0},
                    {'name': 'Cobertura baja', 'value': 1},
                    {'name': 'Cobertura media', 'value': 2},
                    {'name': 'Cobertura alta', 'value': 3},
                    {'name': 'Cobertura muy alta', 'value': 4},
                ],
            },
            {
                'name': 'Cumple sus objetivos',
                'complement': 'De proceso y de impacto',
                'description': 'La práctica ha demostrado cumplir '
                               'sus objetivos establecidos.',
                'reason_text': 'Proporciona evidencia del cumplimiento '
                               'de los objetivos.',
                'options': [
                    {'name': 'No cumplió', 'value': 0},
                    {'name': 'Cumplimiento bajo', 'value': 1},
                    {'name': 'Cumplimiento medio', 'value': 2},
                    {'name': 'Cumplimiento alto', 'value': 3},
                    {'name': 'Cumplimiento total', 'value': 4},
                ],
            },
            {
                'name': 'Popularidad interna',
                'complement': 'La comunidad de la IES participa activamente',
                'description': 'La práctica cuenta con el apoyo y la '
                               'participación activa de la comunidad.',
                'reason_text': 'Describe cómo la comunidad participa en '
                               'la práctica.',
                'options': [
                    {'name': 'Nula participación', 'value': 0},
                    {'name': 'Baja participación', 'value': 1},
                    {'name': 'Participación media', 'value': 2},
                    {'name': 'Alta participación', 'value': 3},
                    {'name': 'Muy alta participación', 'value': 4},
                ],
            },
            {
                'name': 'Sostenimiento',
                'complement': 'A lo largo del tiempo',
                'description': 'La práctica se ha mantenido efectiva a lo '
                               'largo del tiempo.',
                'reason_text': 'Proporciona detalles sobre el sostenimiento '
                               'de la práctica.',
                'options': [
                    {'name': 'Menos de un año', 'value': 0},
                    {'name': '1-3 años', 'value': 1},
                    {'name': '4-6 años', 'value': 2},
                    {'name': '7-8 años', 'value': 3},
                    {'name': 'Más de 9 años', 'value': 4},
                ],
            },
            {
                'name': 'Réplica en otras IES',
                'complement': 'Otras instituciones que han adoptado la práctica',
                'description': 'La práctica ha sido replicada en otras '
                               'instituciones educativas.',
                'reason_text': 'Menciona las instituciones que han replicado '
                               'la práctica.',
                'options': [
                    {'name': 'No ha sido replicada', 'value': 0},
                    {'name': 'Replicada en una IES', 'value': 1},
                    {'name': 'Replicada en 2-3 IES', 'value': 2},
                    {'name': 'Replicada en 4-5 IES', 'value': 3},
                    {'name': 'Replicada en más de 5 IES', 'value': 4},
                ],
            },
            {
                'name': 'Otra',
                'complement': 'Característica adicional',
                'description': 'Puedes agregar otra característica relevante.',
                'reason_text': 'Describe la característica adicional que '
                                 'consideras importante.',
                'options': [],
                'is_other': True
            }
        ]
        order = 1
        for feature_data in init_features:
            feature, _ = Feature.objects.get_or_create(
                name=feature_data['name'],
                complement=feature_data['complement'],
                description=feature_data['description'],
                reason_text=feature_data['reason_text'],
                is_other=feature_data.get('is_other', False),
                order=order
            )
            order += 1
            options = feature_data.get('options', [])
            for option_data in options:
                feature.options.get_or_create(
                    name=option_data['name'],
                    value=option_data['value']
                )
