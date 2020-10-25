# Jisho
Python script which takes a kanji, scrapes [Jisho](https://jisho.org/) for its definition and turns this information into markdown output for notes. The output can be directly appended to a markdown file, or it can be copied and pasted into a markdown viewer/editor. [Typora](https://typora.io/) is a very aesthetically pleasing markdown edition/viewer which supports a variety of syntax. Alternatively, you can use an online editor such as [StackEdit](https://stackedit.io/app#), which also supports the markdown syntax my program returns.

You must have Python 3 and pip installed. Using pip, install "requests" and "beautifulsoup4".

# Examples

## Kanji

Running ```> python3 Jisho.py 旅行 >> Notes.md``` in the MacOS terminal will result in Notes.md being filled with:
<br>

# <ruby> 旅 <rp>(</rp><rt> りょ </rt><rp>)</rp> 行 <rp>(</rp><rt> こう </rt><rp>)</rp> </ruby>
<dl>
<dt><strong> Noun, Suru verb </strong></dt>
<dd> 1. travel; trip; journey; excursion; tour </dd>

<br>
<dt><strong> Wikipedia definition </strong></dt>
<dd> 2. Travel </dd>

<br>
</dl>

## Kanji in this word: 
## [旅](https://www.jisho.org/search/%E6%97%85%20%23kanji)
*trip, travel*  
Kun:  [たび](https://www.jisho.org/search/%E6%97%85%20%E3%81%9F%E3%81%B3)  
On   :[リョ](https://www.jisho.org/search/%E6%97%85%20%E3%82%8A%E3%82%87)  
## [行](https://www.jisho.org/search/%E8%A1%8C%20%23kanji)
*going, journey, carry out, conduct, act, line, row, bank*  
Kun:  [い.く、](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%84%E3%81%8F), [ゆ.く、](https://www.jisho.org/search/%E8%A1%8C%20%E3%82%86%E3%81%8F), [-ゆ.き、](https://www.jisho.org/search/%E8%A1%8C%20%E3%82%86%E3%81%8D), [-ゆき、](https://www.jisho.org/search/%E8%A1%8C%20%E3%82%86%E3%81%8D), [-い.き、](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%84%E3%81%8D), [-いき、](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%84%E3%81%8D), [おこな.う、](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%8A%E3%81%93%E3%81%AA%E3%81%86), [おこ.なう](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%8A%E3%81%93%E3%81%AA%E3%81%86)  
On   :[コウ、](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%93%E3%81%86), [ギョウ、](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%8E%E3%82%87%E3%81%86), [アン](https://www.jisho.org/search/%E8%A1%8C%20%E3%81%82%E3%82%93)  

[Open in Jisho...](https://jisho.org/word/旅行)
<br>

## Vocabulary

Running ```> python3 Jisho.py だらけ >> Notes.md``` in the MacOS terminal will result in:
<br>

# だらけ<ruby> </ruby>
<dl>
<dt><strong> 1. full of (e.g. mistakes); riddled with </strong></dt>
<dd>  </dd>
<dd> この<ruby> 本 <rp>(</rp><rt> ほん </rt><rp>)</rp> </ruby>は<ruby> 間違い <rp>(</rp><rt> まちが </rt><rp>)</rp> </ruby>だらけだ。 </dd>

<br>
<dt><strong> 2. covered all over with (blood, mud, etc.) </strong></dt>
<dd>  </dd>
<dd> その<ruby> 部屋 <rp>(</rp><rt> へや </rt><rp>)</rp> </ruby>は紙くずだらけだった。 </dd>

<br>
</dl>


[Open in Jisho...](https://jisho.org/word/だらけ)
<br>

## How to use

1. Open the terminal
2. Navigate to the directory which contains Jisho.py
3. Type in the following command, replacing "x" with the kanji you would like to search for, and "Notes" with whatever you'd like to call your notes file (make sure to still keep the .md extension). <br>
```> python3 Jisho.py x >> Notes.md```
4. Repeat with as may kanji as you'd like; they'll get added on to the end of the file.

You can also just run ```> python3 Jisho.py x```, then copy the output to a markdown file or editor.

## Important Note

Kanji or Vocabulary will only work if the word you input matches the Jisho url of the word. For example:
- The url for だらけ is https://jisho.org/word/だらけ
- The url for 旅行 is https://jisho.org/word/旅行

***This will not always work due to inconsistencies between the word and its url. For example:***
- The url for 綺麗 is https://jisho.org/word/奇麗 

If it doesn't work, try searching for the kanji on Jisho and going to its page. Copy whatever comes after "word/" in the url (in the above example, it would be 奇麗) and use that as input instead.

TO DO:

- Fix formatting for definitions.
- Fix markdown output for certain words which are not being formatted correctly.

Kanji to fix:
- [x] 問題
- [ ] 疲れる
- [ ] 赤