from django.urls import path
from . import views


urlpatterns = [
    
   path('', views.dashboard, name="dashboard"), 
   path('about', views.about, name="about"), 
   path('<int:post_id>/delete', views.delete, name="delete"),
   path('post_message', views.post_mess, name="post_mess"),
   path('add_comment/<int:id>', views.post_comment, name="post_comment"),
   path('like/<int:id>', views.add_like, name="add_like"),
   path('delete/<int:id>', views.delete_comment, name="delete_comment"),
   path('message_board/', views.message_board, name="message_board"),
   path('message_page/<int:id>', views.message_page, name="message_page"),
   path('user_profile/<int:id>', views.user_profile, name="user_profile"),
   path('update_profile_page/<int:id>', views.update_profile_page, name="update_profile_page"),
   path('edit_profile/<int:id>', views.edit_profile, name="edit_profile"),
   path('contact/', views.contact, name="contact"),
   
   
    
]