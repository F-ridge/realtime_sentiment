from pyknp import Juman
from allennlp.data.tokenizers import Token, Tokenizer
from overrides import overrides

import re
from neologdn import normalize
import emoji_conversion as em

import torch

@Tokenizer.register("juman_tokenizer")
class JumanTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

        self.juman = Juman()

    def _format_text(self, text):
        '''
        Jumanに入れる前のツイートの整形
        '''
        # 絵文字を置換
        text = emoji.demojize(text, delimiters=(" "," "))
        for en, jp in em.conversion_dic.items():
            text = text.replace(en, jp)

        text = text.lower() # 大文字→小文字
        text = normalize(text) # 正規化(表記揺れの是正)

        ''.join(c for c in text if c not in emoji.UNICODE_EMOJI) # 置換できていない絵文字は消去
        text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
        text=re.sub(r'[!-~]', "", text) # 半角記号,数字,英字
        text=re.sub(r'[︰-＠]', "", text) # 全角記号
        text=re.sub('\n', "", text) # 改行文字
        text=re.sub(' ', "", text) # 必須

        return text.encode().decode('unicode-escape')

    def _split(self, text):
        text = self._format_text(text)
        
        if text != "":
            result = self.juman.analysis(text)
            tokens = [mrph.midasi for mrph in result.mrph_list()]
        else:
            tokens = None
        return tokens

    @overrides
    def tokenize(self, text):
        tokens = self._split(text)

        if tokens is None:
            return None

        return [Token(str(token)) for token in tokens]


