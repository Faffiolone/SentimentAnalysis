from app.services.news_client import news_instance

azienda = "Elettromedia S.P.A."
notizie = news_instance.search_news(azienda, limit=5)

print(f"\n--- Ultime notizie su {azienda} ---")
for i, testo in enumerate(notizie):
    print(f"[{i+1}] {testo}")