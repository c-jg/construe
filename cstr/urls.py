from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from pages.views import home_view, pricing_view, features_view, privacy_out_view, terms_out_view
from contact.views import ContactUs, message_sent_view
from dashboard.views import (
    account_settings_view,
    terms_view,
    privacy_policy_view,
    ReportCreateView,
    ReportListView,
    ReportDetailView,
    success_view,
    cancel_view
)
from membership.views import MembershipSelectView, payment_view, update_transactions_view, confirm_cancel_view, cancel_subscription_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^account/', include('allauth.urls')),
    path('', home_view, name='home'),
    path('home/', home_view),
    path('features/', features_view, name='features'),
    path('pricing/', pricing_view, name='pricing'),
    path('contact/', ContactUs.as_view(extra_context={'contact_style': 'opacity:1;border-bottom: 1px solid #fff;'}), name='contact'),
    path('account_settings/', account_settings_view, name='acc_sett'),
    path('terms/', terms_view, name='terms'),
    path('terms_conditions', terms_out_view, name='terms_out'),
    path('privacy/', privacy_policy_view, name='privacy_policy'),
    path('privacy_policy/', privacy_out_view, name='privacy_out'),
    path('billing/', MembershipSelectView.as_view(extra_context={'billing_act': 'vMenu--active', 'dash_style':'opacity:1;border-bottom: 1px solid #fff;'}), name='billing'),
    path('analyze/new/', ReportCreateView.as_view(extra_context={'lyz_style': 'opacity:1;border-bottom: 1px solid #fff;'}), name="report_create"),
    path('saved/', ReportListView.as_view(), name="saved"),
    path('report_details/<int:pk>/', ReportDetailView.as_view(), name='report_details'),
    path('message_sent/', message_sent_view, name='message_sent'),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
    path('payment/', payment_view, name='payment'),
    path('update_transactions/<subscription_id>/', update_transactions_view, name='update_transactions'),
    path('confirm_cancel/', confirm_cancel_view, name='confirm_cancel'),
    path('cancel_subscription/', cancel_subscription_view, name='cancel_subscription')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)