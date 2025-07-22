import requests
import os
from datetime import datetime
import sys

class RaindropClient:
    def __init__(self, token=None):
        self.api_base = "https://api.raindrop.io/rest/v1"
        self.token = token or os.environ.get("RAINDROP_TOKEN")
        
        if not self.token:
            print("Error: Raindrop.io API token is required.")
            print("Please set the RAINDROP_TOKEN environment variable or pass it as an argument.")
            sys.exit(1)
    
    def _fetch_paginated_bookmarks(self, collection_id, limit, sort, start_page=0):
        """Helper method to fetch bookmarks with automatic pagination
        
        Args:
            collection_id (int): The ID of the collection (0 for "All bookmarks")
            limit (int): Total number of bookmarks to fetch
            sort (str): Sort order
            start_page (int): Starting page number
            
        Returns:
            list: List of bookmark objects or None if error
        """
        all_bookmarks = []
        current_page = start_page
        remaining_limit = limit
        
        while remaining_limit > 0:
            # Fetch up to 50 bookmarks per page (API maximum)
            page_limit = min(50, remaining_limit)
            
            url = f"{self.api_base}/raindrops/{collection_id}"
            
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            
            params = {
                "sort": sort,
                "perpage": page_limit,
                "page": current_page
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None if not all_bookmarks else all_bookmarks
            
            page_bookmarks = response.json().get("items", [])
            
            # If we got no bookmarks, we've reached the end
            if not page_bookmarks:
                break
            
            all_bookmarks.extend(page_bookmarks)
            remaining_limit -= len(page_bookmarks)
            current_page += 1
            
            # If we got fewer bookmarks than requested, we've reached the end
            if len(page_bookmarks) < page_limit:
                break
        
        return all_bookmarks
    
    def get_latest_bookmarks(self, limit=10):
        """Get the latest bookmarks from Raindrop.io"""
        return self._fetch_paginated_bookmarks(0, limit, "-created", 0)
    
    def get_collection_bookmarks(self, collection_id, limit=25, sort="-created", page=0):
        """Get bookmarks from a specific collection
        
        Args:
            collection_id (int): The ID of the collection to fetch bookmarks from
            limit (int, optional): Number of bookmarks to return. Defaults to 25.
            sort (str, optional): Sort order. Defaults to "-created" (newest first).
                Other options: "created", "title", "-title", "domain", "-domain"
            page (int, optional): Page number for pagination. Defaults to 0.
            
        Returns:
            list: List of bookmark objects or None if error
        """
        return self._fetch_paginated_bookmarks(collection_id, limit, sort, page)
    
    def get_collections(self):
        """Get all collections
        
        Returns:
            list: List of collection objects or None if error
        """
        # Get root collections
        url = f"{self.api_base}/collections"
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
        root_collections = response.json().get("items", [])
        
        # Get child collections
        url = f"{self.api_base}/collections/childrens"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return root_collections  # Return at least root collections
        
        child_collections = response.json().get("items", [])
        
        # Combine all collections
        all_collections = root_collections + child_collections
        
        # Add system collections
        system_collections = [
            {"_id": 0, "title": "All Bookmarks"},
            {"_id": -1, "title": "Unsorted"},
            {"_id": -99, "title": "Trash"}
        ]
        
        return system_collections + all_collections
    
    def find_collection_by_name(self, name):
        """Find a collection by its name
        
        Args:
            name (str): Collection name to search for
            
        Returns:
            dict: Collection object or None if not found
        """
        collections = self.get_collections()
        if not collections:
            return None
        
        # First try exact match (case insensitive)
        for collection in collections:
            if collection.get("title", "").lower() == name.lower():
                return collection
        
        # Then try partial match
        for collection in collections:
            if name.lower() in collection.get("title", "").lower():
                return collection
        
        return None

def format_bookmark(bookmark):
    """Format a bookmark for display"""
    created = datetime.fromisoformat(bookmark.get("created", "").replace("Z", "+00:00"))
    created_str = created.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "title": bookmark.get("title", "No title"),
        "link": bookmark.get("link", "No link"),
        "created": created_str,
        "tags": bookmark.get("tags", []),
        "collection": bookmark.get("collection", {}).get("title", "Unsorted")
    } 