

# class containing info from meta data file as attributes
class Study:

    def __init__(self, studyID):
        self.studyID = studyID
        self.path = str
        self.study_size = int
        self.phenotype = str
        self.ethnicity = str
        self.build = int
        self.chunksize = int
        self.sep = str
        self.headers = list
        self.head_idx = list
        self.num_variants = int
        self.study_lambda = float
        self.correction = float
        self.sum_eff = float

    def set_path(self, path):
        self.path = path

    def set_study_size(self, size):
        self.study_size = size

    def set_phenotype(self, pheno):
        self.phenotype = pheno

    def set_ethnicity(self, eth):
        self.ethnicity = eth

    def set_build(self, build):
        self.build = build

    def set_chunksize(self, ch):
        self.chunksize = ch

    def set_sep(self, sep):
        self.sep = sep

    def set_headers(self, headers):
        self.headers = headers

    def set_indices(self, indices):
        self.head_idx = indices

    def set_num_variants(self, num_var):
        self.num_variants = num_var

    def set_lambda(self, lb):
        self.study_lambda = lb

    def set_correction(self, cor):
        self.correction = cor

    def set_sum_eff(self, eff):
        self.sum_eff = eff


# run time preferences, given in meta data file
class Preferences:

    def __init__(self):
        self.hpc = bool

    def set_hpc(self, boolean):
        self.hpc = boolean
