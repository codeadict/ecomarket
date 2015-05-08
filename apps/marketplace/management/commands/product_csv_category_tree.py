import os
import glob
import csv

from django.core.management.base import BaseCommand, CommandError, make_option

from apps.marketplace.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            source, destination = args
        except ValueError:
            raise CommandError(
                "This command takes 2 argument: Path where source CSV files are kept, and destination path to save new CSV files")

        if os.path.isfile(source):
            inpath = os.path.realpath(source)
        else:
            inpath = source

        if os.path.isfile(destination):
            outpath = os.path.realpath(destination)
        else:
            outpath = destination

        for infilename in glob.glob('%s*.csv' % inpath):
            path, filename = os.path.split(infilename)
            print filename
            infile = open(infilename, 'r')
            outfile = open(os.path.join(outpath, filename), 'w')

            incsv = csv.reader(infile)
            outcsv = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in incsv:
                try:
                    p = Product.objects.get(pk=row[2])
                    price_obj = p.get_price_instance().amount
                    outrow = row
                    outrow[3] = ' > '.join(p.categories)
                    outrow.append(float(price_obj.amount))
                    outcsv.writerow(outrow)
                    #print outrow
                except:
                    pass

            infile.close()
            outfile.close()