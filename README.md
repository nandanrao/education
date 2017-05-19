# Education.

## Notebooks
The interesting stuff is in the notebooks, everything in the root folder that ends in "ipynb".

## Open Questions

* Do we scale/center the questions from the surveys? This assumes that our sample is representative of the population, or that any transformations across spaces should apply for whatever population our sample IS representative of, which might be different from the population that the surveys/tests were designed for. Or the surveys/tests could just be poorly designed.

* Given the above target (bigfive, maybe scaled), do we seek to treat this as an ordinal or cardinal target??? We most likely care most about maintaining ordinality, but after which how much do we want cardinal deflection to cost?? Decide on a rank-order measure (Kendall Tau) and associated cost.

* Bigfive personality tests is clearly a linear dimensionality reduction, but is there any reason that we need the translation from other test-spaces onto the big-five vectors to be limited by their natural dimensions???


## Current TODO

* solid measure of cardinal error in regression -- r2 score?
* match regressed vectors with sparsepca vectors via cosine and then look at variance??
* decide on rank-correlation cost measures -- kendall tau distance??
* research regression techniques (with sparsity regularization as well?) that seeks to first maintain (perfectly??) rank-order.


## Random Notes

"An affine transformation does not necessarily preserve angles between lines or distances between points, though it does preserve ratios of distances between points lying on a straight line."

If this is true, we should be able to use the ratios for a consistent distance measure across non-uniform scaling:
