from django.db import models

class CarbonCalculation(models.Model):
    variable1 = models.FloatField()
    variable2 = models.FloatField()
    
    predicted_emission = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f'Calculation {self.id}'