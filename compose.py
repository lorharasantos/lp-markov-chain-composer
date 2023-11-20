import os
import re
import string
import random
from graph import Graph, Vertex


def get_words_from_text(text_path):
    with open(text_path, 'rb') as file:
        text = file.read().decode("utf-8")
        text = ' '.join(text.split())
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()

    words = words[:1000]

    return words


def make_graph(words):
    g = Graph()
    prev_word = None

    for word in words:
        word_vertex = g.get_vertex(word)
        if prev_word:
            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex

    g.generate_probability_mappings()

    return g


def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition


def main(artist):
    # passo 1 pegue palavras do texto
    # words = get_words_from_text('texts/hp_sorcerer_stone.txt')

    # for song lyrics
    words = []

    for song_file in os.listdir(f'songs/{artist}'):
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(f'songs/{artist}/{song_file}')
        words.extend(song_words)

    # for song in os.listdir('songs/{}'.format(artist)):
    # if song == '.DS_Store':
    #     continue
    # words.extend(get_words_from_text('songs/{artist}/{song}'.format(artist=artist, song=song)))

    g = make_graph(words)
    composition = compose(g, words, 100)
    return ' '.join(composition)


if __name__ == '__main__':
    print(main(input("Insira o nome do artista: ")))
