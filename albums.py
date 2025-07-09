import requests
from tqdm import tqdm

# === CONFIG ===
SERVER1_URL = "http://server1.url/api"
SERVER2_URL = "http://server2.url/api"
API_KEY_1 = "your_api_key_for_server1"
API_KEY_2 = "your_api_key_for_server2"

# === HELPERS ===
def get_headers(api_key):
    return {
        "x-api-key": api_key,
        "Accept": "application/json"
    }

def get_albums(server_url, headers):
    r = requests.get(f"{server_url}/album", headers=headers)
    r.raise_for_status()
    return r.json()

def get_assets(server_url, headers):
    r = requests.get(f"{server_url}/assets", headers=headers)
    r.raise_for_status()
    return r.json()

def create_album(server_url, headers, album_name):
    r = requests.post(f"{server_url}/album", headers=headers, json={"albumName": album_name})
    r.raise_for_status()
    return r.json()["id"]

def add_to_album(server_url, headers, album_id, asset_ids):
    if not asset_ids:
        return
    r = requests.put(f"{server_url}/album/{album_id}/assets", headers=headers, json={"ids": asset_ids})
    r.raise_for_status()

# === MAIN ===
def main():
    headers1 = get_headers(API_KEY_1)
    headers2 = get_headers(API_KEY_2)

    print("Fetching albums and assets...")
    try:
        albums1 = get_albums(SERVER1_URL, headers1)
        assets1 = get_assets(SERVER1_URL, headers1)
        assets2 = get_assets(SERVER2_URL, headers2)
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return

    # Build checksum -> assetId maps
    assets1_map = {a["id"]: a["checksum"] for a in assets1}
    assets2_checksum_map = {a["checksum"]: a["id"] for a in assets2}

    print(f"Recreating {len(albums1)} albums on Server 2...")

    for album in tqdm(albums1, desc="Albums"):
        album_name = album.get("albumName", "Unnamed Album")
        asset_ids_server1 = album.get("assetIds", [])

        try:
            # Map checksums from server 1 to asset IDs on server 2
            matching_asset_ids = []
            for aid in asset_ids_server1:
                checksum = assets1_map.get(aid)
                if not checksum:
                    continue
                sid2 = assets2_checksum_map.get(checksum)
                if sid2:
                    matching_asset_ids.append(sid2)

            if not matching_asset_ids:
                print(f"⚠️  Skipping album '{album_name}' — no matching assets found.")
                continue

            # Create album and add assets
            new_album_id = create_album(SERVER2_URL, headers2, album_name)
            add_to_album(SERVER2_URL, headers2, new_album_id, matching_asset_ids)

        except Exception as e:
            print(f"❌ Failed to process album '{album_name}': {e}")
            continue

    print("✅ Album recreation completed.")

if __name__ == "__main__":
    main()
