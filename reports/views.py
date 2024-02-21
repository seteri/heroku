# views.py
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class SendDiscordMessageAPIView(APIView):
    webhook_url = ('https://discord.com/api/webhooks/1198806127081689158'
                   '/RuN_3r3ErpLYqdRonrVW5mI1jgm1hMXtG1vdYwUTbpJNFc3Q0IUB4QUPCj9WbxTLKSvy')  # Replace with your

    @method_decorator(ratelimit(key='ip', rate='3/m', block=True))
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        name = request.data.get('name')
        surname = request.data.get('surname')
        issue = request.data.get('issue')
        listing_id = request.data.get('listing_id')

        # Check if the required fields are missing
        if not email or not name or not surname or not issue:
            return Response({'error': 'All required fields must be filled'}, status=status.HTTP_400_BAD_REQUEST)

        # Call the function to send the Discord message
        self.send_discord_webhook(email, name, surname, issue, listing_id)

        # You can customize the success response accordingly
        return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)

    def send_discord_webhook(self, email, name, surname, issue, listing_id='არაა მითითებული'):
        # Create an embed with specified fields
        data = {
            "content": "New Support Request",
            "embeds": [
                {
                    "title": "New Support Request",
                    "color": 0x00ff00,
                    "fields": [
                        {"name": "listing_id", "value": listing_id, "inline": True},
                        {"name": "Email", "value": email, "inline": False},
                        {"name": "Name", "value": name, "inline": True},
                        {"name": "Surname", "value": surname, "inline": True},
                        {"name": "Issue", "value": issue, "inline": False},
                    ]
                }
            ]
        }

        # Make a POST request to the Discord webhook URL
        response = requests.post(self.webhook_url, json=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print('Message sent successfully')
        else:
            print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')