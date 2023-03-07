"""formula1_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist

# # weird error that happens when performing migrate (completely unrelated to the Dash plugin)
try:
    from bets_dash.dash_app import dash_app
except OperationalError as err:
    print(f"Probably a false error, but here it goes: \n {err}")
except IndexError as err:
    print(f"Probably a false error, but here it goes: \n {err}")
except ObjectDoesNotExist as err:
    print(f"Probably a false error, but here it goes: \n {err}")
except ProgrammingError as err:
    print(f"Probably a false error, but here it goes: \n {err}")
except AttributeError as err:
    print(f"Probably a false error, but here it goes: \n {err}")


urlpatterns = [
    # this is needed for dash to work
    path("", include("django_plotly_dash.urls")),
    path("admin/", admin.site.urls),
    path("", include("bets_input.urls")),
    path("dash/", include("bets_dash.urls")),
]
