from django.shortcuts import render, redirect
from .models import Donor,BloodRequest
from .forms import DonorForm
from .forms import BloodRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages



def home(request):
    return render(request, 'home.html')

def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DonorForm()
    return render(request, 'register.html', {'form': form})

def search_donor(request):
    donors = None

    if request.GET:
        donors = Donor.objects.all()

        blood_group = request.GET.get('blood_group')
        full_name = request.GET.get('full_name')

        if blood_group:
            donors = donors.filter(blood_group__icontains=blood_group)

        if full_name:
            donors = donors.filter(full_name__icontains=full_name)

    return render(request, 'search.html', {'donors': donors})

@login_required
def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            return redirect('dashboard')
    else:
        form = BloodRequestForm()

    return render(request, 'request_blood.html', {'form': form})

@login_required(login_url='login_user')
def dashboard(request):

    total_donors = Donor.objects.count()
    total_requests = BloodRequest.objects.count()
    pending_requests = BloodRequest.objects.filter(status='Pending')
    approved_requests = BloodRequest.objects.filter(status='Approved')

    context = {
        'total_donors': total_donors,
        'total_requests': total_requests,
        'pending_count': pending_requests.count(),
        'approved_count': approved_requests.count(),
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
    }

    return render(request, 'dashboard.html', context)



def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register_user')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login_user')

    return render(request, 'register_user.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login_user.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login_user')
def approve_request(request, pk):
    if request.method == "POST":
        blood_request = get_object_or_404(BloodRequest, id=pk)
        blood_request.status = "Approved"
        blood_request.save()
    return redirect('dashboard')