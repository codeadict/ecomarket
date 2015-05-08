from collections import namedtuple
from random import choice
import datetime

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import Context, loader
from djipchat.lib import send_to_hipchat

from accounts.models import UserProfile
from articles.models import Article
from lovelists.models import LoveList
from marketplace.models import Product, Stall, StallVideo, Category, Cause
from annoying.decorators import ajax_request
from apps.accounts.models import Video, VideoType

ACTIVITIES_TITLE = "Activity will be arriving shortly!..."
ACTIVITIES_MESSAGE = ("Coming soon to a website near you (well, this one in "
                      "fact here on Eco Market!) we will be launching "
                      "'Activity'. We'll be announcing this shortly in our "
                      "blog and can't wait to tell you all about it.")


class HomePageView(TemplateView):
    template_name = "main/home.html"

    def find_featured_stall(self):
        sv = (StallVideo.objects
              .filter({"is_published": True, "is_welcome": True})
              .order_by('?'))
        if sv:
            return sv[0].stall
        return None

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        featured_love_lists = (LoveList.objects.filter(is_public=True)
                               .exclude(promoted=None)
                               .order_by("-promoted")
                               .select_related('user__username', 'primary_category')[:1])
        featured_products = (Product.objects.live()
                             .select_related('stall__identifier')
                             .prefetch_related('prices')[:4])
        recent_products = (Product.objects.live()
                           .order_by("-updated")
                           .select_related('stall__identifier')
                           .prefetch_related('prices')[:48])
        articles_slide1 = (Article.objects.live()
                           .order_by("-publish_date")
                           .select_related('author')[:3])
        articles_slide2 = (Article.objects.live()
                           .order_by("-publish_date")
                           .select_related('author')[3:6])
        featured_stall = self.find_featured_stall()
        top_categories = Category.objects.filter(parent=None)
        causes = Cause.objects.all()
        context.update({
            'featured_love_lists': featured_love_lists,
            'featured_products': featured_products,
            'featured_stall': featured_stall,
            'recent_products': recent_products,
            'articles_slide1': articles_slide1,
            'articles_slide2': articles_slide2,
            'categories': top_categories,
            'causes': causes,
            'ecomm_pagetype': 'home'
        })
        return context


def robots_txt(request):
    if request.META['HTTP_HOST'] not in ['ecomarket.com', 'www.ecomarket.com']:
        return render_to_response('main/robots-block-all.txt', mimetype='text/plain')
            
    baseurl = 'http://' + request.META['HTTP_HOST']
    context = {
        'baseurl': baseurl
    }
    return render_to_response('main/robots.txt', context, context_instance=RequestContext(request), mimetype='text/plain')


def sitemap_xml(request):
    # grab items in performance concious way
    categories = Category.objects.all()
    products = Product.objects.live().filter(~Q(slug='')).order_by('-updated').values("id", "stall__identifier", "slug", "updated")
    articles = Article.objects.live().filter(~Q(slug='')).order_by('-publish_date').values("id", "publish_date", "slug", "updated_at")
    stalls = Stall.objects.filter(~Q(slug='')).values("id", "updated", "slug")  # required mapping on Stall._get_absolute_url
    people = User.objects.all().values("id", "username")
    causes = Cause.objects.filter(~Q(slug='')).values("id", "slug")
    lovelists = LoveList.objects.filter(~Q(slug=''), is_public=True).values('id', 'primary_category__slug', 'slug', 'identifier', 'updated')

    # reformat some of these
    stalls = map(lambda x: {
        'updated': x['updated'],
        'slug': x['slug'],
        'absolute_url': Stall._get_absolute_url(x['slug']),
    }, stalls)

    # reformat some of these
    products = map(lambda x: {
        'path': Product._path(
            stall_identifier=x['stall__identifier'],
            slug=x['slug']
        ),
        'updated': x['updated']
    }, products)

    lovelists = map(lambda x: dict(
        path=reverse('lovelist:view', kwargs=dict(
            category=x['primary_category__slug'],
            slug=x['slug'],
            identifier=x['identifier']
        )),
        updated=x['updated']
    ), lovelists)

    baseurl = 'http://' + request.META['HTTP_HOST']

    context = {
        'categories': categories,
        'products': products,
        'articles': articles,
        'stalls': stalls,
        'causes': causes,
        'people': people,
        'lovelists': lovelists,
        'baseurl': baseurl
    }
    return render(request, 'main/sitemap.xml', context,
                  content_type='application/xml')


