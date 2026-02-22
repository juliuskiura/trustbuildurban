from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Serve pages by path (e.g., /about/, /services/our-team/)
    path('', views.page_detail, name='page_by_path'),
    path('<str:path>/', views.page_detail, name='page'),
    
    # Fallback: serve page by ID
    path('id/<int:page_id>/', views.page_by_id, name='page_by_id'),
    
    # Preview page
    path('preview/<int:page_id>/', views.preview_page, name='preview'),
]
