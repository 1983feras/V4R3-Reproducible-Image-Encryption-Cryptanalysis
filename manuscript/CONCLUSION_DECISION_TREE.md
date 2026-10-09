# Evidence-Driven Conclusion Decision Tree

## If V4-R3 is reproducibly broken
The paper's principal contribution becomes the cryptanalytic finding and the methodology that exposed it. Report attack conditions, query/data complexity, transfer conditions, reconstruction quality, and reproducibility evidence. Do not patch V4-R3 inside the same frozen campaign.

## If V4-R3 survives implemented attacks and V5-R3 adds no measurable benefit
Conclude that the tested cryptographically keyed session/state architecture did not yield useful recovery under the implemented attacks, while the nonlinear extension did not justify its added complexity. Emphasize that this is empirical evidence, not proof.

## If V4-R3 survives and V5-R3 reproducibly improves resistance
Report the paired effect and uncertainty. Attribute only an observed association to the V5 ablation unless a mechanism-specific experiment supports a causal explanation. Do not inflate the result into a general claim about chaos/nonlinear encryption.

## In every branch
Recommend standardized, extensively analyzed AEAD for production. Present V4/V5 as research constructions and the cryptanalysis-guided evaluation framework as the transferable methodological contribution.
