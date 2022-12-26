import json
from solo.models import SingletonModel
from ckeditor.fields import RichTextField
from django.db import models
from treebeard.mp_tree import MP_Node
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django_extensions.db.fields import AutoSlugField
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.db.models import JSONField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, AutoSlugField
from django.template.loader import render_to_string
from apps.articles.managers import ArticleManager
from colorfield.fields import ColorField
from django.contrib.contenttypes.models import ContentType


class DateBaseModel(models.Model):
    created = CreationDateTimeField(_('created'))
    last_changed_date = ModificationDateTimeField(_('modified'))

    class Meta:
        get_latest_by = 'modified'
        abstract = True

class ArticleCategory(MP_Node):
    name = models.CharField(('Name'), max_length=255)
    name_en = models.CharField(('Name English'), max_length=255)
    color = ColorField(default='#eb6734')
    slug = AutoSlugField(populate_from='name_en', unique=True)
    show_in_content_editor = models.BooleanField(default=True)
    show_in_level_1 = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='category-icons/', null=True, blank=True)
    img_code = models.CharField(max_length=800,null=True, blank=True)

    class Meta:
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'
        permissions = [
            ("can_edit_category", "Can edit Category"),
        ]

    def __str__(self):
        category_tree = '--> '.join([category.name_en for category in self.get_ancestors()])
        if category_tree:
            return '%s --> %s' % (category_tree, self.name_en)
        else:
            return '%s' % (self.name_en)
        return category_dict.get(self.pk, 'Category')

    def get_absolute_url(self):
        return "/news/%s/" %(self.slug)

categories = ArticleCategory.objects.all()
category_dict = dict()
for category in categories:
    category_tree = '--> '.join([category.name_en for category in category.get_ancestors()])
    if category_tree:
        category_tree = '%s --> %s' % (category_tree, category.name_en)
    else:
        category_tree = category.name_en
    category_dict[category.pk] = category_tree       


