from requests import Response
from rest_framework import serializers
from .models import ProgramActivityModel
from activity.models import Activity

class ProgramActivitySerializer(serializers.ModelSerializer):
    class Meta :
        model=ProgramActivityModel
        fields='__all__'


def combinedata(data):
  
    activity_id=data.get('activity_id')
    program_id=data.get('program_id')
    week_no=data.get('week_no')
    day=data.get('day')
    time=data.get('time')
    if activity_id is not None:
        activity_id = int(activity_id)
    else:
        raise ValueError("activity_id is required")

    if program_id is not None:
        program_id = int(program_id)
    else:
        raise ValueError("program_id is required")

    if week_no is not None:
        week_no = int(week_no)
    else:
        raise ValueError("week_no is required")    
    if activity_id is not None: 
        activity=Activity.objects.get(id=activity_id)
        data={
            'activity_id':activity_id,
            'program_id':program_id,
            'week_no':week_no,
            'day':day,
            'time':time,
            'activity_type':activity.activity_type,
            'language': activity.language,
            'activity': activity.activity,
            'brand': activity.brand,
            'who': activity.who,
            'completion_check': activity.completion_check,
            'show_completed': activity.show_completed,
            'location': activity.location,
            'user_duration': activity.user_duration,
            'teamlead_duration': activity.teamlead_duration,
            'coach_duration': activity.coach_duration,
            'coach_type': activity.coach_type,
            'travel_time': activity.travel_time,
            'url': activity.url,
            'amount': activity.amount,
            'file': activity.file,
            'upload_possible': activity.upload_possible,
            'activity_description': activity.activity_description,
            'activity_name': activity.activity_name,
            'send_reminder': activity.send_reminder,
            'show_in_task': activity.show_in_task,
            'add_comment_option': activity.add_comment_option,
            'indicate_when_completed': activity.indicate_when_completed,
        }
        print('last me aaya combine me ')
        return data
    return Response({
        'message':'activity with this id not exit',
    })


    