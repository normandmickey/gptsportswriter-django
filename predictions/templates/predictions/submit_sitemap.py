from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="https://www.gptsportswriter.com",
    api_key="5c350797837c4c318ea3cf9671c3b3fb",
    api_key_location="https://www.gptsportswriter.com/5c350797837c4c318ea3cf9671c3b3fb.txt",
)

sitemap_location = "https://www.gptsportswriter.com/sitemap.xml"

submit_sitemap_to_index_now(authentication, sitemap_location)