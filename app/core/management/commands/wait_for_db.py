""" 
Django command to wait for database to full load before running app services
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django Command to wait for database to be ready"""
    
    def handle(self, *args, **kwargs):
        """Entry point for command"""
        
        # Message to display on console as command is executed
        self.stdout.write("Waiting for database...")
        db_up = False
        
        while db_up == False: 
            try: 
                self.check(databases=['default']) # Will throw exception (Psycopg2Error or OperationalError) if not ready 
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(self.style.WARNING("Database still unavailabel, waitin 1 second before trying..."))
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS("Database is ready!"))