# World News — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/danielhutapea36/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/danielhutapea36/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world's news of Monday 23 November 2026, for the
make.fun `news-image-20261123` bounty. The image is a newspaper front page
with the masthead "WORLD NEWS", the date line "MONDAY 23 NOVEMBER 2026",
and six panels — one per story below.

## The six stories

1. **Tankers hit in the Strait of Hormuz** — on Saturday, British
   maritime authorities said two tankers were hit by unknown projectiles
   as they left the Gulf; on Sunday, Iran's navy said two more tankers
   caught fire after hitting naval mines east of the strait. Attacks on
   shipping in the area are at their highest level since the war began.
   Source: AP —
   https://www.thesouthasiantimesbd.com/business/news/27549
2. **Sea drones sink Russian corvette Merkury off Libya** — on Sunday,
   suspected Ukrainian sea drones struck the Russian corvette Merkury at
   the Benghazi naval base; satellite imagery showed most of the vessel
   capsized and sunk, with only its bow above water, and 10 people
   suffered minor injuries. Libyan officials said the drones were
   launched from a base run by Ukrainian forces in western Libya.
   Source: AP / Reuters / BBC —
   https://www.europesays.com/3394001/
3. **Russian strikes kill at least 11 in the Kyiv region** — overnight
   strikes hit the Kyiv region on Sunday; a drone struck a five-storey
   apartment block in Dymer, 45 km north of Kyiv, killing at least
   eight people there, and rescuers pulled a child alive from the
   rubble while still searching for 11 missing, including two children.
   A supermarket strike in Vyshneve killed two more people.
   Source: AFP —
   https://www.europesays.com/ukraine/75111/
4. **COP31 ends with no deal** — in Antalya on Sunday, the UN climate
   summit closed without an overarching agreement after the longest COP
   on record; the EU and other countries rejected the final text because
   it made no mention of fossil fuels. It is the first COP failure
   since Copenhagen in 2009.
   Source: Reuters —
   https://www.businessday.co.za/news/science-and-environment/2026-11-22-cop31-climate-talks-collapse-over-fossil-fuels-and-funding/
5. **BepiColombo reaches Mercury** — on 21 November, after an
   eight-year journey, the European-Japanese BepiColombo spacecraft
   entered orbit around Mercury, only the second mission ever to do so.
   Its two probes, ESA's Mercury Planetary Orbiter and JAXA's Mio,
   separate on 9–10 December, and science operations begin in April
   2027.
   Source: ESA —
   https://www.esa.int/media/about-us/directorates/science/bepicolombo-entering-orbit-around-mercury
6. **Indonesia confirms 24 dead in factory fire** — on Monday,
   Indonesia confirmed 24 people died in the fire that tore through the
   PT Fonusa Agung Mulia candy factory in Cikande, Banten, on Saturday
   evening; about 30 people are still missing as rescuers search the
   unstable wreckage.
   Source: Reuters —
   https://wtbx.com/2026/11/22/indonesia-says-24-killed-in-factory-blaze-as-rescuers-search-for-dozens-missing/

## How it works

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` byte-for-byte into the output directory
(`$MAKEFUN_OUTPUT_DIR`, default `/output`). It first checks the PNG
magic bytes, the 1 MiB size cap and the 1024×1024 dimensions of the
source, copies the file, then reads the copy back and confirms it is
identical before reporting its size and SHA-256. No network, no
randomness, no timestamps — two runs write identical bytes.

Run it locally with:

```
MAKEFUN_OUTPUT_DIR=/tmp/ni23-out python3 main.py
```

## Verification

To confirm the copy is faithful, run the program once more into a
fresh folder and compare the digests of the source and the copy:

```
MAKEFUN_OUTPUT_DIR=/tmp/ni23-check python3 main.py
sha256sum entry.png /tmp/ni23-check/entry.png
```

The two digests must be identical, and both must match the SHA-256
recorded under "The image" below. The first eight bytes of the copy
must read `89 50 4E 47 0D 0A 1A 0A`, the PNG signature. If `entry.png`
is missing beside `main.py`, over the size cap, or a copy fails any of
these checks, the program stops with exit code 1 and a
plain-language error instead of leaving behind a bad copy.

## The image

- File: `entry.png`
- Size: 1024 × 1024 pixels, 632713 bytes
- SHA-256: `26acfec885cbdcfe1c8ad4a69a986eb002a43d399361648fa43abdee9b9acf04`

---

<sub>Entered on [make.fun](https://make.fun/?ref=danielhutapea36&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
