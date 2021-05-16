from bs4 import BeautifulSoup
from requests import get
from sys import argv

# Kana range in unicode
START = ord("\u3040")
END = ord("\u30FF")

# Unicode of Japanese full stop, kuten.
KUTEN = "\u3002"


def handle_definitions(defs):
    """Returns a list of dictionaries
    containing kanji definitions/info"""

    results = []
    tag = ""

    for d in defs:
        res = ""

        # If the current thing is a tag, it corresponds to the next definition
        if d["class"] == ["meaning-tags"]:
            tag = d.text + "\n"
            continue

        # If the definition gives an example sentence
        if d.find("div", class_="sentence"):
            example = d.find_all("span", class_=["furigana", "unlinked"])
            furigana = [f.text for f in d.find_all("span", class_="furigana")]
            sentence = sentence_to_markdown(example, furigana)
            ex = d.find("div", class_="sentence").text.split(KUTEN)[0]

            # ex = [word.text for word in example]
            # ex.append(KUTEN)
            res = tag + d.text.replace("\u200b", "\n")
            res = res.replace(KUTEN, "\n")
            res = res.replace(ex, "\n" + sentence)
            res = res.replace("\n\n", "\n")

            if d.find("span", class_="supplemental_info"):
                keys = ["tag", "definition", "info", "example", "translation"]
            else:
                keys = ["tag", "definition", "example", "translation"]

        # If the current thing is a Wikipedia definition, handle the abstract
        elif tag == "Wikipedia definition\n":
            res = tag + d.text.split("\u200b", maxsplit=1)[0]
            res += "\n" + d.find(class_="meaning-abstract").next
            res += "".join(
                str(elem) for elem in d.find(class_="meaning-abstract").findChildren()
            )
            keys = ["tag", "definition", "info", "abstract"]

        # If there's no example sentence
        else:
            res = tag + d.text.replace("\u200b", "\n")
            keys = ["tag", "definition", "info"]

        tag = ""
        values = res.split("\n")
        definition = dict(zip(keys, values))
        results.append(definition)

    return results


def get_contained_kanji(contained_info):
    """Returns a list of dictionaries representing
    each contained kanji. Keys are:
    kanji, definition, kun and on."""

    contained = []

    for k in contained_info:
        kanji_info = k.find("div", class_="literal_block")
        kanji = (
            kanji_info.text.strip(),
            kanji_info.a["href"].replace("//", "https://www."),
        )
        definitions = k.find("div", class_="meanings english sense").text.replace(
            "\n", ""
        )

        kun_info = k.find("div", class_="kun readings")
        on_info = k.find("div", class_="on readings")

        res = {"kanji": kanji, "definitions": definitions}

        if kun_info:
            k_hrefs = [
                a["href"].replace("//", "https://www.") for a in kun_info.find_all("a")
            ]
            kun = list(zip(kun_info.text.strip().split()[1:], k_hrefs))
            res["kun"] = kun

        if on_info:
            o_hrefs = [
                a["href"].replace("//", "https://www.") for a in on_info.find_all("a")
            ]
            on = list(zip(on_info.text.strip().split()[1:], o_hrefs))
            res["on"] = on

        contained.append(res)

    return contained


def is_kana(char):
    return START <= ord(char) <= END


def get_kanji_furigana(soup):

    furi = soup.find_all("span", class_="kanji")

    if furi:
        kanji_text = (
            soup.find("div", class_="concept_light clearfix")
            .find("span", class_="text")
            .text.strip()
        )
        main_furigana = [f.text for f in furi]

        idx = 0
        for i in range(len(kanji_text)):
            if not is_kana(kanji_text[i]):
                idx = i
                break

        start = kanji_text[:idx]
        kanji = [kanji_text[idx]]
        idx += 1

        # If the remaning characters are all kana, add them together
        if kanji_text[idx:] and all(is_kana(char) for char in kanji_text[idx:]):
            kanji.append(kanji_text[idx:])

        else:
            for char in kanji_text[idx:]:
                if is_kana(char):
                    kanji[-1] += char

                else:
                    kanji.append(char)
    else:
        kanji = [soup.find("rb").text]
        main_furigana = [soup.find("rt").text]

    return start, kanji, main_furigana


