from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime
import re


class MedecinInvoice(models.Model):
    medecin = models.ForeignKey('Medecin', on_delete=models.CASCADE, related_name='factures_generales')
    number = models.CharField(max_length=50, unique=True)
    emission_date = models.DateField()
    total_brut = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_redevance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_net = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-emission_date', '-created_at']

    def __str__(self):
        return f"Facture médecin {self.number}"


class MedecinInvoiceLine(models.Model):
    invoice = models.ForeignKey(MedecinInvoice, on_delete=models.CASCADE, related_name='lignes')
    evenement = models.ForeignKey('FicheEvenement', on_delete=models.CASCADE, related_name='factures_medicaux')
    act_code = models.CharField(max_length=30)
    act_label = models.CharField(max_length=120)
    date_acte = models.DateField()
    patient_nom = models.CharField(max_length=120)
    patient_prenom = models.CharField(max_length=120)
    facture_no = models.CharField(max_length=50, blank=True, null=True)
    montant_brut = models.DecimalField(max_digits=12, decimal_places=2)
    redevance = models.DecimalField(max_digits=12, decimal_places=2)
    montant_net = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('evenement', 'act_code')
        ordering = ['date_acte', 'pk']

    def __str__(self):
        return f"Ligne {self.act_code} - {self.invoice.number}"

# --- Médecins ---
class Medecin(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    iban = models.CharField(max_length=34, blank=True, null=True, verbose_name="IBAN / RIB")

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.specialite}"

# --- Compagnies ---
class CompagnieAerienne(models.Model):
    iata = models.CharField(max_length=3, unique=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# --- Personnels navigants ---
class PersonnelNavigant(models.Model):
    dn = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message="Attention Christian, le dn doit contenir exactement 7 chiffres, et aucun autre symbole, ou lettre.",
                code='invalid_dn'
            )
        ]
    )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    compagnie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE, related_name='personnels')
    date_de_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], null=True, blank=True)
    #statut_pn = models.CharField(max_length=100, null=True, blank=True)
    statut_pn = models.CharField(max_length=100, choices=[('Pilote', 'Pilote'), ('PNC', 'PNC'), ('Controleur aérien', 'Contrôleur aérien'), ('Para Pro', 'Para Pro')], null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# --- Bordereaux ---
class Bordereau(models.Model):
    date_bordereau = models.DateField()
    no_bordereau = models.CharField(max_length=50, unique=True)
    virement = models.BooleanField(default=False, verbose_name="Virement effectué ?")


    def __str__(self):
        return self.no_bordereau

    @staticmethod
    def generer_no_bordereau(mois, annee, iata):
        date_creation = datetime.today()
        return f"EB{date_creation.day:02d}{mois:02d}{str(annee)[-2:]}{iata}"

# --- Événements / Factures ---
class FicheEvenement(models.Model):
    date_evenement = models.DateField()
    personnel = models.ForeignKey(PersonnelNavigant, on_delete=models.CASCADE, related_name='evenements', null=False, blank=False)
    bordereau = models.ForeignKey(Bordereau, on_delete=models.SET_NULL, null=True, blank=True, related_name='evenements')

    # Informations générales
    no_facture = models.CharField("Numéro de facture", max_length=50, blank=True, null=True, unique=True, editable=False)
    paiement = models.BooleanField("Paiement", default=False)
    date_paiement = models.DateField("Date de paiement", null=True, blank=True)
    modalite_paiement = models.CharField("Modalité de paiement", max_length=10, choices=[
        ('liquide', 'Liquide'), ('virement', 'Virement'), ('CB', 'Carte Bancaire'), ('Chèque', 'Chèque')],
        null=True, blank=True
    )

    # Honoraires
    honoraire_cempn = models.IntegerField("CEMPN = 10000", default=0)
    honoraire_cs_oph = models.IntegerField("OPH = 10600", default=0)
    honoraire_cs_orl = models.IntegerField("ORL = 13250", default=0)
    honoraire_cs_labo = models.IntegerField("Labo AMJ = 7122", default=0)
    honoraire_cs_lbx = models.IntegerField("Labstix = 2337", default=0)
    honoraire_cs_radio = models.IntegerField("Radio = 8400", default=0)
    honoraire_cs_toxique = models.IntegerField("Toxique = 17442", default=0)
    frais_dossier = models.IntegerField("Frais de dossier = 3000", default=3000)

    # Consultations
    cs_cempn = models.BooleanField(default=False)
    cs_oph = models.BooleanField(default=False)
    cs_orl = models.BooleanField(default=False)
    cs_labo = models.BooleanField(default=False)
    cs_lbx = models.BooleanField(default=False)
    cs_radio = models.BooleanField(default=False)
    cs_toxique = models.BooleanField(default=False)

    date_cempn = models.DateField(null=True, blank=True)
    date_cs_oph = models.DateField(null=True, blank=True)
    date_cs_orl = models.DateField(null=True, blank=True)
    date_cs_labo = models.DateField(null=True, blank=True)
    date_cs_lbx = models.DateField(null=True, blank=True)
    date_cs_radio = models.DateField(null=True, blank=True)
    date_cs_toxique = models.DateField(null=True, blank=True)

    medecin_cempn = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='evenements_cempn')
    medecin_oph = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='evenements_oph')
    medecin_orl = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='evenements_orl')
    medecin_radio = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='evenements_radio')
    medecin_labo = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='evenements_labo', verbose_name="Médecin laboratoire")

    #recherche_toxique = models.BooleanField(default=False)
    quote_part_patient = models.BooleanField(default=False)
    paye_par_patient = models.IntegerField(default=0)

    # Variables relatives à la recherche toxique
    #cs_toxique = models.BooleanField("Recherche toxique", default=False)
    #date_cs_toxique = models.DateField("Date de la recherche toxique", null=True, blank=True)
    #honoraire_cs_toxique = models.IntegerField("Honoraire de la recherche toxique", default=0)


    total = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calcul du total
        self.total = (
            (self.honoraire_cempn or 0) +
            (self.honoraire_cs_oph or 0) +
            (self.honoraire_cs_orl or 0) +
            (self.honoraire_cs_labo or 0) +
            (self.honoraire_cs_lbx or 0) +
            (self.honoraire_cs_radio or 0) +
            (self.honoraire_cs_toxique or 0) +
            (self.frais_dossier or 0)
        )

        if self.quote_part_patient:
            self.paye_par_patient = self.total
        else:
            self.paye_par_patient = 0

        # Génération auto du numéro de facture
        if not self.no_facture:
            d = self.date_evenement or timezone.now().date()
            prefix = f"{d.year}E{d.month:02d}."
            # chercher toutes les factures commençant par ce préfixe
            same_month = FicheEvenement.objects.filter(
                no_facture__startswith=prefix
            ).values_list('no_facture', flat=True)

            # extraire la partie numérique entre le point et la barre oblique
            numbers = [
                int(re.search(r"\.(\d+)/", inv).group(1))
                for inv in same_month
                if re.search(r"\.(\d+)/", inv)
            ]
            next_seq = (max(numbers) if numbers else 0) + 1
            self.no_facture = f"{prefix}{next_seq:02d}/01"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Facture {self.no_facture} - {self.personnel.nom}"

class FactureMedecin(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    bordereau = models.ForeignKey(Bordereau, on_delete=models.CASCADE, related_name='factures_medecins')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Facture pour {self.medecin} - {self.bordereau.no_bordereau}"
