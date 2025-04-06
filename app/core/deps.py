from typing import Optional
from app.services.yelp_client import YelpClient

class ResourceContainer:
    def __init__(self):
        self.yelp_client: Optional[YelpClient] = None

resources: Optional[ResourceContainer] = None

def set_resources(res: ResourceContainer):
    global resources
    resources = res

def get_resources() -> ResourceContainer:
    if not resources:
        raise Exception("Resources not initialized")
    return resources