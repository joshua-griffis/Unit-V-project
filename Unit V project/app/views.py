from django.shortcuts import render, redirect
from app.forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import auth_user, customer_only, hunter_only
from .models import *

# Create your views here.
@auth_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            choice = request.POST.get('choice')

            if choice == 'Customer':
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
            elif choice == 'Bounty Hunter':
                group = Group.objects.get(name='Hunter')
                user.groups.add(group)
                bounty_hunter = Hunter.objects.create(
                    user = user,
                    total_money = 0
                )
                bounty_hunter.save()
            return redirect('login')
        else: 
            print(form.errors)
           
    context = {'form':form}
    return render(request, 'register.html', context)

@auth_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username OR password is incorrect.")
    context={}
    return render(request, 'login.html', context)

@login_required(login_url='login')
@customer_only
def homePage(request):
    context = {}
    return render(request, 'base.html', context)

@login_required(login_url='login')
@customer_only
def create_bounty(request):
    form = CreateBountyPostForm()
    if request.method == 'POST':
        form = CreateBountyPostForm(request.POST)
        if form.is_valid():
            target_name = form.cleaned_data["target_name"]
            description = form.cleaned_data["description"]
            bounty = form.cleaned_data["bounty"]
            dead_or_alive = form.cleaned_data["dead_or_alive"]
            creating(request.user, target_name, description, bounty, dead_or_alive, False)
            content = {}
            messages.info(request, f"Bounty for {target_name} was created.")
            return redirect('create_bounty')
    content = {'form':form}
    return render(request, "create_bounty.html", content)

@login_required(login_url='login')
@customer_only
def viewCreated(request):
    your_post = BountyPost.objects.filter(user = request.user)
    joe = []
    for post in your_post:
        if post.completed == False:
            joe.append(post)
    context = {'posts':joe}
    return render(request, 'view.html', context)

@login_required(login_url='login')
@customer_only
def editBounty(request, id):
    bounty = BountyPost.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name9')
        bounty1 = request.POST.get('bounty9')
        d_or_a = request.POST.get('pref9')
        des = request.POST.get('des9')
        bounty.target_name = name
        bounty.bounty = bounty1
        bounty.dead_or_alive = d_or_a
        bounty.description = des
        bounty.save()
        return redirect('view')
    context= {'form':bounty}
    return render(request, 'edit.html', context)

@login_required(login_url='login')
@customer_only
def deleteBounty(request, id):
    BountyPost.objects.get(id=id).delete()
    return redirect('view')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@hunter_only
def hunter_homePage(request):
    hunter = Hunter.objects.get(user=request.user)
    context = {'money':hunter.total_money, 'hunter': hunter}
    return render(request, 'hunter_base.html', context)

@login_required(login_url='login')
@hunter_only
def view_allpage(request):
    all_posts = BountyPost.objects.filter(completed = False)
    current_hunter = Hunter.objects.get(user=request.user)
    bounties = current_hunter.bountiesaccepted.all()
    posts = []
    for post in all_posts:
        if post not in bounties:
            posts.append(post)
    context = {'posts':posts, 'money':current_hunter.total_money}
    return render(request, 'hunter_view.html', context)

def addPage(request, id):
    current_hunter = Hunter.objects.get(user=request.user)
    BountyPost.objects.get(id=id).accept_bounty.add(current_hunter)
    return redirect('view_all')

def removePage(request, id):
    current_hunter = Hunter.objects.get(user=request.user)
    BountyPost.objects.get(id=id).accept_bounty.remove(current_hunter)
    return redirect('view_all')

def completePage(request, id):
    current_bounty = BountyPost.objects.get(id=id)
    current_bounty.completed = True
    current_bounty.save()
    current_hunter = Hunter.objects.get(user=request.user)
    print(current_hunter.total_money)
    print(current_bounty.bounty)
    current_hunter.total_money += current_bounty.bounty
    current_hunter.save()
    return redirect('view_all')


def viewAccepted(request):
    current_hunter = Hunter.objects.get(user=request.user)
    bounties = current_hunter.bountiesaccepted.all()
    context = {'posts':bounties.filter(completed=False), 'money':current_hunter.total_money}
    return render(request, 'accepted.html', context)

def viewCustomerComplete(request):
    current_bounty = BountyPost.objects.filter(user=request.user)
    list_completed = []
    for bounty in current_bounty:
        if bounty.completed == True:
            list_completed.append(bounty)
    return render(request, 'customer_completed.html', {'posts':list_completed})

