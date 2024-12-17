import bs4

html = """
<html>
    <head><title>Example Page</title></head>
    <body>
        <h1>Welcome to BeautifulSoup</h1>
        <p>This is a paragraph.</p>
        <a href="https://example.com">Visit Example</a>
    </body>
</html>
"""

bs = bs4.BeautifulSoup(html, 'html.parser')
print(bs.contents)

print(bs.find_all('p', class_=''))