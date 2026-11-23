# QA report – Menu 3 Pinyin + Turnstile

## Base

- Source: official GitHub Pages artifact `github-pages` built from commit `5419fac1f2d16949212136eab29d128d271b2654`.
- Existing application version retained: V42.10.22.
- No GitHub commit, push, Worker deployment, or Cloudflare configuration change was made.

## Changes

1. Exact Pinyin dictionary matches remain the first path.
2. When no exact match exists, a new composition step searches full-word/phrase entries supported by the curated HSK seed and verified sentence data. It checks tone marks and numeric tones 1–5. If the source evidence leaves multiple similarly-ranked readings, the UI shows options for the learner; unsupported/low-confidence input is rejected rather than guessed.
3. Menu 3 gets a 12-second overall Turnstile deadline (including script loading and widget execution). Other callers of `getBvtTurnstileToken()` keep the 120-second default.
4. The Turnstile widget is removed/reset on settle; callbacks from a timed-out widget are ignored. No Worker POST is sent without a non-empty token. Worker-side Turnstile verification remains untouched.
5. Menu 3 Worker translation gets a 45-second request timeout. A Turnstile-related failure activates a 60-second cooldown so repeated sentences do not each wait for another token before using MyMemory/Google.
6. Status text now tells the learner when Menu 3 is waiting for Cloudflare and when it has switched to the fallback services.
7. Service Worker cache key is changed so clients do not keep serving the old cached app shell.

## Tests performed

- Pinyin composition cases: `ni jin tian mang ma` → `你今天忙吗？`; `wo jin tian hen mang` → `我今天很忙`; `ni xiang qu nar` → `你想去哪儿`; `ni3 jin1 tian1 mang2 ma5` → `你今天忙吗？`.
- Existing exact matches `wo ai ni` and `ni hao` still resolve via the exact offline data first.
- Unknown/weakly evidenced input is refused rather than silently converted.
- Turnstile mocked success path, short timeout path, late-token rejection, and no-POST-without-token path pass.
- Worker failure fallback and cooldown path pass; next Worker attempt is allowed after cooldown.
- Combined UI and Menu 3 regression harness: 24/24 passed.
- Patch-local Node tests: 17/17 passed.
- Inline JavaScript syntax: 18/18 parsed; four external/data scripts correctly skipped.
- Embedded CVDICT: 122,523 rows; SHA-256 `609abad4255fa2ead68fd2c099f89d14a61432d2bda2ee1c679ded1a0066d006`; byte-identical to the base production artifact.
- No unexpected backspace/control character remains in the Turnstile error matcher.

## Not verified

- No real browser-generated Turnstile token was available in this execution. Tests use a controlled mock token and verify the frontend request policy; they do not prove the real GitHub Pages domain will receive a token from Cloudflare.
- No successful production `POST /translate` with a real valid Turnstile token was observed, so Workers AI production success is still not certified.
- Browser end-to-end tests on a physical Chrome/Safari device were not run in this environment.
- The repository's full Python `tools/` QA suite could not be run from the Pages artifact because that artifact does not contain the source `tools/` directory. No Python source was changed.

## Deploy notes

This ZIP is an overlay patch, not a replacement for the full repository. Keep the existing `.github/`, `tools/`, `audio/`, `luyen-so/`, QA reports, and all other files. Copy/overwrite the included files at their matching repository paths, then run the repository's full test/deploy workflow.
