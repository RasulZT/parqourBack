from django.urls import path
from .views import receive_ticket, SupportSessionCreateView, TicketUpdateUserView, SupportSessionsByTelegramView, \
    SupportFinishedSessionsByTelegramView, TicketDeleteView

urlpatterns = [
    path("tickets/create-ticket/", receive_ticket, name="receive_ticket"),
    path("tickets/create_session/", SupportSessionCreateView.as_view(), name="create_session"),
    path('tickets/<int:ticket_id>/update-ticket/', TicketUpdateUserView.as_view()),
    path("tickets/<int:ticket_id>/delete/", TicketDeleteView.as_view()),

    path("support-sessions/", SupportSessionsByTelegramView.as_view()),
    path("support-finishedsessions/", SupportFinishedSessionsByTelegramView.as_view()),
]
