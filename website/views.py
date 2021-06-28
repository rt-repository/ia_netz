from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Member, Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

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

@views.route('/availability',  methods=['GET', 'POST'])
@login_required
def availability():
    if request.method == 'POST':
        startdate = request.form.get('memberchoice')
        print(startdate)
    
    return render_template("availability.html", user=current_user)


@views.route('/delete-note', methods=['POST'])

def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

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
