# Create your models here.
from ckeditor.fields import RichTextField               # Importa o campo RichTextField do CKEditor, que permite a edição de texto rico em modelos Django.
from django.db import models                            # Importa o módulo models do Django, que contém classes para definir modelos de dados.
from django.utils.translation import gettext as _       # Importa a função gettext do Django, renomeando-a como '_', para facilitar a tradução de strings. Documentação Django: Specify a translation string by using the function gettext(). It’s convention to import this as a shorter alias, _, to save typing.
import reversion
from django.utils import timezone


# Modelo para a área de conhecimento
@reversion.register()
class Area(models.Model):                               # Classe Area herda de models.Model, representando um modelo de dados no Django.
    id = models.CharField(_('Id'), max_length=3, primary_key=True)          # Define o campo 'id' como um IntegerField, que é a chave primária do modelo. Cada 'id' é único.
    name = models.CharField(_('Name'), max_length=255, unique=True, null=True, blank=True) # Define o campo 'name' como um CharField, com um nome traduzido e restrição de ser único.

    class Meta: # Classe interna Meta para definir opções adicionais do modelo.
        verbose_name = _('Area')                        # verbose_name é uma string que fornece um nome legível para o modelo, por ex. no painel de administração do django
    def __str__(self):                                  # Metodo que define a representação em string do modelo.
        return f"{self.id} {self.name}"                 # Retorna uma string formatada com o 'id' e o 'name' da área.


# Modelo para a subárea de conhecimento
@reversion.register()
class SubArea(models.Model):
    ref = models.CharField(_('Reference'), max_length=6, editable=False, primary_key=True) # Ex: 301-01
    id = models.CharField(_('Id'), max_length=2) # Ex: 01
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True) # Define o campo 'name' como um CharField, com um nome traduzido e restrição de ser único.
    area = models.ForeignKey(Area, verbose_name=_('Area'), related_name='subareas', on_delete=models.PROTECT) # Define uma ForeignKey que faz referência ao modelo Area, permitindo associar uma SubArea a uma Area.

    class Meta:                                         # Classe interna Meta para definir opções adicionais do modelo.
        verbose_name = _('Subarea')                     # verbose_name é uma string que fornece um nome legível para o modelo, por ex. no painel de administração do django

    def save(self, *args, **kwargs):
        # Formata o ID com 2 dígitos, apenas se for numérico
        if self.id and self.id.isdigit():
            self.id = f"{int(self.id):02d}"

        self.ref = f'{self.area.id}-{self.id}'
        super().save(*args, **kwargs)

    def __str__(self):                                   # Metodo que define a representação em string do modelo.
        return f"{self.ref} {self.name}"                 # Retorna uma string formatada com o 'id' da área, o 'id' da subárea (com pelo menos dois dígitos inteiros) e o 'name' da subárea.


# Modelo para os termos/vocábulos
@reversion.register()
class Term(models.Model):                               # Classe Term herda de models.Model, representando um modelo de dados no Django.
    ref = models.CharField(_('IEV Reference'), max_length=9, editable=False, primary_key=True)  # Ex: 301-01-01
    id = models.CharField(_('Id'), max_length=2)  # Ex: 01
    subarea = models.ForeignKey(SubArea, verbose_name=_('Subarea'), related_name='termos', on_delete=models.PROTECT) # Define uma ForeignKey que faz referência ao modelo SubArea, permitindo associar um Term a uma SubArea.
    name = models.CharField(_('Name'),max_length=255, null=True, blank=True) # Define o campo 'name' como um CharField, com um nome traduzido e restrição de ser único.
    description = models.TextField(_('Description'), null=True) # Define o campo 'description' como um TextField, para descrever o termo, que pode ser nulo.
    source = models.TextField(_('Source'), blank=True, null=True) # Define o campo 'source' como um TextField, que pode ser deixado em branco ou nulo, para indicar a fonte do termo.
    image = models.ImageField(_('Image'), upload_to='imagens/', null=True, blank=True) # Define o campo 'image' como um ImageField, que pode ser nulo ou em branco, para armazenar uma imagem associada ao termo.
    extra = RichTextField(blank=True, null=True)        # Define o campo 'extra' como um RichTextField, permitindo a edição de texto rico.

    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    def save(self, *args, **kwargs):
        self.ref = f"{self.subarea.ref}-{self.id}"
        super().save(*args, **kwargs)

    class Meta:                                         # Classe interna Meta para definir opções adicionais do modelo.
        verbose_name = _('Term')                        # verbose_name é uma string que fornece um nome legível para o modelo, por ex., no painel de administração do Django.

    def __str__(self):                                  # Metodo que define a representação em string do modelo.
        return f"{self.ref} {self.name}"                # Retorna uma string formatada com a referência IEV e o nome do termo.


# para mostrar mensagens de avisos/notícias na homepage

class News(models.Model):
    title = models.CharField(_("Title"), max_length=200, default=_("Untitled"))
    message = RichTextField(_("Message"))
    active = models.BooleanField(_("Active"), default=False)
    start_date = models.DateTimeField(_("Show from"), null=True, blank=True)
    end_date = models.DateTimeField(_("Hide after"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")

    def is_valid_now(self):
        now = timezone.now()
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True

    def __str__(self):
        return f"{self.title} ({'Active' if self.active else 'Inactive'})"
