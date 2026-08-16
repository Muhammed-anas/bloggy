from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post
from .forms import postForms
# Create your views here.

def main_page(request):
    return render (request, 'views/main.html')

def home_page(request):
    all_posts = Post.objects.all().order_by('-updated_at')
    return render (request, 'views/home.html',{
        'all_posts':all_posts })

def contact_page(request):
    return render (request, 'views/contact.html')

def about_page(request):
    return render (request, 'views/about.html')


class create_post(LoginRequiredMixin,View):
    def get(self, request):
        listing_form = postForms()
        return render (request, 'components/create-post.html',
                    {'listing_form':listing_form,
                    "route":"create_post"})
        
    def post (self, request):    
        listing_form = postForms(request.POST, request.FILES)
        if listing_form.is_valid():
                listing = listing_form.save(commit=False)
                listing.author = request.user.profile
                listing.save()
                messages.info(request,f'new post was created')
                return redirect('home')
        
    

def post_listing(request,id):
    post_details = Post.objects.filter(id=id)
    return render (request,'components/post.html',
                   {'all_posts':post_details})
    

class edit_view(View):
    def get(self, request, id):
        listing=Post.objects.get(id=id)
        if request.method == 'GET':
            listing_form = postForms(instance=listing) 
            return render (request, 'components/create-post.html',
                        {'listing_form':listing_form,
                            'route':'edit_post'})
    
    def post(self, request,id):
        listing=Post.objects.get(id=id)
        if request.method=='POST':
            try:  
                listing_form = postForms(request.POST, request.FILES, instance=listing)
                if listing_form.is_valid():
                    listing = listing_form.save(commit=False)
                    listing.author = request.user.profile
                    listing.save()
                    messages.info(request,f'The post was updated')
                    return redirect('home')
                else:
                    raise Exception
            except Exception as e:
                print(e)    
            return render (request, 'components/create-post.html',
                        {'listing_form':listing_form})


@login_required
def delete_post(request,id):
    del_post_id = Post.objects.get(id=id)
    del_post_id.delete()
    return redirect('home')