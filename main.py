# XLIFF Translator 
#                              o
#                             /\
#                            /::\
#                           /::::\
#             ,a_a         /\::::/\
#            {/ ''\_      /\ \::/\ \
#            {\ ,_oo)    /\ \ \/\ \ \
#            {/  (_^____/  \ \ \ \ \ \
#  .=.      {/ \___)))*)    \ \ \ \ \/
# (.=.`\   {/   /=;  ~/      \ \ \ \/
#     \ `\{/(   \/\  /        \ \ \/
#      \  `. `\  ) )           \ \/
#  jgs  \    // /_/_            \/
#        '==''---))))
#
import os 
import sys
import argparse

from transl import OpenXLIFFTranslator

def main(
    source_path = None,
    target_path = None,
    options = {},
    preferred_translator = 'helsinki'
):
    if not source_path:
        raise Exception('Source path is required')
    
    if not target_path:
        raise Exception('Target path is required')
    
    if not os.path.exists(source_path):
        raise Exception('Source path does not exist: %s' % source_path)
    
    if not os.path.exists(target_path):
        raise Exception('Target path does not exist: %s' % target_path)
    
    translator = OpenXLIFFTranslator(options, preferred_translator)
    translator.translateFromPath(source_path, target_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Welcome to the Open XLIFF Translator.')
    parser.add_argument('input_path', type=str, help='Path to XLIFF input files')
    parser.add_argument('output_path', type=str, help='Path to XLIFF output files')
    parser.add_argument('--translator', type=str, choices=['helsinki'],
                        default='helsinki', help='Type of translator to use (currently only Helsinki NLP is supported)')
    parser.add_argument('--verbose', action='store_true', help='Print verbose output')

    args = parser.parse_args()
    options = { "verbose": args.verbose }

    main(
        source_path = args.input_path,
        target_path = args.output_path,
        options = options,
        preferred_translator=args.translator,
    )
