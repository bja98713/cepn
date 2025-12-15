# expertise/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # pour accéder à views.accueil

from .views import (
    PersonnelListView,
    PersonnelDetailView,
    PersonnelCreateView,
    PersonnelUpdateView,
    PersonnelDeleteView,
    FicheEvenementCreateView,
    FicheEvenementUpdateView,
    FicheEvenementDeleteView,
    bordereau_selection_view,
    bordereau_view,
    download_bordereau,
    FactureView,  # Import de la nouvelle vue
    PersonnelNavigant
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export/excel/', views.export_evenements_excel, name='export_evenements_excel'),
    path('', views.accueil, name='accueil'),  # ta vue d'accueil protégée
    path('factures/recherche/', views.facture_search, name='facture_search'),
    path('factures/par-compagnie/', views.facture_par_compagnie, name='facture_par_compagnie'),
    path('bordereaux/par-compagnie/', views.bordereau_par_compagnie, name='bordereau_par_compagnie'),
    path('relance/', views.relance_factures, name='relance_factures'),
    path('intervenants/', views.intervenants_list, name='intervenants_list'),
    path('intervenants/<int:pk>/historique/', views.intervenant_history, name='intervenant_history'),
    path('intervenants/<int:pk>/facture/<int:invoice_id>/', views.intervenant_invoice, name='intervenant_invoice'),
    path('intervenants/<int:pk>/facture/<int:invoice_id>/supprimer/', views.intervenant_invoice_delete, name='intervenant_invoice_delete'),
    path('intervenants/<int:pk>/factures/telecharger-tout/', views.intervenant_invoices_zip, name='intervenant_invoice_all'),
    path('personnels/', PersonnelListView.as_view(), name='personnel_list'),
    path('personnels/add/', PersonnelCreateView.as_view(), name='personnel_add'),
    path('personnels/<str:dn>/', PersonnelDetailView.as_view(), name='personnel_detail'),
    path('personnels/<str:dn>/edit/', PersonnelUpdateView.as_view(), name='personnel_edit'),
    path('personnels/<str:dn>/delete/', PersonnelDeleteView.as_view(), name='personnel_delete'),
    path('personnels/<str:dn>/evenements/add/', FicheEvenementCreateView.as_view(), name='evenement_add'),
    path('evenement/<int:pk>/edit/', FicheEvenementUpdateView.as_view(), name='evenement_edit'),
    path('evenement/<int:pk>/delete/', FicheEvenementDeleteView.as_view(), name='evenement_delete'),
    path('evenement/<int:pk>/facture/', FactureView.as_view(), name='facture'),
    path("bordereau/<int:annee>/<int:mois>/<str:iata>/", bordereau_view, name="bordereau_detail"),
    path("bordereau/selection/", bordereau_selection_view, name="selectionner_bordereau"),
    path('bordereau/<int:mois>/<int:annee>/<str:iata>/download/', views.download_bordereau, name='download_bordereau'),
    path('bordereaux/', views.liste_bordereaux, name='liste_bordereaux'),
    path('selectionner_bordereau/', views.bordereau_selection_view, name='selectionner_bordereau'),
    path('bordereaux/', views.liste_bordereaux, name='liste_bordereaux'),
    path('bordereau/<str:no_bordereau>/factures/', views.bordereau_factures, name='factures_bordereau'),
    path('bordereau/<int:id>/supprimer/', views.supprimer_bordereau, name='supprimer_bordereau'),
    path('bordereau/<str:no_bordereau>/factures-medecins/', views.factures_medecins_bordereau, name='factures_medecins_bordereau'),
    path('bordereau/<int:id>/toggle_virement/', views.toggle_virement, name='toggle_virement'),
    path('bordereau/<str:bordereau_no>/medecin/<int:medecin_id>/telecharger/', views.telecharger_facture_medecin, name='telecharger_facture_medecin'),
    path('factures/<int:pk>/toggle-paiement/', views.toggle_facture_paiement, name='toggle_facture_paiement'),
]
