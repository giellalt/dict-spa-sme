#!/usr/bin/perl -w
use utf8 ;

# Simple script to convert csv to xml. For input/outpus examples, see below.

print STDOUT "<r>\n";

while (<>) 
{
	chomp ;
	my ($WORD, $GENDER, $LEMMA_SYNONYM, $INFLECTION, $WORD_CLASS_SPA, $BASIC_FORM, $TRANSLATION_NUMBER, $RESTRICTION, $SCIENTIFIC_NAME, $SAAMI, $SAAMI_TRANSLATION_CASE_OR_FORM, $WORD_CLASS_SME, $EXPLANATION, $TRANSLATION_SYNONYM1, $TRANSLATION_SYNONYM2, $TRANSLATION_SYNONYM3, $TRANSLATION_SYNONYM4, $TRANSLATION_SYNONIM_5, $TRANSLATION_SYNONIM_6, $SPANISH_EX_1, $SAAMI_EX_1, $SPANISH_EX_2, $SAAMI_EX_2, $SPANISH_EX_3, $SAAMI_EX_3, $SPANISH_EX_4, $SAAMI_EX_4, $SPANISH_EX_5, $SAAMI_EX_5, $SPANISH_EX_6, $SAAMI_EX_6, $SPANISH_EX_7, $SAAMI_EX_7) = split /\t/ ;
	print STDOUT "   <e>\n";
	print STDOUT "      <lg>\n";
	print STDOUT "         <l pos=\"$WORD_CLASS_SPA\" gen=\"$GENDER\">$WORD</l>\n";
	print STDOUT "      </lg>\n";
	print STDOUT "      <mg>\n";
	print STDOUT "         <tg xml:lang=\"sme\">\n";
	print STDOUT "            <re>$LEMMA_SYNONYM</re>\n";
	print STDOUT "            <t pos=\"$WORD_CLASS_SME\">$SAAMI</t>\n";
	print STDOUT "         </tg>\n";
	print STDOUT "      </mg>\n";
	print STDOUT "   </e>\n";
}

print STDOUT "</r>\n";

# TODO: DEKLARER I DTD: lemmasyn, 

# TODO: slå saman mange mg (?) kvasikode
# if f1,2,5 give an identical triplet, 
# collect them under the same <e> with the same <lg> (eg trur $LEMMA_SYNONYM må ut

# Overview over the csv input
# Inkludert = ##
##     1	WORD
##     2	GENDER
##     3	LEMMA SYNONYM
#     4	INFLECTION
#     5	WORD CLASS SPA
#     6	BASIC FORM
#     7	TRANSLATION NUMBER
#     8	RESTRICTION
#     9	SCIENTIFIC NAME
#    10	SAAMI
#    11	SAAMI TRANSLATION CASE OR FORM
#    12	WORD CLASS SME
#    13	EXPLANATION
#    14	TRANSLATION SYNONYM1
#    15	TRANSLATION SYNONYM2
#    16	TRANSLATION SYNONYM3
#    17	TRANSLATION SYNONYM4
#    18	TRANSLATION SYNONIM 5
#    19	TRANSLATION SYNONIM 6
#    20	SPANISH_EX_1
#    21	SAAMI_EX_1
#    22	SPANISH_EX_2
#    23	SAAMI_EX_2
#    24	SPANISH_EX_3
#    25	SAAMI_EX_3
#    26	SPANISH_EX_4
#    27	SAAMI_EX_4
#    28	SPANISH_EX_5
#    29	SAAMI_EX_5
#    30	SPANISH_EX_6
#    31	SAAMI_EX_6
#    32	SPANISH_EX_7
#    33	SAAMI_EX_7




# Example input:
#
# aampumakenttä	N	skytefelt


#Target output:
#
#   <e src="yr">
#      <lg>
#         <l pos="N">aampumakenttä</l>
#      </lg>
#      <mg>
#         <tg>
#            <t pos="N" gen="x">skytefelt</t>
#         </tg>
#      </mg>
#   </e>
#

    