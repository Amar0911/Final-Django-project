from django.shortcuts import render,redirect,get_object_or_404
from .forms import Registerform,AuthenticationForm,ChangePasswordForm,AdminProfileForm,UserProfileForm,ContactForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from .models import Movie,Watchlist


#================ Forgot Password ======================

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse

##########################################################################################################################################




def index(request):
    return render(request,'core/index.html')



############################################################## Register ####################################################



def register(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        rf = Registerform(request.POST)
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Email is required')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        elif rf.is_valid():
            user = rf.save()
            messages.success(request, 'Registration Successful!!')

            send_mail(
                'Registration Successful',
                'Thank you for choosing us!!',
                'movievistafilm@gmail.com',
                [email],
                fail_silently=False,
            )

            return redirect('login')
        else:
            messages.error(request, 'Invalid form submission')

    else:
        rf = Registerform()

    return render(request, 'core/signup.html', {'rf': rf})
    


############################################################## Login ###############################################################



def log_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            rf = AuthenticationForm(request, request.POST)
            if rf.is_valid():
                name = rf.cleaned_data['username']
                pas = rf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid username or password') 
            else:
                messages.error(request, "Invalid form submission. Please check your details.")

        else:
            rf = AuthenticationForm()

        return render(request, 'core/login.html', {'rf': rf})
    else:
        return redirect('profile')

    


############################################################## Logout ###############################################################




def log_out(request):
    logout(request)
    return redirect('index')
    

    
############################################################## Profile ###############################################################


    
def profile(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            if request.user.is_superuser == True:
                adm = AdminProfileForm(request.POST, instance = request.user)
            else:
                adm = UserProfileForm(request.POST, instance = request.user)
            if adm.is_valid():
                adm.save()
                messages.success(request,'Profile Updated Successfully!!')
        else:
            if request.user.is_superuser == True:
                adm = AdminProfileForm(instance = request.user)
            else:
                adm = UserProfileForm(instance = request.user)
        return render(request,'core/profile.html', {'name': request.user, 'adm': adm})
    else:
        return redirect('login')

############################################################# About ########################################################

def about(request):
    return render(request,'core/about.html')

############################################################## Contact ########################################################


def contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                # Check if the email in the form matches the logged-in user's email
                user_email = form.cleaned_data.get('email')
                if user_email != request.user.email:
                    messages.error(request, 'The email address does not match your registered email.')
                else:
                    # Save the form
                    form.save()

                    # Send a thank-you email to the user
                    subject = "Thank You for Contacting Us"
                    message = f"Dear {request.user.username},\n\nThank you for reaching out! We have received your message and will get back to you soon.\n\nBest regards,\nMovieVista Team"
                    from_email = 'movievistafilm@gmail.com'
                    recipient_list = [user_email]

                    try:
                        send_mail(subject, message, from_email, recipient_list)
                        messages.success(request, 'Your request has been sent successfully, and a confirmation email has been sent to you.')
                    except Exception as e:
                        messages.error(request, f"Message sent, but there was an error sending the confirmation email: {e}")

                    return redirect('contact')
            else:
                messages.error(request, 'There was an error sending your message. Please try again.')
        else:
            form = ContactForm()
        return render(request, 'core/contact.html', {'form': form})
    else:
        return redirect('login')



############################################################## Change Password ############################################################



def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cp = ChangePasswordForm(request.user, request.POST)
            if cp.is_valid():
                cp.save()
                update_session_auth_hash(request, cp.user)
                messages.success(request,'Password Change Successfully')
                return redirect('profile')
        else:
            cp = ChangePasswordForm(request.user)
        return render(request,'core/changepassword.html',{'cp':cp})
    else:
        return redirect('login')

############################################################# Seemore #################################################################

def seemore(request):
    tr = Movie.objects.filter(category ='TRENDING')
    return render(request,'core/seemore.html',{'tr': tr})

def seemore_anime(request):
    am = Movie.objects.filter(category ='ANIME')
    return render(request,'core/seemore_anime.html',{'am' : am})

def seemore_indian(request):
    im = Movie.objects.filter(category = 'INDIAN')
    return render(request,'core/seemore_indian.html',{'im': im})

def seemore_webseries(request):
    ws = Movie.objects.filter(category = 'WEBSERIES')
    return render(request,'core/seemore_webseries.html',{'ws': ws})

def seemore_hollywood(request):
    hm = Movie.objects.filter(category = 'HOLLYWOOD')
    return render(request,'core/seemore_hollywood.html',{'hm': hm})

def carousel(request):
    ca = Movie.objects.filter(category = 'CAROUSEL')
    return render(request,'core/index.html',{'ca': ca})


############################################################## cardplay ####################################################

def cardplay_trending(request,id):
    tr = Movie.objects.get(pk=id)
    return render(request,'core/cardplay_trending.html',{'tr': tr})

# def cardplay_carousel(request, id):
#     cm = Movie.objects.get(pk=id)
#     return render(request,'core/cardplay_carousel.html',{'cm': cm})

def cardplay_anime(request,id): 
    am = Movie.objects.get(pk=id)
    return render(request,'core/cardplay_anime.html',{'am' : am})

def cardplay_indian(request,id):
    im = Movie.objects.get(pk=id)
    return render(request,'core/cardplay_indian.html',{'im': im})

def cardplay_webseries(request,id):
    ws = Movie.objects.get(pk=id)
    return render(request,'core/cardplay_webseries.html',{'ws': ws})

def cardplay_hollywood(request,id):
    hm = Movie.objects.get(pk=id)
    return render(request,'core/cardplay_hollywood.html',{'hm': hm})



######################################################## Add to Watchlist ##############################################################



def watchlistadd(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=id)
        user = request.user
        referer = request.META.get('HTTP_REFERER', '/')  
        
        if Watchlist.objects.filter(user=user, films=movie).exists():
            messages.error(request, 'This movie is already added to your Watchlist')
        else:
            Watchlist.objects.create(user=user, films=movie)
            messages.success(request, 'Added to Watchlist')
        
        return redirect(referer)  
    else:
        messages.error(request, 'You need to log in to add movies to your Watchlist')
        return redirect('login')  


def watchlist(request):
    if request.user.is_authenticated:
        movies = Watchlist.objects.filter(user=request.user)  
        return render(request, 'core/watchlist.html', {'movies': movies})
    else:
        return redirect('login')
    

def watchlistremove(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=id)
        Watchlist.objects.filter(user=request.user, films=movie).delete()
        messages.success(request, 'Removed from Watchlist')
        return redirect('watchlist')
    else:
        return redirect('login')
    

############################################################# Forget Password #########################################################
    

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/resetpassword/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'movievistafilm@gmail.com', 
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request,'Please enter valid email address')
    return render(request, 'core/forgotpassword.html')                                        
    

def resetpassword(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/resetpassword.html')

def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')



######################################################## Subscriptions #################################################################

#===============For Paypal =========================

from .models import SubscriptionPlan, UserSubscription
from django.utils import timezone
from datetime import timedelta
import uuid
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm  
from django.urls import reverse
from django.contrib.auth.decorators import login_required
        
        

@login_required
def subscription(request):
    plans = SubscriptionPlan.objects.all()


    has_active_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).exists()

    return render(request, 'core/subscription.html', {
        'plans': plans,
        'has_active_subscription': has_active_subscription,
    })

        

######################################################### payment ###################################################

def payment(request):
    plan_id = request.GET.get('plan_id')

    if not plan_id:
        messages.error(request, 'No plan selected.')
        return redirect('subscription')

    # Check if the plan exists
    plan = SubscriptionPlan.objects.filter(id=plan_id).first()
    if not plan:
        messages.error(request, 'Subscription plan not found.')
        return redirect('subscription')

    # Check if the user already has an active subscription
    existing_active_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    if existing_active_subscription:
        messages.error(request, 'You already have an active subscription to a plan.')
        return redirect('subscription')

    # Check if there is an inactive subscription for the same plan
    existing_inactive_subscription = UserSubscription.objects.filter(
        user=request.user,
        plan=plan,
        is_active=False
    ).first()

    if existing_inactive_subscription:
        # Update the existing inactive subscription
        existing_inactive_subscription.end_date = timezone.now() + timedelta(days=plan.duration)
        existing_inactive_subscription.save()
        user_subscription = existing_inactive_subscription
    else:
        # Create a new subscription
        end_date = timezone.now() + timedelta(days=plan.duration)
        user_subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            end_date=end_date,
            is_active=False  # Initially inactive
        )

    # PayPal payment setup
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': plan.price,
        'item_name': plan.name,
        'invoice': str(uuid.uuid4()),  # Unique invoice ID
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment_success')}?subscription_id={user_subscription.id}",
        'cancel_url': f"http://{host}{reverse('payment_failed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'paypal': paypal_payment,
        'plan': plan,
        'user': request.user,
        'subscription_start_date': timezone.now(),
        'subscription_end_date': user_subscription.end_date,
    }

    return render(request, 'core/payment.html', context)


