from django.contrib import admin
from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
# Register your models here.


class PostInline(admin.TabularInline):    # StackedInline样式不同
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):

    '''自定义过滤器只展示当前用户分类'''

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # 可以在分类页面直接编辑文章
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    # fields = ('name', 'status', 'is_nav', 'owner')
    fields = ('name', 'status', 'is_nav')
    list_filter = [CategoryOwnerFilter]

    # 重写save_model方法，把owner字段设定为当前登录用户
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 配合过滤器，让用户只能看到自己创建的分类
    # def get_queryset(self, request):
    #     qs = super(CategoryAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    # fields = ('name', 'status', 'owner')
    fields = ('name', 'status')
    list_filter = [CategoryOwnerFilter]


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # 自定义form
    form = PostAdminForm
    # exclude可以指定哪些字段不展示
    exclude = ('owner', )
    # 配置列表展示哪些字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    # 配置哪些字段可以作为链接，点击可以进入编辑页面
    list_display_links = []

    # 配置页面过滤器，需要通过哪些字段来过滤列表页
    # list_filter = ['category', ]
    list_filter = [CategoryOwnerFilter]
    # 配置搜索字段
    search_fields = ['title', 'category__name']
    # 动作相关的配置，是否展示在顶部
    actions_on_top = True
    # 是否展示在底部
    actions_on_bottom = True

    # 保存，编辑，编辑并新建按钮是否在顶部展示
    save_on_top = True
    # fields有两个作用，一是限定要展示的字段，二是配置展示字段的顺序
    # fields = (
    #     ("title", "category"),
    #     'status',
    #     'tag',
    #     'desc',
    #     'content',
    #     )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            # classes的作用是给要配置的版块加上一些css属性，Django admin默认支持collapse和wide
            'classes': ('collapse', ),
            'fields': ('tag', ),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # 加载静态资源
    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )
