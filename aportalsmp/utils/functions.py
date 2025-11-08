from urllib.parse import quote_plus
import re

def listToURL(gifts: list) -> str:
    return '%2C'.join(quote_plus(gift) for gift in gifts)

def activityListToURL(activity: list) -> str:
    return '%2C'.join(activity)

def toShortName(gift_name: str) -> str:
    return gift_name.replace(" ", "").replace("'", "").replace("’", "").replace("-", "").lower()

def convertForListing(nft_id: str = "", price: float = 0):
    return {"nft_id": nft_id, "price": str(price)}

def convertForBuying(nft_id: str = "", price: float = 0):
    return {"id": nft_id, "price": str(price)}