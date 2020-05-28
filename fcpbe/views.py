from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

from fcpbe.models import Vote
import time

week_day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def fd(d):
    return datetime.strftime(d, '%d-%m-%Y')


def pd(s):
    return datetime.strptime(s, '%d-%m-%Y').date()


class VoteView(APIView):
    def get(self, request, voter):
        sunday = (datetime.now() - timedelta(days=datetime.now().weekday() + 1)).date()
        saturday = (datetime.now() + timedelta(days=6)).date()
        votes = Vote.objects.all()
        votes = [{'id': x.id, 'voter': x.voter, 'date': pd(x.date), 'fb_id': x.fb_id} for x in votes if sunday <= pd(x.date) <= saturday]

        days = {}
        for day in range(7):
            current_date = sunday + timedelta(days=day)
            current_day_str = '%s - %s' % (week_day_names[day], fd(current_date))
            days[current_day_str] = [{
                'id': x['id'] if voter == x['voter'] else None,
                'voter': x['voter'],
                'date': fd(x['date']),
                'fb_id': x['fb_id']
            } for x in votes if x['date'] == current_date]

        return Response(days)

    def post(self, request, voter, date_str):
        date = pd(date_str)
        if Vote.objects.filter(voter=voter, date=fd(date)).exists():
            return Response('Exists', 400)

        fb_id = request.data.get('fb_id')

        Vote.objects.create(voter=voter, date=fd(date), fb_id=fb_id)
        return Response()

    def delete(self, request, voter, vote_id):
        if not Vote.objects.filter(voter=voter, id=vote_id).exists():
            return Response('Does not exist', 400)
        Vote.objects.filter(voter=voter, id=vote_id).delete()
        return Response()
