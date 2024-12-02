from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

class Command(BaseCommand):
    help = '탄소 배출량 예측 모델을 학습합니다.'
    
    def handle(self, *args, **options):
        self.stdout.write('데이터 로딩 중...')
        data = pd.read_csv('/Users/sp/Documents/dataset/materials_carbon_emission.csv')
        
        X = data[['variable1', 'variable2', 'variable3']]
        y = data['carbon_emission']
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        scaler_path = os.path.join('calculator', 'models', 'scaler.joblib')
        from joblib import dump
        dump(scaler, scaler_path)
        
        X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1)
        ])
        
        self.stdout.write('모델 학습 중...')
        model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val))
        
        model_path = os.path.join('calculator', 'models', 'carbon_emission_model.h5')
        model.save(model_path)
        self.stdout.write(self.style.SUCCESS(f'모델 학습 완료. 모델이 {model_path}에 저장되었습니다.'))