class ArticleTag(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name = 'Article Tag'
        verbose_name_plural = 'Article Tags'
        permissions = [
            ('can_edit_tag', 'Can Edit Tag')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/tag/%s/' %(self.slug)


class Article(DateBaseModel):

    DRAFT = 'daft'
    PUBLISHED = 'published'
    HIDDEN = 'hidden'
    ARCHIVED = 'archived'
    READYTOPUBLISH = 'readytopublish'
    SUBMITFORREVIEW = 'submitforreview'
    SCHEDULE = 'scheduled'
    DEFAULT = 'default'
    GALLERY_ARTICLE = 'gallery'
    VIDEO = 'video'

    YOUTUBE = 'youtube'
    ADD_MEDIA = 'video'

    PAGE_TYPE_CHOICES = (
        (YOUTUBE, 'Youtube'),
        (ADD_MEDIA, 'video'),
    )

    ARTICLE_CHOICES = (
        (DEFAULT, 'Default'),
        (GALLERY_ARTICLE, 'Gallery'),
        (VIDEO, 'Video'),
    )

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (SUBMITFORREVIEW, 'Submitted for Review'),
        (HIDDEN, 'Hidden'),
        (ARCHIVED, 'Archived'),
        (READYTOPUBLISH, 'Ready to publish'),
        (SCHEDULE, 'Scheduled'),
    )

    title = models.CharField(max_length=500, verbose_name='Headline', db_index=True)
    slug = AutoSlugField(populate_from='title', max_length=500)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default=DRAFT)
    number_of_comments = models.PositiveIntegerField(default=0)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(max_length=250, null=True, help_text='Path to an image',
                                    upload_to='articles/')
    cover_image_description = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(choices=PAGE_TYPE_CHOICES, max_length=200, null=title, blank=True)
    youtube_link = models.CharField(max_length=500, blank=True, null=True)
    location = models.FileField(null=True, blank=True, upload_to='videos/')
    page_title = models.CharField(max_length=500)
    category = models.ForeignKey(ArticleCategory, null=True, related_name='article', blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(ArticleTag, blank=True)
    article_type = models.CharField(choices=ARTICLE_CHOICES, max_length=50, default=DEFAULT)
    trending_article = models.BooleanField(default=False)
    latest_article = models.BooleanField(default=False)
    feature_article = models.BooleanField(default=False)
    objects = ArticleManager()

    class Meta:

        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        permissions = [
            ("can_publish_article", "Can publish the article"),
            ("can_save_draft", "Can save the article as draft"),
            ("can_submit_for_review", "Can submit the article for review"),
            ("can_submit_for_publishing", "Can submit the article for publishing"),
            ("can_edit_article", "Can edit the article"),
            ('can_preview_article', 'Can preview article'),
            ('view_all_articles', 'View all articles'),
            ('can_unpublish_article', 'Can unpublish article'),
            ('can_view_article_history', 'Can View Article History'),
            ('can_schedule_articles', 'Can Schedule Articles for Publishing'),
        ]

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        if self.category:
            return 'http://127.0.0.1:8000/news/%s/%s' % (self.category.name_en, self.slug)
        else:
            return '/news/%s' % (self.slug)


    def get_image_url(self):
        return self.cover_image

    @property
    def get_video_url(self):
        return self.youtube_link

    def render_cover(self):
        return render_to_string('articles/snippets/article_cover_area.html', {'article': self})

    def youtube_video_id(self):
        if self.youtube_link:
            youtube_id = self.youtube_link.split('watch?v=')
        print(youtube_id[1])
        return youtube_id[1]


class ArticleHistory(DateBaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=Article.STATUS_CHOICES, max_length=50)
    title = models.CharField(max_length=500)
    other_changes = JSONField(null=True, blank=True, help_text="json. A json containing the article edit history")

    def __str__(self):
        return self.title

    def save_history(self, article, user):
        self.article = article
        self.description = article.description
        self.title = article.title
        self.status = article.status
        self.user = user
        array_result = serializers.serialize('json', [article], ensure_ascii=False)
        self.other_changes = json.loads(array_result[1:-1])
        self.save()
        return self.title

    @property
    def get_preview_url(self):
        return "/news/%s/?preview=true&history-id=%s" % (self.article.slug, self.pk)


class District(DateBaseModel):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', max_length=200, unique=True)

    def __str__(self):
        return self.name


class Page(DateBaseModel):

    HOME_PAGE = 'home-page'
    DETAIL_PAGE = 'detail-page'
    CATEGORY_PAGE = 'category-page'
    VIDEO_PAGE = 'video-page'
    TAG_PAGE = 'Tag-page'

    DRAFT = 'draft'
    PUBLISHED = 'published'
    INACTIVE = 'inactive'

    PAGE_TYPE_CHOICES = (
        (HOME_PAGE, 'Home'),
        (DETAIL_PAGE, 'Detail'),
        (CATEGORY_PAGE, 'Category'),
        (VIDEO_PAGE, 'video'),
        (TAG_PAGE, 'Tag')
    )

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (INACTIVE, 'Inactive')
    )

    name = models.CharField(max_length=250)
    page_type = models.CharField(choices=PAGE_TYPE_CHOICES, default='', max_length=20)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    layout = models.TextField(help_text='layout html text of the page')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        get_latest_by = 'last_changed_date'
        permissions = [
            ('can_edit_page', 'Can edit page'),
            ('can_modify_page', 'Modify page'),
            ('can_duplicate_and_edit_page', 'Duplicate and Edit page'),
            ('can_view_page_list', 'View Page List'),
            ('can_view_page_code', 'View Page Code'),
            ('can_edit_home_page', 'Can Edit Home Page'),
            ('can_edit_category_page', 'Can Edit Category Page'),
        ]

    def __str__(self):
        return self.name


class LeadNews(DateBaseModel):

    LeadPostitionChoises = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
    )

    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(choices=LeadPostitionChoises, unique=True)
    fixed_lead = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Lead news'
        verbose_name_plural = 'Lead news'
        get_latest_by = ('created')

    def __str__(self):
        return str(self.article)


class LeadNewsHistory(DateBaseModel):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.article)

    class Meta:
        verbose_name = 'Lead news history'
        verbose_name_plural = 'Lead news history'
        get_latest_by = ('created')


class site_cofig(SingletonModel):
    pass





