# Hackathon PayShield - Plan de Projet

## Informations Generales

- **Duree** : 48 heures
- **Equipe** : Dara (Dev), David (Data), Jordan & Cedric (Cybersec)
- **Livrable** : Soutenance 10 min + demo code + 6 slides

---

## Phase 1 : IMPLEMENT

### 1.1 Setup du projet
- [ ] Creer l'environnement Python
- [ ] Installer les dependances (`pandas`, `numpy`)
- [ ] Creer le script principal `scoring.py`

### 1.2 Lecture des donnees
- [ ] Charger `payshield_vulns.csv` avec pandas
- [ ] Charger `payshield_infrastructure.csv` (pour reference)
- [ ] Verifier les colonnes : id, ip, port, service, version, cvss, cve, epss, exposition, criticite, donnees, description, kev

### 1.3 Calcul du Score de Risque Contextuel (SRC)
- [ ] Implementer les ponderations :
  ```
  W_exposition : Internet=2.0 | DMZ=1.5 | Interne=1.0
  W_criticite  : Critique=2.0 | Elevee=1.5 | Moyenne=1.0 | Faible=0.5
  W_donnees    : Sensible=1.5 | Interne=1.0 | Public=0.5
  ```
- [ ] Appliquer la formule : `SRC = CVSS x W_exposition x W_criticite x W_donnees`
- [ ] Normaliser entre 0 et 10 : `SRC_norm = SRC / max(SRC) x 10`

### 1.4 Affichage des resultats
- [ ] Afficher le **Top 10** par ordre decroissant
- [ ] Afficher un **resume par hote** : score max, nombre de vulnerabilites

---

## Phase 2 : ANALYSE

### 2.1 Articuler la problematique
- [ ] Rediger en 3 phrases : quel probleme, pourquoi il existe, comment on y repond
- [ ] Expliquer pourquoi le CVSS seul ne suffit pas

### 2.2 Experience A - Tester 2 configs de ponderation
- [ ] Implementer Config Base :
  ```python
  {'Internet':2.0, 'DMZ':1.5, 'Interne':1.0,
   'Critique':2.0, 'Elevee':1.5, 'Moyenne':1.0, 'Faible':0.5,
   'Sensible':1.5, 'Interne_d':1.0, 'Public':0.5}
  ```
- [ ] Implementer Config Alternative :
  ```python
  {'Internet':3.0, 'DMZ':1.5, 'Interne':0.5,
   'Critique':1.5, 'Elevee':1.2, 'Moyenne':1.0, 'Faible':0.3,
   'Sensible':2.0, 'Interne_d':1.0, 'Public':0.2}
  ```
- [ ] Comparer les Top 10 : combien de positions changent ?
- [ ] Documenter les differences

### 2.3 Experience B - Identifier une anomalie
- [ ] Analyser **V05** : PostgreSQL sans MDP, CVSS 10, BDD paiement, Interne
  - Ou est-il dans le Top 10 ? Est-ce logique ?
- [ ] Analyser **V35** : Confluence RCE, CVSS 10, EPSS 0.94, Interne, Criticite Moyenne
  - L'algo tient-il compte de l'EPSS 0.94 (94% proba exploitation) ?
- [ ] Proposer une correction argumentee

---

## Phase 3 : IMPROVE

### Option A - Integrer l'EPSS (recommande)
- [ ] Nouvelle formule : `SRC_v2 = SRC x (1 + epss)`
- [ ] Recuperer la colonne `epss` du dataframe
- [ ] Appliquer le facteur multiplicatif
- [ ] Renormaliser entre 0 et 10
- [ ] Comparer Top 10 avant/apres

### Option B - Penalite KEV (alternative)
- [ ] Nouvelle formule : `SRC_v2 = SRC x (1 + 1.5 x kev)`
- [ ] Recuperer la colonne `kev` (0 ou 1)
- [ ] Appliquer le multiplicateur (kev=1 -> score x2.5)
- [ ] Renormaliser entre 0 et 10
- [ ] Identifier quelles CVE KEV remontent

---

## Phase 4 : EXTRA (Bonus)

### Extra 50% - Rapport HTML
- [ ] Generer `rapport.html` avec :
  - En-tete : nom cible, date, resume executif (3 phrases)
  - Tableau Top 10 : rang, IP, service, CVE, score, criticite
  - Top 3 detaille : section Impact et Recommandation
  - Pied de page : plan remediation J+7 / J+30 / J+90

### Extra 100% - Combiner EPSS + KEV
- [ ] Formule : `SRC_v3 = SRC x (1 + epss) x (1 + 1.5 x kev)`
- [ ] Comparer 3 Top 10 cote a cote :
  - SRC base
  - SRC + EPSS
  - SRC + EPSS + KEV
- [ ] Preparer demo live

---

## Phase 5 : SLIDES (6 obligatoires)

| # | Titre | Contenu |
|---|-------|---------|
| 1 | Contexte PayShield | Qui est PayShield ? Risques ? Pourquoi un algo de scoring ? |
| 2 | Notre formule SRC | 3 facteurs, coefficients, justification metier |
| 3 | Top 10 - Resultats | Graphique, 3 vulns prioritaires expliquees |
| 4 | Problematique + Analyse | CVSS insuffisant, Experience A/B, 1 anomalie |
| 5 | Notre amelioration | Option choisie, Top 10 avant/apres, limites |
| 6 | Plan J+7 PayShield | 3 actions immediates, responsable, impact si non fait |

---

## Repartition des taches

### Bloc 1 - Jour 1 (mise en place)
| Qui | Quoi |
|-----|------|
| Dara (Dev) | Structure Python, lecture CSV, script principal |
| David (Data) | Calcul SRC, normalisation, Top 10 |
| Jordan & Cedric (Cybersec) | Justification coefficients, analyse V05/V35, argumentation |

### Bloc 2 - Soir/Nuit (amelioration)
- [ ] Integrer option choisie (EPSS ou KEV)
- [ ] Comparer Top 10 avant/apres
- [ ] Commencer les slides

### Bloc 3 - Jour 2 matin (finition)
- [ ] Finaliser les slides
- [ ] Repetition orale (chacun defend sa partie)
- [ ] Preparer la demo live

---

## Vulnerabilites cles a connaitre

| ID | Hote | CVE | CVSS | Description | Point d'attention |
|----|------|-----|------|-------------|-------------------|
| V01 | pay-api | CVE-2014-0160 | 10.0 | Heartbleed | Internet + Critique + KEV |
| V02 | pay-api | CVE-2021-41773 | 9.8 | Apache RCE | Internet + Critique + KEV |
| V05 | db-prod | - | 10.0 | PostgreSQL sans MDP | Interne mais BDD paiement ! |
| V21 | fw-01 | CVE-2021-41282 | 9.8 | pfSense injection | Firewall principal + KEV |
| V25 | monitoring | CVE-2021-43798 | 9.8 | Grafana path traversal | KEV |
| V35 | auth-srv | CVE-2023-22527 | 10.0 | Confluence RCE | EPSS 0.94 + KEV |

---

## Checklist finale

- [ ] Le script Python fonctionne sans erreur
- [ ] Top 10 affiche correctement
- [ ] Anomalie V05/V35 analysee et expliquee
- [ ] Amelioration implementee (EPSS ou KEV)
- [ ] 6 slides pretes
- [ ] Demo live testee
- [ ] Chaque membre sait defendre sa partie
