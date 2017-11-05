
# class containing info from meta data file as attributes
class study:

    def __init__(self, studyID):
        self.studyID = studyID
        self.study_path = str
        self.study_size = int
        self.study_phenotype = str
        self.study_sep = str
        self.study_headers = list
        self.study_num_variants = int
        self.study_lambda = float
        self.study_correction = float
        self.study_sum_eff = float

    def set_path(self, path):
        self.study_path = path

    def set_study_size(self, size):
        self.study_size = size

    def set_phenotype(self, pheno):
        self.study_phenotype = pheno

    def set_sep(self, sep):
        self.study_sep = sep

    def set_headers(self, headers):
        self.study_headers = headers

    def set_num_variants(self, num_var):
        self.study_num_variants = num_var

    def set_lambda(self, lb):
        self.study_lambda = lb

    def set_correction(self, cor):
        self.study_correction = cor

    def set_sum_eff(self, eff):
        self.study_sum_eff = eff
