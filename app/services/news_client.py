from GoogleNews import GoogleNews

class NewsClient:
    def __init__(self):
        # Configura Google News (Lingua Inglese, ultimi 7 giorni)
        self.googlenews = GoogleNews(lang='en', period='7d')
        print("✅ Google News Client initialized")

    def search_news(self, query: str, limit: int = 10):
        """
        Cerca news iterando sulle pagine finché non raggiunge il 'limit'.
        """
        print(f"🔎 Searching News for: {query} (Target: {limit})...")
        self.googlenews.clear()
        
        # 1. Prima ricerca (Pagina 1)
        self.googlenews.search(query)
        all_results = self.googlenews.result()
        
        # 2. Se non bastano, scarichiamo le pagine successive
        page = 2
        while len(all_results) < limit:
            print(f"   ... Fetching page {page} to reach limit ...")
            self.googlenews.getpage(page)
            new_results = self.googlenews.result()
            
            # Se la pagina nuova non aggiunge nulla, ci fermiamo (fine notizie)
            if len(new_results) == len(all_results):
                break
                
            all_results = new_results
            page += 1
            
            # Safety break: Non andiamo oltre pagina 5 per non bloccare tutto
            if page > 5: 
                break

        # 3. Estrazione e Pulizia
        texts_found = []
        # Prendiamo un po' più risultati del necessario per compensare quelli vuoti
        for news in all_results:
            full_text = f"{news['title']}. {news['desc']}"
            
            # Pulizia base: evitiamo stringhe vuote o troppo corte
            if len(full_text) > 20: 
                texts_found.append(full_text)
                
            # Se abbiamo raggiunto il numero richiesto, ci fermiamo
            if len(texts_found) >= limit:
                break
                    
        print(f"✅ Found {len(texts_found)} news items for '{query}'")
        return texts_found

news_instance = NewsClient()