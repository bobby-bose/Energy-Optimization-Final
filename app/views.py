import json
from decimal import Decimal
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile

def custom_logout(request):
    logout(request)
    return redirect('login')


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        # Print the submitted username and password
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print("Submitted username:", username)
        print("Submitted password:", password)

        # Call parent form_valid method to perform default authentication
        response = super().form_valid(form)

        # Check if user is authenticated
        if self.request.user.is_authenticated:
            print("User authenticated successfully")
        else:
            print("Authentication failed")

        return response



def register(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check if the user with the provided email already exists
            if User.objects.filter(email=email).exists():
                print("User with this email already exists")
                return HttpResponse('User with this email already exists')

            # Create and save the new user
            user = User.objects.create_user(username=name, email=email, password=password)
            print("User created successfully")

            # Print list of all users
            all_users = User.objects.all()
            print("List of all users:")
            for user in all_users:
                print(f"Username: {user.username}, Email: {user.email}")

            # Authenticate and login the user

            print("User authenticated and logged in successfully")
            return redirect('home')

        else:
            print("Password does not match")
            return HttpResponse('Password does not match')
    else:
        return render(request, 'register.html')



def home(request):
    bedroom_appliances = BedroomAppliance.objects.all()
    scatter_data = [(appliance.wattage, appliance.quantity) for appliance in bedroom_appliances]

    scatter_data_json = json.dumps({'scatter_data': scatter_data})
    print(scatter_data_json)
    context = {'scatter_data_json': scatter_data_json}
    return render(request, 'home.html', context)




def contact(request):
    return render(request, 'contact.html')

def calculate_carbon_footprint(request):
    if request.method == 'POST':
        print("POST request received")
        fan_usage_hours = int(request.POST['fan_usage_hours']) if 'fan_usage_hours' in request.POST else 0
        light_bulb_usage_hours = int(
            request.POST['light_bulb_usage_hours']) if 'light_bulb_usage_hours' in request.POST else 0
        refrigerator_usage_hours = int(
            request.POST['refrigerator_usage_hours']) if 'refrigerator_usage_hours' in request.POST else 0
        tv_usage_hours = int(request.POST['tv_usage_hours']) if 'tv_usage_hours' in request.POST else 0

        appliance_carbon_footprints = {
            'fan': 0.02,
            'light_bulb': 0.01,
            'refrigerator': 0.5,
            'tv': 0.3,
        }
        total_carbon_footprint = {
            'fan': fan_usage_hours * appliance_carbon_footprints['fan'],
            'light_bulb': light_bulb_usage_hours * appliance_carbon_footprints['light_bulb'],
            'refrigerator': refrigerator_usage_hours * appliance_carbon_footprints['refrigerator'],
            'tv': tv_usage_hours * appliance_carbon_footprints['tv'],
        }
        print("Total carbon footprint: ", total_carbon_footprint)
        return render(request, 'footprintingresult.html', {'total_carbon_footprint': total_carbon_footprint})
    else:
        return render(request, 'carbonfootprinting.html')


def add_appliance(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        type = request.POST.get('type')
        usage_per_hour = request.POST.get('usage_per_hour')
        power_rating = request.POST.get('power_rating')
        quantity = request.POST.get('quantity')
        hours = request.POST.get('hours')
        days = request.POST.get('days')
        months = request.POST.get('months')
        years = request.POST.get('years')
        # Create and save the Appliance object
        Appliance.objects.create(
            name=name,
            type=type,
            usage_per_hour=usage_per_hour,
            power_rating=power_rating,
            quantity=quantity,
            hours=hours,
            days=days,
            months=months,
            years=years
        )
        return redirect('success')
    return render(request, 'add_appliances.html')

def serve_graph(request):
    # Query the database to get data for each room
    rooms = ['Room 1', 'Room 2', 'Room 3']  # Example room names
    room_data = {}
    for room in rooms:
        appliances_in_room = Appliance.objects.filter(room=room)  # Adjust this based on your model structure
        total_usage = sum(appliance.usage for appliance in appliances_in_room)
        appliance_percentages = [appliance.usage / total_usage * 100 for appliance in appliances_in_room]
        room_data[room] = appliance_percentages
    return render(request, 'applianceslineargraph.html', {'room_data': room_data})

def profile(request):
    return render(request, 'profile.html')

def submit_profile(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        middlename = request.POST['middlename']
        mobilenumber = request.POST['mobile']
        countrycode = request.POST['countrycode']
        city = request.POST['city']
        district = request.POST['district']
        state = request.POST.get('state', '')  # Handle if 'state' is not submitted
        secondaryaddress = request.POST['secondaryaddress']
        profile_picture = request.FILES.get('pic')

        user_profile =UserProfile.objects.create(
            first_name=firstname,
            last_name=lastname,
            middle_name=middlename,
            mobile_number=mobilenumber,
            country_code=countrycode,
            city=city,
            district=district,
            state=state,
            secondary_address=secondaryaddress,
            profile_picture=profile_picture

        )
        return redirect('success', pk=user_profile.pk) # Create success.html template for success message
    return render(request, 'profile.html')






def edit_profile(request):
    # Since this view is decorated with @login_required, you don't need to check if the user is authenticated.
    # If the view is accessed, the user is authenticated.

    user_profile = UserProfile.objects.get(id=1)

    if request.method == 'POST':
        # Update user profile details
        user_profile.first_name = request.POST['firstname']
        user_profile.last_name = request.POST['lastname']
        user_profile.middle_name = request.POST['middlename']
        user_profile.mobile_number = request.POST['mobile']
        user_profile.country_code = request.POST['countrycode']
        user_profile.city = request.POST['city']
        user_profile.district = request.POST['district']
        user_profile.state = request.POST.get('state', '')
        user_profile.secondary_address = request.POST['secondaryaddress']

        # Check if a new profile picture is uploaded


        user_profile.save()
        return redirect('success', pk=user_profile.pk)  # Redirect to success page

    return render(request, 'edit_profile.html', {'user_profile': user_profile})


def success(request, pk):
    user_profile = UserProfile.objects.get(pk=pk)
    return render(request, 'success.html', {'user_profile': user_profile})

def optimized_graphs(request):
    return render(request, 'optimized_graphs.html')

def appliance_add(request):
    return render(request, 'add_appliances.html')

def appliance_list(request):
    obj=Appliance.objects.all()
    return render(request, 'list_appliances.html', {'obj': obj})

# ================================================
# =============================================================
# ===========================================================


def bathroom_create(request):
    if request.method == 'POST':
        form = BathroomApplianceForm(request.POST)
        if form.is_valid():
            bathroom_appliance = form.save(commit=False)
            bathroom_appliance.user = request.user.profile.user
            print(bathroom_appliance.user)
            bathroom_appliance.save()
            return redirect('bathroom_list')
    else:
        form = BathroomApplianceForm()
    return render(request, 'bathroom_create.html', {'form': form})
def bathroom_delete(request, bathroom_id):
    bathroom = get_object_or_404(BathroomAppliance, id=bathroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('bathroom_list')  # Redirect to the list view after deletion
    return render(request, 'bathroom_list.html', {'bathroom': bathroom,'bathroom_id':bathroom_id})
def bedroom_delete(request, bedroom_id):
    bathroom = get_object_or_404(BedroomAppliance, id=bedroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('bedroom_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'bedroom_list.html', {'bathroom': bathroom,'bedroom_id':bedroom_id})
def dininghall_delete(request, dininghall_id):
    bathroom = get_object_or_404(DininghallAppliance, id=dininghall_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('dininghall_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'dininghall_list.html', {'bathroom': bathroom,'dinignhall_id':dininghall_id})
def kitchen_delete(request, kitchen_id):
    bathroom = get_object_or_404(KitchenAppliance, id=kitchen_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('kitchen_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'kitchen_list.html', {'bathroom': bathroom,'kitchen_id':kitchen_id})

def livingroom_delete(request, livingroom_id):
    bathroom = get_object_or_404(LivingroomAppliance, id=livingroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('livingroom_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'livingroom_list.html', {'bathroom': bathroom,'livingroom_id':livingroom_id})





@login_required
def kitchen_appliance_create(request):
    if request.method == 'POST':
        form = KitchenApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kitchen_appliance_list')  # Redirect to a success URL
    else:
        form = KitchenApplianceForm()
    return render(request, 'kitchen_appliance_form.html', {'form': form})
@login_required
def kitchen_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    kitchen_appliances = KitchenAppliance.objects.all()
    return render(request, 'kitchen_list.html', {'kitchen_appliances': kitchen_appliances})
@login_required
def bedroom_appliance_create(request):
    if request.method == 'POST':
        form = BedroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bedroom_appliance_list')  # Redirect to a success URL
    else:
        form = BedroomApplianceForm()
    return render(request, 'bedroom_appliance.html', {'form': form})

@login_required
def bathroom_list(request):
    appliances = BathroomAppliance.objects.all()
    return render(request, 'bathroom_list.html', {'appliances': appliances})
def bathroom_create(request):
    if request.method == 'POST':
        form = BathroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bathroom_list')
    else:
        form = BathroomApplianceForm()
    return render(request, 'bathroom_create.html', {'form': form})


def bathroom_delete(request, bathroom_id):
    bathroom = get_object_or_404(BathroomAppliance, pk=bathroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('bathroom_list')  # Redirect to the list view after deletion
    return render(request, 'bathroom_list.html')


def bedroom_delete(request, bedroom_id):
    bathroom = get_object_or_404(BedroomAppliance, id=bedroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('bedroom_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'bedroom_list.html', {'bathroom': bathroom, 'bedroom_id': bedroom_id})


def dininghall_delete(request, dininghall_id):
    bathroom = get_object_or_404(DininghallAppliance, id=dininghall_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('dininghall_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'dininghall_list.html', {'bathroom': bathroom, 'dinignhall_id': dininghall_id})


def kitchen_delete(request, kitchen_id):
    bathroom = get_object_or_404(KitchenAppliance, id=kitchen_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('kitchen_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'kitchen_list.html', {'bathroom': bathroom, 'kitchen_id': kitchen_id})


def bathroom_delete(request, bathroom_id):
    print("1")
    bathroom = get_object_or_404(BathroomAppliance, id=bathroom_id)
    print("2")
    if request.method == 'POST':
        print("3")
        bathroom.delete()

        return redirect('bathroom_list')  # Redirect to the list view after deletion
    return render(request, 'bathroom_list.html', {'bathroom': bathroom})


def livingroom_delete(request, livingroom_id):
    bathroom = get_object_or_404(LivingroomAppliance, id=livingroom_id)
    if request.method == 'POST':
        bathroom.delete()
        return redirect('livingroom_appliance_list')  # Redirect to the list view after deletion
    return render(request, 'livingroom_list.html', {'bathroom': bathroom, 'livingroom_id': livingroom_id})


@login_required
def kitchen_appliance_create(request):
    if request.method == 'POST':
        form = KitchenApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kitchen_appliance_list')  # Redirect to a success URL
    else:
        form = KitchenApplianceForm()
    return render(request, 'kitchen_appliance_form.html', {'form': form})


@login_required
def kitchen_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    kitchen_appliances = KitchenAppliance.objects.all()
    return render(request, 'kitchen_list.html', {'kitchen_appliances': kitchen_appliances})


@login_required
def bedroom_appliance_create(request):
    if request.method == 'POST':
        form = BedroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bedroom_appliance_list')  # Redirect to a success URL
    else:
        form = BedroomApplianceForm()
        obj=BedroomAppliance.objects.all()
        for i in obj:
            print(i)
        print("test")
    return render(request, 'bedroom.html', {'form': form})


@login_required
def bedroom_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    bedroom_appliances = BedroomAppliance.objects.all()

    return render(request, 'bedroom_list.html', {'bedroom_appliances': bedroom_appliances})






@login_required
def livingroom_appliance(request):
    if request.method == 'POST':
        form = LivingroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livingroom_appliance_list')  # Redirect to a success URL
    else:
        form = LivingroomApplianceForm()
    return render(request, 'livingroom_appliance.html', {'form': form})


@login_required
def livingroom_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    livingroom_appliances = LivingroomAppliance.objects.all()
    return render(request, 'livingroom_list.html', {'livingroom_appliances': livingroom_appliances})


@login_required
def bathroom_list(request):
    appliances = BathroomAppliance.objects.all()
    return render(request, 'bathroom_list.html', {'appliances': appliances})

@login_required
def calculate_energy_consumption(request):
    appliances = BathroomAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint
    rate_per_kwh = Decimal('2')
    carbon_emissions_per_kwh = Decimal('0.5')  # Assume carbon emissions factor of 0.5 kgCO2/kWh

    for appliance in appliances:
        total_energy_consumption = 0
        total_carbon_for_appliance = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        total_carbon_for_appliance = total_energy_consumption * carbon_emissions_per_kwh
        total_carbon_footprint += total_carbon_for_appliance

        # Add current appliance's energy consumption and carbon footprint details to energy_results list
        energy_results.append({
            'appliance': appliance,
            'energy_consumption': energy_consumption,
            'total_energy_consumption': total_energy_consumption,
            'total_carbon_footprint': total_carbon_for_appliance
        })

        # Update total energy sum
        total_energy_sum += total_energy_consumption

    # Calculate payment amount
    payment_amount = total_energy_sum * rate_per_kwh
    return render(request, 'energy_consumption_result.html', {
        'energy_results': energy_results,
        'total_energy_sum': total_energy_sum,
        'payment_amount': payment_amount,
        'total_carbon_footprint': total_carbon_footprint
    })

@login_required
def calculate_energy_consumption1(request):
    appliances = KitchenAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    rate_per_kwh = Decimal('2')
    carbon_footprint_per_kwh = Decimal('0.5')  # Carbon footprint per kWh

    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint

    for appliance in appliances:
        total_energy_consumption = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        appliance_carbon_footprint = total_energy_consumption * carbon_footprint_per_kwh

        # Add current appliance's carbon footprint to the total
        total_carbon_footprint += appliance_carbon_footprint

        energy_results.append({
            'appliance': appliance,
            'energy_consumption': energy_consumption,
            'total_energy_consumption': total_energy_consumption,
            'carbon_footprint': appliance_carbon_footprint  # Include carbon footprint for each appliance
        })

        total_energy_sum += total_energy_consumption  # Add current appliance's energy consumption to the total sum
        payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result1.html', {
        'energy_results': energy_results,
        'total_energy_sum': total_energy_sum,
        'payment_amount': payment_amount,
        'total_carbon_footprint': total_carbon_footprint  # Pass total carbon footprint to the template
    })

@login_required
def calculate_energy_consumption2(request):
    appliances = BedroomAppliance.objects.all()
    energy_results = []
    total_energy_sum = Decimal('0')  # Initialize total energy sum as a Decimal
    rate_per_kwh = Decimal('2')
    carbon_footprint_per_kwh = Decimal('0.5')  # Carbon footprint per kWh

    total_carbon_footprint = Decimal('0')  # Initialize total carbon footprint

    for appliance in appliances:
        total_energy_consumption = 0
        energy_consumption = {}
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for month in months:
            usage_hours = getattr(appliance, month)
            energy_consumption[month] = appliance.wattage * usage_hours / 1000
            total_energy_consumption += energy_consumption[month]

        # Calculate carbon footprint for the current appliance
        appliance_carbon_footprint = total_energy_consumption * carbon_footprint_per_kwh

        # Add current appliance's carbon footprint to the total
        total_carbon_footprint += appliance_carbon_footprint

        energy_results.append({'appliance': appliance, 'energy_consumption': energy_consumption,
                               'total_energy_consumption': total_energy_consumption,
                               'carbon_footprint': appliance_carbon_footprint})
        total_energy_sum += total_energy_consumption  # Add current appliance's energy consumption to the total sum
        payment_amount = total_energy_sum * rate_per_kwh

    return render(request, 'energy_consumption_result2.html',
                  {'energy_results': energy_results, 'total_energy_sum': total_energy_sum,
                   'payment_amount': payment_amount, 'total_carbon_footprint': total_carbon_footprint})

def logout_view(request):
    logout(request)
    return redirect('login')



def billings(request):
    return render(request, 'billings.html')



@login_required
def dininghall(request):
    if request.method == 'POST':
        form = DininghallApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dininghall_appliance_list')  # Redirect to a success URL
    else:
        form = DininghallApplianceForm()
    return render(request, 'dininghall.html', {'form': form})

def dininghall_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    dininghall_appliances = DininghallAppliance.objects.all()
    return render(request, 'dininghall_list.html', {'Dining_appliances': dininghall_appliances})


def dining_delete(request, pk):
    # Retrieve the kitchen appliance object
    appliance = get_object_or_404(DininghallAppliance, pk=pk)
    
        # If the form is submitted via POST request, delete the appliance
    appliance.delete()
        # Redirect to a success URL after deletion (you can customize this)
    return redirect('dininghall_appliance_list') 


from django.contrib.auth.models import User

def get_users():
    # Retrieve all users
    users = User.objects.all()
    # Extract usernames
    usernames = [user.username for user in users]
    return usernames

def get_all_details(request):
    all_usernames = get_users()
    print(all_usernames)
    return HttpResponse(all_usernames)


def kitchen_delete(request, pk):
    # Retrieve the kitchen appliance object
    appliance = get_object_or_404(KitchenAppliance, pk=pk)
    
        # If the form is submitted via POST request, delete the appliance
    appliance.delete()
        # Redirect to a success URL after deletion (you can customize this)
    return redirect('kitchen_appliance_list') 



@login_required
def livingroom_appliance(request):
    if request.method == 'POST':
        form = LivingroomApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livingroom_appliance_list')  # Redirect to a success URL
    else:
        form = LivingroomApplianceForm()
    return render(request, 'livingroom_appliance.html', {'form': form})

@login_required
def livingroom_appliance_list(request):
    # Retrieve all kitchen appliances from the database
    livingroom_appliances = LivingroomAppliance.objects.all()
    return render(request, 'livingroom_list.html', {'livingroom_appliances': livingroom_appliances})
