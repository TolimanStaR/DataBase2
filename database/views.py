from django.shortcuts import render
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, DetailView, TemplateView, ListView
from django.contrib import messages
from django.views.generic.base import View, TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
import uuid
from django.utils import timezone
from django.core.files import File
from .models import *
from .forms import *

import psycopg2


class Connection(object):
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.result = None

    def connect(self, db):
        self.conn = psycopg2.connect(dbname=db, user='postgres',
                                     password='semin@1', host='193.162.143.101')
        self.cursor = self.conn.cursor()

    def get_result(self):
        self.result = self.cursor.fetchall()
        return self.result

    def return_table(self, db, table):
        self.connect(db)
        self.execute_query(f"SELECT * FROM {table}")
        return self.get_result()

    def execute_function(self, function_name, *args):
        print(self.cursor)
        self.cursor.callproc(function_name, [*args])
        self.result = self.cursor.fetchall()
        self.conn.commit()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        # self.cursor.close()
        # self.conn.close()

    def delete_row_by_id(self, table, id_):
        self.execute_query(f'DELETE FROM {table} WHERE id = {id_};')


class DataBaseList(ListView):
    model = DataBase
    template_name = 'database/database_list.html'


class DataBaseDetail(DetailView):
    model = DataBase
    template_name = 'database/database_detail.html'


class DataBaseCreateView(CreateView):
    model = DataBase
    template_name = 'database/database_create_update.html'
    fields = (
        'title',
        'description',
    )

    def form_valid(self, form):
        db_name = form.cleaned_data['title']
        manager = Connection()
        manager.connect('test')
        manager.execute_query(f"SELECT f_create_db('{db_name}');")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('db_list')


class DataBaseUpdateView(UpdateView):
    model = DataBase
    template_name = 'database/database_create_update.html'
    fields = (
        'description',
    )

    def get_success_url(self):
        return reverse('db_detail', kwargs=self.kwargs)


class DataBaseDeleteView(DeleteView):
    model = DataBase

    def get_success_url(self):
        return reverse('db_list', kwargs={})


class TableList:
    pass


class TableDetail(DetailView):
    model = Table
    template_name = 'table/table_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = Table.objects.get(pk=self.kwargs['pk'])
        context['form'] = EmptyForm
        context['search_form'] = RowForm
        c = Connection()
        context['table_table'] = c.return_table(context['table'].db.title, context['table'].title)
        return context


class TableCreateView(CreateView):
    model = Table
    fields = (
        'title',
    )
    template_name = 'table/table_create_update.html'

    def form_valid(self, form):
        db = DataBase.objects.get(pk=self.kwargs['pk'])
        form.instance.db = db
        table_name = form.instance.title
        c = Connection()
        c.connect(db.title)
        try:
            c.execute_query(f'SELECT create_table_{table_name}();')
        except Exception:
            c.execute_query(f'CREATE TABLE {table_name} ();')
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('db_list', kwargs={})


class TableCreateQuery(TemplateView):
    template_name = 'table/table_create_query.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['db'] = Table.objects.get(pk=self.kwargs['pk'])
        context['form'] = RowForm

        return context


class TableCreateQueryFormHandle(FormView):
    pass


class SearchTableRow(FormView):
    template_name = 'table/table_detail.html'
    form_class = RowForm

    def form_valid(self, form):
        table = Table.objects.get(pk=self.kwargs['pk'])
        search = form.cleaned_data['value']
        c = Connection()
        table_contains = c.return_table(table.db.title, table.title)
        for row in table_contains:
            print(search, row)
            if search in row:
                messages.success(self.request, f'Запись найдена. ID: {row[0]}')
                return super().form_valid(form)
        messages.success(self.request, f'Запись не найдена')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table_detail', kwargs={'pk': self.kwargs['pk']})


class DeleteTableRow(FormView):
    template_name = 'table/table_detail.html'
    form_class = RowForm

    def form_valid(self, form):
        table = Table.objects.get(pk=self.kwargs['pk'])
        search = form.cleaned_data['value']
        c = Connection()
        table_contains = c.return_table(table.db.title, table.title)
        for row in table_contains:
            print(search, row)
            if search in row:
                messages.success(self.request, f'Запись удалена. ID: {row[0]}')
                c.execute_query(f'DELETE FROM {table.title} WHERE id = {row[0]};')
                return super().form_valid(form)
        messages.success(self.request, f'Запись не найдена')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table_detail', kwargs={'pk': self.kwargs['pk']})


class TableUpdateView(UpdateView):
    model = Table
    template_name = 'table/table_create_update.html'
    fields = (
        'title',
    )


class TableDeleteView(DeleteView):
    model = Table

    def get_success_url(self):
        return reverse('db_list')


class TableRowAddView(TemplateView):
    template_name = 'database/row_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = Table.objects.get(pk=self.kwargs['pk'])
        context['form'] = RowForm
        return context


class AddRowForm(FormView):
    form_class = RowForm
    template_name = 'database/row_add.html'

    def form_valid(self, form):
        table = Table.objects.get(pk=self.kwargs['pk'])
        c = Connection()
        c.connect(table.db.title)
        values = form.cleaned_data['value'].split(',')
        print(values)
        if table.title == 'book':
            c.execute_function(f'insert_into_book', *values)
        if table.title == 'lib_user':
            c.execute_function(f'insert_into_lib_user', *values)
        if table.title == 'usage':
            c.execute_function(f'insert_into_usage', *values)
        if table.title == 'library':
            c.execute_function(f'insert_into_library', *values)
        return super(AddRowForm, self).form_valid(form)

    def get_success_url(self):
        return reverse('table_detail', kwargs=self.kwargs)


class TableRowDeleteView(FormView):
    form_class = EmptyForm
    template_name = 'table/table_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = Table.objects.get(pk=self.kwargs['pk'])
        context['form'] = RowForm
        return context

    def form_valid(self, form):
        id = self.kwargs['id']
        table = Table.objects.get(pk=self.kwargs['pk'])
        c = Connection()
        c.connect(table.db.title)
        c.delete_row_by_id(table.title, id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table_detail', kwargs={'pk': self.kwargs['pk']})


class TableRowEditView:
    pass


class Tutorial(TemplateView):
    template_name = 'database/tutorial.html'
