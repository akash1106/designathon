
from django.contrib import admin
from django.urls import path,include
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data.urls')),  # Include your app's URLs here
=======
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("data.urls"))
>>>>>>> 9f4f27808ad8522efbca7d8a50fc608262f973fa
]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)