#################################################### Payment success ################################################


def payment_success(request):
    subscription_id = request.GET.get('subscription_id')

    if not subscription_id:
        messages.error(request, 'Invalid subscription details.')
        return redirect('subscription')

    # Check if the subscription exists
    user_subscription = UserSubscription.objects.filter(id=subscription_id, user=request.user).first()
    if not user_subscription:
        messages.error(request, 'Subscription not found.')
        return redirect('subscription')

    payment_confirmed = True  

    if payment_confirmed:
        # Activate the subscription
        user_subscription.is_active = True
        user_subscription.save()

        context = {
            'subscription': user_subscription,
            'plan': user_subscription.plan,
        }
        return render(request, 'core/payment_success.html', context)
    else:
        messages.error(request, 'Payment could not be verified. Please try again.')
        return redirect('subscription')

############################################ Payment Failed #############################################

def payment_failed(request):
    messages.error(request, 'Payment was canceled or failed. No subscription was activated.')
    return render(request, 'core/payment_failed.html')



#####################################################  Subscriptions ####################################

from .models import UserSubscription


def subscription_status(request):
    """
    Add `has_active_subscription` to the context for all templates.
    """
    if request.user.is_authenticated:
        has_active_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).exists()
    else:
        has_active_subscription = False

    return {
        'has_active_subscription': has_active_subscription,
    }


############################################ Movie Search ############################################

def movie_search(request):
    query = request.GET.get('q') 
    print("Search Query:", query)
    if query:  
        movie = Movie.objects.filter(name__icontains=query) | Movie.objects.filter(starcast__icontains=query)
        print("Movies Found:", movie)
    else:
        movie = Movie.objects.all()

    context = {
        'movie': movie,  
        'query': query,
    }
    return render(request, 'core/movie_search.html', context)


