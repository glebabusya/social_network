from django.shortcuts import render
from django.views.generic import View


class HomePageView(View):
    def get(self, request):
        context = {}
        return render(request, 'homepage/homepage.html', context)

    def post(self, request):
        pass
