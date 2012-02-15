from datetime import date, datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import connection, models
from django.db.models import permalink, Q, signals
from django.template.loader import render_to_string

from core.models import ContentArea, Level
from utils.filter_text import *
from utils.stem import get_wildcard_stem
        
class CoreContentManager(models.Manager):
    """
    Custom manager for the ``CoreContent`` model.
    
    The methods here are for giving statistics on what
    ``CoreContent`` objects are being used and which ones are not used.
    """

    def unused(self, content_area_id=None):
        """
        Finds out which ``CoreContent``s are not being used.
        
        If a ``content_area_id`` is given, the ``CoreContent``s
        are filtered based on the ``id``.
        """     
        cursor = connection.cursor()
        extra = ''

        if content_area_id:
            extra = "AND c.content_area_id = %s" % content_area_id

        cursor.execute("""
            SELECT c.id, c.code, c.description
            FROM tick_corecontent c
            LEFT OUTER JOIN tick_resource_content_standards r
            ON c.id = r.corecontent_id
            WHERE r.corecontent_id IS NULL %s
            ORDER BY c.code""" % extra) 
                
        result_list = []
        for row in cursor.fetchall():
            c = {'id': row[0], 'code': row[1], 'description': row[2]}
            result_list.append(c)

        return result_list

class CoreContent(models.Model):
    """
    Core Content class. Used by Resource called content_standards.
    """
    subject = models.CharField(max_length=5)
    level = models.CharField(max_length=5)
    bigidea = models.IntegerField()
    subcategory = models.IntegerField()
    catpoint = models.IntegerField()
    dok = models.IntegerField()
    tested = models.BooleanField()
    code = models.CharField(max_length=25)
    description = models.TextField()
    content_area = models.ForeignKey(ContentArea)
    
    objects = CoreContentManager()

    def __unicode__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name = "Core Content Standard"
        verbose_name_plural = "Core Content Standards"

#Choices for TechIndicator field "indicator"
INDICATOR_CHOICES = (
    ('Indicator 1', 'Indicator 1'),
    ('Indicator 2', 'Indicator 2'),
    ('Indicator 3', 'Indicator 3'),
    ('Indicator 4', 'Indicator 4'),
    ('Indicator 5', 'Indicator 5'),
    ('Indicator 6', 'Indicator 6'),
    ('Indicator 7', 'Indicator 7'),
    ('Indicator 8', 'Indicator 8'),
    ('Indicator 9', 'Indicator 9'),
    ('Indicator 10', 'Indicator 10'),
    ('Indicator 11', 'Indicator 11'),
    ('Indicator 12', 'Indicator 12'),
    ('Indicator 13', 'Indicator 13'),
    ('Indicator 14', 'Indicator 14'),
    ('Indicator 15', 'Indicator 15'),
    ('Indicator 16', 'Indicator 16'),
)

class TechIndicator(models.Model):
    """
    Tech Indicator class.
    """
    standard = models.CharField('standard', max_length=20)
    description = models.TextField()
    tech_standards = models.ManyToManyField("TechnologyStandard")

    def __unicode__(self):
        return self.standard

    class Meta:
        verbose_name = "Kentucky's Teacher Technology Standard"
        verbose_name_plural = "Kentucky's Teacher Technology Standards"
        ordering = ['id',]

class TechnologyComponent(models.Model):
    """
    Technology Component class.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TechnologySubComponent(models.Model):
    """
    Technology Sub Component class.
    """
    name = models.CharField(max_length=50)
    tech_component = models.ForeignKey(TechnologyComponent)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Focus(models.Model):
    """
    Focus class.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SubFocus(models.Model):
    """
    Sub Focus class
    """
    name = models.CharField(max_length=50)
    focus = models.ForeignKey(Focus)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TechnologyStandard(models.Model):
    """
    Technology Standard class.
    """
    point = models.IntegerField()
    subpoint = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=75)
    name = models.CharField(max_length=50)
    #pos = models.ManyToManyField(Pos, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ProgramOfStudy(models.Model):
    """
    Program of Study class.
    """
    code = models.CharField(max_length=45)
    subject = models.CharField(max_length=45)
    level = models.CharField(max_length=45)
    bigidea = models.CharField(max_length=45)
    category = models.CharField(max_length=45)
    point = models.CharField(max_length=45)
    description = models.TextField()
    tech_standards = models.ManyToManyField(TechnologyStandard, null=True, blank=True)

    def __unicode__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name = "Program of Study"
        verbose_name_plural = "Program of Studies"
        
