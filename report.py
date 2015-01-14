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

columns =[
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
] 


sys.stdout.write('\t'.join(columns)+'\n')

colum_refs = ''

for line in open(sys.argv[1]):
  # Skip headers.
  if line[0] == '#': continue
  line = line.strip().split('\t')
  if line[0] == 'contig': 
    column_refs = line
    continue

  report = list()
  report.append(line[column_refs.index('contig')]) # chromosome
  report.append(line[column_refs.index('0')]) # position
  report.append(line[column_refs.index('context')]) # context
  report.append(line[column_refs.index('REF_ALLELE')]) # reference
  report.append(line[column_refs.index('ALT_ALLELE')]) # alternative
  report.append(line[column_refs.index('n_ref_count')]) # normal reference count
  report.append(line[column_refs.index('n_alt_count')]) # normal alternative count
  report.append(line[column_refs.index('t_ref_count')]) # tumor reference count
  report.append(line[column_refs.index('t_alt_count')]) # tumor alternative count

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
