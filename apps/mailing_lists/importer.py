from __future__ import print_function

from itertools import chain, izip, repeat
import sys
import warnings

from django.db import transaction

from django.contrib.auth.models import User

from marketplace.models import Category, Country

from mailing_lists.constants import LeadSources
from mailing_lists.models import MailingListSignup


class MissingRequiredColumn(Exception):

    pass


class CsvRow(object):

    def __init__(self, email, first_name=None, last_name=None, full_name=None,
                 category_name=None, company_name=None, telephone_number=None,
                 is_seller_lead=None, country_name=None, ip_address=None,
                 source=None):
        self.email = email
        if first_name and last_name:
            self.first_name = first_name
            self.last_name = last_name
        elif full_name:
            names = full_name.split()
            self.first_name = names[0]
            self.last_name = "".join(names[1:])
            if len(names) >= 2:
                if len(names) > 2:
                    msg = "Unsure how to split '{}' into first and last names"
                    warnings.warn(msg.format(full_name))
        else:
            raise MissingRequiredColumn("First Name/Last Name or Full Name")
        self.category_name = category_name
        self.company_name = company_name
        self.telephone_number = telephone_number
        self.is_seller_lead = is_seller_lead
        self.country_name = country_name
        if ip_address:
            if ":" in ip_address:
                # Try and convert an IPv6 address to IPv4
                if ip_address.startswith("::ffff:"):
                    self.ip_address = ip_address[7:]
                else:
                    warnings.warn("Unable to convert IPv6 address {}, so "
                                  "dropping it".format(ip_address))
            else:
                self.ip_address = ip_address
        self.source = "Data Collection" if source is None else source

    REQUIRED_FIELDS = {
        "E-mail Address": "email",
    }
    OPTIONAL_FIELDS = {
        "First Name": "first_name",
        "Last Name": "last_name",
        "Full Name": "full_name",
        "Category": "category_name",
        "Company Name": "company_name",
        "Telephone Number": "telephone_number",
        "Is Seller Lead?": "is_seller_lead",
        "Seller Country": "country_name",
        "IP Address": "ip_address",
        "Source": "source",
    }

    @classmethod
    def from_dict(cls, row):
        kwargs = {}
        required = izip(cls.REQUIRED_FIELDS.iteritems(), repeat(True))
        optional = izip(cls.OPTIONAL_FIELDS.iteritems(), repeat(False))
        for (key, value), is_required in chain(required, optional):
            try:
                kwargs[value] = row[key].strip()
            except KeyError:
                if is_required:
                    raise MissingRequiredColumn(key)
        return cls(**kwargs)