COMMON_CORE_CHOICES = (
    ('CCS', 'CCS'),
    ('CCR', 'CCR'),
)
        
class CommonCoreManager(models.Manager):
    def __init__(self):
        super(CommonCoreManager, self).__init__()
        
    def build_names(self):
        """Used to build the names after import"""
        for c in self.get_query_set().all():
            c.name = c.get_name()
            c.save()
            
    def build_order(self):
        """
        Used to build the order field. Multiplies the ID by 10 to allow
        for records to be added in between records. This is just a way
        to protect the order a little.
        """
        for c in self.get_query_set().all():
            c.order = int(c.id) * 10
            c.save()
        
            
    def build_grades(self):
        """Used to build the grades from the `grade` field"""
        pass
        
    def build_tree(self):
        """Used to build the child/parent relationships of standards"""
        pass

class CommonCoreStandard(models.Model):
    order = models.IntegerField(blank=True)
    name = models.CharField(max_length=18, blank=True)
    group = models.CharField(max_length=4, choices=COMMON_CORE_CHOICES)
    grade = models.CharField(max_length=10)
    #grades = models.ManyToManyField(CommonCoreStandardGrade)
    domain = models.CharField(max_length=5)
    strand = models.CharField(max_length=5, blank=True)
    standard = models.IntegerField()
    sub_standard = models.CharField(max_length=1, blank=True)
    stem = models.BooleanField()
    description = models.TextField(blank=True)
    
    objects = CommonCoreManager()
    
    class Meta:
        ordering = ('id',)
    
    def __unicode__(self):
        return self.name
        
    def get_name(self):
        if self.strand:
            return "%s.%s.%s.%s" % (self.group, self.strand, self.domain, self.standard)
        if self.sub_standard:
            return "%s.%s.%s.%s%s" % (self.group, self.grade, self.domain, self.standard, self.sub_standard)
        return "%s.%s.%s.%s" % (self.group, self.grade, self.domain, self.standard)
        
    def subject(self):
        if self.id <= 488:
            return 'Math'
        return 'Lang/Arts'

# How the resources evaluated
ENTERED_BY_CHOICES = (
    ('hand','Hand'),
    ('computer','Computer'),
    ('none','None'),
    ('evaluated', 'Evaluated'),
    ('web', 'Web')
)

# LoTI levels for Resource field loti_level
LOTI_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)

# Types for Resource field resource_type
TYPE_CHOICES = (
    ('Web', 'Web'),
    ('File', 'File')
)

STATUS_CHOICES = (
    ('none', 'None'),
    ('checked_out', 'Checked Out'),
    ('completed', 'Completed'),
    ('reviewed', 'Reviewed'),
)

# Here are the fields we search when doing a basic search and advanced search
SEARCH_FIELDS = ['title', 'description', 'content_areas__name', 'sub_focus__name']
ADVANCED_SEARCH_FIELDS = ['content_standards', 'common_core_standards', 'levels', 'content_areas', 'sub_focus']
ADVANCED_KEYWORD_SEARCH = ['title', 'description']

ALTERNATIVE_SEARCHES = {'math': 'mathematics'}

