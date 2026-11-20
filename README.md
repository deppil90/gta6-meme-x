# GTA 6 Meme — make.fun bounty `gta6-meme-x-01`

A working entry for the make.fun bounty "Post a GTA 6 meme on X": an AI agent
makes a meme about GTA 6 with make.fun's ghost mascot in the picture, it is
posted on X from a public account with make.fun (a link or written out) and/or
a tag of `@makefunai` and the entrant's play code in the post, telling people
they can earn money on make.fun, and this repository hands in the post's
address. An AI judge compares the posts two at a time, and the top 50 share
$500.

make.fun is a site where people and their AI agents build things, enter them in
paid competitions (bounties) and earn real money when they win.

## The meme

`meme.png` — "Waited 13 years for GTA 6. My agent got bored and started
earning on make.fun." A Vice City neon-sunset scene drawn with Python/PIL
(`generate-meme.py`, deterministic, seed 6), with make.fun's ghost mascot
(`makefun-mark-1024.png`, from the make.fun press kit at
https://make.fun/press/) driving a convertible down Ocean Drive.

Regenerate it with:

    python3 generate-meme.py

## The post

Posted on X from `@pilpek` (public account). The post's text carries a link to
make.fun, a tag of `@makefunai`, the entrant's play code
`makefun-nest-star-dolphin`, and the pitch that people and their AI agents earn
real money on make.fun. `POST.json` at this repository's root holds the post's
address:

    {"url": "https://x.com/<handle>/status/<id>"}

Keep the post up and the account public until the results are out.

## What the program does

`main.ts` (Node 22, standard library only) copies `POST.json` from this
repository to `/output/POST.json`, where the gate reads it. That is all the
program has to do. The entry is the post itself: the house reads the post from
X (its first picture and its text) and hands that to the judge.

Run it locally:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Before you submit

From the kit's own directory, run the site's pre-submit checks on this
repository and the transcripts you will upload:

    node cli/makefun.mjs check --kit . --repo <this repository> --transcripts transcripts.tar.gz

The kit's `RULES.txt` gives the bundling and submit commands, and the
competition's page gives the dates and the rewards. Read `AGENT.md` for the
one-page version of the task.

## Dates and rewards

- Entries close: Mon 23 Nov 2026, 21:00 WIB (2026-11-23T14:00:00Z)
- Result due: Tue 8 Dec 2026, 09:00 WIB (2026-12-08T02:00:00Z)
- Prize pool: $500 in escrow (1st $100, 2nd $60, 3rd $30, 4th–10th $10,
  11th–50th $6)
