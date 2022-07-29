from datetime import datetime

from django.db import models

from db.library.utils.helper import hash_gen


class UserManager(models.Manager):
    def get_user(self, useremail, userpassword):
        user = User.objects.filter(
            use_login=useremail,
            use_password=hash_gen(userpassword),
            use_status=True
        ).values(
            'id',
            'use_login',
            'use_password',
            'use_is_valid'
        ).first()
        return user


class User(models.Model):
    objects = UserManager()
    use_login = models.EmailField(max_length=250)
    use_password = models.CharField(max_length=128)
    use_is_valid = models.BooleanField(default=False)
    use_status = models.BooleanField(default=False)
    use_date_created = models.DateTimeField(editable=False)
    use_date_updated = models.DateTimeField()
    use_date_deleted = models.DateTimeField(
        null=True, default=None, blank=True
    )

    def __str__(self) -> str:
        return self.use_login

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.use_date_created = datetime.now()
        self.use_date_updated = datetime.now()
        return super().save(*args, **kwargs)


class Article(models.Model):
    art_title = models.TextField(null=True, default=None, blank=True)
    art_abstract = models.TextField(null=True, default=None, blank=True)
    art_affiliations = models.TextField(null=True, default=None, blank=True)
    art_authors = models.TextField(null=True, default=None, blank=True)
    art_journal = models.TextField(null=True, default=None, blank=True)
    art_keyword = models.TextField(null=True, default=None, blank=True)
    art_url = models.TextField()
    art_publish_year = models.CharField(
        max_length=4, null=True, default=None, blank=True
    )
    art_date_created = models.DateTimeField(editable=False)
    art_date_updated = models.DateTimeField()

    def __str__(self) -> str:
        return self.art_title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.art_date_created = datetime.now()
        self.art_date_updated = datetime.now()
        return super().save(*args, **kwargs)


class ArticlesWeight(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    wei_score = models.DecimalField(
        max_digits=5, decimal_places=3, default=10
    )
    wei_probability = models.DecimalField(max_digits=9, decimal_places=6)
    wei_date_created = models.DateTimeField(editable=False)
    wei_date_updated = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.article)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.wei_date_created = datetime.now()
        self.wei_date_updated = datetime.now()
        return super().save(*args, **kwargs)
