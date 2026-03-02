# dependence/management/commands/generate_data_dict.py

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models.fields import NOT_PROVIDED
from datetime import datetime


class Command(BaseCommand):
    help = 'Genera un diccionario de datos en formato Markdown desde los modelos Django'

    # Mapeo de tipos de campo a español
    FIELD_TYPE_MAP = {
        'AutoField': 'entero (auto)',
        'BigAutoField': 'entero (auto)',
        'BooleanField': 'booleano',
        'NullBooleanField': 'booleano',
        'CharField': 'texto',
        'TextField': 'texto largo',
        'IntegerField': 'entero',
        'BigIntegerField': 'entero grande',
        'SmallIntegerField': 'entero pequeño',
        'PositiveIntegerField': 'entero positivo',
        'PositiveSmallIntegerField': 'entero positivo pequeño',
        'PositiveBigIntegerField': 'entero positivo grande',
        'FloatField': 'decimal flotante',
        'DecimalField': 'decimal',
        'DateField': 'fecha',
        'DateTimeField': 'fecha y hora',
        'TimeField': 'hora',
        'EmailField': 'email',
        'URLField': 'URL',
        'UUIDField': 'UUID',
        'FileField': 'archivo',
        'ImageField': 'imagen',
        'JSONField': 'JSON',
        'SlugField': 'slug',
        'BinaryField': 'binario',
        'DurationField': 'duración',
        'GenericIPAddressField': 'dirección IP',
    }

    # Apps a procesar en orden
    APP_ORDER = [
        'ies',
        'example',
        'indicator',
        'question',
        'survey',
        'answer',
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--output',
            default='media/diccionario_datos.md',
            help='Nombre del archivo de salida (default: diccionario_datos.md)'
        )
        parser.add_argument(
            '--apps',
            nargs='+',
            help='Lista de apps específicas a procesar (default: todas las configuradas)'
        )
        parser.add_argument(
            '--all-apps',
            action='store_true',
            help='Procesar todas las apps del proyecto (no solo las configuradas)'
        )

    def handle(self, *args, **options):
        output_file = options['output']

        # Determinar qué apps procesar
        if options['all_apps']:
            app_list = [
                config.name for config in apps.get_app_configs()
                if not config.name.startswith('django.')
            ]
        elif options['apps']:
            app_list = options['apps']
        else:
            app_list = self.APP_ORDER

        lines = self.generate_header()
        lines.extend(self.generate_toc(app_list))
        lines.extend(self.generate_content(app_list))

        # Escribir archivo
        content = '\n'.join(lines)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Diccionario de datos generado exitosamente: {output_file}')
        )

    def generate_header(self):
        """Genera el encabezado del documento."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        return [
            "# 📚 Diccionario de Datos",
            "",
            f"> **Generado automáticamente:** {now}",
            ">",
            "> Este documento contiene la descripción de todas las tablas y campos del sistema.",
            "",
            "---",
            "",
        ]

    def generate_toc(self, app_list):
        """Genera la tabla de contenido."""
        lines = [
            "## 📑 Índice de Aplicaciones",
            "",
        ]

        for app_name in app_list:
            try:
                app_config = apps.get_app_config(app_name)
                app_verbose = getattr(app_config, 'verbose_name', app_name)
                anchor = f"app-{app_name.lower().replace('_', '-')}"
                lines.append(f"- [{app_verbose}](#{anchor})")
            except LookupError:
                pass

        lines.extend(["", "---", ""])
        return lines

    def generate_content(self, app_list):
        """Genera el contenido principal."""
        lines = []

        for app_name in app_list:
            try:
                app_config = apps.get_app_config(app_name)
            except LookupError:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  App "{app_name}" no encontrada, saltando...')
                )
                continue

            app_lines = self.process_app(app_config)
            lines.extend(app_lines)

        return lines

    def process_app(self, app_config):
        """Procesa una app y retorna sus líneas."""
        lines = []
        app_name = app_config.name
        print(f'Procesando app: {app_name}')
        app_verbose = getattr(app_config, 'verbose_name', app_name)

        # Encabezado de la app con estilo
        separator = "=" * 60
        lines.extend([
            "",
            f"<a name='app-{app_name.lower().replace('_', '-')}'></a>",
            "",
            separator,
            f"## 🗂️ App *{app_name}*: **{app_verbose}**",
            separator,
            "",
        ])

        # Obtener modelos
        model_list = list(app_config.get_models())

        if not model_list:
            lines.append("*No hay modelos definidos en esta aplicación.*")
            lines.extend(["", "---", ""])
            return lines

        # Lista de modelos en esta app
        # lines.append(f"**Modelos en esta app:** {len(model_list)}")
        # lines.append("")
        print("Modelos encontrados:", [model.__name__ for model in model_list])
        print("model_list", model_list)
        # sorted_models = sorted(
        #     model_list, key=lambda m: m.verbose_name_plural
        # )
        sorted_models = sorted(
            model_list, key=lambda m: getattr(m._meta, 'verbose_name_plural', m.__name__)
        )

        for model in sorted_models:
            model_lines = self.process_model(model)
            lines.extend(model_lines)

        return lines

    def process_model(self, model):
        """Procesa un modelo y retorna sus líneas."""
        lines = []
        model_name = model.__name__
        meta = model._meta

        # Verbose names
        verbose_singular = str(meta.verbose_name).capitalize()
        try:
            verbose_plural = str(meta.verbose_name_plural).capitalize()
        except AttributeError:
            verbose_plural = verbose_singular + "s"

        # Encabezado del modelo
        lines.extend([
            f'### 📋 Tabla *"{verbose_plural}"* (`{model_name}`)',
            "",
        ])

        # Información adicional del modelo
        # if verbose_singular != model_name.lower():
        #     lines.append(f"> **Nombre singular:** {verbose_singular}")

        # Obtener campos
        fields_to_process = []
        for field in meta.get_fields():
            # Ignorar campos reversos (sin get_internal_type)
            if not hasattr(field, 'get_internal_type'):
                continue
            # Ignorar campo id auto
            if getattr(field, 'primary_key', False) and field.name == 'id':
                continue
            fields_to_process.append(field)

        lines.append("")
        lines.append("**Campos:**")
        lines.append("")

        for field in fields_to_process:
            field_lines = self.format_field(field)
            lines.extend(field_lines)

        lines.extend(["", "---", ""])
        return lines

    def get_field_type(self, field):
        """Retorna el tipo de campo en español."""
        internal_type = field.get_internal_type()

        # Verificar si tiene choices primero
        if getattr(field, 'choices', None):
            return 'texto con opciones'

        # Manejar ForeignKey
        if internal_type == 'ForeignKey':
            related_model = field.related_model
            related_app = related_model._meta.app_label
            related_name = related_model.__name__
            return f'llave foránea a ***{related_app}-{related_name}***'

        # Manejar OneToOneField
        if internal_type == 'OneToOneField':
            related_model = field.related_model
            related_app = related_model._meta.app_label
            related_name = related_model.__name__
            return f'relación uno a uno con ***{related_app}-{related_name}***'

        # Manejar ManyToManyField
        if internal_type == 'ManyToManyField':
            related_model = field.related_model
            related_app = related_model._meta.app_label
            related_name = related_model.__name__
            return f'relación muchos a muchos con ***{related_app}-{related_name}***'

        return self.FIELD_TYPE_MAP.get(internal_type, internal_type.lower())

    def format_default_value(self, default):
        """Formatea el valor default para mostrar."""
        if default is NOT_PROVIDED:
            return None

        if callable(default):
            func_name = getattr(default, '__name__', str(default))
            return f'función `{func_name}`'

        if isinstance(default, bool):
            return '"Verdadero"' if default else '"Falso"'

        if default == '':
            return '"" (vacío)'

        if default is None:
            return '"None"'

        if isinstance(default, (list, dict)):
            return f'`{default}`'

        return f'"{default}"'

    def format_field(self, field):
        """Genera las líneas de descripción de un campo."""
        lines = []

        # Obtener verbose_name
        verbose_name = getattr(field, 'verbose_name', None)
        if verbose_name:
            verbose_name = str(verbose_name).strip()
            if verbose_name:
                verbose_name = verbose_name[0].upper() + verbose_name[1:]

        field_name = field.name

        # Construir la parte del nombre
        if verbose_name and verbose_name.lower() != field_name.lower().replace('_', ' '):
            name_part = f"**{verbose_name}** (`{field_name}`)"
        else:
            name_part = f"(`{field_name}`)"

        # Tipo de dato
        field_type = self.get_field_type(field)

        # Construir partes adicionales
        extras = []

        # Default value
        default = getattr(field, 'default', NOT_PROVIDED)
        default_str = self.format_default_value(default)
        if default_str:
            extras.append(f'default: {default_str}')

        # Help text
        help_text = getattr(field, 'help_text', '')
        if help_text:
            extras.append(f'[{help_text}]')

        # Verificar si es opcional
        blank = getattr(field, 'blank', False)
        null = getattr(field, 'null', False)
        is_optional = blank or null
        if is_optional:
            extras.append('***opcional***')

        # Construir línea principal
        line = f"- {name_part}: {field_type}"
        if extras:
            line += "; " + "; ".join(extras)

        lines.append(line)

        # Agregar choices si existen (indentados)
        choices = getattr(field, 'choices', None)
        if choices:
            for choice_key, choice_value in choices:
                lines.append(f'    - `"{choice_key}"`: "{choice_value}"')

        return lines
