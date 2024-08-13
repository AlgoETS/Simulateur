from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import Event

class EventManagement(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract event data
        event_name = data.get('name')
        event_description = data.get('description')
        event_date = data.get('date')

        if not event_name or not event_description or not event_date:
            return Response(
                {'status': 'error', 'message': 'Event name, description, and date are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the Event
        event = Event.objects.create(
            name=event_name,
            description=event_description,
            date=event_date
        )

        return Response(
            {
                'status': 'success',
                'message': 'Event created successfully',
                'data': {
                    'id': event.id,
                    'name': event.name,
                    'description': event.description,
                    'date': event.date
                }
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        data = request.data

        # Update event data
        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.date = data.get('date', event.date)

        event.save()

        return Response(
            {
                'status': 'success',
                'message': 'Event updated successfully',
                'data': {
                    'id': event.id,
                    'name': event.name,
                    'description': event.description,
                    'date': event.date
                }
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return Response(
            {'status': 'success', 'message': 'Event deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        event_data = [{
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date
        } for event in events]

        return Response(
            {'status': 'success', 'data': event_data},
            status=status.HTTP_200_OK
        )
