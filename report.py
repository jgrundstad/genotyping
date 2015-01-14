#!/usr/bin/env python

import re
import sys

REGEX = re.compile(r'(?P<eff>[\w\_]+)\(%s\)' % '\|'.join([
  '(?P<effect_impact>[^\|]*)',
  '(?P<functional_class>[^\|]*)',
  '(?P<codon_change>[^\|]*)',
  '(?P<amino_acid_change>[^\|]*)',
  '(?P<amino_acid_length>[^\|]*)',
  '(?P<gene_name>[^\|]*)',
  '(?P<transcript_biotype>[^\|]*)',
  '(?P<gene_coding>[^\|]*)',
  '(?P<transcript_id>[^\|]*)',
  '(?P<exon_intro_rank>[^\|]*)',
  '(?P<genotype_number>[^\|]*)',
  '?(?P<warnings_errors>[^\|]*)?',
]))

sys.stdout.write('\t'.join([
  'chr',
  'pos',
  'context',
  'ref',
  'alt',
  'normal_ref_count',
  'normal_alt_count',
  'tumor_ref_count',
  'tumor_alt_count',
  'gene',
#  'transcript',
  'effect',
#  'biotype',
  'coding',
  'codon_change',
  'amino_acid_change',
  'amino_acid_length',
  'mutect_call',
])+'\n')

for line in open(sys.argv[1]):
  # Skip headers.
  if line[0] == '#': continue
  line = line.strip().split('\t')
  if line[0] == 'contig': continue

  report = list()
  report.append(line[0]) # chromosome
  report.append(line[1]) # position
  report.append(line[2]) # context
  report.append(line[3]) # reference
  report.append(line[4]) # alternative
  report.append(line[30]) # normal reference count
  report.append(line[31]) # normal alternative count
  report.append(line[20]) # tumor reference count
  report.append(line[21]) # tumor alternative count

  # Interpret the effects of the variant.
  for match in REGEX.finditer(line[7]):
    # NOTE this is a hack for Kevin's request
    if match.group('functional_class') not in ['MISSENSE','NONSENSE']: continue

    sys.stdout.write('\t'.join(report))
    sys.stdout.write('\t%s' % match.group('gene_name'))
    # NOTE this is a hack for Kevin's request
    #sys.stdout.write('\t%s' % match.group('transcript_id'))
    sys.stdout.write('\t%s' % match.group('eff'))
    # NOTE this is a hack for Kevin's request
    #sys.stdout.write('\t%s' % match.group('transcript_biotype'))
    sys.stdout.write('\t%s' % match.group('gene_coding'))
    sys.stdout.write('\t%s' % match.group('codon_change'))
    sys.stdout.write('\t%s' % match.group('amino_acid_change'))
    sys.stdout.write('\t%s' % match.group('amino_acid_length'))
    sys.stdout.write('\t%s' % line[-1]) # keep?
    sys.stdout.write('\n')

    # NOTE this is a hack for Kevin's request
    break
