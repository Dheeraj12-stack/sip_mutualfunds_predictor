from django.shortcuts import render
import pandas as pd
import random


def dashboard(request):
    future_value = None
    total_investment = None
    gain = None
    ai_future_value = None
    ai_gain = None
    ai_return_percent = None
    ai_message = None
    ai_suggestion = None
    months_list = []
    values_list = []

    if request.method == 'POST':
        try:
            monthly_investment = float(request.POST.get('monthly_investment', 0))
            years = int(request.POST.get('years', 0))
            annual_rate = float(request.POST.get('rate', 0))

            months = years * 12
            monthly_rate = annual_rate / 12 / 100

            # --- Standard SIP Calculation ---
            df = pd.DataFrame({'Month': range(1, months + 1)})
            df['Value'] = df['Month'].apply(
                lambda m: monthly_investment *
                (((1 + monthly_rate) ** m - 1) / monthly_rate) *
                (1 + monthly_rate)
            )

            total_investment = monthly_investment * months
            future_value = round(df['Value'].iloc[-1], 2)
            gain = round(future_value - total_investment, 2)

            # --- AI Predicted Slight Variation (±5%) ---
            variation_percent = random.uniform(-0.05, 0.05)
            ai_future_value = round(future_value * (1 + variation_percent), 2)
            ai_gain = round(ai_future_value - total_investment, 2)
            ai_return_percent = round((ai_gain / total_investment) * 100, 2)

            # --- AI Performance Message ---
            if ai_return_percent < 60:
                ai_message = "Low performance detected — consider increasing duration or rate slightly."
                ai_suggestion = (
                    "AI suggests extending your SIP duration by 3–4 years or "
                    "switching to a higher-growth fund category for better returns."
                )
            elif 60 <= ai_return_percent < 100:
                ai_message = "Moderate performance detected — your plan is steady but can be optimized."
                ai_suggestion = (
                    "AI recommends maintaining your current SIP but reviewing it annually. "
                    "You can also slightly increase monthly contributions for higher future gains."
                )
            else:
                ai_message = "Excellent performance — your investment plan is showing strong growth potential!"
                ai_suggestion = (
                    "AI advises continuing this SIP strategy consistently. "
                    "You may also diversify into balanced or equity funds to enhance long-term growth."
                )

            # --- Prepare Chart Data ---
            df['AIPredicted'] = df['Value'] * (1 + variation_percent)
            months_list = list(df['Month'])
            values_list = list(df['AIPredicted'])

        except Exception as e:
            print("Error:", e)

    return render(request, 'dashboard.html', {
        'future_value': future_value,
        'total_investment': total_investment,
        'gain': gain,
        'ai_future_value': ai_future_value,
        'ai_gain': ai_gain,
        'ai_return_percent': ai_return_percent,
        'ai_message': ai_message,
        'ai_suggestion': ai_suggestion,
        'months_list': months_list,
        'values_list': values_list,
    })
