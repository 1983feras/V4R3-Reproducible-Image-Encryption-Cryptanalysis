# Manuscript-Ready Wording for Completed Results

## Correctness/authentication
"The frozen confirmatory regression suite completed successfully (16/16 tests). The tested cases included byte-exact round-trip recovery across predefined sizes/patterns and rejection of the covered ciphertext, tag, nonce, metadata, and wrong-key modifications. These tests establish implementation correctness for the tested cases and the behavior of the implemented authentication checks; they do not constitute a formal proof of authenticated-encryption security."

## Positive control
"The deliberately weak V0W construction was fully recovered once the analytically sufficient chosen-plaintext information was available. At a payload length of 196,608 bytes, four total chosen-plaintext queries recovered the reusable mask, permutation, and target plaintext exactly. The positive result is important methodologically because it demonstrates that the evaluation harness does not merely return negative attack results."

## Session-transfer diagnostic
"The fixed equivalent-XOR diagnostic produced mean exact-byte recovery rates of 0.004362, 0.003776, 0.004883, and 0.003776 for same-key/same-nonce, same-key/new-nonce, new-key/same-nonce, and new-key/new-nonce conditions, respectively, compared with the random byte-match reference of 1/256=0.00390625. Thus, no practically useful reconstruction was obtained from this specific reusable-XOR hypothesis in any tested session condition."

## Query-budget diagnostic
"Increasing the frozen lookup-diagnostic budget from Q=1 to Q=64 did not produce a monotonic recovery gain. Mean exact-byte recovery remained close to 1/256: 0.003841, 0.003841, 0.003906, 0.003971, 0.004297, 0.004232, and 0.004036 for Q={1,2,4,8,16,32,64}, respectively. In contrast, the V0W positive control achieved exact recovery at the first sampled budget exceeding its analytical threshold for the 32x32x3 experiment. This contrast supports the sensitivity of the protocol to reusable structure while limiting the V4-R3 conclusion to the implemented diagnostic."
