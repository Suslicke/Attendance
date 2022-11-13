
from tokenize import group
from wsgiref.handlers import format_date_time
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from django.http import HttpResponse
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.db.models import Sum, Avg

import pandas as pd 
import plotly.express as px
from plotly.offline import plot
import datetime
import calendar
import locale
import xlwt


from .forms import TruancyForm, DateForm, SignUpForm, LogInForm
from .models import Truancy


# Create your views here.

class LoginUser(LoginView):
    form_class = LogInForm
    template_name = 'login.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('main')
    
        
class MainPage(LoginRequiredMixin, TemplateView):
    
    login_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin', group=1)
            if not request.user.is_staff:
                return redirect('group')
        return super().dispatch(request, *args, **kwargs)
    
    
    
class Admin(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'admin.html'
    
    form_dateFilter = DateForm
    initial = {'key': 'value'}
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        group = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return group

    
    def get(self, request, group):

        class GeneratePage():
            def graph(self, request, graph_data, start):
                if graph_data:
                    fig = px.bar(
                        x=[c['date'] for c in graph_data],
                        y=[c['percent'] for c in graph_data],
                        labels={'x': 'Дата', 'y':'Общий процент'},
                        )
                    
                    
                    
                    if start:
                        fig.update_layout(yaxis_range=[0, 100],
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      autosize=True,
                                      height=430,                                      
                                    #   width=1000,
                                    
                                      
                                    )
                    else:
                        fig.update_layout(yaxis_range=[0, 100],
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        autosize=True,
                                        height=430,
                                        xaxis_range=[datetime.datetime.today().replace(day=1), datetime.datetime.today().replace(day=1) + datetime.timedelta(days=calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])],
                                        
                                        #   width=1000,
                                        
                                        
                                        )
                         #xaxis_range=[datetime.datetime.today().replace(day=1), datetime.datetime.today().replace(day=1) + datetime.timedelta(days=monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])]
                    

                    chart = fig.to_html(full_html=False)

                
                    # date_form = self.form_date(initial=self.initial)
                    
                    return chart
                
            def today_data(self, request, today_info, group, start, end):
                if group != 1:
                    group_info = Truancy.objects.filter(group=group)
                    
                    if start:
                        group_info = Truancy.objects.filter(group=group).filter(date__gte=start)
                    if end:
                        group_info = Truancy.objects.filter(group=group).filter(date__lte=end)
                        
                    if start and end:
                        group_info = Truancy.objects.filter(group=group).filter(date__gte=start).filter(date__lte=end)
                    
                    
                    def avg(group_info):
                        avg_percent = 0
                        avg_absenteeism = 0
                        all_num_hours = 0
                        
                        i = 0
                        for data in group_info:
                            avg_percent += data.percent
                            avg_absenteeism += data.absenteeism
                            all_num_hours += data.num_hours
                            i += 1
                        
                        try:
                            avg_percent /= i
                            avg_absenteeism /= i
                        except ZeroDivisionError:
                            pass
                        
                        group_avg = {
                            'avg_percent': round(avg_percent, 2),
                            'avg_absenteeism': round(avg_absenteeism, 2),
                            'all_num_hours': round(all_num_hours, 2),
                        }
                        
                        return group_avg
                    
                    group_avg = avg(group_info)
                    
                    today = {
                        'group_today': today_info,
                    }
                    today.update(group_avg)
                    
                elif group == 1:
                    
                    def avg(start, end):
                        avg_info = Truancy.objects.values('date').annotate(absenteeism=Avg('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date')
                        if start and end:
                            avg_info = Truancy.objects.values('date').annotate(absenteeism=Avg('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date').filter(date__gte=start).filter(date__lte=end)
                        
                        avg_percent = 0
                        avg_absenteeism = 0
                        all_num_hours = 0
                        
                        i = 0
                        for data in avg_info:
                            avg_percent += data['percent']
                            avg_absenteeism += data['absenteeism']
                            all_num_hours += data['num_hours']
                            i += 1
                            
                        try:
                            avg_percent /= i
                            avg_absenteeism /= i
                        except ZeroDivisionError:
                            pass
                            
                        all_group_avg = {
                            'avg_percent': round(avg_percent, 2),
                            'avg_absenteeism': round(avg_absenteeism, 2),
                            'all_num_hours': round(all_num_hours, 2),
                        }
                        
                        return all_group_avg
                        
                    all_group_avg = avg(start, end)
                    
                    today = {
                        'today': today_info,
                    }
                    
                    today.update(all_group_avg)

                    
                    
                return today
            
                    
            def do(self, request, group):
                
                start = request.GET.get('start')
                end = request.GET.get('end')
                
                if group == 1:
                    graph_data = Truancy.objects.values('date').annotate(absenteeism=Sum('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date')
                    
                    if start:
                        graph_data = Truancy.objects.values('date').annotate(absenteeism=Sum('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date').filter(date__gte=start)
                    if end:
                        graph_data = Truancy.objects.values('date').annotate(absenteeism=Sum('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date').filter(date__lte=end)
                    
                    if start and end:
                        graph_data = Truancy.objects.values('date').annotate(absenteeism=Sum('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date').filter(date__gte=start).filter(date__lte=end)
                    
                    chart = GeneratePage.graph(self, request, graph_data, start)
                    
                    get_today = datetime.date.today()
                    today_info = Truancy.objects.values('date').annotate(absenteeism=Sum('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date').filter(date=get_today)
                    
                    today_all_group = GeneratePage.today_data(self, request, today_info, group, start, end)
                    
                    context_data = {
                        'chart': chart,
                    }
                    context_data.update(today_all_group)
                    return context_data
                
                else:
                    graph_data = Truancy.objects.filter(group=group).values()
                    
                    if start:
                        graph_data = Truancy.objects.filter(group=group).values().filter(date__gte=start)
                    if end:
                        graph_data = Truancy.objects.filter(group=group).values().filter(date__lte=end)
                    
                    chart = GeneratePage.graph(self, request, graph_data, start)
                    
                    get_today = datetime.date.today()
                    today_info = Truancy.objects.filter(date=get_today, group=group)
                    
                    today_group = GeneratePage.today_data(self, request, today_info, group, start, end)
                    
                    context_data = {
                        'chart': chart,
                    }
                    context_data.update(today_group)
                    return context_data
                    

        
        # data_list = Truancy.objects.values('date').annotate(absenteeism=Sum('absenteeism'), percent=Avg('percent'), num_hours=Sum('num_hours')).order_by('date')
        
        group_report = Truancy.objects.filter(date=datetime.date.today()).values_list('group', flat=True)
        
        status_report = Truancy.objects.filter(date=datetime.date.today()).values()
        
        error_groups = User.objects.filter(is_staff=False).exclude(id__in=group_report)
        
        
        def get_group(self, request):
            groups = Truancy.objects.order_by('group').distinct('group') #Truancy.objects.order_by('group').distinct('group')
            return groups
        
        form = self.form_dateFilter(initial=self.initial)
        
        # if datetime.date.today() in data_list.values_list('date', flat=True):
            
        context_data = GeneratePage.do(self, request, group=group)
        groups = get_group(self, request)
        
        current_group = User.objects.get(id=group)
        
        current_date = datetime.datetime.today()
        
        context = {
            'current_date': current_date.strftime('%Y-%m-%d'),
            'form': form,
            'current_group': current_group,
            'groups': groups,
            'error': error_groups, 
            'status_report': status_report,
        }
        context.update(context_data)


        return render(request, self.template_name, context)
    # else:
        #     return render(request, self.template_name, {'form': form})
    
        # render_page(self, request)
        
        
class AdminRegistration(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'admin_registration.html'
    
    form_registration = SignUpForm
    
    initial = {'key': 'value'}
    
    def get(self, request):
        form = self.form_registration(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):        
        
        if request.method == "POST":
            form = self.form_registration(request.POST or None)
            
            if form.is_valid():
                form.save()
                # login(request, user)
                messages.success(request, 'Вы успешно зарегистрировали пользователя')
                return redirect('/')
            
            else:
                messages.error(request, 'При регистрации нового пользователя возникла ошибка')

        else:
            form = self.form_registration()
                
        return render(request, self.template_name, {'form': form})
    
    

class Group(LoginRequiredMixin, TemplateView):
    # http_method_names = ['get', 'post'] 
    login_url = reverse_lazy('login')
    template_name = 'group.html'
    
    form_truancy = TruancyForm
    form_date = DateForm
    
    
    initial = {'key': 'value'}


    def get(self, request, *args, **kwargs):
        get_today = datetime.date.today()
        get_skip = Truancy.objects.filter(date=get_today, group=request.user)
         
        get_all_skip = Truancy.objects.filter(group=request.user)
        
        if get_all_skip:
            fig = px.bar(
                x=[c.date for c in get_all_skip],
                y=[c.absenteeism for c in get_all_skip],
                labels={'x': 'Дата', 'y':'Колличество отсутствующих'},
                )
            
            last_range = [c.all_people for c in get_all_skip]
            
            fig.update_layout(yaxis_range=[0, min(sorted(last_range))],
                            xaxis_range=[datetime.datetime.today().replace(day=1), datetime.datetime.today().replace(day=1) + datetime.timedelta(days=calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])],
                            paper_bgcolor='rgba(0,0,0,0)',
                            height=430,
                            )
            chart_skip = fig.to_html()
        
            form = self.form_truancy(initial=self.initial)
            # date_form = self.form_date(initial=self.initial)
            return render(request, self.template_name, {'form': form,
                                                        'chart': chart_skip}) 
        else:    
            form = self.form_truancy(initial=self.initial)
            # date_form = self.form_date(initial=self.initial)
            return render(request, self.template_name, {'form': form})
            
    
    def post(self, request, *args, **kwargs):        
        # data = {
        #     'form': form,
        #     'error': error,
        # }
        
        if request.method == "POST":
            form = self.form_truancy(request.POST or None)
            
            if form.is_valid():
                
                truancy = form.save(commit=False)

                truancy.group = request.user
                truancy.num_hours = int((float(form.data.get('num_pairs')) * 2)) * float(form.data.get('absenteeism'))
                truancy.percent = float(float(form.data.get('absenteeism')) / (float(form.data.get('all_people'))) * 100)

                truancy.save()
                # print(post)
                
                # print(form.data)
                
                return redirect('/')

            else:
                form = self.form_truancy()

        return render(request, self.template_name, {'form': form})
    
    

class ExportExcel(LoginRequiredMixin, TemplateView):
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    login_url = reverse_lazy('login')
    template_name = 'admin.html'
    
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{str(datetime.datetime.today())}.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        first_month = Truancy.objects.first().date.month
        
        last_month = Truancy.objects.last().date.month
        

        for num_month in range(first_month, last_month + 1):
            ws = wb.add_sheet(calendar.month_name[num_month])
            col_i = 1
            row_num = 0
            
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            
            period = pd.period_range(start=f'{datetime.datetime.today().year}.{num_month}.01', end=f'{str(datetime.datetime.today().year)}.{str(num_month)}.{calendar.monthrange(datetime.datetime.today().year, num_month)[1]}', freq='D')
            
            columns_list = ['Группа']
            
            for x in period:
                columns_list.append(str(x))
                columns_list.append("%")

                
            for col_num in range(len(columns_list)):
                ws.write(row_num, col_num, columns_list[col_num], font_style)

            font_style = xlwt.XFStyle()
            # rows = Truancy.objects.filter().values_list('date')
            groups = User.objects.filter(is_staff=False) #Truancy.objects.order_by('group').distinct('group') rows = Truancy.objects.filter().values_list('group')
            # .filter(date__gte=f'{datetime.datetime.strptime(str(datetime.datetime.today().year) + {num_month} + "01", "%Y%m%d")}').filter(date__lte=f'{datetime.datetime.strptime(str(datetime.datetime.today().year) + {num_month} + calendar.monthrange(datetime.datetime.today().year, {num_month}), "%Y%m%d")}')            
            for row in range(len(groups)):
                row_num += 1
                
                col_i = 1
                for col in columns_list:
                    if col == "Группа" or col == "%":
                        continue
                    column = Truancy.objects.filter(group=groups[row], date=col).values_list('absenteeism', 'percent')
                    if column:
                        ws.write(row_num, col_i, str(column[0][0]))
                        col_i += 1
                        ws.write(row_num, col_i, str(column[0][1]))
                        col_i += 1
                    else:
                        ws.write(row_num, col_i, "Нет данных")
                        col_i += 1
                        ws.write(row_num, col_i, "Нет данных")
                        col_i += 1
                    
                
                ws.write(row_num, 0, str(groups[row]), font_style)
                
                    
        wb.save(response)
        
        return response

    
def logout_user(request):
    logout(request)
    return redirect('login')