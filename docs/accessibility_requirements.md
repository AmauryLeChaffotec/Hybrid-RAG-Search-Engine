# Exigences d'Accessibilité Numérique

## Directive (UE) 2016/2102 sur l'Accessibilité Web et Loi du 11 février 2005 pour l'égalité des droits

### 1. Présentation du Cadre Légal

L'accessibilité numérique désigne la capacité des sites web, applications mobiles et logiciels à être utilisés par toutes les personnes, y compris celles en situation de handicap (visuel, auditif, moteur, cognitif). En Europe, la directive 2016/2102 impose aux organismes du secteur public des obligations d'accessibilité depuis 2019-2020. La directive sur l'accessibilité des produits et services (European Accessibility Act — EAA, directive 2019/882) étend ces obligations au secteur privé à partir du 28 juin 2025.

En France, l'obligation d'accessibilité numérique repose sur l'article 47 de la loi du 11 février 2005 pour l'égalité des droits et des chances, modifié par la loi pour une République Numérique de 2016. Le référentiel technique de référence est le **RGAA** (Référentiel Général d'Amélioration de l'Accessibilité), dont la version 4.1 est en vigueur depuis 2021.

### 2. Entités Concernées

**Secteur public (depuis 2019-2020)**
- Services de l'État et opérateurs de l'État
- Collectivités territoriales et leurs groupements
- Établissements publics
- Organismes de droit privé remplissant une mission de service public

**Secteur privé (à partir du 28 juin 2025)**
Les entreprises de plus de 10 salariés et réalisant un chiffre d'affaires supérieur à 2 millions d'euros devront rendre accessibles :
- Les services bancaires aux consommateurs (sites web et applications)
- Les terminaux de paiement et distributeurs automatiques
- Les services de transport (billetterie, informations en temps réel)
- Les services de commerce électronique (sites de vente en ligne)
- Les livres électroniques et logiciels de lecture
- Les services de communications électroniques

### 3. Standards Techniques : Les WCAG

Les **Web Content Accessibility Guidelines (WCAG)**, développées par le W3C, constituent la référence internationale. La directive européenne impose le respect des WCAG 2.1 niveau AA. Les WCAG 2.2, publiées en octobre 2023, ajoutent 9 nouveaux critères de succès.

Les WCAG sont organisées autour de **4 principes** (POUR) :

**Perceptible**
- Fournir des alternatives textuelles à tout contenu non textuel (images, boutons graphiques)
- Proposer des sous-titres pour les vidéos et des alternatives audio pour les contenus audio
- Assurer un contraste suffisant entre le texte et son arrière-plan (ratio minimum 4,5:1 pour le texte normal, 3:1 pour le grand texte)
- Permettre le redimensionnement du texte jusqu'à 200 % sans perte de contenu

**Utilisable**
- Rendre toutes les fonctionnalités accessibles au clavier (sans souris)
- Donner aux utilisateurs suffisamment de temps pour lire et utiliser le contenu
- Ne pas concevoir de contenu susceptible de provoquer des crises d'épilepsie (pas de clignotement > 3 fois/seconde)
- Aider les utilisateurs à naviguer et à trouver le contenu (titres, liens descriptifs, fil d'Ariane)

**Compréhensible**
- Rendre le texte lisible et compréhensible (langue du document déclarée, abréviations expliquées)
- Permettre aux utilisateurs d'éviter et de corriger leurs erreurs dans les formulaires
- Assurer la cohérence de la navigation et de l'identification des composants

**Robuste**
- Maximiser la compatibilité avec les technologies d'assistance actuelles et futures (lecteurs d'écran, plages Braille, commandes vocales)
- Utiliser du HTML sémantique valide

### 4. Obligations Déclaratives

**Déclaration d'accessibilité**
Toute entité concernée doit publier une déclaration d'accessibilité sur son site ou son application. Cette déclaration mentionne :
- Le niveau de conformité atteint (non conforme / partiellement conforme / totalement conforme)
- Les contenus non accessibles et leurs justifications
- Les dérogations (charge disproportionnée, contenu tiers non modifiable)
- Les alternatives accessibles disponibles
- Les coordonnées pour signaler un problème et demander une alternative

**Schéma pluriannuel d'accessibilité**
Les administrations publiques doivent publier un plan pluriannuel de mise en accessibilité précisant les actions prévues et le calendrier de leur réalisation.

### 5. Contrôle et Sanctions

**Mécanisme de signalement**
Tout utilisateur peut signaler une difficulté d'accessibilité. En l'absence de réponse satisfaisante dans un délai de deux mois, il peut saisir le Défenseur des droits.

**Contrôle**
La Direction Générale de la Cohésion Sociale (DGCS) et les directions régionales peuvent effectuer des contrôles. Le RGAA prévoit des audits de conformité basés sur 106 critères répartis en 13 thématiques.

**Amendes**
- Non-publication de la déclaration d'accessibilité : **2 000 € par service** en défaut
- Non-conformité persistante après mise en demeure : jusqu'à **20 000 € par an**

### 6. Bonnes Pratiques de Mise en Œuvre

Pour atteindre la conformité RGAA/WCAG 2.1 AA, les équipes de développement doivent :
- Intégrer l'accessibilité dès la phase de conception (accessibility by design)
- Utiliser des composants HTML natifs sémantiquement corrects avant tout recours à des solutions JavaScript personnalisées
- Tester avec de vrais lecteurs d'écran (NVDA, JAWS, VoiceOver)
- Impliquer des utilisateurs en situation de handicap dans les tests utilisateurs
- Former régulièrement les équipes de développement, design et rédaction
