import numpy as np
from questplus import qp


def test_threshold():
    # Watson 2017, Example 1:
    # "Estimation of contrast threshold {1, 1, 2}"
    slope, guess, lapse = 3.5, 0.5, 0.02
    contrasts = np.arange(-40, 0+1)

    expected_contrasts = [-18, -22, -25, -28, -30, -22, -13, -15, -16, -18,
                          -19, -20, -21, -22, -23, -19, -20, -20, -18, -18,
                          -19, -17, -17, -18, -18, -18, -19, -19, -19, -19,
                          -19, -19]

    responses = ["Correct", "Correct", "Correct", "Correct", "Incorrect",
                 "Incorrect", "Correct", "Correct", "Correct", "Correct",
                 "Correct",  "Correct", "Correct", "Correct", "Incorrect",
                 "Correct", "Correct", "Incorrect", "Correct", "Correct",
                 "Incorrect", "Correct", "Correct", "Correct", "Correct",
                 "Correct", "Correct", "Correct", "Correct", "Correct",
                 "Correct", "Correct"]

    expected_mode_threshold = -20
    expected_mean_threshold = -20.39360311638961

    stim_domain = dict(intensity=contrasts)
    param_domain = dict(threshold=contrasts, slope=slope,
                        lower_asymptote=guess, lapse_rate=lapse)
    resp_domain = ['Correct', 'Incorrect']
    f = 'weibull'
    scale = 'dB'

    q = qp.QuestPlus(stim_domain=stim_domain, param_domain=param_domain,
                     resp_domain=resp_domain, func=f, stim_scale=scale)

    for expected_contrast, response in zip(expected_contrasts, responses):
        next_contrast = q.next_stim(method='min_entropy')
        assert next_contrast == expected_contrast
        q.update(stimulus=dict(intensity=next_contrast), response=response)

    assert np.allclose(q.get_param_estimates(method='mode')['threshold'],
                       expected_mode_threshold)
    assert np.allclose(q.get_param_estimates(method='mean')['threshold'],
                       expected_mean_threshold)


# def test_threshold_slope_lapse():
#     # Watson 2017, Example 2:
#     # "Estimation of contrast threshold, slope, and lapse {1, 3, 2}"
#     contrasts = np.arange(-40, 0+1)
#     slope = np.arange(2, 5+1)
#     guess = 0.5
#     lapse = np.arange(0, 0.4+0.1, 0.1)
#
#     expected_mode_threshold = -20
#     expected_mean_threshold = -19.5
#
#     stim_domain = dict(intensity=contrasts)
#     param_domain = dict(threshold=contrasts, slope=slope,
#                         lower_asymptote=guess, lapse_rate=lapse)
#     resp_domain = ['Correct', 'Incorrect']
#     f = 'weibull'
#     scale = 'dB'
#
#     q = qp.QuestPlus(stim_domain=stim_domain, param_domain=param_domain,
#                      resp_domain=resp_domain, func=f, stim_scale=scale)
#
#     for expected_contrast, response in zip(expected_contrasts, responses):
#         next_contrast = q.next_stim(method='min_entropy')
#         assert next_contrast == expected_contrast
#         q.update(stimulus=dict(intensity=next_contrast), response=response)
#
#     assert np.allclose(q.get_param_estimates(method='mode')['threshold'],
#                        expected_mode_threshold)
#     assert np.allclose(q.get_param_estimates(method='mean')['threshold'],
#                        expected_mean_threshold)

if __name__ == '__main__':
    test_threshold()