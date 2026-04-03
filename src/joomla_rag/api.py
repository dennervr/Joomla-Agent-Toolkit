from pathlib import Path
import urllib.request
import urllib.parse
import json
import sys

CREDENTIALS_PATH = Path.cwd() / ".joomla-rag" / "credentials.json"

def api_login(url: str, token: str):
    # Ensure url doesn't end with slash
    if url.endswith('/'):
        url = url.rstrip('/')
    
    # If not containing /api/index.php/v1 or /api/v1, append /api/index.php/v1
    if '/api/index.php/v1' not in url and '/api/v1' not in url:
        url += '/api/index.php/v1'
    
    # Ensure it doesn't have /api/v1 if it has /api/index.php/v1, but since we append only if not present, ok.
    
    credentials = {"url": url, "token": token}
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_PATH, 'w') as f:
        json.dump(credentials, f)
    print("API credentials saved successfully.")

def api_request(endpoint: str, method: str = "GET", data: dict = None):
    if not CREDENTIALS_PATH.exists():
        print("[ERROR] API Token missing. Please ask the user for their Joomla Super User API Token and the site URL, then run 'joomla-rag api login <url> <token>'")
        sys.exit(1)
    
    with open(CREDENTIALS_PATH, 'r') as f:
        creds = json.load(f)
    
    url = creds["url"] + "/" + endpoint
    headers = {
        "X-Joomla-Token": creds["token"],
        "Content-Type": "application/json",
        "Accept": "application/vnd.api+json"
    }
    
    if data:
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            print(f"[ERROR] HTTP {e.code}: {error_data}")
        except:
            print(f"[ERROR] HTTP {e.code}")
        return None
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

def manage_articles(action: str, id: int = None, title: str = None, text: str = None, search: str = None, limit: int = 5, category: int = None, state: int = None):
    if action == "list":
        endpoint = "content/articles?page[limit]=" + str(limit) + "&fields[articles]=id,title,alias,state,catid"
        if search:
            endpoint += "&filter[search]=" + urllib.parse.quote(search)
        if category is not None:
            endpoint += f"&filter[catid]={category}"
        if state is not None:
            endpoint += f"&filter[state]={state}"
        response = api_request(endpoint)
        if response and "data" in response:
            print("ID  | State | Cat | Title (Alias)")
            print("-" * 40)
            for article in response["data"]:
                attrs = article["attributes"]
                state_str = {1: 'Pub', 0: 'Unpub', -2: 'Trash'}.get(attrs['state'], str(attrs['state']))
                catid = article.get('relationships', {}).get('category', {}).get('data', {}).get('id', '')
                title_alias = f"{attrs['title']} ({attrs.get('alias', '')})"
                print(f"{article['id']:3} | {state_str:5} | {catid:3} | {title_alias}")
        else:
            print("No articles found or error.")
    elif action == "get":
        if not id:
            print("[ERROR] ID required for get action.")
            return
        response = api_request(f"content/articles/{id}")
        if response and "data" in response:
            attrs = response["data"]["attributes"]
            print(f"ID: {response['data']['id']}")
            print(f"Title: {attrs['title']}")
            print(f"Alias: {attrs.get('alias', '')}")
            print(f"State: {'Published' if attrs['state'] == 1 else 'Unpublished'}")
            print(f"Text: {attrs.get('articletext', '')}")
        else:
            print("Article not found or error.")
    elif action == "create":
        if not title or not text:
            print("[ERROR] Title and text required for create action.")
            return
        data = {"title": title, "articletext": text, "catid": 2}
        response = api_request("content/articles", method="POST", data=data)
        if response and "data" in response:
            print(f"Article created with ID: {response['data']['id']}")
        else:
            print("Failed to create article.")
    elif action == "delete":
        if not id:
            print("[ERROR] ID required for delete action.")
            return
        response = api_request(f"content/articles/{id}", method="DELETE")
        if response is None:  # DELETE might return None on success
            print("Article deleted.")
        else:
            print("Failed to delete article.")
    else:
        print(f"[ERROR] Unknown action: {action}")