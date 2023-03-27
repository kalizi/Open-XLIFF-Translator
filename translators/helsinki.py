import torch
import warnings
from transformers import MarianTokenizer, MarianMTModel

class HelsinkiTranslator:
    MODEL_BASE_NAME = 'Helsinki-NLP/opus-mt-'

    # This should probably be expanend or fetched from the API
    SUPPORTED_LANGUAGES = [
        'en', 'fi', 'sv', 'de', 'fr', 'es', 'it', 'nl', 'pt', 'ru', 'ar', 'zh', 'ja', 'ko'
    ]

    SPLIT_EVERY = 256

    def __init__(self, options = {}):
        self.options = options
        warnings.filterwarnings("ignore")

    @classmethod
    def loadModel(self, source, target):
        '''
        Load a model for a given source and target language.

        @param source: Source language.
        @type source: string
        @param target: Target language.
        @type target: string
        @return: Model.
        '''
        modelName = self.MODEL_BASE_NAME + source + '-' + target

        tokenizer = MarianTokenizer.from_pretrained(modelName)
        model = MarianMTModel.from_pretrained(modelName)

        self.isCudaAvailable = torch.cuda.is_available()
        if self.isCudaAvailable:
            model = model.to('cuda')

        return (tokenizer, model)
    
    @classmethod
    def translateSentence(self, sentence, model, tokenizer):
        '''
        Translate a sentence.

        @param sentence: Sentence to translate.
        @type sentence: string
        @param model: Model.
        @type model: MarianMTModel
        @param tokenizer: Tokenizer.
        @type tokenizer: MarianTokenizer
        @return: Translated sentence.
        @rtype: string
        '''
        # Tokenize
        inputs = tokenizer([sentence], return_tensors="pt")

        # Translate
        if self.isCudaAvailable:
            inputs = inputs.to('cuda')

        outputs = model.generate(**inputs)

        # Decode
        translation = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        return translation[0]

    def translate(self, source, target, text):
        '''
        Translate text from source language to target language.

        @param source: Source language.
        @type source: string
        @param target: Target language.
        @type target: string
        @param text: Text to translate.
        @type text: string
        @return: Translated text.
        @rtype: string
        '''
        if source not in self.SUPPORTED_LANGUAGES:
            raise Exception('Source language not supported: %s' % source)

        if target not in self.SUPPORTED_LANGUAGES:
            raise Exception('Target language not supported: %s' % target)

        tokenizer, model = self.loadModel(source, target)

        if len(text) > self.SPLIT_EVERY:
            # split text into sentences
            sentences = text.split('.')

            translation = ''        
            for sentence in sentences:
                # Split the sentence into chunks of up to max_sentence_length characters
                chunks = []
                chunk = ""
                for word in sentence.split():
                    if len(chunk) + len(word) + 1 <= self.SPLIT_EVERY:
                        # Add the word to the current chunk
                        chunk += word + " "
                    else:
                        # Add the current chunk to the list of chunks
                        chunks.append(chunk)
                        chunk = word + " "

                # Add the final chunk to the list of chunks
                chunks.append(chunk)

                # Translate each chunk separately
                for chunk in chunks:
                    # Translate
                    output_chunk = self.translateSentence(chunk, model, tokenizer)

                    # Concatenate the output chunk to the final result
                    translation += output_chunk
                    translation += " "
        else:
            translation = self.translateSentence(text, model, tokenizer)

        return translation