class PublicQuerySet(models.query.QuerySet):
    """
    Public Query Set class.  This is for doing the basic and advanced
    searches.

    Usage for Basic Search:
    Resource.public_objects.search('words to search')

    Usage for Advanced Search:
    Resource.public_objects.advanced_search(**form.cleaned_data)
    """
    def __init__(self, model=None, *args, **kwargs):
        super(PublicQuerySet, self).__init__(model, *args, **kwargs)
        self.fields = SEARCH_FIELDS
        self.is_advanced = False
        
    def prep(self):
        """
        This is used when doing advanced searches.  If this class has
        an extra_filter attribute, we unpack it into the filter function
        so we can drill down a little further in our searches.  In the 
        search() function below, there is prep() used on every query
        so we search the same things for each queryset.
        """
        if hasattr(self, 'extra_filter'):
            return self.filter(**self.extra_filter)
        return self

    def search(self, keywords):
        """
        Basic search.  Keyword is required.
        
        This uses a full text search. Read here for docs on full text search:
        http://dev.mysql.com/doc/refman/5.0/en/fulltext-natural-language.html
        
        There are some constraints to how it works, and can cause
        headaches if you don't know them.
        
        Also, to create the full text indexes, there is an SQL file in the SQL folder
        of this app, called resource.sql.  It's automatically ran on syncdb.
        
        A lot goes on here.  First, notice the prep() function used in each 
        lookup.  This is used for advanced searches, which is described in the prep() section.
        
        The function starts out be creating a stem string.  This is a string of "stems" for
        each keyword in the "keywords" variable with a wildcard (*) character on the end.  For
        example, if the keyword is "nationalities, it will strip everything off and create
        a stem "nation" and then add a wildcard to make it "nation*".  This way, when we do
        some of the searches using full text search and the stem, it will find resources that
        have "nations," "national," and "nationality" in it.
        
        After that, we do a series of searches.  First we do a lookup on title and description
        and order it by the scoring.  This gets our best results at the top.
        
        Second, we do a stem search on those same fields and exclude exact matches.
        
        Third, we do content areas, and sub focus.
        """    
        import itertools
        
        queries = []
        
        # Create stem string
        stem_list = []
        stem_string = get_wildcard_stem(keywords) # Custom function I wrote, not part of the library
        
        # First search title and description, sort by score
        queries.append(self.prep().extra(
            select={'score': 'MATCH (title,description) AGAINST ("%s")' % keywords}, 
            where=['MATCH (title,description) AGAINST ("%s")' % keywords]).order_by('-score')
        )
        
        # Do a stem search on title and description
        queries.append(self.prep().extra(
            select={'score': 'MATCH (title, description) AGAINST ("%s" IN BOOLEAN MODE)' % stem_string}, 
            where=['MATCH (title, description) AGAINST ("%s -(%s)" IN BOOLEAN MODE)' % (stem_string, keywords)]).order_by('-score')
        )
        
        if not self.is_advanced:
            # Make a list of resources not to include, if nothing, return 0
            ids = [str(r.id) for r in queries[0]] + [str(r.id) for r in queries[1]] or ['0']
            
            # Find all of the resources that come up with matches using the stem_string
            # in the content_areas and sub_focus fields but are not in the previous searches.
            queries.append(
                self.prep().filter(
                    Q(content_areas__name__search=stem_string) | Q(sub_focus__name__search=stem_string)
                ).extra(where=['tick_resource.id NOT IN (%s)' % ",".join(ids)])
            )
        
        # Create a list of all the results
        queryset = [i for i in itertools.chain(*queries)]
        
        return queryset

    def advanced_search(self, keyword=None, **search_kwarg):
        """
        This searches for the fields selected on the advanced search page.
        None of the fields are required.
        """
        self.fields = ADVANCED_KEYWORD_SEARCH
        self.is_advanced = True
        kwargs = {}
        for key in ADVANCED_SEARCH_FIELDS:
            value = search_kwarg.get(key, None)
            if value:
                kwargs[key] = value
        self.extra_filter = kwargs
        if keyword:
            resources = self.search(keyword)
        else:
            resources = self.filter(**self.extra_filter)
        return resources

