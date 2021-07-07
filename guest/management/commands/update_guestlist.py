from django.core.management.base import BaseCommand                                                                                                                                            
from django.db import transaction                                                                                                                                                              
                                                                                                                                                                                               
from guest.models import Guest, User
                                                                                                                                                                                               
import csv                                                                                                                                                                                     
import hashlib                                                                                                                                                                                 
                                                                                                                                                                                               
class Command(BaseCommand):                                                                                                                                                                    
    help = 'Seed the database with the guestlist'                                                                                                                                              
                                                                                                                                                                                               
    def add_arguments(self, parser):                                                                                                                                                           
        parser.add_argument('guestlist')                                                                                                                                                       
                                                                                                                                                                                               
    @transaction.atomic                                                                                                                                                                        
    def save_guests_to_db(self, csv_reader):                                                                                                                                                   
        h = hashlib.md5()                                                                                                                                                                      
        for row in csv_reader:                                                                                                                                                                 
            first_name = row['First name']
            last_name = row['Last name']
            concat_name = row['First name'] + row['Last name']                                                                                                                                 
            h.update(str.encode(concat_name))                                                                                                                                                  
            pword = h.hexdigest()[0:8]                                                                                                                                                         
            u = User.objects.create_user(first_name=first_name, last_name=last_name, username=concat_name, password=pword)
            guest = Guest(user=u, hasVoted=False)
            guest.save()
            self.stdout.write(                                                                                                                                                                 
                    self.style.SUCCESS("%s,%s,%s,1" % (first_name, last_name, pword)))                                                                                                                        
                                                                                                                                                                                               
                                                                                                                                                                                               
    def handle(self, *argrs, **options):                                                                                                                                                       
        filename = options['guestlist']                                                                                                                                                        
        with open(filename, newline='') as csvfile:                                                                                                                                            
            reader = csv.DictReader(csvfile)                                                                                                                                                   
            self.save_guests_to_db(reader)       