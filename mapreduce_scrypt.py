import matplotlib.pyplot as plt
import requests
import concurrent.futures
from collections import Counter
from urllib.parse import urlparse

# Функція для завантаження тексту з URL
def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# Мапер для підрахунку частоти слів
def mapper(text):
    # Розділяємо текст на слова і підраховуємо їх кількість
    words = text.split()
    return Counter(words)

# Редуктор для об'єднання результатів
def reducer(results):
    final_count = Counter()
    for count in results:
        final_count.update(count)
    return final_count

# Функція для візуалізації топ-слів
def visualize_top_words(word_freq, top_n=10):
    top_words = word_freq.most_common(top_n)
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Most Frequent Words')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Головна функція для виконання MapReduce та візуалізації результатів
def main(url):
    # Завантаження тексту з URL
    text = fetch_text(url)
    if not text:
        return

    # Розбиваємо текст на частини для MapReduce
    chunks = text.split('\n\n')  # Припустимо, що текст поділений на абзаци для MapReduce

    # Використовуємо ThreadPoolExecutor для асинхронного виконання MapReduce
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Мапуємо функцію mapper до кожного чанку тексту
        mapped_results = executor.map(mapper, chunks)

    # Редукція результатів
    reduced_result = reducer(mapped_results)

    # Візуалізація топ-слів
    visualize_top_words(reduced_result)

if __name__ == "__main__":
    # Приклад використання: задамо URL для завантаження тексту
    url = "https://example.com/text.txt"  # Замініть це на реальний URL

    main(url)
