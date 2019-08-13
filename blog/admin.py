from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Category,Tag,Post
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site

# Register your models here.


class PostInline(admin.TabularInline):   #StackedInline样式不同
	"""在分类页面直接编辑文章"""
	fields = ('title','desc')
	extra = 1 #控制额外多几个
	model = Post



@admin.register(Category,site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
	inlines = [PostInline,] 
	list_display = ('name','status','is_nav','owner','created_time','post_count')
	fields = ('name','status','is_nav','owner')

	"""
	def save_model(self,request,obj,form,change):
		自动设置owner
		obj.owner = request.user
		return super(CategoryAdmin,self).save_model(request,obj,form,change)
	"""

	def post_count(self,obj):
		"""自定义函数"""
		return obj.post_set.count()

	post_count.short_description = '文章数量'



@admin.register(Tag,site=custom_site)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name','status','created_time')
	fields = ('name','status','owner')

	"""
	def save_model(self,request,obj,form,change):
		obj.owner = request.user
		return super(TagAdmin,self).save_model(request,obj,form,change)
	"""



class CategoryOwnerField(admin.SimpleListFilter):
	"""自定义过滤器只展示当前用户分类"""
	title = '分类过滤器' 
	parameter_name = 'owner_category'

	def lookups(self,request,model_admin):
		"""返回要展示的内容和查询用的ID"""
		return Category.objects.filter(owner=request.user).values_list('id','name')

	def queryset(self,request,queryset):
		"""根据URL Query的内容返回列表页数据"""
		category_id = self.value()
		if category_id:
			return queryset.filter(category_id=self.value())
		return queryset

        


@admin.register(Post,site=custom_site)
class PostAdmin(admin.ModelAdmin):
	# 用来配置列表页面展示那些字段
	form = PostAdminForm
	list_display = [
	    'title','category','status',
	    'created_time','owner','operator',
	    ]
	list_display_links = [] #用来配置那些字段可以作为链接，点击他们可以进行编辑

	list_filter = [CategoryOwnerField] #配置页面过滤器，需通过那些字段来过滤列表
	search_fields = ['title','catgroy__name'] #配置搜索字段

	actions_on_top = True
	actions_on_bottom = True

	#编辑页面
	save_on_top = True

	exclude = ('owner',) #指定那些字段不展示

	"""
	fields = (
		('category','title'),
		'decs',
		'status',
		'content',
		'tag',
		)  
	被下文替代
	"""

	fieldsets = (
		('基础配置',{
			'description':'基础配置描述',
			'fields':(
				('title','category'),
				'status',
				),
			}),
		('内容',{
			'fields':(
				'desc',  
				'content',
				),
			}),
		('额外信息',{
			'classes':('collapse',),
			'fields':('tag',),
			}),
		)
	"""
	针对多对多字段展示的配置
	filter_horizontal = ('tag',)
	filter_vertical = ('tage',)
	"""

	def operator(self,obj):
		#自定函数可以返回HTML，需要通过format_html函数处理
		#reverse根据名称解析出URL地址
		return format_html('<a href="{}">编辑</a>',
			reverse('cus_admin:blog_post_change',args=(obj.id,))
			)
	operator.short_description = '操作' #指定表头的展示文案

	"""
	重构至typetider/base_admin.py admin基类中
	def save_model(self,request,obj,form,change):
		obj.owner = request.user
		return super(PostAdmin,self).save_model(request,obj,form,change)

	def get_queryset(self,request):
		qs = super(PostAdmin,self).get_queryset(request)
		return qs.filter(owner=request.user)
	"""

	class Meta:
		css = {
		'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
			),
		}
		js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)



@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
	"""查看操作日志"""
	list_display = ['object_repr','object_id','action_flag','user','change_message']


