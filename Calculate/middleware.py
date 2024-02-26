# from django.shortcuts import redirect
# from django.urls import reverse

# class RedirectAuthenticatedUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         # Redirect authenticated users from login and signup pages
#         if request.user.is_authenticated and request.path in [reverse('calculate:login'), reverse('calculate:signup')]:
#             return redirect('calculate:exp_post')

#         # Redirect logged-out users from authenticated pages
#         if not request.user.is_authenticated and request.path != reverse('calculate:login'):
#             return redirect('calculate:login')

#         return response
