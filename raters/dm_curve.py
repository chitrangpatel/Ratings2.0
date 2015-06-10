import numpy as np

import base
from rating_classes import freq_vs_phase

class DMComparisonPeakRater(base.BaseRater):
    short_name = "dmcurve"
    long_name = "DM Curve"
    #description = "Compute the ratio of peak height for the profile " \
    #              "dedispersed at DM 0 divided by that for the profile " \
    #              "dedispersed at the best-fit DM."
    description = ""
    version = 1

    rat_cls = freq_vs_phase.FreqVsPhaseClass()

    def _compute_rating(self, cand):
        """Return a rating for the candidate.
            === MORE EXPLANATION ===

            Input:
                cand: A Candidate object to rate.

            Output:
                value: The rating value.
        """
        fvph = cand.get_from_cache('freq_vs_phase')
        pfd = cand.get_from_cache('pfd')

        fvph.dedisperse(DM=0)
        prof_dm0 = fvph.get_profile()
        peak_dm0 = np.amax(prof_dm0) - np.median(prof_dm0)

        fvph.dedisperse(DM=pfd.bestdm)
        prof_bestdm = fvph.get_profile()
        peak_bestdm = np.amax(prof_bestdm) - np.median(prof_bestdm)

        return peak_dm0/peak_bestdm
    

Rater = DMCurveRater
