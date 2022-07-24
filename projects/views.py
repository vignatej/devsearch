from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project, Review,Tag
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProject,paginateProjects
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages
# Create your views here.
def projects(request):
    search_query,projects = searchProject(request)
    custom_range, projects=paginateProjects(request,projects,6)
    context={'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectobj=Project.objects.get(id=pk)
    form=ReviewForm()

    if request.method=='POST':
        form = ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=projectobj
        review.owner=request.user.profile
        review.save()
        projectobj.getVoteCount

        messages.success(request,"your review was sucessfully submitted")
        return redirect('project', pk=projectobj.id )
    return render(request,'projects/single-project.html',{'project':projectobj,'form':form})

@login_required(login_url='login')   
def createproject(request):
    profile=request.user.profile
    form=ProjectForm()

    if request.method=='POST':
        newtags=request.POST.get('newtags').replace(","," ").split()
        form=ProjectForm(request.POST,request.FILES)  
        if form.is_valid:
            project = form.save(commit=False)
            project.owner=profile
            project.save()
            for tag in newtags:
                tagg,created=Tag.objects.get_or_create(name=tag)
                project.tag.add(tagg)
            return redirect('account')

    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')   
def updateproject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method=='POST':
        newtags=request.POST.get('newtags').replace(","," ").split()

        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid:
            form.save()
            for tag in newtags:
                tagg,created=Tag.objects.get_or_create(name=tag)
                project.tag.add(tagg)
            return redirect('account')

    context={'form':form,'project':project}
    return render(request,'projects/project_form.html',context)


@login_required(login_url='login')   
def deleteProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)  
    if request.method=='POST':
        project.delete()
        return redirect('projects')
    context={'object':project}
    return render(request,'delete_template.html',context)