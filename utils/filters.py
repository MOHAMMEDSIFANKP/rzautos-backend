from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from typing import Dict, List, Any

# Custom filter

def custom_filter(queryset: Any, filter_params: Dict[str, Any], search_fields: List[str], page: int, page_limit: int) -> Any:
    """
    Custom filter, search, and paginate a queryset.
    
    Args:
        queryset: The initial queryset to filter.
        filter_params: A dictionary of parameters to filter on.
        search_fields: A list of fields to perform a search on.
        page: The page number for pagination.
        page_limit: The number of items per page.
    
    Returns:
        A paginated, filtered, and searched queryset.
    
    Raises:
        ValueError: If invalid pagination parameters are provided.
    """

    filter_params = {k: v for k, v in filter_params.items() if k not in ['page', 'page_limit','price_order_type']}

    filter_conditions = Q()
    if filter_params:
        field_names = set(field.name for field in queryset.model._meta.get_fields())

        for key, value in filter_params.items():
            if key == 'search':
                search_conditions = Q()
                for search_field in search_fields:
                    search_conditions |= Q(**{f"{search_field}__icontains": value})
                filter_conditions &= search_conditions
            elif key in field_names or "__" in key and value:
                filter_conditions &= Q(**{key: value})
            else:
                print(f"Warning: Invalid field '{key}' for filtering.")
    filtered_queryset = queryset.filter(filter_conditions)

    paginator = Paginator(filtered_queryset, page_limit)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    return paginated_queryset