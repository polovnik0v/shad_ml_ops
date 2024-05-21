
import os
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.views import View
from src.preprocessing import import_data, run_preproc
from src.scorer import make_pred, get_top5, save_plot
from django.contrib import messages
import json 

# Путь к директориям
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'datasets')
PREDICTION_DIR = os.path.join(BASE_DIR, 'output_pred')
TOP_FEATURES_DIR = os.path.join(BASE_DIR, 'output_top5')
IMAGE_DIR = os.path.join(BASE_DIR, 'output_image')

class UploadDatasetView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        if 'dataset' in request.FILES:
            dataset = request.FILES['dataset']
            dataset_path = os.path.join(DATASET_DIR, 'dataset.csv')
            os.makedirs(DATASET_DIR, exist_ok=True)
            with open(dataset_path, 'wb+') as destination:
                for chunk in dataset.chunks():
                    destination.write(chunk)
            
            # Run preprocessing
            input_df = import_data(dataset_path)
            preprocessed_df = run_preproc(input_df)

            # Make prediction
            prediction_df = make_pred(preprocessed_df, dataset_path)
            prediction_path = os.path.join(PREDICTION_DIR, 'prediction.csv')
            os.makedirs(PREDICTION_DIR, exist_ok=True)
            prediction_df.to_csv(prediction_path, index=False)
                
            messages.success(request, 'Dataset uploaded and predictions made successfully')

            save_plot(preprocessed_df, dataset_path)

            return render(request, 'index.html')
        messages.error(request, 'No file uploaded')
        return render(request, 'index.html')
    
class DownloadPredictionView(View):
    def get(self, request):
        file_path = os.path.join(PREDICTION_DIR, 'prediction.csv')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="prediction.csv"'
                return response
        return HttpResponseNotFound('Prediction file not found')

# class DownloadTopFeaturesView(View):
#     def get(self, request):
#         file_path = os.path.join(TOP_FEATURES_DIR, 'top_5_features.csv')
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as f:
#                 response = HttpResponse(f.read(), content_type='text/csv')
#                 response['Content-Disposition'] = 'attachment; filename="top_5_features.csv"'
#                 return response
#         return HttpResponseNotFound('File not found')

class DownloadTopFeaturesView(View):
    def get(self, request):
        top_5_json = get_top5()  # Получаем JSON с топ 5 фичами

        # Создаем временный файл для сохранения JSON
        temp_file_path = os.path.join(TOP_FEATURES_DIR, 'top_5_features.json')
        with open(temp_file_path, 'w') as f:
            json.dump(top_5_json, f, indent=1, ensure_ascii=False)

        # Отправляем временный файл как HTTP-ответ
        if os.path.exists(temp_file_path):
            with open(temp_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="top_5_features.json"'
                return response
        return HttpResponseNotFound('Top 5 features file not found')

class DownloadImageView(View):
      def get(self, request):
        file_path = os.path.join(IMAGE_DIR, 'image.png')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename="image.png"'
                return response
        return HttpResponseNotFound('Picture not found')

