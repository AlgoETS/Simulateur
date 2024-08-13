from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import ScenarioManager, News

class NewsManagement(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract news data
        title = data.get('title')
        content = data.get('content')
        published_date = data.get('published_date')

        if not title or not content:
            return Response(
                {'status': 'error', 'message': 'Title and content are required for creating news.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the News item
        news = News.objects.create(
            title=title,
            content=content,
            published_date=published_date,
        )

        return Response(
            {'status': 'success', 'message': 'News created successfully', 'data': {'id': news.id, 'title': news.title}},
            status=status.HTTP_201_CREATED
        )

    def put(self, request, news_id, *args, **kwargs):
        news = get_object_or_404(News, id=news_id)

        data = request.data
        title = data.get('title', news.title)
        content = data.get('content', news.content)
        published_date = data.get('published_date', news.published_date)

        # Update the News item
        news.title = title
        news.content = content
        news.published_date = published_date
        news.save()

        return Response(
            {'status': 'success', 'message': 'News updated successfully', 'data': {'id': news.id, 'title': news.title}},
            status=status.HTTP_200_OK
        )

    def delete(self, request, news_id, *args, **kwargs):
        news = get_object_or_404(News, id=news_id)

        # Delete the News item
        news.delete()
        return Response(
            {'status': 'success', 'message': 'News deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, news_id=None, *args, **kwargs):
        if news_id:
            news = get_object_or_404(News, id=news_id)
            data = {
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'published_date': news.published_date
            }
            return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)

        news_items = News.objects.all()
        data = [
            {
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'published_date': news.published_date
            }
        for news in news_items]

        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
