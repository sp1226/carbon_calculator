# calculator/views.py

import os
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CarbonCalculation
from .serializers import CarbonCalculationSerializer
import tensorflow as tf
import numpy as np
from joblib import load

class CarbonCalculationViewSet(viewsets.ModelViewSet):
    queryset = CarbonCalculation.objects.all()
    serializer_class = CarbonCalculationSerializer

    # 모델 및 스케일러 로드
    model_path = os.path.join(settings.BASE_DIR, 'calculator', 'models', 'carbon_emission_model.h5')
    scaler_path = os.path.join(settings.BASE_DIR, 'calculator', 'models', 'scaler.joblib')
    model = tf.keras.models.load_model(model_path)
    scaler = load(scaler_path)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 입력 변수 추출
        production_volume = serializer.validated_data.get('production_volume')
        energy_consumption = serializer.validated_data.get('energy_consumption')
        transport_distance = serializer.validated_data.get('transport_distance')
        recycled_content = serializer.validated_data.get('recycled_content')

        # 입력 데이터 전처리
        input_data = np.array([[production_volume, energy_consumption, transport_distance, recycled_content]])
        input_data_scaled = self.scaler.transform(input_data)

        # 예측 수행
        prediction = self.model.predict(input_data_scaled)

        # 결과 저장
        serializer.save(carbon_emission=prediction[0][0])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)