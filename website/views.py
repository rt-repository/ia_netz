from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Member, Availability
from . import db
import json
from datetime import datetime, time


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    av = Availability.query.all()
    memb = Member.query.filter_by(user_id=current_user.id).all()
    tday = datetime.now()
    strtdts = []
    nested_strtdts = []
    enddts = []
    nested_enddts = []
    days = []
    final_strtdts = []
    final_enddts = []
    result = []
    
    
    if request.method == 'POST':

        # get all start and end dates from db
        
        for x  in range(1,len(av)+1,1):
            y = Availability.query.filter_by(id=x).first()
            if y.user_id == current_user.id:
                #if y.startdate >= tday:
                strtdts.append(y.startdate)
                #latest startdate should be first index
                strtdts = sorted(strtdts, reverse=True)
                #earliest enddate should be first index
                #if y.enddate >= tday:
                enddts.append(y.enddate)
                enddts = sorted(enddts, reverse=False)

        
        
        #get days where avalibilities are declared
        for b in range(len(strtdts)):
            days.append(strtdts[b].day)
            daycount= list(set(days))
        
        #creating a nested list with sub lists  of dates with same day
        #fort start dates
        for c in range(len(daycount)):
            innerList = []
            for d in range (len(strtdts)):
                if strtdts[d].day == daycount[c] :#and strtdts[d].month == tday.month:
                    innerList.append(strtdts[d])
            nested_strtdts.append(innerList)
        #and end dates
        for c in range(len(daycount)):
            innerList = []
            for d in range (len(enddts)):
                if enddts[d].day == daycount[c]: #and enddts[d].month == tday.month:
                    innerList.append(enddts[d])
            nested_enddts.append(innerList)
         
        #checking if every member gave a availability for this day.
            #if not, the plan should not be calculated
        for c in range(len(daycount)):
            if(len(nested_strtdts[c]))== len(memb):
                final_strtdts.append(nested_strtdts[c][0])

            if(len(nested_enddts[c]))== len(memb):
                final_enddts.append(nested_enddts[c][0])

        
        for c in range(len(final_strtdts)):
            result.append(final_strtdts[c].strftime('%d.%m.%Y %H:%M') + ' - '+ final_enddts[c].strftime('%H:%M'))
        
        if result[0] > result[1]:
            result.reverse()
        
            
    return render_template("plan.html", user=current_user, result = result)

@views.route('/memberlist', methods=['GET', 'POST'])
@login_required
def memberlist():
    if request.method == 'POST':
        member = request.form.get('member')

        if len(member) < 1:
            flash('The name of the  new member is too short!',
                  category='error')
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


@views.route('/availability', methods=['GET', 'POST'])
@login_required
def availability():
    if request.method == 'POST':
        form_date = request.form.get('date')
        form_starttime = request.form.get('starttime')
        form_endtime = request.form.get('endtime')
        member = request.form.get('memberchoice')
        startdate = datetime.strptime(form_date +" "+ form_starttime,"%Y-%m-%d %H:%M")
        enddate = datetime.strptime(form_date +" "+ form_endtime,"%Y-%m-%d %H:%M")
        present = datetime.now()

        if not form_date  :
            flash('Values are missing.', category= 'error')
        elif startdate < present:
            flash('The date is in the past.', category = 'error')
        elif enddate <= startdate:
            flash('Your availability ends earlier than it starts.', category = 'error')
        else:
            new_availability = Availability(startdate = startdate, enddate = enddate, member = member, user_id=current_user.id)
            db.session.add(new_availability)
            db.session.commit()
            flash(' New availability added!', category='success') 
        
    return render_template("availability.html", user=current_user)


@views.route('/delete-availability', methods=['POST'])
def delete_availability():
    availability = json.loads(request.data)
    availabilityId = availability['availabilityId']
    availability = Availability.query.get(availabilityId)
    if availability:
        if availability.user_id == current_user.id:
            db.session.delete(availability)
            db.session.commit()

    return jsonify({})