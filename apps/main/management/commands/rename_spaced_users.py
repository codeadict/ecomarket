from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import csv
import contextlib

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open("spaced_username_mapping.csv", "w") as out, \
             open("unresolvable_usernames.csv", "w") as unresolvable:
            writer = csv.writer(out)
            for user in User.objects.filter(username__contains=" "):
                print("Processing user {0}".format(user.username))
                new_username = user.username.replace(" ", "")
                if User.objects.filter(username=new_username).count() > 0:
                    unresolvable.write(user.username + "\n")
                else:
                    writer.writerow([user.username, new_username])
                    user.username = new_username
                    user.save()
