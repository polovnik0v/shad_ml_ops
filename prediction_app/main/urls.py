# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),  # Маршрут для домашней страницы
#     path('upload_dataset/', views.upload_dataset, name='upload_dataset'),
#     path('download_prediction/', views.download_prediction, name='download_prediction'),
#     path('download_top_features/', views.download_top_features, name='download_top_features'),
#     path('download_image/', views.download_image, name='download_image'),
# ]

from django.urls import path
from .views import UploadDatasetView, DownloadPredictionView, DownloadTopFeaturesView, DownloadImageView

urlpatterns = [
    path('', UploadDatasetView.as_view(), name='upload_dataset'),
    path('upload_dataset/', UploadDatasetView.as_view(), name='upload_dataset'),
    path('download_prediction/', DownloadPredictionView.as_view(), name='download_prediction'),
    path('download_top5/', DownloadTopFeaturesView.as_view(), name='download_top5'),
    path('download_image/', DownloadImageView.as_view(), name='download_image'),
]




