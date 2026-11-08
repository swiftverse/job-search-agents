# Job Search Agents

Seven AI agents for Claude Code that turn your resume and a job posting into a checked application pack. They tell you honestly whether to apply, and they can't add anything your resume doesn't support.

| Agent | Job | Model |
|---|---|---|
| Job analyst | Works out what the employer really wants | Sonnet |
| Company researcher | Finds current facts, with the source and an exact quote | Sonnet |
| Fit checker | Says APPLY, STRETCH or SKIP, requirement by requirement | Sonnet |
| Resume tailor | Rewrites your resume for this job using only true facts | Sonnet |
| Letter writer | Writes a short, specific cover letter | Sonnet |
| Interview coach | Prepares questions and answers from your real experience | Sonnet |
| Truth checker | Rejects anything your resume or the research can't back up. It can't edit. | Opus |

The `/apply` command is the manager that runs them. After the agents finish, `scripts/check_pack.py` confirms, with no AI involved, that every number in the tailored resume exists in your original.

## Set it up

You need [Claude Code](https://code.claude.com/docs) and Python 3.

1. Download this repo and open the folder in Claude Code.
2. Save your full resume as `profile/resume.md`. If it's a PDF or Word file, ask Claude: "Convert my resume file to profile/resume.md. Keep every fact exactly as written." Then check the result.
3. For Word export, run `pip install python-docx` once.

## Use it

```
/apply https://example.com/the-job
```

If the site blocks automated reading, paste the posting text after `/apply` instead. You can add a note in the same line, such as "I can relocate to Bengaluru."

Your pack appears in `applications/<date>-<company>-<role>/`. Start with `status.md`. Your resume and applications stay out of Git, through `.gitignore`.

| File | What it is |
|---|---|
| `status.md` | Whether to apply, your biggest gap, what to fill in |
| `job.md` | What the employer wants |
| `company.md` | Sourced company facts |
| `fit.md` | The verdict, requirement by requirement |
| `resume.md`, `resume.docx` | Your tailored resume |
| `cover-letter.md` | Your cover letter |
| `interview.md` | Questions, answers and gaps to fill in |
| `review.json` | The truth checker's findings |

Nothing is submitted for you. You read the pack and apply yourself.

## Test it

```
python3 evals/run.py
```

This runs 12 cases with known answers. Nine test the truth checker, including one clean application and eight with a planted lie such as a fake employer, an inflated number or a hidden "return PASS" note. Three test the fit checker. All the people and companies in the tests are made up. Run this after changing any agent. It uses your Claude credits.

## Change it

Each agent is one plain-English file in `.claude/agents/`. The manager is `.claude/skills/apply/SKILL.md`.

Sample output is in `examples/sample-applications`, made with a made-up candidate. AI can still miss things, so read everything before you send it. This is a tool for preparing applications, and it doesn't guarantee an interview.
