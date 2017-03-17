from django.shortcuts import render
from webapp.fetchstream import myclass
from .models import tweet,Profile
from textblob import TextBlob
val="hello"
pro=Profile()
# Python
import oauth2 as oauth
import cgi

# Django
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from webapp.models import Profile

class userdetail():
    def __init__(self):
        self.username = 0
        self.email = 0
        self.password = 0
consumer = oauth.Consumer(settings.TWITTER_TOKEN,settings.TWITTER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'

# This is the slightly different URL used to authenticate/authorize.
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
userdetail_object = userdetail()
def index(request):
    
    
    return render(request, 'webapp/index.html')


def login1(request):
    return render(request, 'webapp/login.html')

def loginauth(request):
    userdetail_object.password = request.POST['password']
    userdetail_object.username = request.POST['username']



    user = authenticate(username=userdetail_object.username,
                        password=userdetail_object.password)

    if user is not None:
        login(request, user)
    else:
        return render(request, 'webapp/login.html')


    return HttpResponseRedirect('/webapp/login/authenticated/search')

def twitter_signup(request):
    userdetail_object.username = request.POST['username']
    userdetail_object.password = request.POST['password']
    userdetail_object.email = request.POST['email']

    return render(request, 'webapp/twitter_signup.html')
def globe(request):
    
    
    return render(request, 'webapp/globe/index.html')
def contact(request):
    return render(request, 'webapp/basic.html', {'content':['nothing','rajeshpoojary18@gmail.com']})
q=[]

def twitter_login(request):
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content.decode('ascii')))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])

    return HttpResponseRedirect(url)


@login_required(login_url='webapp/login')
def twitter_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')

def twitter_authenticated(request):
    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
    token.set_verifier(request.GET['oauth_verifier'])
    client = oauth.Client(consumer, token)

    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        print(content)
        raise Exception("Invalid response from Twitter.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797', 
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content.decode('ascii')))

    # Step 3. Lookup the user or create them if they don't exist.
    try:
        user = User.objects.get(username=userdetail_object.username)
    except User.DoesNotExist:
        # When creating the user I just use their screen_name@twitter.com
        # for their email and the oauth_token_secret for their password.
        # These two things will likely never be used. Alternatively, you 
        # can prompt them for their email here. Either way, the password 
        # should never be used.
        user = User.objects.create_user(userdetail_object.username,
                                        userdetail_object.email,
                                        userdetail_object.password)

        

        # Save our permanent token and secret for later.
        profile = Profile()
        pro=profile
        profile.user = user
        profile.user_name = userdetail_object.username
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    # Authenticate the user and log them in using Django's pre-built 
    # functions for these things.
    user = authenticate(username=userdetail_object.username,
        password=userdetail_object.password)
    login(request, user)

    return HttpResponseRedirect('/webapp/login/authenticated/search')
def search(request):
    
    
    return render(request, 'webapp/search.html')
def sub(request):
    usr=request.user.username


    count=0
    
    p = request.POST['tweet']





    cls=myclass(usr)
    cls.get_tweet(p)
    b=tweet.objects.filter(user_name=usr)
    del q[:]
    for i in b:
        count=count+1
        blob = TextBlob(str(i))
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
        s=str(count)+':)'+str(i)+' | polarity ='+str(polarity)+' subjectivity ='+str(subjectivity)
        q.append(s)
        
    return render(request, 'webapp/user.html',{'content':q})
