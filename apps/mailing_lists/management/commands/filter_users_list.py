from sailthru.sailthru_client import SailthruClient
from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.db import transaction
from mailing_lists.models import BatchJob, MailingListSignup
import csv, pprint, json
from datetime import datetime

def parse_datetime(dt):
	if dt is None:
		return None
	if '/' in dt:
		if ':' not in dt:
			return datetime.strptime(dt, '%Y/%m/%d')	
		return datetime.strptime(dt, '%Y/%m/%d %H:%M:%S')	
	if '.' in dt:
		return datetime.strptime(dt.replace('+00:00', ''), '%Y-%m-%d %H:%M:%S.%f')
	return datetime.strptime(dt.replace('+00:00', ''), '%Y-%m-%d %H:%M:%S')

def clean_user(non_empty_row):
	if 'Signup' in non_empty_row and 'signup' in non_empty_row:
		old_signup = parse_datetime(non_empty_row['Signup'])
		new_signup = parse_datetime(non_empty_row['signup'])
		if old_signup is None:
			if new_signup is not None:
				non_empty_row['Signup'] = old_signup
		elif new_signup is None:
			if old_signup is not None:
				non_empty_row['Signup'] = old_signup
		elif old_signup < new_signup:
			non_empty_row['Signup'] = old_signup
		else:
			non_empty_row['Signup'] = new_signup
		non_empty_row['Signup'] = non_empty_row['Signup'].strftime('%Y/%m/%d %H:%M:%S')
		non_empty_row['signup'] = None

	if non_empty_row.get('signup_date', None) is not None and non_empty_row.get('signup_date', None) != '':
		new_signup = datetime.strptime(non_empty_row['signup_date'], '%m/%d/%Y')
		non_empty_row['Signup'] = new_signup.strftime('%Y/%m/%d %H:%M:%S')
		non_empty_row['signup_date'] = None

	if non_empty_row.get('gender', None) is not None:
		if non_empty_row['gender'] == 'N':
			non_empty_row['gender'] = None				

	rename_fields = {
		#'cc': 'country',
		#'cityortown': 'city_or_town',
		'paypal_email_address': 'stall_paypal_email',
		'short_stall_description': 'stall_short_description',
		'shortstall': 'stall_short_description',
		'fullstall': 'stall_full_description',
		'paypal': 'stall_paypal_email',
		'purchased': 'user_purchased_orders',
		'prodcreated': 'stall_product_count',
		'prodactive': 'stall_active_product_count',
		'orders': 'stall_orders_sold',
		'lovelists': 'user_lovelist_count',
		'prodloved': 'user_products_loved_count',
		'following': 'user_following_count',
		'followedby': 'user_followers_count',
		'avatar': 'user_profile_has_avatar',
		'fname': 'first_name',
		'lname': 'last_name',
		'products_currently_active': 'stall_active_product_count',
		'orders_sold_to_date': 'stall_orders_sold',
		'number_of_love_lists': 'user_lovelist_count',
		'full_stall_description': 'stall_full_description',
		'products_ever_created': 'stall_product_count',
		'stall_name': 'stall_title',
		'purchased_orders': 'user_purchased_orders'
	}

	is_seller_lead = ('is_user' not in non_empty_row or non_empty_row['is_user'] == False) and ('is_seller' not in non_empty_row or non_empty_row['is_seller'] == False) and ('business' in non_empty_row or 'company' in non_empty_row)
	if not is_seller_lead:
		if 'sellers_main_product_category' in non_empty_row:
			is_seller_lead = True

	non_empty_row['is_seller_lead'] = is_seller_lead
	if non_empty_row.get('business', None) is not None:
		if is_seller_lead:
			non_empty_row['company_name'] = non_empty_row['business']
		else:
			non_empty_row['stall_title'] = non_empty_row['business']
		non_empty_row['business'] = None

	if non_empty_row.get('company', None) is not None and len(non_empty_row['company']):
		non_empty_row['company_name'] = non_empty_row['company']
		non_empty_row['company'] = None

	if non_empty_row.get('cc', None) is not None:
		non_empty_row['Geolocation Country'] = non_empty_row['cc']
		non_empty_row['cc'] = None

	if non_empty_row.get('country', None) is not None:
		non_empty_row['Geolocation Country'] = non_empty_row['country']
		non_empty_row['country'] = None

	if non_empty_row.get('cityortown', None) is not None:
		country = non_empty_row.get('Geolocation Country', None)
		if country:
			non_empty_row['Geolocation City'] = '%s, %s' % (non_empty_row['cityortown'], country)
		else:
			non_empty_row['Geolocation City'] = non_empty_row['cityortown']
		non_empty_row['cityortown'] = None

	for from_k, to_k in rename_fields.items():
		if non_empty_row.get(from_k, None) is not None:
			if non_empty_row.get(to_k, None) is None:
				non_empty_row[to_k] = non_empty_row[from_k]
			non_empty_row[from_k] = None

	if non_empty_row.get('is_user', None) is not None:
		non_empty_row['is_user'] = non_empty_row['is_user'] == 1

	if non_empty_row.get('is_seller', None) is not None:
		non_empty_row['is_seller'] = non_empty_row['is_seller'] == 1

	if non_empty_row.get('member_type', None) is not None:
		non_empty_row['is_seller'] = non_empty_row['member_type'] == 'stall owner'
		non_empty_row['is_user'] = non_empty_row['member_type'] == 'regular member'
		if non_empty_row['member_type'] not in ['stall owner', 'regular member']:
			print non_empty_row['member_type']
		non_empty_row['member_type'] = None

	# This data is next to useless, only a few people have it
	if 'Opens' in non_empty_row:
		non_empty_row['Opens'] = None
	if 'Pageviews' in non_empty_row:
		non_empty_row['Pageviews'] = None
	if 'Clicks' in non_empty_row:
		non_empty_row['Clicks'] = None

	if 'is_user' not in non_empty_row:
		non_empty_row['is_user'] = False

	if 'is_seller' not in non_empty_row:
		non_empty_row['is_seller'] = False

	if 'user_followers_count' in non_empty_row and non_empty_row['is_user'] == False and non_empty_row['is_seller'] == False:
		non_empty_row['is_user'] = True

	if 'do_you_sell_products' in non_empty_row:
		if non_empty_row['do_you_sell_products']:
			if non_empty_row['is_seller'] == False and non_empty_row['is_user'] is False and non_empty_row['is_seller_lead'] is False:
				non_empty_row['is_seller_lead'] = True
			non_empty_row['do_you_sell_products'] = None			

	non_empty_row['is_user_lead'] = non_empty_row['is_user'] == False and non_empty_row['is_seller'] == False and non_empty_row['is_seller_lead'] == False
	return non_empty_row

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def _encoder_default(obj):
    encoders = [
        ((datetime.date, datetime.time, datetime.datetime),
          lambda date: str(date)),
        (Country, lambda country: country.code),
    ]
    for types, encoder in encoders:
        if isinstance(obj, types):
            return encoder(obj)
    raise TypeError("Unable to serialise {}!".format(repr(obj)))