def contained_kanji_to_markdown(contained):

    result = (
        f"## [{contained['kanji'][0]}]({contained['kanji'][1]})\n"
        f"*{contained['definitions']}*\n"
    )

    if "kun" in contained:
        result += f"Kun:  "

        for kun in contained["kun"]:
            result += f"[{kun[0]}]({kun[1]}), "

        result = result[:-2] + "\n"

    if "on" in contained:
        result += "On   :"

        for on in contained["on"]:
            result += f"[{on[0]}]({on[1]}), "

        result = result[:-2] + "\n"

    return result


def kanji_to_markdown(start, kanji, furigana):
    """Takes a list of kanji and their corresponding
    furigana and returns a string that will display
    the kanji with furigana in markdown."""

    final = "<ruby> "

    if start:
        final = start + final

    for _ in range(len(furigana)):
        final += f"{kanji.pop(0)} <rp>(</rp><rt> {furigana.pop(0)} </rt><rp>)</rp> "

    if kanji:
        final += f"{''.join(kanji)}"

    final += "</ruby>"

    return final


def sentence_to_markdown(sentence, furigana):
    """Takes a sentence, which is a result set of all the
    words in the sentence, and takes a list of furigana
    in the sentence, then returns a string that will
    display the sentence with furigana in markdown."""

    final = ""
    kanji = False

    for word in sentence:

        if kanji:
            final += f"<ruby> {word} <rp>(</rp><rt> {furigana.pop(0)} </rt><rp>)</rp> </ruby>"
            kanji = False
            continue

        if word["class"] == ["furigana"]:
            kanji = True

        else:
            final += word.text

    return final + KUTEN


def defs_to_markdown(defs):
    """Takes a dictionary containing the definition
    info for one kanji, and returns a string that
    will display the defnition in markdown."""

    if defs["tag"]:
        md = f'<sub> {defs["tag"]} </sub><br>\n'

    else:
        md = ""

    md += f'<dt><strong> {defs["definition"]} </strong></dt><br>\n'

    if "info" in defs:
        md += f'  <dd> {defs["info"]} </dd><br>\n'

    if "abstract" in defs:
        md += f'  <dd> {defs["abstract"]} </dd><br>\n'

    if "example" in defs:
        md += (
            f'  <dd> {defs["example"]} </dd>\n'
            f'  <dd> {defs["translation"]} </dd><br>\n'
        )
    return md


def get_kanji(word):

    url = f"https://jisho.org/word/{word}"
    response = get(url)

    # print(url, response)
    soup = BeautifulSoup(response.text, "html.parser")
    just_kana = True

    for i in word:
        if not is_kana(i):
            just_kana = False
            break

    # Get kanji we are defining; turn into markdown to display furigana
    if not just_kana:
        start, kanji, main_furigana = get_kanji_furigana(soup)
        kanji_md = kanji_to_markdown(start, kanji, main_furigana)

    else:
        kanji_md = kanji_to_markdown(word, [], [])

    # Get all definitions
    all_defs = soup.find("div", class_="meanings-wrapper")
    definitions = handle_definitions(all_defs)

    # Get contained kanji details
    contained_info = soup.find_all("div", class_="entry kanji_light clearfix")
    contained_kanji = get_contained_kanji(contained_info)

    # Generate markdown for this kanji
    header = "# " + kanji_md
    definitions = (
        "<dl>\n" + "".join(defs_to_markdown(d) for d in definitions) + "</dl>\n"
    )
    contained = "## Kanji in this word: \n" if not just_kana else ""
    link = f"\n[Open in Jisho...]({url})\n\n"

    for c in contained_kanji:
        contained += contained_kanji_to_markdown(c) + "\n"

    return header + "\n" + definitions + "\n" + contained + link


if __name__ == "__main__":

    # print(get_kanji("来る"))

    with open(argv[1], "a", encoding="utf-8") as f:
        for kanji in argv[2:]:
            print(kanji)
            # print(get_kanji(kanji))
            f.write(get_kanji(kanji))
