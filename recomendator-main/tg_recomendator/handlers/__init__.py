from .common import register_common_hadlers
from .admin import register_admin_hadlers
from .categories import register_categories_hadlers
from .search import register_search_hadlers
from .trending import register_trending_hadlers

def register_handlers(dp):
    register_common_hadlers(dp)
    register_admin_hadlers(dp)
    register_categories_hadlers(dp)
    register_search_hadlers(dp)
    register_trending_hadlers(dp)