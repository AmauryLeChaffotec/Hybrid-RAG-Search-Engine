# Mandat de Facturation Électronique en France — Réforme 2024-2026

## Ordonnance n° 2021-1190 du 15 septembre 2021 et Arrêté du 7 octobre 2022

### 1. Contexte et Objectifs de la Réforme

La réforme de la facturation électronique obligatoire entre entreprises (B2B domestique) constitue l'une des transformations les plus structurantes pour les entreprises françaises depuis l'introduction de la TVA. Initiée par la loi de finances pour 2020 (article 153), elle a été précisée par l'ordonnance n° 2021-1190 et l'arrêté du 7 octobre 2022 définissant les données à transmettre.

Les deux objectifs principaux de cette réforme sont :
1. **Lutter contre la fraude à la TVA** estimée à environ 15 milliards d'euros par an en France
2. **Simplifier les obligations déclaratives** grâce au pré-remplissage des déclarations de TVA à partir des données de facturation

### 2. Calendrier de Déploiement

En raison de la complexité technique du projet, le calendrier initial a été revu. Le nouveau calendrier est le suivant :

| Date | Obligation |
|---|---|
| **1er septembre 2026** | Obligation de réception pour toutes les entreprises + obligation d'émission pour les grandes entreprises |
| **1er septembre 2027** | Obligation d'émission pour les entreprises de taille intermédiaire (ETI) |
| **1er septembre 2027** | Obligation d'émission pour les PME et micro-entreprises |

Toutes les entreprises assujetties à la TVA en France seront concernées, quel que soit leur secteur d'activité, dès lors que leurs transactions sont réalisées avec d'autres entreprises établies en France.

### 3. Architecture du Système

**Le Portail Public de Facturation (PPF)**
Géré par l'AIFE (Agence pour l'Informatique Financière de l'État), le PPF est la colonne vertébrale publique du dispositif. Il assure :
- L'annuaire des entreprises (répertoire des identifiants de routage)
- La transmission des données de facturation à l'administration fiscale (DGFiP)
- Un service de facturation de base pour les entreprises ne souhaitant pas passer par une PDP

**Les Plateformes de Dématérialisation Partenaires (PDP)**
Les PDP sont des opérateurs privés immatriculés par l'administration fiscale. Elles proposent des services à valeur ajoutée : archivage légal, intégration ERP, rapprochement automatique, gestion des statuts de cycle de vie. Chaque entreprise doit choisir au moins une PDP ou utiliser le PPF.

### 4. Formats de Facturation Obligatoires

Trois formats structurés sont acceptés par le dispositif :

**Factur-X**
Format hybride franco-allemand combinant un PDF/A-3 lisible par l'humain et un fichier XML structuré selon la norme EN 16931. Il est particulièrement adapté aux PME souhaitant une transition progressive.

**UBL 2.1 (Universal Business Language)**
Format XML international standardisé par l'OASIS. Très répandu dans les pays nordiques et en Allemagne, il est utilisé pour les marchés publics européens.

**CII (Cross Industry Invoice)**
Format XML développé sous l'égide de l'ONU/CEFACT. Compatible avec les normes comptables internationales, il est préféré par les grandes entreprises industrielles.

### 5. Données Obligatoires à Transmettre (e-reporting)

Au-delà des mentions légales classiques, la réforme impose la transmission de données de transaction pour les opérations non couvertes par la facturation électronique B2B (B2C, opérations avec l'étranger) :
- Montant de la transaction
- Montant de TVA collectée par taux
- Date de l'opération
- Identifiant acheteur si disponible

Ces données doivent être transmises à l'administration dans des délais stricts (10 jours pour les opérations B2C).

### 6. Cycle de Vie de la Facture

La réforme introduit des statuts obligatoires de cycle de vie que les plateformes doivent gérer et communiquer :
- **Déposée** : la facture a été soumise à la plateforme
- **Rejetée** : erreur de format ou données manquantes détectées
- **Mise à disposition** : la facture est disponible pour le destinataire
- **Prise en charge** : le destinataire a accusé réception
- **Approuvée** / **Refusée** : décision du destinataire
- **Approuvée partiellement** : en cas de litige partiel

### 7. Impact sur les Entreprises

Les entreprises doivent engager plusieurs chantiers :
- **Audit des processus actuels** de facturation (émission, réception, archivage)
- **Sélection et contractualisation** avec une ou plusieurs PDP
- **Adaptation des ERP** et systèmes comptables pour produire les formats requis
- **Formation des équipes** comptables et financières
- **Révision des conditions générales** de vente pour intégrer les nouvelles modalités

Les entreprises qui n'auront pas adapté leurs systèmes à la date d'entrée en vigueur s'exposent à des amendes et au risque de ne pas pouvoir émettre ou recevoir de factures valides.
