from django.contrib.admin import AdminSite

"""自定义网站(site)"""

class CustomSite(AdminSite):
	site_header = 'Typeidea'
	site_title = 'Typeidea 后台管理'
	index_title = '首页'

custom_site =CustomSite(name='cus_admin') 