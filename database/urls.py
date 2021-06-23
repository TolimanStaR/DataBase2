from django.urls import path
from .views import *

urlpatterns = [
    path('', DataBaseList.as_view(), name='db_list'),
    path('create/', DataBaseCreateView.as_view(), name='db_create'),
    path('<int:pk>/', DataBaseDetail.as_view(), name='db_detail'),
    path('<int:pk>/update/', DataBaseUpdateView.as_view(), name='db_update'),
    path('table/<int:pk>/', TableDetail.as_view(), name='table_detail'),
    path('table/<int:pk>/insert/', TableRowAddView.as_view(), name='table_add_row'),
    path('table/<int:pk>/insert/success/', AddRowForm.as_view(), name='table_add_row_success'),
    path('table/<int:pk>/delete_value/<id>/', TableRowDeleteView.as_view(), name='delete_value_by_id'),
    path('table/<int:pk>/create/', TableCreateView.as_view(), name='table_create', ),
    path('table/<int:pk>/update/', TableUpdateView.as_view(), name='table_update', ),
    path('table/<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete', ),
    path('table/<int:pk>/create_query/', TableCreateQuery.as_view(), name='table_create_query', ),
    path('table/<int:pk>/search_by_value/', SearchTableRow.as_view(), name='search_by_value', ),
    path('table/<int:pk>/delete_by_value/', DeleteTableRow.as_view(), name='delete_by_value', ),
    path('tutorial/', Tutorial.as_view(), name='tutorial'),
]
