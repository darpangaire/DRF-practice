from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
load_dotenv()

openai_api_key = os.getenv('tokens')
endpoints = os.getenv('urls')



def ask_openai(message):

  endpoint = endpoints
  model = "openai/gpt-4.1"
  token = openai_api_key

  client = ChatCompletionsClient(
      endpoint=endpoint,
      credential=AzureKeyCredential(token),
  )

  response = client.complete(
    messages=[
      SystemMessage(""),
      UserMessage(message),
    ],
    temperature=1,
    top_p=1,
    model=model
  )

  answer = response.choices[0].message.content
  return answer

  
  #print(response)
  # answer = response.choices[0].text.strip()
  # return answer
  


def chatbot(request):
  if request.method == 'POST':
    message = request.POST.get('message')
    response = ask_openai(message)
    return JsonResponse({'message':message,'response':response})
  return render(request,'protected.html')