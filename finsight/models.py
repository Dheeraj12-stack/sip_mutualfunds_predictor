from django.db import models

class SIPRecord(models.Model):
    monthly_investment = models.FloatField(default=0)
    expected_rate = models.FloatField(default=0)
    years = models.IntegerField(default=0)
    total_investment = models.FloatField(default=0)
    future_value = models.FloatField(default=0)
    gain = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SIP - ₹{self.monthly_investment} x {self.years} yrs"
