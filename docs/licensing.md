# Open-source license research

**Decision status:** Not selected. This document compares options; it does not
license the repository. This is engineering guidance, not legal advice.

## Summary

All licenses below allow commercial use, modification, and redistribution.
The main distinction is **permissive licensing** (MIT/BSD) versus **copyleft**
(GPL). Copyleft does not mean "noncommercial."

| Option | Model | Main redistribution obligations | Proprietary derivatives |
| --- | --- | --- | --- |
| MIT (`MIT`) | Permissive | Preserve the copyright and permission notice in copies or substantial portions. | Allowed, subject to notice obligations. |
| BSD 2-Clause (`BSD-2-Clause`) | Permissive | Retain copyright, conditions, and disclaimer in source; reproduce them in documentation/materials accompanying binary distributions. | Allowed, subject to notice obligations. |
| BSD 3-Clause (`BSD-3-Clause`) | Permissive | BSD 2-Clause obligations plus no use of copyright-holder/contributor names to endorse derived products without prior written permission. | Allowed, subject to those conditions. |
| GNU GPLv3 (`GPL-3.0-only` or `GPL-3.0-or-later`) | Strong copyleft | Preserve notices and license; mark changes; license distributed covered derivatives under GPL; meet corresponding-source obligations when distributing non-source forms. | A covered derivative cannot generally be distributed as proprietary-only software without separate permission. |

"BSD" is a family, not a precise license choice. Prefer an explicit 2-Clause or
3-Clause identifier; the older 4-Clause variant includes an advertising clause
and has different compatibility implications.

GPLv2 and GPLv3 are also distinct licenses. This comparison focuses on GPLv3;
do not substitute "GPL" alone for an exact version and an explicit choice of
"only" versus "or later."

## What matters for a FastAPI backend

### Hosted service versus distributed software

Under ordinary GPLv3, merely allowing users to interact with the backend over a
network, without transferring a copy of the program, is not conveying it and does
not by itself trigger source-distribution obligations. Distributing the backend
to customers, including in a container image, is a different situation.
GPL does not require publishing every private modification to the whole world;
source obligations depend on how covered software is conveyed.

If the goal is to require users of modified hosted versions to receive a source
offer, evaluate **GNU AGPLv3** separately. Its section 13 addresses remote network
interaction with modified versions. GPLv3 alone does not provide that rule.

### Dependency and data boundaries

- A project license does not override dependency licenses. Review direct and
  transitive dependencies and bundled assets before a release.
- Combining GPL code into one covered program can create copyleft obligations;
  a separate HTTP client does not automatically become GPL merely by calling an
  API. Whether components form a combined work is context-dependent.
- MIT and modern BSD licenses are generally GPL-compatible, but compatibility is
  directional: incorporating permissive code into a GPL-covered combination does
  not let you relicense someone else's GPL code as MIT.
- The software license does not automatically license user records, fishing
  locations, third-party maps, or API data. Those need their own terms and privacy
  decisions.
- MIT and BSD do not contain an express patent-license clause comparable to
  GPLv3's contributor patent grant. If an explicit permissive patent grant matters,
  consider Apache-2.0 as an additional option.
- PlantUML's own license does not automatically become this project's license
  simply because it is used to render original diagrams.

## Recommendation

For a new backend where the priority is broad adoption and low-friction commercial
integration, **MIT is the simplest starting recommendation**, provided the owners
are comfortable with proprietary forks and reuse.

Choose **BSD-3-Clause** instead if an explicit non-endorsement condition is
important. BSD-2-Clause is another short permissive option, but offers little
practical differentiation from MIT for this project's stated goals.

Choose **GPLv3** if preserving recipients' rights to source and modification in
distributed derivatives is more important than permissive reuse. Evaluate
**AGPLv3** if reciprocity for modified hosted services is the actual objective.
Do not choose GPL merely because the project is a web application.

The owners should answer: **Should others be allowed to distribute closed-source
derivatives, and should operators of modified hosted versions have source-offer
obligations?**

## Adoption checklist

Once the owners decide:

1. Confirm who owns the copyright and can authorize the license, including
   employer and contributor rights.
2. Record the exact license identifier and rationale.
3. Add the complete, unmodified license text in a root `LICENSE` file, filling in
   copyright details where the license template calls for them.
4. Update the README and future package metadata; add appropriate source notices.
   For GPL, follow GNU's application instructions rather than just copying the
   license into the repository.
5. Audit dependencies, copied code, and assets for compatible terms and notices.
6. Clarify whether documentation shares the code license or uses a separate one.
7. Agree on contribution licensing before accepting third-party contributions.

Changing licenses later may require permission from other copyright holders;
it also does not revoke rights already granted for earlier releases.
Until a license is adopted, do not describe the repository as MIT-, BSD-, or
GPL-licensed, or assume that public visibility grants general reuse rights.

## Sources

License texts control over this summary:

- [MIT text and overview — Choose a License](https://choosealicense.com/licenses/mit/)
- [BSD 2-Clause text and overview — Choose a License](https://choosealicense.com/licenses/bsd-2-clause/)
- [BSD 3-Clause text and overview — Choose a License](https://choosealicense.com/licenses/bsd-3-clause/)
- [GNU GPLv3 full text](https://www.gnu.org/licenses/gpl-3.0.html), particularly
  sections 0, 4–6, and 11.
- [GNU license FAQ](https://www.gnu.org/licenses/gpl-faq.html), including
  [GPL and hosted websites](https://www.gnu.org/licenses/gpl-faq.html#UnreleasedMods),
  [private modifications](https://www.gnu.org/licenses/gpl-faq.html#GPLRequireSourcePostedPublic),
  and [applying the license](https://www.gnu.org/licenses/gpl-faq.html#LicenseCopyOnly).
- [GNU AGPLv3 full text, section 13](https://www.gnu.org/licenses/agpl-3.0.html#section13).
