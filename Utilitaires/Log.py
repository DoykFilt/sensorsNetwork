import logging

from logging.handlers import RotatingFileHandler


class Singleton(object):
    """
        class Singleton

        Utilisée par la classe Log, permet de n'utiliser qu'une seule instance de la classe sur tout le projet

        Cette classe permet de gérer les logs de l'application

    """

    # Elements clé pour la création d'un singleton en python
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls].__init__()
        return cls._instances[cls]

    def __init__(self):
        """
            Constructeur de la classe, initialise la redirection des logs
        """

        # création de l'objet logger qui va nous servir à écrire dans les logs
        self.L_logger = logging.getLogger()
        # on met le niveau du logger à DEBUG, comme ça il écrit tout
        self.L_logger.setLevel(logging.DEBUG)

        # Si le log n'est pas déjà redirigé
        if not self.L_logger.hasHandlers():
            # création d'un formateur qui va ajouter le temps, le niveau
            # de chaque message quand on écrira un message dans le log
            L_formatter = logging.Formatter('%(asctime)s :: %(message)s')
            # création d'un handler qui va rediriger une écriture du log vers
            # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
            L_file_handler = RotatingFileHandler('activite.log', 'a', 1000000, 1)
            L_file_handler.setLevel(logging.DEBUG)
            L_file_handler.setFormatter(L_formatter)
            self.L_logger.addHandler(L_file_handler)

            # # création d'un second handler qui va rediriger chaque écriture de log
            # # sur la console
            # stream_handler = logging.StreamHandler()
            # stream_handler.setLevel(logging.DEBUG)
            # self.L_logger.addHandler(stream_handler)

    def Linfo(self, _texte):
        """
            Permet d'écrire un log de type info
            :param : _texte str
        """
        self.L_logger.info(_texte)

    def Lerror(self, _texte):
        """
            Permet d'écrire un log de type error
            :param : _texte str
        """
        self.L_logger.error(_texte)


class Log(Singleton):
    """
        class FileManager

        Classe appelée depuis l'extérieur. Hérite du singleton qui est la structure réelle de la classe

    """
    pass
