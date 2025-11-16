import os
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def chatbot_page(request):
    return render(request, "chatbot_app/chatbot.html")

def simple_chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=user_message
            )

            # Extract reply
            reply = response.output[0].content[0].text

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
