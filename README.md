# Markdown to HTML

Cette application Flask permet de convertir du Markdown en HTML et d'en avoir un aperçu en temps réel. Elle fournit une interface web simple où l'on peut saisir du Markdown à gauche et obtenir l'HTML généré à droite.

## Installation

1. (Recommandé) Créez un environnement virtuel `venv` et activez-le :
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Installez les dépendances :
   
   ```bash
   pip install -r requirements.txt
   ```

## Lancement de l'application

Exécutez le fichier `app.py` avec Python :

```bash
python app.py
```

Par défaut, l'application démarre en mode développement sur l'adresse `http://127.0.0.1:5000/`. Ouvrez ce lien dans votre navigateur pour accéder à l'interface.

## Utilisation

- Saisissez votre Markdown dans la zone de texte de gauche.
- L'aperçu HTML est généré automatiquement dans la zone de droite.
- Vous pouvez copier le résultat HTML en cliquant sur le bouton « Copier le HTML ».

## Personnalisation

Le convertisseur Markdown est implémenté dans la fonction `simple_markdown_to_html` du fichier `app.py`. 
Elle est adaptable pour prendre en charge d'autres éléments Markdown ou modifier le rendu HTML.

## Technologies utilisées

Le projet repose sur **Flask** pour la création du serveur web et sur un petit moteur de conversion écrit en Python. L'interface HTML et le JavaScript fourni permettent un aperçu en temps réel du rendu. 
Au-delà du simple script attendu, cette version propose une interface enrichie qui facilite l'expérimentation et la compréhension du rendu HTML en temps réel.

## Détails techniques

- **Routes Flask** : l'application définit deux routes principales. `/` sert la page d'interface tandis que `/convert` reçoit le Markdown en AJAX et renvoie l'HTML généré sous forme JSON.
- **Conversion** : la fonction `simple_markdown_to_html` analyse chaque ligne de Markdown et construit l'HTML progressivement. Elle gère entre autres les titres, listes, citations, blocs de code, tableaux et liens.
- **Mise à jour en direct** : dans `static/script.js`, un écouteur sur la zone de texte envoie le contenu au serveur à chaque modification puis insère l'HTML obtenu dans la zone d'aperçu.
- **Interface statique** : le fichier `templates/index.html` présente deux panneaux côte à côte, stylisés par `static/style.css`, pour saisir le Markdown et consulter le résultat.