class Command(NoArgsCommand):
	def handle_noargs(self, **kwargs):
		api = SailthruClient(settings.SAILTHRU_API_KEY, settings.SAILTHRU_API_SECRET)
		pp = pprint.PrettyPrinter(indent=4)
		i = 0
		total_i = 0
		out_file_count = 0
		out_file = None
		with open('/home/ubuntu/Project/ecomarket/all-users.csv', 'rb') as csvfile:
			reader = csv.reader(csvfile)
			headers = None
			for row in reader:
				if headers is None:
					headers = row
					continue
				row = dict(zip(headers, row))
				non_empty_row = {}
				for k, v in row.items():
					if v is not None:
						v = v.strip()
						if len(v) == 0:
							v = None					
						non_empty_row[k] = v
				st_user = api.api_get('user', {'id': non_empty_row['Profile Id']})
				if st_user is None:
					print "Cannot find user '%s'" %(non_empty_row['Profile Id'],)				
				body = st_user.get_body()
				st_user_vars = body['vars']
				if st_user_vars is None:
					continue
				for key in st_user_vars.keys():
					try:
						if st_user_vars[k] is not None:
							if type(st_user_vars[k]) == str:
								st_user_vars[k] = st_user_vars[k].strip()
								if st_user_vars[k] == '':
									st_user_vars[k] = None
					except:
						pass
				new_vars = clean_user(st_user_vars)				
				email = body['keys']['email']
				if out_file is None or i > 5000:
					i = 0
					if out_file is not None:
						out_file.close()
					out_file_count += 1
					out_file = open('batch_%d.txt'%(out_file_count,),'wb')						
				out_file.write(json.dumps({
					'email': email, 
					'vars': new_vars
				}, default=_encoder_default) + "\n")
				i += 1
				total_i += 1
				print "%d %d %d" % (i, total_i, out_file_count)
				#print st_user_vars
				#print new_vars
				#print ""
				#print "--------------------------"
				#print ""
