from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Member, Availability
from . import db
import json
import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/memberlist',  methods=['GET', 'POST'])
@login_required
def memberlist():
    if request.method == 'POST':
        member = request.form.get('member')

        if len(member) < 1:
            flash('The name of the  new member is too short!', category='error')
        else:
            new_member = Member(name=member, user_id=current_user.id)
            db.session.add(new_member)
            db.session.commit()
            flash(' New member added!', category='success')

    return render_template("memberlist.html", user=current_user)


@views.route('/delete-member', methods=['POST'])
def delete_member():
    member = json.loads(request.data)
    memberId = member['memberId']
    member = Member.query.get(memberId)
    if member:
        if member.user_id == current_user.id:
            db.session.delete(member)
            db.session.commit()

    return jsonify({})

@views.route('/availability',  methods=['GET', 'POST'])
@login_required
def availability():
    if request.method == 'POST':
        form_date = request.form.get('date')
        form_starttime = request.form.get('starttime')
        form_endtime = request.form.get('endtime')
        startdate=datetime.datetime.strptime(form_date + form_starttime,"%Y-%m-%d %H:%M")
        enddate=datetime.datetime.strptime(form_date + form_endtime,"%Y-%m-%d %H:%M")
        new_availability = Availability(startdate = startdate, enddate = enddate,  user_id=current_user.id)
        
        db.session.add(new_availability)
        db.session.commit()
        flash(' New availability added!', category='success')
        print(enddate)
            
    return render_template("availability.html", user=current_user)

