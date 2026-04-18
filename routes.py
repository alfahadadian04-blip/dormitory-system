from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Tenant, Payment
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    tenants = Tenant.query.all()
    total_tenants = len(tenants)
    active_tenants = Tenant.query.filter_by(status='active').count()
    total_rent = sum(t.rent_amount for t in tenants if t.status == 'active')
    return render_template('index.html', tenants=tenants, total_tenants=total_tenants, 
                         active_tenants=active_tenants, total_rent=total_rent)

@main.route('/tenants')
@login_required
def tenants():
    all_tenants = Tenant.query.all()
    return render_template('tenants.html', tenants=all_tenants)

@main.route('/tenant/<int:id>')
@login_required
def tenant_detail(id):
    tenant = Tenant.query.get_or_404(id)
    return render_template('tenant_detail.html', tenant=tenant)

@main.route('/tenant/add', methods=['GET', 'POST'])
@login_required
def add_tenant():
    if request.method == 'POST':
        tenant = Tenant(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            room_number=request.form.get('room_number'),
            rent_amount=float(request.form.get('rent_amount', 0)),
            status=request.form.get('status', 'active')
        )
        move_in = request.form.get('move_in_date')
        if move_in:
            tenant.move_in_date = datetime.strptime(move_in, '%Y-%m-%d')
        
        db.session.add(tenant)
        db.session.commit()
        flash('Tenant added successfully!')
        return redirect(url_for('main.tenants'))
    
    return render_template('add_tenant.html')

@main.route('/tenant/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    
    if request.method == 'POST':
        tenant.name = request.form.get('name')
        tenant.phone = request.form.get('phone')
        tenant.email = request.form.get('email')
        tenant.room_number = request.form.get('room_number')
        tenant.rent_amount = float(request.form.get('rent_amount', 0))
        tenant.status = request.form.get('status')
        
        move_in = request.form.get('move_in_date')
        if move_in:
            tenant.move_in_date = datetime.strptime(move_in, '%Y-%m-%d')
        
        db.session.commit()
        flash('Tenant updated successfully!')
        return redirect(url_for('main.tenant_detail', id=id))
    
    return render_template('edit_tenant.html', tenant=tenant)

@main.route('/tenant/<int:id>/delete', methods=['POST'])
@login_required
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    flash('Tenant deleted successfully!')
    return redirect(url_for('main.tenants'))

@main.route('/payments')
@login_required
def payments():
    all_payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    return render_template('payments.html', payments=all_payments)

@main.route('/payment/add', methods=['GET', 'POST'])
@login_required
def add_payment():
    if request.method == 'POST':
        payment = Payment(
            tenant_id=request.form.get('tenant_id'),
            amount=float(request.form.get('amount', 0)),
            payment_month=request.form.get('payment_month'),
            notes=request.form.get('notes')
        )
        payment_date = request.form.get('payment_date')
        if payment_date:
            payment.payment_date = datetime.strptime(payment_date, '%Y-%m-%d')
        
        db.session.add(payment)
        db.session.commit()
        flash('Payment recorded successfully!')
        return redirect(url_for('main.payments'))
    
    tenants = Tenant.query.filter_by(status='active').all()
    return render_template('add_payment.html', tenants=tenants)
