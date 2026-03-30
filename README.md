# Hackathon Cybersécurité — Gestion des Vulnérabilités Assistée par IA

**Référentiel T-NOC | PayShield Fintech | Master Cybersécurité**

## Contexte

PayShield est une fintech béninoise spécialisée dans les paiements digitaux en Afrique de l'Ouest (280 employés, 15 000 transactions/jour, 1,2M utilisateurs). Suite à une alerte CERT, un scan complet (Nessus + OpenVAS) a identifié **35 vulnérabilités sur 10 systèmes**.

L'objectif : construire un **outil Python de scoring de vulnérabilités assisté par IA** qui va au-delà du score CVSS brut en intégrant le contexte métier de PayShield.

## Équipe

| Rôle | Personne | Responsabilité |
|------|----------|----------------|
| Dev | Dara | Scaffolding Python, lecture CSV (pandas), script principal, rapport HTML (bonus) |
| Data | David | Calcul du SRC, normalisation, Top 10 |
| Cybersec | Jordan & Cédric | Justification des coefficients, analyse des anomalies (V05/V35), slides |

## Référentiel T-NOC

Le travail est découpé en 4 niveaux progressifs :

### Implement — Script de scoring SRC

Le **Score de Risque Contextuel (SRC)** enrichit le CVSS brut avec 3 facteurs contextuels :

```
SRC(v) = CVSS(v) × W_exposition × W_criticité × W_données

W_exposition : Internet = 2.0 | DMZ = 1.5 | Interne = 1.0
W_criticité  : Critique = 2.0 | Élevée = 1.5 | Moyenne = 1.0 | Faible = 0.5
W_données    : Sensible = 1.5 | Interne = 1.0 | Public = 0.5

SRC_norm = SRC / max(SRC) × 10   (normalisé 0–10)
```

Le script doit :
1. Lire `payshield_vulns.csv` avec pandas
2. Calculer le SRC pour chaque vulnérabilité
3. Normaliser les scores entre 0 et 10
4. Afficher le Top 10 par ordre décroissant
5. Afficher un résumé par hôte (score max, nombre de vulnérabilités)

### Analyse — Challenger l'algorithme

Identifier les limites du CVSS brut via deux expériences :

- **Expérience A** : comparer deux jeux de coefficients (Config Base vs Config Alt) et observer l'impact sur le Top 10
- **Expérience B** : identifier des anomalies de classement (ex. V05 vs V35 — même CVSS 10, contextes très différents)

### Improve — Améliorer la formule

**Option A — Intégrer l'EPSS :**
```
SRC_v2 = SRC × (1 + epss)
```

**Option B — Pénalité exploitation active (CISA KEV) :**
```
SRC_v2 = SRC × (1 + 1.5 × kev)
```
_(kev = 1 → score × 2.5 ; kev = 0 → inchangé)_

### Extra (bonus)

- **Extra 50%** : Génération automatique d'un rapport HTML (en-tête, Top 10, impact/recommandation Top 3, plan de remédiation J+7/J+30/J+90)
- **Extra 100%** : Combiner EPSS + KEV :
  ```
  SRC_v3 = SRC × (1 + epss) × (1 + 1.5 × kev)
  ```

## Fichiers fournis

| Fichier | Description |
|---------|-------------|
| `data/payshield_vulns.csv` | 35 vulnérabilités, 13 colonnes (id, ip, port, service, version, cvss, cve, epss, exposition, criticite, donnees, description, kev) |
| `data/payshield_infrastructure.csv` | 10 systèmes, 12 colonnes (id, ip, nom, os, services, port_principaux, zone, criticite, donnees, role, employes_acces, conformite) |

## Infrastructure (10 systèmes)

| # | IP | Nom | OS | Services | Zone | Criticité | Données | Conformité |
|---|----|----|-----|----------|------|-----------|---------|------------|
| H01 | 10.0.0.10 | pay-api | Ubuntu 20.04 | Node.js 14 / HTTPS / Kubernetes | Internet | Critique | Sensible | PCI-DSS requis |
| H02 | 10.0.0.15 | db-prod | Debian 11 | PostgreSQL 12 | Interne | Critique | Sensible | PCI-DSS requis |
| H03 | 10.0.0.20 | web-front | Ubuntu 18.04 | Nginx 1.14 | Internet | Élevée | Interne | RGPD applicable |
| H04 | 10.0.0.25 | auth-srv | Ubuntu 20.04 | Keycloak 12 / **Confluence 7.13** | DMZ | Critique | Sensible | ISO 27001 cible |
| H05 | 10.0.0.30 | admin-panel | CentOS 7 | Apache 2.4 / MySQL 5.7 | Interne | Élevée | Interne | Audit interne annuel |
| H06 | 10.0.0.35 | mail-srv | Debian 10 | Postfix 3.4 | DMZ | Moyenne | Public | Aucune |
| H07 | 10.0.0.40 | fw-01 | FreeBSD 12 | pfSense 2.5 | Internet | Critique | Interne | ISO 27001 cible |
| H08 | 10.0.0.45 | monitoring | Ubuntu 20.04 | Grafana 8.0 | Interne | Moyenne | Interne | Aucune |
| H09 | 10.0.0.50 | backup | Ubuntu 20.04 | Bacula 9.4 | Interne | Élevée | Sensible | PCI-DSS requis |
| H10 | 10.0.0.55 | dev-env | Ubuntu 22.04 | Apache 2.4 / MySQL 8.0 | Interne | Faible | Public | Aucune |

## Structure de la soutenance (6 slides imposées)

| # | Titre | Contenu |
|---|-------|---------|
| 1 | Contexte PayShield | Présentation, risque, pourquoi un algorithme de scoring |
| 2 | Notre formule SRC | Les 3 facteurs, coefficients et justification métier |
| 3 | Top 10 — résultats | Graphique Top 10, 3 vulnérabilités prioritaires expliquées |
| 4 | Problématique + Analyse | Limites du CVSS seul, Expérience A ou B, 1 anomalie identifiée |
| 5 | Notre amélioration | Formule v2, Top 10 avant/après, limites |
| 6 | Plan J+7 pour PayShield | 3 actions immédiates, responsable, impact si non fait |

Soutenance : **10 min de présentation + 5 min de questions jury**

## Installation & lancement

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Outils autorisés

Python 3 · pandas · numpy · ChatGPT / Claude · VS Code
