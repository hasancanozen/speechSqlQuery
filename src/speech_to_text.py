# speech_recognition.py
import speech_recognition as sr


def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Konuşmaya başlayın... (Çıkmak için 'çık' yazın)")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                audio = recognizer.listen(source)
                print("Ses alındı, metne dönüştürülüyor...")
                text = recognizer.recognize_google(audio, language='tr-TR')
                print("Duyduğum: ", text)

                # Yıldız ve alt çizgi karakterlerini dönüştürme
                text = text.lower()  # Duyduğumuz metni küçük harfe çeviriyoruz
                text = text.replace("yıldız", "*")  # "yıldız" kelimesini "*" ile değiştiriyoruz
                text = text.replace("alt çizgi", "_")  # "alt çizgi" ifadesini "_" ile değiştiriyoruz

                print("Dönüştürülmüş metin: ", text)

                if 'çık' in text:
                    print("Program sonlandırılıyor.")
                    break

            except sr.UnknownValueError:
                print("Anlaşılamadı, tekrar deneyin.")
            except sr.RequestError as e:
                print(f"Hata oluştu: {e}")
