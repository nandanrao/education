# EEG -> Personality

### Waves vs Responses

Most studies relating personality to EEG activity look primarily at the Power Spectral Density during stimulation (music videos, flashing lights) and at rest (closed-eyes) and find correlations between average powers of the different bands (alpha, beta, delta, theta) and personality traits.

The n-back and stroop tests seem to generally be analyzed in light of the responses of individuals, two major responses are calls the N200 and P300 responses.


## Waves

General strategy here seems to be, get the PSD (Welch or similar, window with overlap FFT), divide it up by "band" (alpha, beta, etc.), then take the average power of each band over the entire "stimulus" period, and use that as a feature.


### Alpha

Shown to have positive correlation with extraversion?

### Beta

### Delta

### Theta


## Responses

These are looked at across all bands, and are examined as a negative dip ~200ms (150ms-300ms) after the stimulus and a postiive peak ~300ms (250ms - 500ms) after the stimulus. There are different subgroups of these stimulus that occur in different regions of the brain.

### N200

N2A - Anterior. During repetetive stimulus, conscious attention or ignoring of deviations
N2B - Central Cortical. Seen suring conscious stimulus attention.

### P300

Broad recognition and memory updating processes.

P3A - frontal. Reflects a passive component. Elicited by the more infrequent stimulus in target/non-target tasks.



# Literature Review

## [Personality, affect and EEG](personality-affect-and-eeg.pdf)

Looks at resting brain activity, finds associations with regions and alpha waves that prove predictive of extraversion and nueroticism via regression.
