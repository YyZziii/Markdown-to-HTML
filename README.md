+# Markdown to HTML
+
+Cette application Flask permet de convertir du Markdown en HTML et d'en avoir un aperçu en temps réel. Elle fournit une interface web simple où l'on peut saisir du Markdown à gauche et obtenir l'HTML généré à droite.
+
+## Installation
+
+1. (Recommandé) Créez un environnement virtuel `venv` et activez-le :
+   ```bash
+   python3 -m venv venv
+   source venv/bin/activate
+   ```
+2. Installez les dépendances :
+   ```bash
+   pip install -r requirements.txt
+   ```
+
+## Lancement de l'application
+
+Exécutez le fichier `app.py` avec Python :
+
+```bash
+python app.py
+```
+
+Par défaut, l'application démarre en mode développement sur l'adresse `http://127.0.0.1:5000/`. Ouvrez ce lien dans votre navigateur pour accéder à l'interface.
+
+## Utilisation
+
+- Saisissez votre Markdown dans la zone de texte de gauche.
+- L'aperçu HTML est généré automatiquement dans la zone de droite.
+- Vous pouvez copier le résultat HTML en cliquant sur le bouton « Copier le HTML ».
+
+## Personnalisation
+
+Le convertisseur Markdown est implémenté dans la fonction `simple_markdown_to_html` du fichier `app.py`. Vous pouvez l'adapter pour prendre en charge d'autres éléments Markdown ou modifier le rendu HTML.
+
+## Technologies utilisées
+
+Le projet repose sur **Flask** pour la création du serveur web et sur
+un petit moteur de conversion écrit en Python. L'interface HTML et le
+JavaScript fourni permettent un aperçu en temps réel du rendu. Ce
+projet illustre donc l'utilisation conjointe de Python et de technologies
+web légères pour transformer du Markdown en HTML.
+
+
