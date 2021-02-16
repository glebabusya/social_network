from django.shortcuts import render
from django.views.generic import View


class NewsView(View):
    def get(self, request):
        context = {}
        return render(request, 'news/news.html', context)

    def post(self, request):
        pass
