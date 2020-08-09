from django.db import models
from log_reg_app.models import User

# VALIDATION FOR CONTACT US FORM 
class ContactUserManager(models.Manager):
    def validate(self, form_data):
        errors = {}
        if len(form_data['name']) < 1:
            errors['name'] = 'Sorry, you must have a name!'

        if len(form_data['email']) < 1:
            errors['email'] = "C'mon please put in your E-mail!" 
            
        if len(form_data['message']) < 1:
            errors['message'] = "You must have a message!" 
               
        return errors

# VALIDATIONS FOR MESSAGE BOARD
class PostManager(models.Manager):
    def validate(self, form_data):
        errors = {}
        # needs content
        if len(form_data['content']) < 1:
            errors['content'] = 'Content should not be empty.'
            
        return errors

# MODELS 
# MESSAGES 
class Post(models.Model):
    content = models.CharField(max_length=255)
    # users who liked it 
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author_id
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    
    def __str__(self):
        return f"{self.id}{self.content}"
# COMMENTS ON MESSAGES 
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    message_post = models.ForeignKey(Post, related_name="post_comments", on_delete=models.CASCADE)

# CONTACT FORM INFORMATION 
class ContactUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContactUserManager()
    
    def __str__(self):
        return f"{self.id} {self.name}"
    

