from flask import Flask, render_template, request, redirect, url_for, session
from math import ceil

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# Home page - Solar principles
@app.route('/')
def home():
    return render_template('solar.html')

# Add loads page
@app.route('/add_load', methods=['GET', 'POST'])
def add_load():
    if 'loads' not in session:
        session['loads'] = []
    
    if request.method == 'POST':
        new_load = {
            'name': request.form['name'],
            'devices': request.form['devices'],
            'power': float(request.form['power']),
            'day_hours': float(request.form['day_hours']),
            'night_hours': float(request.form['night_hours'])
            ##print ('night_hours')
            ##print (night_hours)
        }
        print ('new_load')
        print (new_load)
        session['loads'] = session['loads'] + [new_load]
        session.modified = True
        return redirect(url_for('add_load'))
    
    return render_template('add_load.html', loads=session['loads'])



# Delete load page

# Delete load page
@app.route('/delete_load/<int:load_index>')
def delete_load(load_index):
    if 'loads' in session and 0 <= load_index < len(session['loads']):
        session['loads'].pop(load_index)
        session.modified = True
    
    return redirect(url_for('add_load'))
    
   
# Update load page
@app.route('/update_load/<int:load_index>', methods=['GET', 'POST'])
def update_load(load_index):
    if 'loads' not in session or load_index >= len(session['loads']):
        return redirect(url_for('add_load'))

    if request.method == 'POST':
        # Update the existing load
        updated_load = {
            'name': request.form['name'],
            'devices': request.form['devices'],
            'power': float(request.form['power']),
            'day_hours': float(request.form['day_hours']),
            'night_hours': float(request.form['night_hours'])
        }
        session['loads'][load_index] = updated_load
        session.modified = True
        return redirect(url_for('add_load'))

    # GET request - show the form with current values
    load_to_edit = session['loads'][load_index]
    return render_template('update_load.html', load=load_to_edit, load_index=load_index)









# Calculate panels page
@app.route('/calculate_panels', methods=['GET', 'POST'])
def calculate_panels():
    # calculate the 1.2 loss
    loss = 1.2 

    total_energy = sum(
        #load['power'] * (load['day_hours'] + load['night_hours'])
        #load['power'] * (load['day_hours'])
        #powerLoss = load['power'] * loss
        #print ('powerLoss')
        #print (powerLoss)
        
        #power1 = load['power'] * 1.2
        load['power'] * (load['day_hours'] )
        for load in session.get('loads', [])
    )

    # now we add the loss 1.2

    total_energy = total_energy * 1.2
    print ('total_energy')
    print (total_energy)



    energy_night = sum(
        #load['power'] * + load['night_hours']
        load['power'] * load['night_hours']
        for load in session.get('loads', [])
    )
   
    print ('energy_night')
    print (energy_night)

    # now we add the loss 1.2 to energy_night
    energy_night = energy_night * 1.2
    print ('energy_night')
    print (energy_night)  

    
    if request.method == 'POST':
        panel_wattage = float(request.form['panel_wattage'])
        sun_hours = float(request.form['sun_hours'])
        panels_needed = ceil(total_energy / (panel_wattage * sun_hours))
        print ('energy_night')
        print (energy_night)
        ##total_energy_night = 11111

        return render_template('panels.html', 
                              total_energy=total_energy,
                              energy_night=energy_night,
                              result=panels_needed,
                              panel_wattage=panel_wattage,
                              sun_hours=sun_hours)
    
    return render_template('panels.html', total_energy=total_energy)

# Calculate batteries page
@app.route('/calculate_batteries', methods=['GET', 'POST'])
def calculate_batteries():
    night_energy = sum(
        load['power'] * load['night_hours']
        for load in session.get('loads', [])
    )
    
    if request.method == 'POST':
        battery_voltage = float(request.form['battery_voltage'])
        dod = float(request.form['dod'])
        battery_capacity = float(request.form['battery_capacity'])
        
        ah_needed = night_energy / (battery_voltage * dod)
        batteries_needed = ceil(ah_needed / battery_capacity)
        
        return render_template('batteries.html',
                              night_energy=night_energy,
                              result=batteries_needed,
                              battery_voltage=battery_voltage,
                              dod=dod,
                              battery_capacity=battery_capacity)
    
    return render_template('batteries.html', night_energy=night_energy)



@app.route('/delete')
def delete():
    return render_template('delete.html', loads, load)


@app.route('/calculate_inverter', methods=['GET', 'POST'])
def calculate_inverter():
    if request.method == 'POST':
        safety_factor = float(request.form['safety_factor'])

        # Calculate total peak power and handle inductive loads
        peak_power = 0
        for load in session.get('loads', []):
            # Assume inductive loads need 3x surge power
            if load.get('load_type', 'resistive') == 'inductive':
                peak_power += load['power'] * 3
            else:
                peak_power += load['power']

        inverter_size = peak_power * (1 + safety_factor/100)
        return render_template('inverter.html',
                             peak_power=peak_power,
                             inverter_size=inverter_size,
                             safety_factor=safety_factor)
    
    return render_template('inverter.html')


@app.route('/contoller')
def controller():
    return render_template('controller.html')

@app.route('/calculate_controller', methods=['GET', 'POST'])
def calculate_controller():

    '''

    if request.method == 'POST':
        #safety_factor = float(request.form['safety_factor'])
        
        # Calculate total peak power and handle inductive loads
        peak_power = 0
        for load in session.get('loads', []):
            # Assume inductive loads need 3x surge power
            if load.get('load_type', 'resistive') == 'inductive':
                peak_power += load['power'] * 3
            else:
                peak_power += load['power']
        
        inverter_size = peak_power * (1 + safety_factor/100)
        return render_template('inverter.html',
                             peak_power=peak_power,
                             inverter_size=inverter_size,
                             safety_factor=safety_factor)
    '''
    return render_template('controller.html')







if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
