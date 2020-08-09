from django.shortcuts import render, redirect , HttpResponse
from log_reg_app.models import *
from .models import *
from django.contrib import messages
# THIS IMPORT IS FOR FILE UPLOADS
from django.core.files.storage import FileSystemStorage


# LOADS ABOUT PAGE 
def about(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render (request, 'about.html', context)

# LOADS MAIN PAGE 
def dashboard(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'contacts': ContactUser.objects.all(),
        }
        return render (request, 'main_page.html', context)

# LOADS MESSAGE BOARD 
def message_board(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'post': Post.objects.order_by('-updated_at')
        }
        return render (request, 'message_board.html', context)
    
# LOADS MESSAGE PAGE
def message_page(request, id):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        # grabbed current post 
        current_post = Post.objects.get(id=id)
        # got all the likes for that post 
        liked_by = current_post.user_likes.all()
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'posts': Post.objects.get(id=id),
            'current_post': Post.objects.get(id=id),
            # passed into context with this library 
            'liked_by' : liked_by
            
        }
        return render (request, 'message_page.html', context)
    
# LOADS PROFILE PAGE    
def user_profile(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=id),
            'posts': Post.objects.all(),
        }
        
        return render(request, 'profile_page.html', context)
    
# LOADS UPDATE PROFILE PAGE    
def update_profile_page(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'other_users': User.objects.get(id=id),
            'posts': Post.objects.all(),
        }
        return render(request, 'update_profile.html', context)
    
# DELETES A POST
def delete(request, post_id):
    # Deleting a post with the information of the current logged in user 
    to_delete = Post.objects.get(id=post_id)
    if to_delete.author_id == request.session['user_id']:
        to_delete.delete()
    return redirect('/vroom/message_board')

# POSTS A MESSAGE 
def post_mess(request):
    Post.objects.create(content=request.POST['content'], author=User.objects.get(id=request.session['user_id']))
    return redirect('/vroom/message_board')

# COMMENTS ON A POST 
def post_comment(request, id):
    author = User.objects.get(id=request.session['user_id'])
    message = Post.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], author=author, message_post=message)
    return redirect('/vroom/message_board')

# DELETES A COMMENT 
def delete_comment(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        destroyed = Comment.objects.get(id=id)
        destroyed.delete()
        return redirect('/vroom/message_board')

# LIKES A POST 
def add_like(request, id):
    liked_message = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/vroom/message_board')

# # EDITS A PROFILE 
# def edit_profile(request, id):
#     edit_user = User.objects.get(id=id)
#     edit_user.username = request.POST['username']
#     edit_user.car = request.POST['car']
#     edit_user.email = request.POST['email']
#     edit_user.save()
#     return redirect(f'/vroom/user_profile/{id}')

# CONTACT FORM INFO FOR ADMIN VIEWING
def contact(request):
    errors = ContactUser.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='nope')
        return redirect('/vroom/about')
    else:
        ContactUser.objects.create(name=request.POST['name'], email=request.POST['email'], message=request.POST['message'])
    return redirect('/vroom/about')















# you are working on the actual update and upload form now.
# working code below 



# UPLOAD FILE 


# def uploadfilepage(request,id):
#     context = {
#             'user': User.objects.get(id=request.session['user_id']),
            
#         }
#     return render(request, 'uploadfile.html',context)



# def upload(request,id):
#     if request.method == "POST":
        
     
#         context = {
#             "url" : url,
#             "curr_user": curr_user,
#         }
        
#     return render(request, 'uploadfile.html',context)


def edit_profile(request, id):
    curr_user = User.objects.get(id=id)
    curr_user.username = request.POST['username']
    curr_user.car = request.POST['car']
    curr_user.email = request.POST['email']
    picture = request.FILES['picture']
    fs = FileSystemStorage()
    user_picture = fs.save(picture.name, picture)
    url = fs.url(user_picture)
    curr_user.profile_pic = url
    curr_user.save()

    return redirect(f'/vroom/user_profile/{id}')

