#Module for automatic check on datatypes in the individual columns
import re
import App.check_correct as checker
import App.global_functions as glob

def init_header_ider():
    header_ider()

def header_ider():
    
    replacement_headers = {'additional info': 'info', 'strand orientation': 'strand', 'control samplesize': 'controls',
                       'samplesize cases': 'case', 'P-value' : 'P', 'effect size or Beta': 'Beta',
                       'effect allele frequency': 'EAf', 'major allele frequency': 'RAF',
                       'non-effect allele frequency' : 'CAF', 'minor allele frequency': 'MAF', 'effect/risk allele':
                       'effect_allele', 'major allele': 'major_allele', 'non-effect allele': "non_effect_allele",
                       'minor allele': 'minor_allele', 'position or location of SNP': 'BP', 'chromosome number': 'CHR',
                       'rsID of marker or SNP': 'marker_original'}

    
    col_types = ['rs_id', 'chr_id', 'loc_id', 'allele_id', 'beta_id', 'pval_id', 'sample_id', 'info_id']
    col_types = [
    if not headers:
        headers, col = df.columns
    for i, header in enumerate(headers):
        df = glob.filetodf(cols=i)
        while True:
            for check in col_checks:
                if col_check(df):
                    break
            break

def col_id(df, 

def rs_id(df, head= False, col= False):
    
    if df.headers:
        hdPattern = re.compile(r'(snp)*(marker(name)*)*(rs(id))*', re.I)
        if hdPattern:
            head = True
    cnt -= 0
    rsPattern = re.compile(r'[0-9]*')
    for row in df.tolist():
        if rsPattern.match:
            cnt += 1
    if cnt <

    if head or col:
        return True
        

def chr_id(df, head= False, col= False):
 
    if df.headers:
        hdPattern = re.compile(r'ch(r)*(omosome)*', re.I)
         if hdPattern.match(df.header):
            head = True
    chrPattern = re.compile(r'(1-21)[XY]*', re.I)
    if chrPattern.match:
        col = True
        
    if head or col: 
        return True
    
def loc_id(df,head= False, col= False):
    
    if df.headers:
        hdattern = re.compile(r'(loc)*(pos*)*(bp)*(hg)*(grch(\d){2})*', re.I)
        if hdPattern.match:
            head = True
    locPattern = re.compile(r'\d*$')
    if 
    
def allele_id():

def beta_id():
                 
def pval_id():
                 
                 
def sample_id():
                 

def info_id():
        
        