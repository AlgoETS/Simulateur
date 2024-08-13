from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import Trigger, Event


class TriggerManagement(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract trigger data
        trigger_name = data.get('name')
        trigger_description = data.get('description')
        trigger_type = data.get('type')
        trigger_value = data.get('value')

        if not trigger_name or not trigger_description or not trigger_type:
            return Response(
                {'status': 'error', 'message': 'Trigger name, description, and type are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the Trigger
        trigger = Trigger.objects.create(
            name=trigger_name,
            description=trigger_description,
            type=trigger_type,
            value=trigger_value
        )

        # Associate events if provided
        event_ids = data.get('events', [])
        if event_ids:
            events = Event.objects.filter(id__in=event_ids)
            trigger.events.set(events)

        return Response(
            {
                'status': 'success',
                'message': 'Trigger created successfully',
                'data': {
                    'id': trigger.id,
                    'name': trigger.name,
                    'description': trigger.description,
                    'type': trigger.type,
                    'value': trigger.value,
                    'events': [{'id': event.id, 'name': event.name} for event in trigger.events.all()],
                    'timestamp': trigger.timestamp
                }
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request, trigger_id, *args, **kwargs):
        trigger = get_object_or_404(Trigger, id=trigger_id)
        data = request.data

        # Update trigger data
        trigger.name = data.get('name', trigger.name)
        trigger.description = data.get('description', trigger.description)
        trigger.type = data.get('type', trigger.type)
        trigger.value = data.get('value', trigger.value)

        # Update associated events if provided
        event_ids = data.get('events', None)
        if event_ids is not None:
            events = Event.objects.filter(id__in=event_ids)
            trigger.events.set(events)

        trigger.save()

        return Response(
            {
                'status': 'success',
                'message': 'Trigger updated successfully',
                'data': {
                    'id': trigger.id,
                    'name': trigger.name,
                    'description': trigger.description,
                    'type': trigger.type,
                    'value': trigger.value,
                    'events': [{'id': event.id, 'name': event.name} for event in trigger.events.all()],
                    'timestamp': trigger.timestamp
                }
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, trigger_id, *args, **kwargs):
        trigger = get_object_or_404(Trigger, id=trigger_id)
        trigger.delete()
        return Response(
            {'status': 'success', 'message': 'Trigger deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, trigger_id=None, *args, **kwargs):
        if trigger_id:
            trigger = get_object_or_404(Trigger, id=trigger_id)
            trigger_data = {
                'id': trigger.id,
                'name': trigger.name,
                'description': trigger.description,
                'type': trigger.type,
                'value': trigger.value,
                'events': [{'id': event.id, 'name': event.name} for event in trigger.events.all()],
                'timestamp': trigger.timestamp
            }
            return Response({'status': 'success', 'data': trigger_data}, status=status.HTTP_200_OK)

        triggers = Trigger.objects.all()
        trigger_data = [{
            'id': trigger.id,
            'name': trigger.name,
            'description': trigger.description,
            'type': trigger.type,
            'value': trigger.value,
            'events': [{'id': event.id, 'name': event.name} for event in trigger.events.all()],
            'timestamp': trigger.timestamp
        } for trigger in triggers]

        return Response({'status': 'success', 'data': trigger_data}, status=status.HTTP_200_OK)
