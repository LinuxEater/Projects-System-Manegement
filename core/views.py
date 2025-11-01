from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Client
from .forms import ProjectForm, ClientForm
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from collections import defaultdict
import json
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    projects = Project.objects.all().order_by('-start_date')
    search_query = request.GET.get('search_query', '')
    filter_param = request.GET.get('filter', '')

    if request.user.is_authenticated and hasattr(request.user, 'client_profile'):
        # If the logged-in user is a client, show only their projects
        projects = projects.filter(client=request.user.client_profile)
    
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(client__name__icontains=search_query)
        )

    if filter_param:
        today = datetime.today().date()
        if filter_param == 'week':
            start_week = today - timedelta(days=today.weekday())
            projects = projects.filter(start_date__gte=start_week)
        elif filter_param == 'month':
            projects = projects.filter(start_date__year=today.year, start_date__month=today.month)

    context = {
        'projects': projects,
        'search_query': search_query,
    }
    return render(request, 'core/home.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Ensure client can only see their own projects
    if request.user.is_authenticated and hasattr(request.user, 'client_profile'):
        if project.client != request.user.client_profile:
            return redirect('home') # Redirect if not their project
    return render(request, 'core/project_detail.html', {'project': project})

def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Ensure client can only edit their own projects
    if request.user.is_authenticated and hasattr(request.user, 'client_profile'):
        if project.client != request.user.client_profile:
            return redirect('home') # Redirect if not their project
    return render(request, 'core/project_edit.html', {'form': form, 'project': project})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'core/project_create.html', {'form': form})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'core/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            return redirect('client_list') # Redirect to client list after creation
    else:
        form = ClientForm()
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Add New Client'})

def client_edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list') # Redirect to client list after edit
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Edit Client'})

def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'core/client_confirm_delete.html', {'client': client})

def client_projects(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    projects = Project.objects.filter(client=client).order_by('-start_date')
    context = {
        'projects': projects,
        'client': client, # Pass the client object to the template
        'search_query': '', # Clear search for this view
    }
    return render(request, 'core/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def dashboard(request):
    filter_param = request.GET.get('filter', '')
    
    projects_qs = Project.objects.all()
    completed_projects_qs = Project.objects.filter(status='C')

    today = datetime.today().date()
    if filter_param == 'week':
        start_week = today - timedelta(days=today.weekday())
        completed_projects_qs = completed_projects_qs.filter(end_date__gte=start_week)
        projects_qs = projects_qs.filter(start_date__gte=start_week)
    elif filter_param == 'month':
        completed_projects_qs = completed_projects_qs.filter(end_date__year=today.year, end_date__month=today.month)
        projects_qs = projects_qs.filter(start_date__year=today.year, start_date__month=today.month)

    # KPIs
    total_revenue = completed_projects_qs.aggregate(Sum('value'))['value__sum'] or Decimal('0.00')
    total_completed_projects = completed_projects_qs.count()
    in_progress_projects = projects_qs.filter(status='I').count()
    pending_projects = projects_qs.filter(status='P').count()

    # Monthly earnings
    monthly_earnings = defaultdict(Decimal)
    for project in completed_projects_qs.filter(end_date__isnull=False):
        month = project.end_date.strftime('%Y-%m')
        monthly_earnings[month] += project.value
    
    sorted_monthly_earnings = sorted(monthly_earnings.items())
    
    # Chart 1: Monthly Earnings
    monthly_chart_labels = [item[0] for item in sorted_monthly_earnings]
    monthly_chart_data = [float(item[1]) for item in sorted_monthly_earnings]

    # Chart 2: Earnings per project
    projects_by_value = completed_projects_qs.order_by('-value')[:10] # Top 10 projects
    per_project_chart_labels = [p.title for p in projects_by_value]
    per_project_chart_data = [float(p.value) for p in projects_by_value]

    # Chart 3: Project Status Distribution
    status_counts = projects_qs.values('status').annotate(count=Count('status'))
    status_map = dict(Project.STATUS_CHOICES)
    status_chart_labels = [status_map.get(s['status'], 'Unknown') for s in status_counts]
    status_chart_data = [s['count'] for s in status_counts]

    context = {
        'total_revenue': total_revenue,
        'total_completed_projects': total_completed_projects,
        'in_progress_projects': in_progress_projects,
        'pending_projects': pending_projects,
        'monthly_chart_labels': json.dumps(monthly_chart_labels),
        'monthly_chart_data': json.dumps(monthly_chart_data),
        'per_project_chart_labels': json.dumps(per_project_chart_labels),
        'per_project_chart_data': json.dumps(per_project_chart_data),
        'status_chart_labels': json.dumps(status_chart_labels),
        'status_chart_data': json.dumps(status_chart_data),
    }
    return render(request, 'core/dashboard.html', context)

def generate_pdf(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    textob.textLine(f"Project: {project.title}")
    textob.textLine(" ")
    textob.textLine(f"Client: {project.client.name}")
    textob.textLine(f"Email: {project.client.email}")
    textob.textLine(f"Phone: {project.client.phone}")
    if project.client.contact_number:
        textob.textLine(f"Contact Number: {project.client.contact_number}")
    textob.textLine(" ")
    textob.textLine(f"Description: {project.description}")
    textob.textLine(" ")
    textob.textLine(f"Status: {project.get_status_display()}")
    textob.textLine(f"Start Date: {project.start_date}")
    if project.end_date:
        textob.textLine(f"End Date: {project.end_date}")
    textob.textLine(f"Value: R$ {project.value}")
    if project.observations:
        textob.textLine(" ")
        textob.textLine(f"Observations: {project.observations}")

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'{project.title}.pdf')