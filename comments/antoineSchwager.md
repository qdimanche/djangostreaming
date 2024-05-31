À partir de l'initialisation de Quentin, j'ai fait une première version de l'application. Cette première version mono-page permettait déjà de récupérer des données à partir de l'API et de les enregistrer dans une base de données très simple. Sur ce premier jet, j'avais implémenté une option de filtrage des films via un script basique en JavaScript intégré directement dans le HTML, mais cette option ne sera pas conservée car hors sujet.

Après relecture du sujet, j'ai retravaillé le fonctionnement de l'application pour que lors d'une recherche d'un film non déjà connu en local, tous les résultats de l'API soient sauvegardés (un seul résultat était enregistré précédemment).

Une fois le cahier des charges complété, j'ai pu ensuite mettre en place une page de détails pour afficher un maximum d'informations provenant de l'API et j'en ai profité pour étoffer le modèle de la base de données.

Une autre fonctionnalité que j'ai voulu rajouter a été de pouvoir supprimer un film précédemment ajouté à la base de données.

À la fin du projet, nous avons rencontré un problème : les caractères spéciaux dans les titres des films lors des recherches auprès de la base de données empêchaient un résultat correct. J'ai donc mis en place différentes fonctions de filtrage pour résoudre ce problème.

Enfin, pour clore le projet, j'ai établi une documentation basique dans le README du projet.