"""

class Command(NoArgsCommand):
	def handle_noargs(self, **kwargs):
		api = SailthruClient(settings.SAILTHRU_API_KEY, settings.SAILTHRU_API_SECRET)
		pp = pprint.PrettyPrinter(indent=4)
		has_values = {}
		known_fields = {}
		i = 0
		out_file_count = 0
		out_file = None
		with open('/home/ubuntu/Project/ecomarket/all-users.csv', 'rb') as csvfile:
			reader = csv.reader(csvfile)
			headers = None
			for row in reader:
				if headers is None:
					headers = row
					continue
				row = dict(zip(headers, row))
				non_empty_row = {}
				for k, v in row.items():
					if v is not None:
						v = v.strip()
						if len(v) == 0:
							v = None					
						non_empty_row[k] = v

				non_empty_row = clean_user(non_empty_row)
				ignore_keys = ['Profile Id', 'Email Hash', 'Domain', 'Engagement', 
							   'Lists', 'Profile Created Date', 'Signup', 'Opens',
							   'Clicks', 'Pageviews', 'Last Open', 'Last Click',							  
							   'Last Pageview', 'Optout Time', 'Delivery Status Time',
							   'Delivery Message', 'List Signup', 'Geolocation City',
							   'Geolocation State', 'Geolocation Country', 'Geolocation Zip',
							   'birthday', 'company_name', 'confirm_ip', 'confirm_time',
							   'dstoffset', 'email_notifications', 'gmtoffset',
							   'is_seller', 'is_seller_lead', 'is_user', 'is_user_lead',
							   'last_changed', 'latitude', 'lists', 'login_date',
							   'logindate', 'longitude', 'mailchimp_rating',
							   'optin_ip', 'optin_time', 'phone', 'gender',
							   'sellers_main_product_category', 'stall_name',
							   'timezone', 'username', 'region']

				sailth_keys = ['Profile Id', 'Email Hash', 'Domain', 'Engagement', 
							   'Lists', 'Profile Created Date', 'Signup', 'Opens',
							   'Clicks', 'Pageviews', 'Last Open', 'Last Click',							  
							   'Last Pageview', 'Optout Time', 'Delivery Status Time',
							   'Delivery Message', 'List Signup', 'Geolocation City',
							   'Geolocation State', 'Geolocation Country', 'Geolocation Zip']

				for k, v in non_empty_row.items():
					if k not in known_fields:
						known_fields[k] = True
					if v is not None:						
						has_values[k] = True

				if out_file is None or i > 5000:
					if out_file is not None:
						out_file.close()
					out_file_count += 1
					out_file = open('batch_%d.txt'%(out_file_count,),'wb')						
				out_file.write(json.dumps({
					'id': 
				}, default=_encoder_default) + "\n")

			print "Derp"
			derp = set(known_fields.keys()).difference(set(has_values.keys()))
			derp2 = set(derp).difference(sailth_keys)
			pp.pprint(set(has_values.keys()) - derp2)
"""			