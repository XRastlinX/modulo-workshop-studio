# AI build brief: Modulo Workshop

State: implemented local starter, optional unconnected Discord adapter. Scope and visual anchor: README.md. This brief is a candidate design, not deployment permission.

vocational_verb: DRAFT
recommendation_effect: ADVISORY_ONLY
automatic_execution: FORBIDDEN
residual_posture: OPEN_ACKNOWLEDGED
sovereign_boundary: EXTERNAL_HUMAN_DISPOSITION_REQUIRED
authority_effect: NONE
crown: DETACHED

## Formal kernel

For integer total n and modulus m > 0, divmod returns q,r with n=q*m+r and 0<=r<m. The integer model keeps q and n alongside r. Model bounds are modulus 2..24, start -10000..10000, steps -24..24. There is no physical inference or general complexity result.

## Interfaces and acceptance predicates

| Component | Contract | Distinct checking step |
|---|---|---|
| Integer core | Position list and final quotient/remainder | Identity and range tests, including negative walks |
| Episode inspector | Missing required fields | Missing-field tests; no scientific verification claim |
| MP4 CLI | Local 1280x720 H.264, 24fps, two seconds per position | ffprobe dimensions, codec and duration; human visual review |
| MCP | Exactly two local stdio tools | Real client initialization, discovery and tool invocation |
| Discord | Guild-scoped /modulo, /demo, /blueprint | Offline adapter checks; live server check remains open |

## Interpretation residuals

Generation, verification, authorization and execution are distinguishable and re-entrant; residuals remain visible throughout. Tests concern declared predicates. A hash identifies bytes; it does not establish scientific truth. Episode metadata and coherent graphics do not establish understanding. The studio has no general natural-language-to-code agent, sandbox, durable job queue, moderation service or unattended feed collection.

The Discord adapter uses fixed subprocess arguments, bounded inputs, an explicit user allowlist, one active render and an 8 MB upload ceiling. Preview files accumulate locally. No arbitrary code supplied by Discord is executed. Future agent execution would require a separate design and review of its filesystem, network, credential and resource boundaries.
