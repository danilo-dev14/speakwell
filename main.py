from googletrans import Translator
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

words_by_level = {
    "fácil": [
        ("gato", "cat"),
        ("cachorro", "dog"),
        ("maçã", "apple"),
        ("leite", "milk"),
        ("sol", "sun"),
    ],
    "médio": [
        ("casa", "house"),
        ("escola", "school"),
        ("amigo", "friend"),
        ("janela", "window"),
        ("amarelo", "yellow"),
    ],
    "difícil": [
        ("tecnologia", "technology"),
        ("universidade", "university"),
        ("informação", "information"),
        ("pronúncia", "pronunciation"),
        ("imaginação", "imagination"),
    ],
}

print("Bem-vindo ao jogo de pronúncia! Você verá a palavra em português, mas deve pronunciá-la em inglês.")
difficulty = input("Escolha o nível de dificuldade (fácil, médio, difícil): ").lower()
if difficulty not in words_by_level:
    print("Nível de dificuldade inválido. Por favor, escolha entre 'fácil', 'médio' ou 'difícil'.")
    exit()

duration = 5  # segundos de gravação
sample_rate = 44100
recognizer = sr.Recognizer()
translator = Translator()

for pt_word, en_word in words_by_level[difficulty]:
    print(f"🎙 Por favor, pronuncie em inglês a palavra correspondente a: {pt_word}")
    print(f"(Palavra correta em inglês: {en_word})")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print("✅ Gravação concluída, estou reconhecendo...")

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="en-US")
        print("📝 Você disse:", recognized_text)

        if recognized_text.strip().lower() == en_word.lower():
            print("✅ Correto!")
        else:
            print(f"❌ Incorreto! A palavra correta era: {en_word}")

        translated = translator.translate(recognized_text, dest="pt")
        print("🌍 Tradução do que você falou para o português:", translated.text)
        print()

    except sr.UnknownValueError:
        print("😕 A fala não pôde ser reconhecida.")
        print(f"A palavra correta era: {en_word}\n")
    except sr.RequestError as e:
        print(f"❗ Erro no serviço de reconhecimento: {e}")
        break
