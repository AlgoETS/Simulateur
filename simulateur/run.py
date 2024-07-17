import sys
import os
import django

if __name__ == '__main__':
    # insert here whatever commands you use to run daphne
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simulateur.settings")

    sys.argv = ['daphne', 'simulateur.asgi:application', '-b', '0.0.0.0', '-p', '8000']
    from daphne.cli import CommandLineInterface
    django.setup()
    CommandLineInterface.entrypoint()
