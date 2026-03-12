# Procédures de Notification de Violation de Données Personnelles

## RGPD — Articles 33 et 34 — Obligations des Responsables de Traitement et Sous-traitants

### 1. Cadre Légal et Définitions

Une **violation de données personnelles** se définit, au sens de l'article 4 paragraphe 12 du RGPD, comme « une violation de la sécurité entraînant, de manière accidentelle ou illicite, la destruction, la perte, l'altération, la divulgation non autorisée de données à caractère personnel transmises, conservées ou traitées d'une autre manière, ou l'accès non autorisé à de telles données ».

Trois types de violations sont distingués :
- **Violation de confidentialité** : divulgation ou accès à des données par des personnes non autorisées
- **Violation d'intégrité** : modification non autorisée ou accidentelle de données
- **Violation de disponibilité** : perte d'accès ou destruction de données (accidentelle ou non)

### 2. Obligations du Responsable de Traitement

**Notification à l'autorité de contrôle (article 33 du RGPD)**

En cas de violation susceptible d'engendrer un risque pour les droits et libertés des personnes concernées, le responsable de traitement doit notifier la violation à la CNIL **dans les 72 heures** suivant sa découverte.

La notification doit contenir :
- La nature de la violation (confidentialité, intégrité, disponibilité)
- Les catégories et le nombre approximatif de personnes concernées
- Les catégories et le nombre approximatif d'enregistrements de données concernés
- Le nom et les coordonnées du délégué à la protection des données (DPO) ou d'un autre point de contact
- La description des conséquences probables de la violation
- Les mesures prises ou envisagées pour remédier à la violation et en atténuer les effets

Si toutes les informations ne sont pas disponibles dans ce délai, une notification initiale partielle est admise, complétée par des informations supplémentaires sans délai excessif.

**Communication aux personnes concernées (article 34 du RGPD)**

Lorsque la violation est susceptible d'engendrer un risque **élevé** pour les droits et libertés des personnes physiques, le responsable de traitement doit également informer les personnes concernées **dans les meilleurs délais**.

Cette communication doit être rédigée en langage clair et simple, et comporter :
- La nature de la violation
- Les coordonnées du DPO
- Les conséquences probables de la violation
- Les mesures prises ou recommandées aux personnes concernées pour se protéger

La communication n'est pas requise si des mesures techniques et organisationnelles appropriées avaient été mises en œuvre rendant les données incompréhensibles (chiffrement), si des mesures ultérieures éliminent le risque élevé, ou si une communication individuelle nécessiterait des efforts disproportionnés (communication publique possible).

### 3. Obligations du Sous-traitant

Le sous-traitant doit notifier toute violation au responsable de traitement **dans les meilleurs délais** après en avoir pris connaissance (article 33, paragraphe 2 du RGPD). Cette obligation doit être expressément prévue dans le contrat de sous-traitance (article 28 du RGPD). Le sous-traitant doit assister le responsable de traitement pour que ce dernier puisse respecter ses propres obligations de notification dans le délai de 72 heures.

### 4. Documentation Interne Obligatoire

Le responsable de traitement doit tenir un **registre interne de toutes les violations**, y compris celles ne nécessitant pas de notification à la CNIL. Ce registre documente :
- La date et l'heure de la découverte de la violation
- La description des faits
- Les effets et conséquences probables
- Les mesures correctives prises
- La justification de la décision de notifier ou non

Ce registre doit être conservé et mis à disposition de la CNIL lors des contrôles.

### 5. Procédure de Réponse aux Incidents — Bonnes Pratiques

**Phase de détection et qualification**
- Mise en place de systèmes de détection (SIEM, alertes anomalies)
- Procédure de remontée des incidents au DPO et au RSSI
- Grille de qualification du niveau de risque (faible / moyen / élevé / critique)

**Phase de confinement**
- Isolation des systèmes compromis
- Révocation des accès compromis
- Préservation des preuves (logs, captures mémoire)

**Phase de notification**
- Préparation du dossier de notification CNIL via le portail notifications.cnil.fr
- Rédaction du message aux personnes concernées si nécessaire
- Contact avec les partenaires et sous-traitants impliqués

**Phase de remédiation**
- Correction des failles exploitées
- Renforcement des mesures de sécurité
- Rapport post-incident et retour d'expérience

### 6. Sanctions en Cas de Non-Notification

Le non-respect de l'obligation de notification peut entraîner des amendes administratives pouvant atteindre **10 millions d'euros** ou **2 % du chiffre d'affaires annuel mondial**, selon le montant le plus élevé. La CNIL a sanctionné plusieurs entreprises pour notification tardive ou incomplète, notamment dans les secteurs de la santé, de la banque et du e-commerce.
