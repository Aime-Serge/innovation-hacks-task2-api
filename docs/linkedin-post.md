# LinkedIn post draft — Task 2

Post this once the demo video is recorded and uploaded.

**Before posting**: confirm Innovation Hacks' real LinkedIn page yourself
(search for it directly in LinkedIn) and tag it using LinkedIn's own
`@`-mention autocomplete as you type — typing "@Innovation Hacks" as
plain text does not create a real tag/link, you have to select their
page from the dropdown.

**Only post claims you can explain.** Every statement below is true of
this repo, but you should be able to talk through each one (why the
framework's own errors bypassed the format, how the cascade works) if
someone asks. Edit the wording so it sounds like you.

## Post copy

**Hook:**
My API's "one consistent error format" wasn't consistent.

**Body:**
Task 2 of my Full Stack Development Internship with @Innovation Hacks: a
REST API for users, projects, and tasks, built with FastAPI and Pydantic v2.

The bug I'm glad I caught: every error my own code raised used one JSON
shape, but hit an unknown route or the wrong HTTP method and the
framework answered in its own format instead. I found it by testing that
path directly, fixed it, and added tests so it stays fixed.

Also fixed: deleting a user used to leave their projects behind, pointing
at an owner that no longer existed. Deleting now cascades to their
projects and tasks.

You don't have to take my word for it. The live API's landing page has a
"Run live checks" button that fires ten real requests at the deployed
server and shows pass/fail for each, right in your browser.

Stack: FastAPI, Pydantic v2, pytest (48 tests), deployed on Render.

**Tag:** @Innovation Hacks (via the real mention dropdown — see above)

**Hashtags:** #FullStackDevelopment #FastAPI #Python #APIDesign
#BuildInnovateImpact

**Call to action:**
Repo, live API, and demo video are in the first comment. Would love
feedback on the API design.

## First comment (outbound links go here, not in the post body)

Live API (click "Run live checks"): https://ih-task2-api.onrender.com
Repo: https://github.com/Aime-Serge/innovation-hacks-task2-api
Demo: [add after recording]

Note: the API runs on a free tier, so the first request after a quiet
period can take up to a minute to wake up.

## Before you post

- [ ] Demo video recorded and uploaded (see `DEMO_SCRIPT.md`)
- [ ] Open the live link yourself once and click "Run live checks"
- [ ] Tag applied via LinkedIn's mention dropdown, not typed as plain text
- [ ] Video or a screenshot (`docs/screenshots/`) attached to the post itself
- [ ] Repo, live, and demo links added as the first comment
