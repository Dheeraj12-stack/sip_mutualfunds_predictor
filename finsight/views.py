from django.shortcuts import render
import math
from datetime import datetime
import random

def dashboard(request):
    ai_message = ""
    suggestion_message = ""
    results = None
    user_data = {}

    # --- AI Dynamic Suggestions (Before Input) ---
    if request.method == "GET":
        suggestions = [
            "💡 If you invest ₹5000 monthly for 10 years at 12% annual return, you can grow ₹6 lakh into ₹11.6 lakh!",
            "📈 Consider a SIP of ₹2000/month for 5 years — your savings can grow over 40% with consistent investing.",
            "💰 Investing early increases compounding gains! Even ₹1000/month for 15 years can grow to ₹5.6 lakh.",
            "🚀 The longer you stay invested, the bigger the compounding magic. Try increasing your tenure for higher growth.",
        ]
        suggestion_message = random.choice(suggestions)

    # --- SIP Calculation + AI Advisor ---
    if request.method == "POST":
        monthly_investment = float(request.POST.get("monthly_investment", 0))
        annual_rate = float(request.POST.get("annual_rate", 0))
        years = int(request.POST.get("years", 0))

        months = years * 12
        monthly_rate = annual_rate / (12 * 100)

        # SIP Future Value Formula
        future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        total_investment = monthly_investment * months
        gain = future_value - total_investment

        results = {
            "total_investment": round(total_investment, 2),
            "future_value": round(future_value, 2),
            "gain": round(gain, 2),
        }

        # Store user-entered data
        user_data = {
            "monthly_investment": monthly_investment,
            "annual_rate": annual_rate,
            "years": years,
        }

        # --- AI Advisor (Smart Analysis) ---
        if annual_rate < 8:
            ai_message = (
                "📊 Your expected rate seems low. Consider exploring mutual funds with 10–12% annual return potential."
            )
        elif annual_rate >= 8 and annual_rate <= 12:
            ai_message = (
                "💼 Great choice! Your plan looks balanced between growth and safety. "
                "If you extend your tenure by 2 years, you could earn nearly "
                f"{round(future_value * 0.15 / 1000, 2)}k more."
            )
        else:
            ai_message = (
                "🔥 High-risk high-reward! Ensure you diversify investments to manage volatility effectively."
            )

        # Add motivational tone
        extra_tips = [
            "💪 Stay consistent — SIP works best with discipline!",
            "🎯 Small investments today build financial freedom tomorrow.",
            "📆 Reinvest your gains annually for even stronger compounding!",
        ]
        ai_message += " " + random.choice(extra_tips)

    return render(
        request,
        "dashboard.html",
        {
            "results": results,
            "ai_message": ai_message,
            "suggestion_message": suggestion_message,
            "user_data": user_data,
        },
    )
