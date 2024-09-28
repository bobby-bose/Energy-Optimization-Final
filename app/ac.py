from .models import AirConditioner
from django.shortcuts import render, redirect

def ac(request):
    if request.method == 'POST':
        # Get the duration, wattage, and quantity from the form
        duration = request.POST.get('duration')
        wattage = request.POST.get('wattage')
        quantity = request.POST.get('quantity')

        # Extract consumption data for each month from the request
        energy_january = request.POST.get('energy_Jan')
        energy_february = request.POST.get('energy_Feb')
        energy_march = request.POST.get('energy_Mar')
        energy_april = request.POST.get('energy_Apr')
        energy_may = request.POST.get('energy_May')
        energy_june = request.POST.get('energy_Jun')
        energy_july = request.POST.get('energy_Jul')
        energy_august = request.POST.get('energy_Aug')
        energy_september = request.POST.get('energy_Sep')
        energy_october = request.POST.get('energy_Oct')
        energy_november = request.POST.get('energy_Nov')
        energy_december = request.POST.get('energy_Dec')


        print(energy_january, energy_february, energy_march, energy_april, energy_may, energy_june, energy_july, energy_august, energy_september, energy_october, energy_november, energy_december)
        # Create a list of consumption data

        total=sum([int(energy_january), int(energy_february), int(energy_march), int(energy_april), int(energy_may), int(energy_june), int(energy_july), int(energy_august), int(energy_september), int(energy_october), int(energy_november), int(energy_december)])
        print(total)

        # Save data to AirConditioner model
        ac_instance = AirConditioner.objects.create(
            duration=duration,
            wattage=wattage,
            quantity=quantity
        )

        # Calculate total energy consumption
        context= {
            'total': total,
            'duration': duration,
            'wattage': wattage,
            'quantity': quantity,
            'energy_january': energy_january,
            'energy_february': energy_february,
            'energy_march': energy_march,
            'energy_april': energy_april,
            'energy_may': energy_may,
            'energy_june': energy_june,
            'energy_july': energy_july,
            'energy_august': energy_august,
            'energy_september': energy_september,
            'energy_october': energy_october,
            'energy_november': energy_november,
            'energy_december': energy_december

        }

        return render(request, 'ac_results.html', context)

    # For GET requests or any other method, render the 'ac' template
    return render(request, 'ac.html')
