from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import SellerForm, UserForm
from .models import Seller, Chat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

#AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']



def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        seller = Seller.objects.filter(user=request.user)
        #song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            seller_results = seller.filter(
                Q(key__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'seller': seller_results
            })
        else:
            return render(request, 'music/index.html', {'seller': seller})



def create_seller(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = SellerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.BookSet_Photo = request.FILES['BookSet_Photo']
            file_type = seller.BookSet_Photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'seller': seller,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_seller.html', context)
            seller.save()
           # return render(request, 'music/detail.html', {'seller': seller})
        context = {
            "form": form,
        }
        return render(request, 'music/create_seller.html', context)



def buyer(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
       #seller = Seller.objects.filter(user=request.user)
        seller_results = Seller.objects.all()
        query = request.GET.get("q")
        if query:
            seller = seller_results.filter(
                Q(Key__icontains=query)
            ).distinct()
            return render(request, 'music/buyer.html', {
                'seller_results': seller
            })
        else:
            return render(request, 'music/buyer.html', {'seller_results': seller_results})



def delete_seller(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)
    seller.delete()
    seller = Seller.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'seller': seller})



def detail(request, seller_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        seller = get_object_or_404(Seller, pk=seller_id)
        return render(request, 'music/detail.html', {'seller': seller, 'user': user})


def detail1(request, seller_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        seller = get_object_or_404(Seller, pk=seller_id)
        return render(request, 'music/detail1.html', {'seller': seller, 'user': user})










def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                seller_results = Seller.objects.all()
                query = request.GET.get("q")
                if query:
                    seller = seller_results.filter(
                        Q(key__icontains=query)
                    ).distinct()
                    return render(request, 'music/buyer.html', {
                        'seller_results': seller
                    })
                else:
                    return render(request, 'music/buyer.html', {'seller_results': seller_results})
               #seller = Seller.objects.filter(user=request.user)
               #return render(request, 'music/buyer.html', {'seller_results': seller})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                seller = Seller.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'seller': seller})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)



def detail(request, seller_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        seller = get_object_or_404(Seller, pk=seller_id)
        return render(request, 'music/detail.html', {'seller': seller, 'user': user})


def Home(request, seller_id):
    c = Chat.objects.all()
    seller = get_object_or_404(Seller, pk=seller_id)
    return render(request, "music/home.html", {'seller': seller, 'chat': c})


def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        c = Chat(user=request.user, message=msg)




        if msg != '':
            c.save()

        context = {
            'msg': msg,
            'user': c.user.username,
            'time': c.created.time()
        }
        # mg = src="https://scontent-ord1-1.xx.fbcdn.net/hprofile-xaf1/v/t1.0-1/p160x160/11070096_10204126647988048_6580328996672664529_n.jpg?oh=f9b916e359cd7de9871d8d8e0a269e3d&oe=576F6F12"
        return JsonResponse({context})
    else:
        return HttpResponse('Request must be POST.')


def Messages(request):
    c = Chat.objects.all()
    return render(request, 'music/messages.html', {'chat': c})




def wishlist(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)
    try:
        if seller.wishlist:
            seller.wishlist = False
        else:
            seller.wishlist = True
        seller.save()
    except (KeyError, Seller.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def wishlisted_seller(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            seller = Seller.objects.all()
            if filter_by == 'wishlist':
                seller = seller.filter(wishlist=True)
        except Seller.DoesNotExist:
            seller = []
        return render(request, 'music/wishlist.html', {
            'seller': seller,

        })