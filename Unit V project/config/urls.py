
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registerPage, name='register'),
    path('create_bounty/', create_bounty, name='create_bounty'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('homepage/', homePage, name='home'),
    path('view_bounty/', viewCreated, name='view'),
    path('edit_bounty/<int:id>/', editBounty, name='edit'),
    path('delete_bounty/<int:id>/', deleteBounty, name='delete'),
    path('hunter_home/', hunter_homePage, name='hunter_home'),
    path('view_all/bounty/', view_allpage, name='view_all'),
    path('add_bounty/<int:id>/', addPage, name='add'),
    path('view_accepted/', viewAccepted, name='accepted'),
    path('remove/<int:id>/', removePage, name='remove'),
    path('completed/<int:id>/', completePage, name='completed'),
    path('customer_complete/', viewCustomerComplete, name='customer_complete')
]