class SellPageView(TemplateView):
    """
    This is marketing page for any user to user as well as a landing page
    for marketing emails.
    """
    template_format = "main/sell/%s.html"
    template_name = "main/sell/default.html"

    def get(self, request, *args, **kwargs):
        # Commenting out as we;re not ready for launch. To be revisted!
        try:
            url_slug = request.GET.get('c')
            category = Category.objects.get(slug=url_slug, parent__isnull=True)
            self.template_name = self.template_format % url_slug
        except Category.DoesNotExist:
            category = None

        category_slug = category.slug if category else 'default'

        # Wow, this isn't nice, but it's launch day and we're out of time.
        Seller = namedtuple('Seller', ['username', 'description', 'image'])

        a = Seller('hayley', "Eco Market has really created a hub for stylish eco and ethical fashion", 'eco-boutique.png')
        b = Seller('wewood', "Simple to use and quick to set up and we have had some great promotion from the site", 'wewood-watch.png')
        c = Seller('beezeeecokid', "I love being a part of Eco Market a real caring shopping community is developing hear", 'bee-zee-eco-kid.png')
        d = Seller('plumethical', "Easy to setup and run and great customer support highly recommended. Our range of fair trade bags have been very well received", 'plum-ethical.png')
        e = Seller('sophie', "Eco Market is a site full of organic and natural foodies who really understand the value of good healthy food and an ethical supply chain", 'steenbergs-organics.png')
        f = Seller('heyshuga', "A really sweet site to sell on if you excuse the pun! The shoppers on Eco Market love natural and organic food and certainly have a sweet tooth", 'hey-shuga.png')
        g = Seller('oromo', "Our Stall on Eco Market helps us to share our passion for Oromo coffee with a community who really enjoy great tasting fairtrade coffee,  they just keep coming back as they cant get enough!", 'oromo-cofee.png')
        h = Seller('lindabarrie', "It seemed daunting at first adding all my products but it was actually surprisingly quick and has certainly been worth the effort", 'choc-affair.png')
        i = Seller('laura', "Eco Market has proven a great outlet to sell our sustainably sourced and lovingly crafted wooden baby toys", 'wooden-toy-gallery.png')
        j = Seller('linsdcb', "A friend told me about Eco Market and as soon as I opened my stall I started getting lots of interest in my organic cotton baby range highly recommend!", 'daisy-chain-baby.png')
        k = Seller('littlegreensheep', "I must admit at first I was skeptical how well Eco Market would work as our products are priced in the hundreds of pounds,  however they have proven really popular and its been a great experiance!", 'green-sheep.png')
        l = Seller('organicmonkey', "A really fun place to sell,  simple to set up and run a great fit for our organic baby oils", 'organic-monkey.png')
        m = Seller('bamboo', "Very easy to use and orders have been growing steadily since we created our stall", 'bamboosk8.png')
        n = Seller('redmaloo', "Intuitive well designed and easy to manager store front which puts your products infront of design focused conscious shoppers", 'red-maloo.png')
        o = Seller('ettitude', "Our Organic bamboo bedding has rapidly become a hit on Eco Market! I am really pleased I gave this a try,  Its been a breeze to set up and the team have been really helpful and supportive.", 'ettitude.png')
        p = Seller('tom raffield', "It's great to have a marketplace targeted to sustainable designed interior products", 'tom-raffield.png')
        q = Seller('wudwerx', "Great site simple to use and has certainly kept me business producing bee hotels long into the night to meet the demand!", 'wudwerx.png')
        r = Seller('ekobo', "A really nice well designed site,  friendly team and all around great place to sell", 'ekobo-ecology-design.png')
        s = Seller('antoine', "Highly recommend the Eco Market platform to anyone looking to grow sales and reach new customers", 'hu2.png')
        t = Seller('gardeneve', "Easy to set up and has provided us with lots of very valuable feedback from shoppers", 'garden-of-eve.png')
        u = Seller('MuLondon', "A fab site and a lovely place to share our passion for natural living,  skin and body care", 'mu-london.png')
        v = Seller('hhc', "A great site and is getting more and more busy every month highly recommended", 'freezy-pups.png')
        w = Seller('ettitude', "Our Organic bamboo bedding has rapidly become a hit on Eco Market! I am really pleased I gave this a try,  Its been a breeze to set up and the team have been really helpful and supportive.", 'ettitude.png')
        x = Seller('sophie', "Eco Market is a site full of organic and natural foodies who really understand the value of good healthy food and an ethical supply chain", 'steenbergs-organics.png')
        y = Seller('oromo', "Our Stall on Eco Market helps us to share our passion for Oromo coffee with a community who really enjoy great tasting fairtrade coffee,  they just keep coming back as they cant get enough!", 'oromo-coffee.png')
        z = Seller('lindabarrie', "It seemed daunting at first adding all my products but it was actually surprisingly quick and has certainly been worth the effort", 'choc-affair.png')
        aa = Seller('plumethical', "Easy to setup and run and great customer support highly recommended. Our range of fair trade bags have been very well received", 'plum-ethical.png')
        ab = Seller('redmaloo', "Intuitive well designed and easy to manager store front which puts your products infront of design focused conscious shoppers", 'redmaloo.png')

        sellers = {
            'default': [w, x, y, z, aa],
            'animals-and-pets': [v],
            'baby-and-parenting': [i, j, k, l],
            'electricals': [n],
            'fashion': [a, b, c, d],
            'food-and-drink': [e, f, g, h],
            'health-and-beauty': [t, u],
            'home': [o, p, q, r, s],
            'office-and-stationery': [ab],
            'outdoors': [m],
        }

        featured_seller = choice(sellers[category_slug])
        featured_stall = Stall.objects.get(user__username=featured_seller.username)

        cta_url = None
        if request.user.is_authenticated():
            try:
                profile = request.user.get_profile()
            except UserProfile.DoesNotExist:
                profile = None

            if profile and profile.is_seller:
                cta_url = None
            else:
                cta_url = reverse('create_stall')
        else:
            cta_url = reverse('register')

        context = {
            'name': request.GET.get('n'),
            'cta_url': cta_url,
            'seller': featured_seller,
            'stall': featured_stall,
        }
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SellPageView, self).get_context_data(**kwargs)
        return context