class PublicResourceManager(models.Manager):
    """
    Resource manager for querying only public resources and searching those resources
    """
    def __init__(self):
        super(PublicResourceManager, self).__init__()

    def get_query_set(self):
        """ Return only published resources """
        return PublicQuerySet(self.model).filter(published=True)

    def search(self, keyword_string):
        """
        Simple keyword search on public items.  Calls the search function in
        the PublicQuerySet classs.
        """
        return self.get_query_set().search(keyword_string)

    def advanced_search(self, **kwargs):
        """
        For the advanced search, I send a kwarg of my cleaned data (shown below).
        To make it easier, I just use **kwargs so that is all this class
        will accept.

        Usage:
        Resource.public_objects.advanced_search(**form.cleaned_data)
        """
        return self.get_query_set().advanced_search(**kwargs)
        
    def not_aligned(self):
        return self.get_query_set().filter(aligned_to_common_core=False)

class Resource(models.Model):
    """
    Resource class. Dependent on the Level, ContentArea, TechnologyStandard,
    CoreContent, ProgramOfStudy, TechIndicator, Focus, SubFocus, TechnologyComponent,
    TechnologySubComponent, and User classes.
    """
    levels = models.ManyToManyField(Level, blank=True)
    content_areas = models.ManyToManyField(ContentArea, blank=True)
    tech_standards = models.ManyToManyField(TechnologyStandard, null=True, blank=True)
    content_standards = models.ManyToManyField(CoreContent, null=True, blank=True)
    programs_of_studies = models.ManyToManyField(ProgramOfStudy, null=True, blank=True)
    common_core_standards = models.ManyToManyField(CommonCoreStandard, null=True, blank=True)
    tech_indicators = models.ManyToManyField(TechIndicator, null=True, blank=True, verbose_name="Teacher Technology Indicators")
    focus = models.ForeignKey(Focus, blank=True, null=True)
    sub_focus = models.ForeignKey(SubFocus, blank=True, null=True)
    tech_component = models.ForeignKey(TechnologyComponent, blank=True, null=True)
    tech_sub_component = models.ManyToManyField(TechnologySubComponent, null=True, blank=True)
    created = models.DateField(default=date.today())
    resource_type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    source = models.TextField()
    url = models.CharField(max_length=255, null=True, blank=True, unique=True)
    filename = models.FileField(upload_to="tick/resource/%Y/%m/%d", null=True, blank=True)
    published = models.BooleanField()
    feebased = models.BooleanField()
    user = models.ForeignKey(User)
    entered_by = models.CharField(max_length=255, default='none', choices=ENTERED_BY_CHOICES, help_text="This tells how the POS and Tech Standards were generated (by hand, by computer, or not at all)")
    loti_level = models.CharField(max_length=10, choices=LOTI_CHOICES, blank=True)
    disabled = models.BooleanField()
    aligned_to_common_core = models.BooleanField()
    
    aligned_by = models.ForeignKey(User, related_name='aligned_by', blank=True, null=True)
    status = models.CharField(max_length=55, default='none', choices=STATUS_CHOICES, blank=True, null=True)

    objects = models.Manager()
    public_objects = PublicResourceManager()

    def student_tech_standards(self):
        """ Unique programs of study """
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT ts.name AS name, ts.description AS description, ts.id AS id
                          FROM tick_resource_programs_of_studies rps INNER JOIN tick_pos_tech_standards pt
                          ON rps.pos_id = pt.pos_id INNER JOIN tick_technologystandard ts
                          ON pt.technologystandard_id = ts.id
                          WHERE rps.resource_id = %s ORDER BY ts.name""", [self.id])
        row = cursor.fetchall()
        return row

    def teacher_tech_standards(self):
        """ Unique indicators """
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT ts.name AS name, ts.description AS description, ts.id AS id
                          FROM tick_resource_tech_indicators rti INNER JOIN tick_techindicator_tech_standards tt
                          ON rti.techindicator_id = tt.techindicator_id INNER JOIN tick_technologystandard ts
                          ON tt.technologystandard_id = ts.id
                          WHERE rti.resource_id = %s ORDER BY ts.name""", [self.id])
        row = cursor.fetchall()
        return row

    def get_absolute_url(self):
        return ('tick-resource', (), {'object_id': self.id,})
    get_absolute_url = permalink(get_absolute_url)
    
    def get_full_url(self):
        protocol = 'http'
        domain = Site.objects.get_current().domain
        return "http://%s%s" % (domain, self.get_absolute_url())
        
    def short_url(self):
        """
        Uses bitly to shorten the url from `get_full_url`
        katetick123
        """
        from utils import bitly
        a = bitly.Api(login='coekate', apikey='R_d0d4e0623bcd6bee28fe3ae129e61d15')
        return a.shorten(self.get_full_url())
        
    
    def get_url_path(self):
        if hasattr(self.get_url, 'dont_recurse'):
            raise NotImplemented
        try:
            url = self.get_url()
        except NotImplemented:
            raise
        bits = urlparse.urlparse(url)
        return urlparse.urlunparse(('', '') + bits[2:])
    get_url_path.dont_recurse = True

    def get_resource_url(self):
        if self.url:
            return self.url
        if self.filename:
            return self.filename.url
        return ''

    def resource_url(self):
        return self.get_resource_url()
    
    def save(self):
        from kate.logger.models import Entry
        logged = False
        if self.id:
            if self.published:
                resource = Resource.objects.get(pk=self.id)
                if not resource.published:
                    log = Entry.objects.log(self, 'Published')
                else:
                    log = Entry.objects.log(self)
                logged = True
                if not resource.user.is_staff and not resource.published:
                    to_address = resource.user.email
                    from_address = 'Tick@coe.murraystate.edu'
                    subject = 'Dear TICK Contributor'
                    message = render_to_string('tick/published_email.txt',
                                               {'resource': resource, 'site': Site.objects.get_current()})
                    send_mail(subject, message, from_address, [to_address,])
            else:
                log = Entry.objects.log(self, 'Updated')
                logged = True
                
        super(Resource, self).save()
        
        # If this resource was just created, we have to wait until after
        # the save to log the entry.
        if not logged:
            if self.published:
                log = Entry.objects.log(self, 'Published')
            else:
                log = Entry.objects.log(self, 'New')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title',]

