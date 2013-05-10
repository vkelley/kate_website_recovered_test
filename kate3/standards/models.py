from django.db import models

class Subject(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return self.name

class Cluster(models.Model):
	name = models.CharField(max_length=200, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name_plural = 'clusters'

	def __unicode__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=150, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.name

class Subcategory(models.Model):
	name = models.CharField(max_length=150, unique=True)
	category = models.ManyToManyField(Category)

	class Meta:
		ordering = ('name',)
		verbose_name_plural = 'subcategories'

	def __unicode__(self):
		return self.name

class Grade(models.Model):
	name = models.CharField(max_length=10)

	class Meta:
		ordering = ('id',)
		verbose_name_plural = 'Grades'

	def __unicode__(self):
		return self.name

class CommonCoreStandard(models.Model):
	standard_code = models.CharField(max_length=25)
	subject = models.ForeignKey(Subject, blank=True, null=True)
	grade = models.ForeignKey(Grade, blank=True, null=True)
	domain = models.CharField(max_length=5)
	strand = models.CharField(max_length=5, blank=True)
	cluster = models.ForeignKey(Cluster, blank=True, null=True)
	standard = models.IntegerField()
	substandard = models.CharField(max_length=5, blank=True)
	category = models.ForeignKey(Category, blank=True, null=True)
	subcategory = models.ForeignKey(Subcategory, blank=True, null=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ('standard_code',)
		verbose_name = 'Common Core Standard'
		verbose_name_plural = 'Common Core Standard'

	def __unicode__(self):
		return self.standard_code

class Activity(models.Model):
	standard = models.ForeignKey(CommonCoreStandard)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	link = models.URLField()

	class Meta:
		ordering = ('id',)
		verbose_name_plural = 'Activities'

	def __unicode__(self):
		return self.name

class Website(models.Model):
	standard = models.ForeignKey(CommonCoreStandard)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	link = models.URLField()

	class Meta:
		ordering = ('id',)
		verbose_name_plural = 'Websites'

	def __unicode__(self):
		return self.name

class Application(models.Model):
	standard = models.ForeignKey(CommonCoreStandard)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	link = models.URLField()

	class Meta:
		ordering = ('id',)
		verbose_name_plural = 'Applications'

	def __unicode__(self):
		return self.name