from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="https://www.gptsportswriter.com",
    api_key="c41a1070cbfa4d5ea66773fc0519716c",
    api_key_location="https://www.gptsportswriter.com/c41a1070cbfa4d5ea66773fc0519716c.txt",
)

sitemap_location = "https://www.gptsportswriter.com/sitemap.xml"

submit_sitemap_to_index_now(authentication, sitemap_location)