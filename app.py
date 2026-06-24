import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        family = int(request.form["family"])
        showers = int(request.form["showers"])
        washing = int(request.form["washing"])
        vehicle = int(request.form["vehicle"])
        garden = int(request.form["garden"])

        water_usage = (
            family * 135 +
            showers * 20 +
            washing * 60 +
            vehicle * 100 +
            garden * 50
        )

        monthly_savings = int(water_usage * 0.15 * 30)

        recommendations = []

        if showers > family:
            recommendations.append("Reduce shower duration to conserve water.")

        if vehicle > 1:
            recommendations.append("Reduce vehicle washing frequency.")

        if garden > 1:
            recommendations.append("Use drip irrigation for gardening.")

        if washing > 3:
            recommendations.append("Run washing machines with full loads.")

        if len(recommendations) == 0:
            recommendations.append("Excellent water management practices.")

        labels = ['Family Use', 'Showers', 'Washing', 'Vehicle Wash', 'Garden']

        sizes = [
            family * 135,
            showers * 20,
            washing * 60,
            vehicle * 100,
            garden * 50
        ]

        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title("Water Usage Distribution")

        chart_path = os.path.join('static', 'water_chart.png')
        plt.savefig(chart_path)
        plt.close()

        if water_usage < 500:
            score = 9
            status = "Low Water Consumption"
            color = "green"

        elif water_usage < 1000:
            score = 6
            status = "Moderate Water Consumption"
            color = "orange"

        else:
            score = 3
            status = "High Water Consumption"
            color = "red"

        result = {
            "usage": water_usage,
            "status": status,
            "monthly_savings": monthly_savings,
            "color": color,
            "score": score,
            "recommendations": recommendations
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)