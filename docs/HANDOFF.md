# Handoff — state of the project (updated 2026-09-29)

## Who / what
- Teacher (javedani66@gmail.com) teaches a term on **simple machines** to grades 2–6 over **12 sessions**. Students use phones and computers; class messengers are **Telegram and WhatsApp**. Iran: claude.ai is not reachable for students; the game is distributed via GitHub Pages (this repo) and as a single offline HTML file.
- More games are planned for other physics topics, chemistry and later biology, all under this one site (shared origin → a shared student profile is possible later).

## The simple-machines game (src/simple-machines)
- 8 stations (`ST` in app.js): force, scale («جرم و وزن»), lever, ramp, pulley, wheel, wedge (+screw), sort. Each has a free lab, levels, endless mode.
- 3 tracks by grade: **a کاوشگر** (2–3), **b سازنده** (4), **c مهندس** (5–6). `levelsOf(k)` returns the track's levels (b/c get an extra mixed level «همه با هم»/«قهرمان»).
- **Journey map «نقشهٔ سفر»** (journey.js) is the home screen: 12 stops = 12 class sessions, in 3 lands (نیرو 1–4، ماشین‌ها 5–10، کارگاه مهندسی 11–12). Each stop: main missions (real interactive levels), optional side quest (endless mode with goal SIDEG), lab, parent-confirmed home task (2-second hold button), word cards before first mission, «امروز یاد گرفتی» line after. «تو اینجایی» marker + big «ادامه بده» resumes the exact challenge.
- Welcome: name → grade (دوم..ششم) → traveler (ربات/موشک/ماشین/بالن). Multiple players per device. Grade can be changed later in «بزرگ‌ترها» (stars of each track are kept separately).
- «بزرگ‌ترها» (hold-gate): confirm home tasks, set the class-week flag (or link `#m5` style hash), manage players, open the old station grid for free play, teacher page.
- Backpack: badges, word cards, **message for teacher** with a 23-letter checksummed code carrying all stars/home/side/grade/traveler; pasting it restores progress (also the only backup). Teacher page (`#teacher`) parses many pasted messages into a class table sorted by who is behind.
- Saving: localStorage only (per device + browser). Service worker makes the site work offline and installable.

## Teacher decisions so far
- Traveler chosen by the child; home task ticked by a parent at home (keep simple); all tracks go through stops in order, b/c have more steps and harder side quests land by land; keep full-fidelity progress code inside the teacher message (she rejected a shorter lossy code).
- She wants Persian that fits each reading level, interactive games over text quizzes, and **no text overlapping graphics** (reported twice — use tests/ov.py + gal.py).
- Portal: unreleased games are shown only as one box «سرزمینِ علوم بزرگ‌تر می‌شه… منتظر بمونید!», not as individual "coming soon" cards.

## Related documents (Claude Docs, owned by the teacher)
- Lesson plan doc id `8daba727-aed4-4b34-8670-dfa09e7f8fc7` (session table, session↔stop mapping, misconceptions).
- Design/report doc id starting `ca76416b` (journey-map research and comparison).
- Old claude.ai artifact of the game: https://claude.ai/artifact/7DHz6NV8dadWLELYMnGJdA (private; superseded by this site).

## Open items / ideas (not started unless the teacher asks)
1. Ask the browser for persistent storage (`navigator.storage.persist()`) — offered, not yet approved.
2. Server-side saving so progress follows the child and reaches the teacher automatically — needs a host reachable from Iran; not decided.
3. Android/Windows packaging — the PWA install covers most of this for now.
4. Shared student profile across future games (same origin).
5. Verify github.io is reachable from students' phones without VPN (teacher to check).
