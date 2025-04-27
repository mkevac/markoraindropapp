import sys
import argparse
from .client import RaindropClient, format_bookmark

def main():
    parser = argparse.ArgumentParser(description="Raindrop.io CLI")
    parser.add_argument("--token", help="Raindrop.io API token (optional if set as environment variable)")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List collections command
    list_collections_parser = subparsers.add_parser("collections", help="List all collections")
    
    # Bookmarks command
    bookmarks_parser = subparsers.add_parser("bookmarks", help="Get bookmarks")
    bookmarks_parser.add_argument("--collection", help="Collection name to fetch bookmarks from")
    bookmarks_parser.add_argument("--limit", type=int, default=10, help="Number of bookmarks to fetch (default: 10)")
    bookmarks_parser.add_argument("--sort", default="-created", help="Sort order (default: -created)")
    bookmarks_parser.add_argument("--page", type=int, default=0, help="Page number for pagination (default: 0)")
    
    args = parser.parse_args()
    
    # If no command was provided, default to 'bookmarks'
    if not args.command:
        args.command = "bookmarks"
        args.collection = None
        args.limit = 10
        args.sort = "-created"
        args.page = 0
    
    client = RaindropClient(args.token)
    
    if args.command == "collections":
        # List all collections
        collections = client.get_collections()
        if not collections:
            print("No collections found or error occurred.")
            return
        
        print("\nRaindrop.io Collections:\n")
        for i, collection in enumerate(collections, 1):
            print(f"{i}. {collection.get('title', 'Unnamed')} (ID: {collection.get('_id')})")
            if collection.get("count") is not None:
                print(f"   Bookmarks: {collection.get('count')}")
            print()
    
    elif args.command == "bookmarks":
        if args.collection:
            # Find collection by name
            collection = client.find_collection_by_name(args.collection)
            if not collection:
                print(f"Collection '{args.collection}' not found. Use 'collections' command to see available collections.")
                return
            
            # Get bookmarks from specific collection
            collection_id = collection.get("_id")
            bookmarks = client.get_collection_bookmarks(
                collection_id=collection_id,
                limit=args.limit,
                sort=args.sort,
                page=args.page
            )
            collection_text = f"Collection: {collection.get('title')}"
        else:
            # Get latest bookmarks (all collections)
            bookmarks = client.get_latest_bookmarks(args.limit)
            collection_text = "All collections"
        
        if not bookmarks:
            print("No bookmarks found or error occurred.")
            return
        
        print(f"\nRaindrop.io bookmarks ({collection_text}):\n")
        
        for i, bookmark in enumerate(bookmarks, 1):
            formatted = format_bookmark(bookmark)
            print(f"{i}. {formatted['title']}")
            print(f"   URL: {formatted['link']}")
            print(f"   Created: {formatted['created']}")
            print(f"   Collection: {formatted['collection']}")
            if formatted['tags']:
                print(f"   Tags: {', '.join(formatted['tags'])}")
            print()

if __name__ == "__main__":
    main() 