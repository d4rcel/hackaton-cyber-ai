import pandas as pd
import matplotlib.pyplot as plt

# === 1. POIDS DE PONDÉRATION ===
W_EXPOSITION = {"Internet": 2.0, "DMZ": 1.5, "Interne": 1.0}
W_CRITICITE  = {"Critique": 2.0, "Élevée": 1.5, "Moyenne": 1.0, "Faible": 0.5}
W_DONNEES    = {"Sensible": 1.5, "Interne": 1.0, "Public": 0.5}

SRC_MAX_THEORIQUE = 10.0 * 2.0 * 2.0 * 1.5  # = 60.0

# === 2. CHARGEMENT DES DONNÉES ===
vulns = pd.read_csv("data/payshield_vulns.csv")
infra = pd.read_csv("data/payshield_infrastructure.csv")

# === 3. CALCUL DU SRC ===
vulns["w_exposition"] = vulns["exposition"].map(W_EXPOSITION)
vulns["w_criticite"]  = vulns["criticite"].map(W_CRITICITE)
vulns["w_donnees"]    = vulns["donnees"].map(W_DONNEES)

vulns["src"]      = vulns["cvss"] * vulns["w_exposition"] * vulns["w_criticite"] * vulns["w_donnees"]
vulns["src_norm"] = (vulns["src"] / SRC_MAX_THEORIQUE * 10).round(2)

# === 4. TOP 10 ===
top10 = (
    vulns[["id", "ip", "service", "cve", "cvss", "exposition", "criticite", "donnees", "src_norm", "description"]]
    .sort_values("src_norm", ascending=False)
    .head(10)
    .reset_index(drop=True)
)
top10.index += 1

print("=" * 80)
print("TOP 10 VULNÉRABILITÉS — Score de Risque Contextuel (SRC normalisé)")
print("=" * 80)
print(top10[["id", "ip", "service", "cve", "cvss", "src_norm", "description"]].to_string())
print()

plt.bar(top10["id"], top10["src_norm"], palette="dark")
plt.show()


# === 5. RÉSUMÉ PAR HÔTE ===
resume = (
    vulns.groupby("ip")
    .agg(
        src_max=("src_norm", "max"),
        nb_vulns=("id", "count")
    )
    .reset_index()
)

resume = resume.merge(
    infra[["ip", "nom", "role"]],
    on="ip",
    how="left"
)

resume = resume.sort_values("src_max", ascending=False).reset_index(drop=True)
resume.index += 1

print("=" * 80)
print("RÉSUMÉ PAR HÔTE")
print("=" * 80)
print(resume[["ip", "nom", "role", "src_max", "nb_vulns"]].to_string())
print()
