import sys
import os

def parse_input_file(path):
    fields = []
    if not os.path.exists(path):
        return fields
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or ":" not in line:
                continue
            parts = line.split(":", 1)
            fields.append((parts[0].strip(), parts[1].strip()))
    return fields

def build_search_queries(fields):
    data = dict(fields)
    queries = []
    
    body_elements = [data.get("Brand", ""), data.get("Type", ""), data.get("CPU", "")]
    body_query = " ".join(filter(None, body_elements)).strip()
    if body_query:
        queries.append(("body", body_query))
    
    mouse = data.get("Mouse")
    if mouse:
        mouse_elements = [mouse, data.get("Mouse Model No", "")]
        mouse_query = " ".join(filter(None, mouse_elements)).strip()
        queries.append(("mouse", mouse_query))
    return queries

def get_image_url(query):
    query_formatted = query.replace(" ", ",")
    return f"https://source.unsplash.com/featured/?{query_formatted}"

def main_process(path):
    fields = parse_input_file(path)
    if not fields:
        return []
        
    queries = build_search_queries(fields)
    image_links = []

    for label, q in queries:
        url = get_image_url(q)
        image_links.append((label, url))
    
    return image_links

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        links = main_process(sys.argv[1])
        for label, url in links:
            print(f"{label.upper()}: {url}")
