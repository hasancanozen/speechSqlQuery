from src.speech_to_text import recognize_speech_from_mic
from src.db_connection import create_connection, execute_query, close_connection
import sqlparse

# Türkçe karakterleri İngilizce karşılıklarına dönüştüren fonksiyon
def normalize_turkish_characters(text):
    # Türkçe karakterleri İngilizce karşılıklarına dönüştürmek için bir dönüşüm haritası
    translation_table = str.maketrans("çığöşü", "cigosu")
    return text.translate(translation_table)

def is_sql_query(query):
    sql_keywords = ["select", "insert", "update", "delete", "from", "where", "join", "create", "drop"]
    words = query.lower().split()
    return any(keyword in words for keyword in sql_keywords)

def is_valid_sql(query):
    try:
        parsed = sqlparse.parse(query)
        return len(parsed) > 0
    except Exception:
        return False

def attempt_query_correction(query):
    query = query.lower()
    corrections = {
        "selek": "select",
        "prom": "from",
        "wer": "where",
    }
    for wrong, correct in corrections.items():
        query = query.replace(wrong, correct)
    return query

def main():
    connection = None
    try:
        connection = create_connection()
        print("Veritabanı bağlantısı başarıyla kuruldu.")

        while True:
            print("Sorgunuzu söyleyin... (Çıkmak için 'çık' deyin)")
            query = recognize_speech_from_mic()

            if query.lower() == "çık":
                print("Uygulama sonlandırılıyor...")
                break

            print(f"Duyulan metin: {query}")

            # Türkçe karakterleri normalleştire
            normalized_query = normalize_turkish_characters(query)
            print(f"Dönüştürülmüş metin: {normalized_query}")

            # Sorgu düzeltmelerini uygula
            query = attempt_query_correction(normalized_query)
            print(f"Düzeltilmiş sorgu: {query}")

            if is_sql_query(query) and is_valid_sql(query):
                try:
                    results = execute_query(query, connection)
                    for row in results:
                        print(row)
                except Exception as e:
                    print(f"Sorgu çalıştırılırken bir hata oluştu: {e}")
            else:
                print("Bu metin bir SQL sorgusu değil veya geçerli bir sorgu değil.")
    except Exception as e:
        print(f"Veritabanına bağlanırken bir hata oluştu: {e}")
    finally:
        if connection:
            close_connection(connection)

if __name__ == "__main__":
    main()
