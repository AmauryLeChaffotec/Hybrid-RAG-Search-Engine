# Règles de Conservation des Données Personnelles — RGPD

## Règlement (UE) 2016/679 — Règlement Général sur la Protection des Données

### 1. Présentation et Cadre Légal

Le Règlement Général sur la Protection des Données (RGPD), entré en application le 25 mai 2018, impose aux responsables de traitement et à leurs sous-traitants de ne pas conserver les données personnelles au-delà de la durée strictement nécessaire aux finalités pour lesquelles elles ont été collectées. Ce principe de limitation de la conservation est consacré à l'article 5, paragraphe 1, point e) du RGPD.

En France, la Commission Nationale de l'Informatique et des Libertés (CNIL) est l'autorité de contrôle chargée de veiller au respect de ces obligations. Elle publie régulièrement des référentiels sectoriels précisant les durées de conservation recommandées ou imposées par secteur.

### 2. Principe de Limitation de la Conservation

Le RGPD impose que les données personnelles soient :
- **Conservées sous une forme permettant l'identification** des personnes concernées pendant une durée n'excédant pas celle nécessaire au regard des finalités du traitement
- **Supprimées ou anonymisées** dès que la finalité du traitement est atteinte ou que la base légale cesse d'exister

Toute prolongation de la durée de conservation doit être justifiée par une obligation légale, un intérêt public, ou un intérêt légitime prépondérant du responsable de traitement dûment documenté.

### 3. Durées de Conservation par Catégorie

**Données clients et prospects**
- Données de clients actifs : durée de la relation commerciale + 3 ans pour la prospection commerciale
- Données de prospects n'ayant pas donné suite : 3 ans à compter du dernier contact
- Contrats commerciaux : 5 ans après expiration (prescription de droit commun)
- Enregistrements d'appels téléphoniques au service client : 6 mois maximum

**Données de ressources humaines**
- Dossiers des salariés en poste : durée de la relation de travail + 5 ans
- Données de candidats non retenus : 2 ans maximum (sauf accord du candidat pour une durée plus longue)
- Bulletins de paie : 5 ans (prescription des créances salariales)
- Données de vidéosurveillance en entreprise : 30 jours maximum sauf incident constaté
- Données relatives aux accidents du travail et maladies professionnelles : 40 ans minimum (risques différés)

**Données de santé**
- Dossiers médicaux patients : 20 ans à compter du dernier acte médical (article R. 1112-7 du Code de la santé publique)
- Données de médecine du travail : 10 ans après la fin d'exposition pour les risques professionnels

**Données financières et comptables**
- Pièces comptables justificatives : 10 ans (article L. 123-22 du Code de commerce)
- Documents fiscaux : 6 ans pour les contrôles fiscaux (article L. 169 du Livre des procédures fiscales)
- Preuves de transaction et relevés bancaires : 10 ans

**Données de connexion et logs**
- Logs d'accès aux systèmes d'information à des fins de sécurité : 6 mois à 1 an selon les contextes
- Données de navigation et cookies de traçage : 13 mois maximum (recommandation CNIL 2020)

### 4. Obligation de Documentation

Chaque responsable de traitement doit tenir un **registre des activités de traitement** (article 30 RGPD) mentionnant pour chaque traitement :
- Les finalités du traitement
- Les catégories de données traitées
- Les durées de conservation prévues
- Les mesures de sécurité mises en œuvre

Ce registre doit être tenu à jour et mis à disposition de la CNIL sur simple demande lors d'un contrôle.

### 5. Archivage Intermédiaire et Suppression

Le RGPD reconnaît trois phases de conservation :
1. **Conservation active** : les données sont nécessaires à l'activité courante et accessibles à tous les utilisateurs habilités
2. **Archivage intermédiaire** : les données ne sont plus utiles au quotidien mais doivent être conservées pour des raisons légales ou probatoires ; l'accès est restreint au service juridique ou à la direction
3. **Archivage définitif ou suppression** : conservation à valeur historique, scientifique ou statistique, ou destruction sécurisée en fin de délai

La suppression doit être effective et irréversible. La destruction des supports physiques (disques durs, clés USB) doit suivre la norme DIN 66399 ou équivalente.

### 6. Droit à l'Effacement (« Droit à l'Oubli »)

L'article 17 du RGPD confère aux personnes concernées le droit d'obtenir l'effacement de leurs données sans délai excessif lorsque :
- Les données ne sont plus nécessaires à la finalité pour laquelle elles ont été collectées
- La personne retire son consentement et il n'existe pas d'autre base légale
- La personne s'oppose au traitement et il n'existe pas de motif légitime prépondérant
- Les données ont fait l'objet d'un traitement illicite

Les exceptions à ce droit incluent notamment : les obligations légales de conservation, les litiges en cours, les motifs d'intérêt public.

### 7. Mesures Techniques de Mise en Conformité

- **Purges automatiques** : configuration de jobs de suppression automatique au sein des bases de données
- **Étiquetage des données** : classification des données avec leur catégorie de rétention et leur date d'expiration
- **Journaux d'audit** : traçabilité des opérations de suppression pour démontrer la conformité
- **Sauvegardes** : les copies de sauvegarde doivent être soumises aux mêmes règles de conservation ; les sauvegardes archivées contenant des données expirées doivent être purgées dans un délai raisonnable

### 8. Sanctions

Le non-respect des règles de conservation peut entraîner des amendes administratives pouvant atteindre **20 millions d'euros** ou **4 % du chiffre d'affaires annuel mondial**, selon le montant le plus élevé. La CNIL a sanctionné plusieurs entreprises pour conservation excessive de données dans les secteurs de la grande distribution, des télécommunications, des ressources humaines et de la santé.