def activities_modal(request, template_name="main/activities_info.html"):

    context = {
        'title': ACTIVITIES_TITLE,
        'message': ACTIVITIES_MESSAGE}

    return render(request, template_name, context)


class RecordGuestVideo(TemplateView):
    template_name = 'main/guest_video.html'

    def get_context_data(self, **kwargs):
        context = super(RecordGuestVideo, self).get_context_data(**kwargs)
        context['video_type'] = VideoType.objects.get(pk=3)
        return context

    @ajax_request
    def post(self, *args, **kwargs):
        save_as_user = User.objects.get(username='jason-dainter')
        vid_type = VideoType.objects.get(pk=3)
        vid = Video(
            video_guid=self.request.POST['guid'],
            embed_url=self.request.POST['embed_url'],
            splash_url=self.request.POST['splash_url'],
            user=save_as_user,
            video_type=vid_type
        )
        vid.save()
        print "Heler"

        messages.info(
            self.request,
            'Great job! Your video has been saved. Since we are still testing this feature we will manually review videos and get back to you about these shortly'
        )

        # send notification to hipchat
        template_context = Context({
            'request': self.request,
            'user': save_as_user,
            'now': datetime.datetime.now()
        })
        template = loader.get_template("accounts/video/fragments/hipchat_notification.html")
        output = template.render(template_context)

        send_to_hipchat(
            output,
            room_id=82667,
            notify=1,
        )

        return {
            "success": True
        }