class Favorite(models.Model):
    notes = models.TextField()
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True)
    resource = models.ForeignKey(Resource)
    user = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        return 'Favorite: %s' % self.resource
        
    def _get_tags(self):
        return tagging.models.Tag.objects.get_for_object(self)
        
    def _set_tags(self, tag_list):
        tagging.models.Tag.objects.update_tags(self, tag_list)
        
    tags = property(_get_tags, _set_tags)
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        super(Favorite, self).save(*args, **kwargs)

class Announcement(models.Model):
	"""
	Manage announcements through the admin.  Located on right side of the main tick page.
	"""
	created_at = models.DateTimeField(blank=True, null=True)
	body = models.TextField()
	body_html = models.TextField(blank=True)
	body_filter = models.CharField(max_length=100, choices=FILTER_CHOICES, default="Markdown")
	picture = models.FileField(upload_to='tick/announcements/', blank=True, null=True)
	
	def __unicode__(self):
		return self.body
		
	def save(self, *args, **kwargs):
		if not self.id:
			self.created_at = datetime.now()
		self.body_filter = 'Markdown'
		self.body_html = filter_text(self.body, self.body_filter)
		super(Announcement, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ['-created_at',]

class Notice(models.Model):
	"""
	Manage notices and prize notifications through the admin.  Located at the bottom of the main tick page.
	"""
	created_at = models.DateTimeField(blank=True, null=True)
	body = models.TextField()
	body_html = models.TextField(blank=True)
	body_filter = models.CharField(max_length=100, choices=FILTER_CHOICES, default="Markdown")
	winner = models.ManyToManyField(User, null=True, blank=True,
									limit_choices_to={'is_staff': False, 'is_active': True})
	
	def __unicode__(self):
		return self.body
	
	def save(self, *args, **kwargs):
		if not self.id:
			self.created_at = datetime.now()
		self.body_filter = 'Markdown'
		self.body_html = filter_text(self.body, self.body_filter)
		super(Notice, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ['-created_at',]
