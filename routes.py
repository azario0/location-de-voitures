from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Car, Allocation
from datetime import datetime

@app.route('/')
def dashboard():
    cars = Car.query.all()
    return render_template('dashboard.html', cars=cars)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    past_allocations = [a for a in car.allocations if a.status == "Past"]
    current_allocations = [a for a in car.allocations if a.status == "Current"]
    future_allocations = [a for a in car.allocations if a.status == "Future"]
    return render_template('car_detail.html', car=car, 
                           past_allocations=past_allocations,
                           current_allocations=current_allocations,
                           future_allocations=future_allocations)

@app.route('/car/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        new_car = Car(
            mark=request.form['mark'],
            color=request.form['color'],
            class_type=request.form['class_type'],
            category=request.form['category']
        )
        db.session.add(new_car)
        db.session.commit()
        flash('Car added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('car_form.html')

@app.route('/car/<int:car_id>/allocate', methods=['POST'])
def allocate_car(car_id):
    car = Car.query.get_or_404(car_id)
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

    if not car.is_available_between(start_date, end_date):
        flash('The car is not available for the selected dates', 'error')
        return redirect(url_for('car_detail', car_id=car_id))

    new_allocation = Allocation(
        car_id=car.id, 
        start_date=start_date, 
        end_date=end_date,
        client_name=request.form['client_name'],
        client_email=request.form['client_email'],
        client_phone=request.form['client_phone']
    )
    db.session.add(new_allocation)
    db.session.commit()
    flash('Car allocated successfully', 'success')
    return redirect(url_for('car_detail', car_id=car_id))