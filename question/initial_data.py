from .models import QuestionGroup


class InitQuestionGroups:
    def __init__(self):

        initial_data = [
            ('a_questions', 'Institucionalización', 'a_weight',
             'AQuestion', 'AResponse', 60),
            ('b_questions', 'Instancias', 'b_weight',
             'BQuestion', 'BResponse', 40),
            ('reach', 'Sectores', 'reach_weight',
             'ReachQuestion', 'ReachResponse', 0),
            ('plans', 'Planes de estudio', 'plan_weight',
             'PlanQuestion', 'PlanResponse', 0),
            ('special', 'Pregunta especial', 'special_weight',
             'SpecialQuestion', 'SpecialResponse', 0),
            ('population', 'Distribución de población', 'pop_weight',
             None, None, 0),
        ]

        for name, public, weight, m_question, m_response, weight_value in initial_data:
            QuestionGroup.objects.update_or_create(
                name=name,
                defaults={
                    'public_name': public,
                    'weight_name': weight,
                    'model_question': m_question,
                    'model_response': m_response,
                    'default_weight': weight_value
                }
            )