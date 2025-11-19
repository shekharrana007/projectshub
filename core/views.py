from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Membership, Comment, StudentProfile
from .forms import ProjectForm, CommentForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q

def project_list(request):
    q = request.GET.get('q', '')
    uni = request.GET.get('university', '')
    projects = Project.objects.all().order_by('-created_at')
    if q:
        projects = projects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(tags__icontains=q))
    if uni:
        projects = projects.filter(university__icontains=uni)
    return render(request, 'core/project_list.html', {'projects': projects, 'q': q, 'uni': uni})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comment_form = CommentForm()
    return render(request, 'core/project_detail.html', {'project': project, 'comment_form': comment_form})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.owner = request.user
            proj.save()
            # owner is also a collaborator
            Membership.objects.get_or_create(user=request.user, project=proj, role='owner')
            return redirect('project_detail', pk=proj.pk)
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form, 'create': True})

@login_required
def project_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.user != proj.owner:
        return redirect('project_detail', pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=proj)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=proj.pk)
    else:
        form = ProjectForm(instance=proj)
    return render(request, 'core/project_form.html', {'form': form, 'create': False})

@login_required
def project_delete(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.user != proj.owner:
        return redirect('project_detail', pk=pk)
    if request.method == 'POST':
        proj.delete()
        return redirect('project_list')
    return render(request, 'core/project_confirm_delete.html', {'project': proj})

@login_required
def project_join(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.user != proj.owner:
        Membership.objects.get_or_create(user=request.user, project=proj)
    return redirect('project_detail', pk=pk)

@login_required
def add_comment(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.project = proj
            c.author = request.user
            c.save()
    return redirect('project_detail', pk=pk)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optional: save university
            uni = form.cleaned_data.get('university')
            if uni:
                profile = StudentProfile.objects.get(user=user)
                profile.university = uni
                profile.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, created = StudentProfile.objects.get_or_create(user=user)
    owned = profile.user.owned_projects.all()
    collaborations = profile.user.collaborations.all()
    return render(request, 'core/profile.html', {'profile': profile, 'owned': owned, 'collaborations': collaborations})

# Create your views here.
