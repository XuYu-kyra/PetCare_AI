from django.contrib import admin
from .models import QandA,Oridata,ODIndex
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class QA(resources.ModelResource):
    class Meta:
        model = QandA
        export_order = ('question','answer')

@admin.register(QandA)
class QAAdmin(ImportExportModelAdmin):
    list_display = ('question','answer')
    search_fields = ['question']
    resource_class = QA

class OD(resources.ModelResource):
    class Meta:
        model = Oridata
        export_order = ('question','answer')

@admin.register(Oridata)
class ODAdmin(ImportExportModelAdmin):
    list_display = ('question','answer')
    search_fields = ['question']
    resource_class = OD

class ODIndexResource(resources.ModelResource): 
    class Meta: 
        model = ODIndex 
        export_order = ('q_keyword','q_doclist') 
 
@admin.register(ODIndex) 
class ODIndexAdmin(ImportExportModelAdmin): 
    list_display = ('q_keyword','q_doclist') 
    search_fields = ['q_keyword'] 
    resource_class = ODIndexResource 

