import os
import glob
import xmltodict
from translators.helsinki import HelsinkiTranslator

class OpenXLIFFTranslator:
    '''
    Translator class for translating XLIFF files.

    :ivar translator: Name of the translator.
    :type translator: string
    '''
    TRANSLATORS = {
        'helsinki': HelsinkiTranslator,
    }

    def __init__(self, options = {}, translator = 'helsinki'):
        self.translator = translator
        self.t = self.TRANSLATORS[translator](options)
        self.verbose = 'verbose' in options and options['verbose']

    @classmethod
    def readXliffFromPath(self, path):
        '''
        Read XLIFF file from path and parse it.

        @param path: Path to XLIFF file.
        @type path: string
        @return: XLIFF file as dictionary.
        '''
        if not os.path.exists(path):
            raise Exception('Path does not exist: %s' % path)
        
        with open(path, 'r') as f:
            xliff = xmltodict.parse(f.read())
        
        return xliff
    
    @classmethod
    def writeXliffToPath(self, xliff, path):
        '''
        Write XLIFF file to path.

        @param xliff: XLIFF file as dictionary.
        @type xliff: dict
        @param path: Path to XLIFF file.
        @type path: string
        '''
        with open(path, 'w') as f:
            f.write(xmltodict.unparse(xliff, pretty=True))
    
    def translateFromPath(self, sourcePath, targetPath):
        '''
        Translate XLIFF file from path.

        @param sourcePath: Path to XLIFF file.
        @type sourcePath: string
        @param targetPath: Path to XLIFF file.
        @type targetPath: string
        '''
        for xliffFile in glob.glob(sourcePath + '/*.xliff'):
            xliff = self.translate(xliffFile)
            filename = os.path.basename(xliffFile)
            targetFile = os.path.join(targetPath, filename)
            self.writeXliffToPath(xliff, targetFile)

    def translate(self, xliffPath):
        '''
        Translate XLIFF file.

        @param xliffPath: XLIFF file.
        @type xliffPath: string
        @return: Translated XLIFF file as dictionary.
        '''
        xliff = self.readXliffFromPath(xliffPath)
        
        # extract translation languages
        translateFrom = xliff['xliff']['file']['@source-language']
        translateTo = xliff['xliff']['file']['@target-language']

        # read body of the file
        body = xliff['xliff']['file']['body']['trans-unit']

        isSingleTranslation = type(body) is not list

        # check if body is array, generalize instead
        if isSingleTranslation:
            body = [body]
        
        for unit in body:
            # get the body to be translated
            source = unit['source']

            translated = self.t.translate(translateFrom, translateTo, source)

            # write the translated text to the target
            unit['target'] = translated

            if self.verbose:
                print('Translated: %s' % translated)

        # unwrap
        if isSingleTranslation:
            body = body[0]

        # overwrite the body (now it's translated)
        xliff['xliff']['file']['body']['trans-unit'] = body

        return xliff
