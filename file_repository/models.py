from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your models here.


class EmailBackend(ModelBackend):
    def authenticate(request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class Repository(models.Model):
    #PK is automatic
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE)
    fileName = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    upload_date = models.DateField('upload_date')
    uploader = models.CharField(max_length=150)
    file_uploaded = models.FileField(upload_to='FILES')

    def get_query_set(self):
        return self.objects.all()

# filter by category

    def get_category(self, category):
        return self.objects.all().filter(category=category)

# sorting
    def get_sorted_increasing(self, order_by):
        return self.objects.all().order_by(order_by)[0:]

    def get_sorted_decreasing(self, order_by):
        return self.objects.all().order_by(order_by)[:0]
# end sorting

    def search(self, search_term):
        fields = [self.fileName, self.category,
                  self.uploader, self.upload_date]
        queries = [Q(**{f + "__icontains": search_term}) for f in fields]
        return queries

    def edit_details(self, id, fileName, category, upload_date):
        repo = get_object_or_404(self, pk=id)
        repo.fileName = fileName if fileName != None else repo.fileName
        repo.category = category if category != None else repo.category
        repo.upload_date = upload_date if upload_date != None else repo.upload_date
        repo.save()
