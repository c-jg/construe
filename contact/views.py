from django.shortcuts import render
from django.views.generic import CreateView
from .models import Contact, Plan

# Create your views here.
class ContactUs(CreateView):
    model = Contact
    fields = ['first_name', 'email', 'message']
    success_url = '/message_sent/'

    def form_valid(self, form):

        import os
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        sendgrid_key = os.environ['SG_KEY']

        message = Mail(
            from_email='EMAIL_ADDRESS',
            to_emails='EMAIL_ADDRESS',
            subject='New Customer Message',
            html_content=self.request.POST['message'])
        try:
            sg = SendGridAPIClient(sendgrid_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return super().form_valid(form)

class RequestPlan(CreateView):
    model = Plan
    fields = ['first_name', 'email', 'comments', 'multiple_channels', 'advertisement', 'other_platforms', 'message']
    success_url = '/message_sent/'

    def form_valid(self, form):

        import os
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        sendgrid_key = os.environ['SG_KEY']

        message = Mail(
            from_email='EMAIL_ADDRESS',
            to_emails='EMAIL_ADDRESS',
            subject='New Plan Requested',
            html_content=self.request.POST['message'])
        try:
            sg = SendGridAPIClient(sendgrid_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return super().form_valid(form)

def message_sent_view(request):
    return render(request, 'message_sent.html', {})
