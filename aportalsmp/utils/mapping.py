from aportalsmp.handlers import fetch, requestExceptionHandler
from aportalsmp.utils.other import HEADERS_MAIN
from aportalsmp.utils.functions import toShortName

###########################
# Collection ID Mapping   #
###########################

# Global memory cache for collections
_collections_cache = None


async def get_collection_id(gift_name: str, authData: str = "") -> str:
    """
    Get collection ID (UUID) for a gift name.

    Behavior:
    - Normalizes gift name to short format (removes all non-alphanumeric characters, lowercase)
    - First call: Fetches all collections from API and caches in memory
    - If gift not found: Re-fetches from API to get latest collections
    - If still not found: Raises ValueError

    Args:
        gift_name (str): Name of the gift (e.g., "Jack-in-the-Box")
        authData (str): The authentication data required for the API request.

    Returns:
        str: Collection UUID for the gift

    Raises:
        ValueError: If gift name is not found in available collections
    """
    global _collections_cache

    # Normalize the gift name to short format for matching
    normalized_name = toShortName(gift_name)

    # First run: fetch and cache
    if _collections_cache is None:
        await _fetch_and_cache_collections(authData)

    # Try to find in cache using normalized name
    if normalized_name in _collections_cache:
        return _collections_cache[normalized_name]

    # Not found: re-fetch to get latest collections
    await _fetch_and_cache_collections(authData)

    # Try again after refresh
    if normalized_name in _collections_cache:
        return _collections_cache[normalized_name]

    # Still not found: raise error
    raise ValueError(f"aportalsmp: get_collection_id(): Error: Gift name '{gift_name}' not found in available collections")


async def get_collection_ids(gift_names: list, authData: str = "") -> list:
    """
    Get collection IDs for multiple gift names.

    Args:
        gift_names (list): List of gift names
        authData (str): The authentication data required for the API request.

    Returns:
        list: List of collection UUIDs

    Raises:
        ValueError: If any gift name is not found
    """
    return [await get_collection_id(name, authData) for name in gift_names]


async def _fetch_and_cache_collections(authData: str = ""):
    """
    Fetches all collections from API and caches {short_name: id} mapping in memory.

    The cache uses normalized short names as keys (all non-alphanumeric characters removed, lowercase).
    This allows matching regardless of apostrophe style, spaces, hyphens, etc.

    Examples of normalized keys:
    - "Durov's Cap" -> "durovscap"
    - "Jack-in-the-Box" -> "jackinthebox"
    - "Plush Pepe" -> "plushpepe"

    Internal function called by get_collection_id() when cache is empty or needs refresh.

    Args:
        authData (str): The authentication data required for the API request.
    """
    global _collections_cache

    url = "https://portal-market.com/api/collections/filters/preview?owned_only=false"

    # Build headers with auth
    headers = {**HEADERS_MAIN, "Authorization": authData}

    # Fetch from API
    response = await fetch(method="GET", url=url, headers=headers)

    # Handle errors
    requestExceptionHandler(response, "get_collection_id")

    # Parse response
    data = response.json()

    # Build cache: {short_name: id}
    # Store collections using normalized short names as keys for robust matching
    _collections_cache = {}
    for collection in data.get("collections", []):
        original_name = collection["name"]
        normalized_name = toShortName(original_name)
        _collections_cache[normalized_name] = collection["id"]
