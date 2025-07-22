from import_export import resources, fields
from django.contrib import admin                            # Importa o módulo admin do Django
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export.widgets import ForeignKeyWidget
from modeltranslation.admin import TranslationAdmin         # Importa o TranslationAdmin, uma classe fornecida pelo pacote django-modeltranslation para facilitar a tradução de campos de modelos do Django na interface de administração
from reversion.admin import VersionAdmin
from .models import Area, SubArea, Term, News                     # Importa os modelos Area, SubArea, e Term de models.py

#####tentativa####  (tem que ficar antes do AreaAdmin)                  #Define as colunas de importação/exportação para o modelo Area
class AreaResource(resources.ModelResource):
    class Meta:
        model = Area
        import_id_fields = ['id']                                       # Define o campo que será usado como identificador único durante a importação
        fields = ['id', 'name_en', 'name_pt', 'name_pt_br', 'name_es']  # Define os campos a serem importados/exportados

##########                                                              #Define as colunas de importação/exportação para o modelo SubArea
class SubAreaResource(resources.ModelResource):
    class Meta:
        model = SubArea
        import_id_fields = ['ref']
        fields = ['ref', 'area', 'id', 'name_en', 'name_pt', 'name_pt_br', 'name_es']
##########

@admin.register(Area)                                                   # Regista o modelo Area na interface de administração do Django, permitindo a sua gestão através do painel de administração.
class AreaAdmin(VersionAdmin,TranslationAdmin, ImportExportModelAdmin):                    # Classe AreaAdmin herda de TranslationAdmin, permitindo que a interface de administração suporte a tradução dos campos do modelo Area.
    list_display = ['id', 'name']                                       # Define os campos do modelo que serão exibidos na lista de objetos na interface de administração.
    search_fields = ['name']                                            # Permite adicionar uma barra de pesquisa na interface de administração, onde os utilizadores podem procurar por 'name'.
    resource_classes = [AreaResource]                                   # Adiciona a classe de recurso para importação, para definir as colunas a importar.

@admin.register(SubArea)                                                # Regista o modelo SubArea na interface de administração do Django, permitindo a sua gestão através do painel de administração.
class SubAreaAdmin(VersionAdmin, TranslationAdmin, ImportExportModelAdmin):                # Classe SubAreaAdmin herda de TranslationAdmin, permitindo que a interface de administração suporte a tradução dos campos do modelo SubArea.
    list_display = ['ref','id', 'name', 'area']                         # Define os campos do modelo que serão exibidos na lista de objetos na interface de administração.
    list_filter = ['area']                                              # Adiciona um filtro na interface de administração, permitindo filtrar os objetos com base na 'area' associada.
    search_fields = ['name']                                            # Permite adicionar uma barra de pesquisa na interface de administração, onde os utilizadores podem procurar por 'name'.
    resource_classes = [SubAreaResource]

class IEVRefWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
                                                                        # Get values separated by '-' ex: '301-02-01'
        area_id = value.split('-')[0]                                   # 301
        subarea_ref = value.rsplit('-', 1)[0]                           # 301-02
        term_id = value.rsplit('-', 1)[-1]                              # 01

        try:
            subarea = super().clean(value)
        except SubArea.DoesNotExist:
            (area, created) = Area.objects.get_or_create(name=row['area'], defaults={'id': row['area_id']})
            subarea = SubArea.objects.create(name=row['subarea'], area=area)
        return subarea

##Acrescentei uma parte no fundo da class
# class IEVRefWidget(ForeignKeyWidget):
#     def clean(self, value, row=None, **kwargs):
#         # Get values separated by '-' ex: '301-02-01'
#         area_id = value.split('-')[0]  # 301
#         subarea_ref = value.rsplit('-', 1)[0]  # 301-02
#         term_id = value.rsplit('-', 1)[-1]  # 01
#
#         try:
#             subarea = super().clean(value)  # Tenta buscar a subárea
#         except SubArea.DoesNotExist:
#             # Se a subárea não existir, criamos uma nova subárea
#             (area, created) = Area.objects.get_or_create(name=row['area'], defaults={'id': area_id})
#
#             # Garante que o ID da subárea será sempre dois dígitos
#             formatted_subarea_id = f"{subarea_ref.split('-')[1]:02d}"  # Garantir que o ID da subárea tem dois dígitos
#             subarea = SubArea.objects.create(
#                 name=row['subarea'],
#                 area=area,
#                 id=formatted_subarea_id  # Usamos o ID formatado
#             )
#         return subarea


