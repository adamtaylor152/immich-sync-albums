# immich-sync-albums
This script will sync all albums from one [immich](https://github.com/immich-app/immich) server to another.

I recently wanted to consolidate all my photos into an [immich](https://github.com/immich-app/immich) instance. Since I imported photos manually over time, not all the metadata was correct, missing dates, etc. I was able to move all the photos into a new instance, but all the work I did to create hundreds of albums was lost.

This simple Python script will recreate and populate all albums in SERVER 1 and replicate them on SERVER 2 using the photo checksum values to write to the replicated albums.

UPDATED FOR NEW IMMICH API PERMISSIONS - API key must have permission to:

Read albums

Read assets

Create albums

Add assets to albums


# ✅ Requirements
Python 3.x

requests package (pip install requests)

Immich tokens for both servers (username/password or API key)

Admin access to both Immich servers


# 🧠 Assumptions
Assets (photos/videos) have been transferred and maintain filename/checksum consistency.

You have admin/user access to both servers.

You use username/password auth (easy to modify for API token auth).



# 🎞️ Usage:

Download the script.

Edit the script and add your values for the servers and API keys.

Config
SERVER1_URL = "http://server1.url/api"

SERVER2_URL = "http://server2.url/api"

API_KEY_1 = "your_server_1_api_key_here"

API_KEY_2 = "your_server_2_api_key_here"

Run the script.
