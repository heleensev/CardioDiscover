import logger

logger = logging.getLogger(__name__)

beta_sum = list()
weight_sum = list()

ratio = float
beta = float
weighted_beta = float
se = float
study = object


"""
  if ( $study_okay[$study] == 1 ) {
#        print STDERR " *** DEBUG *** Examining sample size for [ $study_name[$study] ]: n = $sample_size[$study] and info = $ratio[$study].\n";
  $sample_size_eff[$study] = $sample_size[$study] * ( $ratio[$study] > 1 ? 1 : $ratio[$study] );
  $n_eff += $sample_size_eff[$study];
  $n_okay_studies++;


          ### put BETA and SE on same scale across studies and correct SE for inflation
          $beta[$study] = $beta[$study] / $correction_factor[$study];
          $se[$study] = $se[$study] * sqrt($lambda[$study]) / $correction_factor[$study];

              ### inverse variance weighted z-score
          $signed_beta[$study] = $sign * $beta[$study];
          $weight[$study] = 1 / ( $se[$study] * $se[$study] );
          my $weighted_beta = $signed_beta[$study] * $weight[$study];
          $total_weighted_beta += $weighted_beta;
          $total_weight += $weight[$study];
          $total_weight_squared += $weight[$study] * $weight[$study];

          ### sample-size weighted z-score
          my $z_weight = sqrt( $sample_size_eff[$study] / $n_eff );
          my $z = ( $signed_beta[$study] / $se[$study] );
          $z_sqrtn += ($z * $z_weight);

  """

def init_compute(study, FRQ, effect, SE, P, V, chnk_num):
    try:
        effective_sample()
        determine_variance(V)
        effective_sample()
        correct_values(beta, se)
        compute_weight(SE)
        compute_z_score()
    except UnsignificantSNP:
        logger.info('skipping this one')


def determine_variance(V):
    if V:
        if V[0] < 0:
            ratio = 0.1
        else:
            ratio = V[0]
    else:
        ratio = 1

def effective_sample():

    effective_size = sample-size * ratio
    if effective_size > 1:
        effective = 1
    else:
        effective = ratio
    # if effective size is zero, raise exception
    if eff < 0:
        # exception to be handled in init_compute
        raise UnsignificantSNP

def determine_values(beta, se):
    global beta, se
    # get correction_factor from study object
    correction_factor = study.correction
    study_lambda = study.study_lambda
    # correction for beta value
    if correction_factor:
        beta = float(beta / correction_factor)
        if study_lambda:
            se = float(se * sqrt(study_lambda))/correction_factor
    # else (no correction factor given) beta and standard deviation stay the same

def compute_weight(se):
    global se, weighted_beta, z_weight
    weight = 1/(se)**
    weighted_beta = beta*weigth

    z_weight = study_e