class TermResource(resources.ModelResource):
#    area = fields.Field(column_name='IEV_ref', attribute='ref', widget=IEVRefWidget(Area, 'name'))
#    area_id = fields.Field(column_name='area_id', attribute='subarea__area__id')
#    subarea_name = fields.Field(column_name='subarea_name', attribute='subarea__name') ###################
#    area_id = fields.Field()

#   def dehydrate_area_id(self, term):
#        return f'{term.subarea.area.id}'
#     def import_instance(self, instance, row, **kwargs):
#         # Convert empty strings to None for specific fields
#         for field in ['name_en', 'name_pt', 'name_pt_br', 'name_es', 'name']:
#             if getattr(instance, field) == '':
#                 setattr(instance, field, None)
#         super().import_instance(instance, row, **kwargs)


    def before_save_instance(self, instance, row, **kwargs):
        for field in ['name_en', 'name_pt', 'name_pt_br', 'name_es', 'name']:
            if getattr(instance, field) == '':
                setattr(instance, field, None)

    def before_import(self, dataset, **kwargs):
                                                            # mimic a 'dynamic field' - i.e. append field which exists on
        dataset.headers.append("subarea")                   # Book model, but not in dataset
        #dataset.headers.append("id")
        dataset.headers.append("ref")
        super().before_import(dataset, **kwargs)
    #
    def before_import_row(self, row, **kwargs):
        iev_ref = row['ref'].strip()                        ##########estava 'IEV_ref' em vez de 'ref'#############
        #area_id = iev_ref.split('-')[0]                    # 301
        subarea_ref = iev_ref.rsplit('-', 1)[0]             # 301-02
        term_id = iev_ref.rsplit('-', 1)[-1]                # 01
        row["id"] = term_id
        row["subarea"] = subarea_ref
        row['ref'] = iev_ref

        # # List of columns to check
        # columns_to_check = ['name_en', 'name_pt', 'name_pt_br', 'name_es']
        #
        # # Iterate over the columns and set blank values to None
        # for column in columns_to_check:
        #     if column in row and (row[column] == '' or row[column] is None):
        #         row[column] = None

    class Meta:
        model = Term
        import_id_fields = ['ref']
        # fields = ['id', 'name_en', 'name_pt', 'name_pt_br', 'name_es',
        #           'area_id', 'area', 'subarea_id', 'subarea__name',
        #           'description_en', 'description_pt', 'description_pt_br', 'description_es',
        #           'source_en', 'source_pt', 'source_pt_br', 'source_es',
        #           'image', 'extra', 'created', 'updated']
        ############## tentativa
        fields = ['ref', 'subarea', 'id',
                  'name_en', 'description_en', 'source_en', 'extra_en',
                  'name_pt', 'description_pt', 'source_pt', 'extra_pt',
                  'name_es', 'description_es', 'source_es', 'extra_es',
                  'name_pt_br', 'description_pt_br', 'source_pt_br', 'extra_pt_br',
                  'image',
                  'created', 'updated'
                  ]
        ##############
        import_order = ['ref', 'subarea', 'id',
                        'name_en', 'description_en', 'source_en',
                        'name_pt', 'description_pt', 'source_pt',
                        'name_es', 'description_es', 'source_es',
                        'name_pt_br', 'description_pt_br', 'source_pt_br',
                        ]
        #export_order = ('id', 'price', 'author', 'name')

@admin.register(Term)                                                       # Regista o modelo Term na interface de administração do Django, permitindo a sua gestão através do painel de administração.
class TermAdmin(VersionAdmin, TranslationAdmin, ImportExportModelAdmin, ExportActionMixin) :         # Classe TermAdmin herda de TranslationAdmin, permitindo que a interface de administração suporte a tradução dos campos do modelo Term.
    list_display = ['ref','id', 'name', 'subarea__area', 'subarea']         # Define os campos do modelo que serão exibidos na lista de objetos na interface de administração.
    list_filter = ['subarea__area', 'subarea']                              # Adiciona filtros na interface de administração, permitindo filtrar os objetos com base na 'subarea' e na 'area' associada à 'subarea'.
    search_fields = ['name']
    resource_classes = [TermResource]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo', 'inicio', 'fim', 'criado_em')
    list_filter = ('ativo',)
    ordering = ('-criado_em',)

