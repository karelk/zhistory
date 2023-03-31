#!/bin/python3

import os, sys, argparse, re

##############################################################################################################################################################
###   parse commandline arguments   ##########################################################################################################################
##############################################################################################################################################################

parser = argparse.ArgumentParser()


parser.add_argument('-A','--after-context'	, type=int,			help='print NUM lines after matching line')
parser.add_argument('-B','--before-context'	, type=int,			help='print NUM lines before matching line')
parser.add_argument('-C','--context'		, type=int,			help='print NUM lines of context')
parser.add_argument('--cut'                     , action='store_true',		help='cut')
parser.add_argument('-F','--fixed-strings'	, action='store_true',		help='interpret PATTERN as literal string')
parser.add_argument('-i','--ignorecase'		, action='store_true',		help='ignore case')
parser.add_argument('-t','--time'		, action='store_true',		help='match time')
parser.add_argument('-w','--word'		, action='store_true',		help='match whole words')
parser.add_argument('pattern'			, nargs='+',			help='pattern(s)')

args = parser.parse_args()

##############################################################################################################################################################
###   variables   ############################################################################################################################################
##############################################################################################################################################################

if args.context:
    NL, A, B		= '\n', args.context, args.context
else:
    NL, A, B		= '', 0, 0
    if args.before_context:
        NL, B		= '\n', args.before_context
    if args.after_context:
        NL, A		= '\n', args.after_context

##############################################################################################################################################################

if args.time:
    INDEX		= [7,24]
    RED			= ''
    WORD_MATCH		= r'\b'
    CASE_SENSITIVE	=  re.IGNORECASE
else:
    INDEX		= [26,-1]
    RED			=  r'\033[1;31m\1\033[0m'	if sys.stdout.isatty()	else r'\1'
    WORD_MATCH		=  r'\b'			if args.word		else ''
    CASE_SENSITIVE	=  re.IGNORECASE		if args.ignorecase	else 0

##############################################################################################################################################################

if sys.stdout.isatty():
    GREEN	=  '\033[00;38;5;65m'
    GREY	=  '\033[00;38;5;102m'
    ENDCOLOR	=  '\033[0m'
else:
    GREEN	=  ''
    GREY	=  ''
    ENDCOLOR	=  ''

##############################################################################################################################################################
###   regex   ################################################################################################################################################
##############################################################################################################################################################

PATTERN = []

for p in args.pattern:
    if args.fixed_strings:
        PATTERN.append(re.compile(re.escape(p), flags=CASE_SENSITIVE))
    else:
        if args.word:
            PATTERN.append(re.compile(WORD_MATCH + p + WORD_MATCH, flags=CASE_SENSITIVE))
        else:
            PATTERN.append(re.compile(p, flags=CASE_SENSITIVE))

PATTERNS = re.compile(WORD_MATCH + r'(' + "|".join("%s" % i for i in args.pattern) + r')' + WORD_MATCH, flags=CASE_SENSITIVE)

##############################################################################################################################################################
###   main   #################################################################################################################################################
##############################################################################################################################################################

if sys.stdin.isatty():
    sys.exit(1)
else:

    context = []
    match = [A] * len(PATTERN)

    print(NL, end='')

    sys.stdin.reconfigure(errors="backslashreplace")

    while True:
        line = sys.stdin.readline()

        if line:
            context.append(line)

        for i in range(len(PATTERN)):

            if re.search(PATTERN[i], line[INDEX[0]:INDEX[1]]):
                match[i] = 0
            else:
                match[i] += 1

        ############################################################################################
        if max(match) == A or (line == '' and max(match) < A):
        ############################################################################################

            for i in range(len(context)):

                ################################################################

                if args.cut:
                    print(' ', end='')
                else:
                    print(GREY + context[i][0:24] + ENDCOLOR + '  ', end='')

                ################################################################

                if context[i][26:27] == '#':
                    print(GREEN + context[i][26:-1] + ENDCOLOR)
                else:
                    print(re.sub(PATTERNS, RED, context[i][26:]), end='')

                ################################################################

            print(NL, end='')
            del context[:]

        ############################################################################################
        elif context and max(match) > A + B:
        ############################################################################################

            del context[0]

        if line == '':
            break

sys.exit(0)