class CsvImporter(object):

    CATEGORY_MAPPING = {
        "Art": "Home",
        "Baby & Child": "Baby and Parenting",
        "EcoEco Baby and Child": "Baby and Parenting",
        "Eco Baby and Child": "Baby and Parenting",
        "Eco Home and Garden": "Home",
        "Entertainment": "Home",
        "Fashiion": "Fashion",
        "Fashions": "Fashion",
        "Fashon": "Fashion",
        "Health and Baby": "Baby and Parenting",
        "Health & beauty": "Health and Beauty",
        "Health & Beauty": "Health and Beauty",
        "Home and Garden": "Home",
        "Pet": "Animals and Pets",
        "Pets": "Animals and Pets",
        "Out Doors": "Outdoors",
        "Stationary": "Office and Stationery",
        "Stationery": "Office and Stationery",
    }

    COUNTRY_MAPPING = {
        "BELIGIUM": "Belgium",
        "BOLIVIA": "Bolivia, Plurinational State Of",
        "BULGARAIA": "Bulgaria",
        "DUBAI": "United Arab Emirates",
        "GEERMANY": "Germany",
        "HAWAII": "United States",
        "HOLAND": "Netherlands",
        "HOLLAND": "Netherlands",
        # We make an assumption here, but I think it's fair
        "KOREA": "Korea, Republic Of",
        "LATIVIA": "Latvia",
        "MACEDONIA": "Macedonia, The Former Yugoslav Republic Of",
        "MAYALSIA": "Malaysia",
        "MUMBAI": "India",
        "NERTHERLANDS": "Netherlands",
        "NEWZEALAND": "New Zealand",
        "PALESTINE": "Palestinian Territory, Occupied",
        "SCOTLAND": "United Kingdom",
        "SOUTH KOREA": "Korea, Republic Of",
        "SOIUTH AFRICA": "South Africa",
        "TAIWAN": "Taiwan, Province Of China",
        "VIRGIN-ISLANDS(USA)": "Virgin Islands, U.S.",
        "IRAN": "Iran, Islamic Republic Of",
        "ITALT": "Italy",
        "UNITED STAES": "United States",
        "UNITED STATED": "United States",
        "UNITED STATERS": "United States",
        "UNITED KINGADOM": "United Kingdom",
        "UNITED KINGDON": "United Kingdom",
        "UNITED KINGODM": "United Kingdom",
        "UNITED KINGOM": "United Kingdom",
        "UNITD KINGDOM": "United Kingdom",
        "VIETNAM": "Viet Nam",  # Why is this spelt like this?
    }

    SOURCE_MAPPING = {
        "Data Collection": LeadSources.DATA_COLLECTION,
        "Product Giveaway": LeadSources.PRODUCT_GIVEAWAY,
    }

    def __init__(self, reject_filename, stdout=sys.stdout, stderr=sys.stderr):
        self.reject_filename = reject_filename
        self.import_count = 0
        self.reject_count = 0

        self.stdout = stdout
        self.stderr = stderr

    def _write_reject(self, row):
        # It would be nice to write a CSV here, but it can't be done now we
        # no longer have a standard format.
        with open(self.reject_filename, "a") as fh:
            print(row.email, file=fh)
        self.reject_count += 1

    @transaction.commit_on_success
    def import_csv(self, reader):
        count = 1
        for row in reader:
            row = CsvRow.from_dict(row)
            print("Processing email {0}, (number "
                  "{1})".format(row.email, count),
                  file=self.stdout)
            count += 1
            if (row.is_seller_lead and
                    row.is_seller_lead.lower() in ["n", "no"]):
                print("is_seller_lead == '{}'".format(row.is_seller_lead),
                      file=self.stdout)
                # Make sure any duplicates are deleted
                # This is not bullet-proof - any duplicates added later will
                # still appear in the list
                MailingListSignup.objects.filter(
                        email_address__iexact=row.email).delete()
                continue
            if (row.category_name in self.CATEGORY_MAPPING):
                row.category_name = self.CATEGORY_MAPPING[row.category_name]
            if row.category_name:
                try:
                    category = Category.objects.get(name=row.category_name)
                except Category.DoesNotExist:
                    msg = "Category '{}' does not exist"
                    print(msg.format(row.category_name), file=self.stderr)
                    self._write_reject(row)
                    continue
            else:
                category = None
            if row.country_name in self.COUNTRY_MAPPING:
                row.country_name = self.COUNTRY_MAPPING[row.country_name]
            if row.country_name:
                try:
                    country = Country.objects.get(
                            title__iexact=row.country_name)
                except Country.DoesNotExist:
                    msg = "Country '{}' does not exist"
                    print(msg.format(row.country_name), file=self.stderr)
                    self._write_reject(row)
                    continue
            else:
                country = None
            try:
                source = self.SOURCE_MAPPING[row.source]
            except KeyError:
                print("Unknown source '{}'".format(row.source),
                      file=self.stderr)
                self._write_reject(row)
                continue
            try:
                MailingListSignup.objects.get(email_address__iexact=row.email)
            except MailingListSignup.DoesNotExist:
                try:
                    MailingListSignup.objects.create_from_email(
                        row.email,
                        first_name=row.first_name,
                        last_name=row.last_name,
                        company_name=row.company_name,
                        category=category,
                        telephone_number=row.telephone_number,
                        country=country,
                        ip_address=row.ip_address,
                        source=source,
                        is_seller_lead=(row.is_seller_lead is not None),
                    )
                except User.MultipleObjectsReturned:
                    print("Multiple users with that email address, skipping",
                          file=self.stderr)
        self.import_count = (count - 1) - self.reject_count
