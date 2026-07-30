<div align="center">

<img src="./hello.svg" alt="Hi, I'm Muhammad Moiz" width="600"/>

<br/>

<a href="mailto:moiz.codez@gmail.com"><img src="https://img.shields.io/badge/email-moiz.codez%40gmail.com-24292f?style=flat-square&logo=gmail&logoColor=white" alt="Email"/></a>
<a href="https://www.linkedin.com/in/moiz-siyal/"><img src="https://img.shields.io/badge/linkedin-moiz--siyal-24292f?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="https://www.reddit.com/user/moiz-codez"><img src="https://img.shields.io/badge/reddit-u%2Fmoiz--codez-24292f?style=flat-square&logo=reddit&logoColor=white" alt="Reddit"/></a>
<a href="https://github.com/moiz-codez"><img src="https://img.shields.io/badge/github-moiz--codez-24292f?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a>

</div>

<img src="./hd-portrait.svg" width="940" alt="portrait"/>

<div align="center">
<img src="./ascii.svg" width="400" alt="Muhammad Moiz"/>
</div>

> Computer Science major at Mehran University of Engineering & Technology, Hyderabad, Sindh.<br>
> Full-stack developer, currently deep in agentic AI.

I'm usually the one holding the messy middle together — coordinating between product, QA and dev so the release actually ships on time. At [Verior](https://www.linkedin.com/company/81822374/) that went from a QA internship to Execution Lead inside three months; from there it was release trains, sprint velocity, and turning "it's flaky" into a repeatable pipeline.

<img src="./hd-system-info.svg" width="940" alt="system info"/>

<img src="./neofetch.svg" width="940" alt="moiz@codez system info"/>

<sub>`assets/profile.jpg` isn't in this build yet, so `ascii.svg` above is a placeholder silhouette, and the GitHub Stats rows show "—" until the Actions workflow runs once. See <b>about this readme</b> below to switch both on.</sub>

<img src="./hd-ecosystem.svg" width="940" alt="ecosystem"/>

<img src="./system-map.svg" width="940" alt="tech stack ecosystem, radiating from one pipeline"/>

<div align="center">
<img src="https://skillicons.dev/icons?i=c,cpp,java,py,js,ts,react,nextjs,nodejs,express,flask,django,fastapi,mongodb,postgres,mysql,redis,firebase,supabase,docker,kubernetes,aws,gcp,vercel,git,github,linux,arduino,flutter,dart,androidstudio&perline=11" alt="tech stack icons"/>
</div>

<img src="./hd-timeline.svg" width="940" alt="timeline"/>

<img src="./timeline.svg" width="940" alt="career and education timeline"/>

### Experience

**Execution Lead** · [Verior](https://www.linkedin.com/company/81822374/) · Full-time, Hybrid — Mar 2024 – Dec 2024 (10 mos)
- Led cross-functional execution across product, QA and dev; spearheaded 5+ releases, cutting deployment delays 40%
- Coordinated a team of 10+ developers and QA engineers, improving sprint velocity and issue-resolution rates
- Overhauled internal testing pipelines, dropping QA-to-fix turnaround from 3 days to under 24 hours
- Designed internal KPI/delivery dashboards for stakeholder visibility

**Software Quality Assurance Intern** · Verior · Part-time, On-site — Jan 2024 – Mar 2024 (3 mos)
- Executed 100+ manual test cases across API, UI and end-to-end flows
- Reported 50+ critical bugs; raised test coverage 30% through documentation and exploratory testing
- Supported pre-release validation across 3 major product updates

### Education

**B.S. Computer Science** · Mehran University of Engineering and Technology — Dec 2022 – Jun 2027
Director, IEEE Student Chapter (MUET CS) 2024–25 · TEDxMUET'23 volunteer · MUET Job Fair volunteer

**High School Diploma, Computer Science** · Cadet College Petaro — May 2017 – Jul 2022 · Grade A+
President, Computer & Robotics Club · Director, PMUN-IV · College Band Commander 2020–22 · GK/CB, college hockey · outdoor & indoor shooting teams

<img src="./hd-about-this-readme.svg" width="940" alt="about this readme"/>

Every graphic on this page is generated, not embedded from anyone else's server, and nothing here can rate-limit or go dark.

- **`ascii.svg`** is a photo pushed through a character ramp by [`scripts/make_portrait.py`](scripts/make_portrait.py). It's a one-off — run it locally after adding `assets/profile.jpg`, not on a schedule.
- **`neofetch.svg`**, the section headings, and the numbers under GitHub Stats are drawn by [`scripts/generate_neofetch.py`](scripts/generate_neofetch.py), run daily by [a GitHub Action](.github/workflows/stats.yml) using the workflow's built-in token — no secret to add.
- **`hello.svg`**, **`system-map.svg`** and **`timeline.svg`** are static, built once from [`scripts/make_hello.py`](scripts/make_hello.py), [`scripts/make_system_map.py`](scripts/make_system_map.py) and [`scripts/make_timeline.py`](scripts/make_timeline.py) — re-run any of them by hand if the underlying facts change.
- Everything animates with SMIL inside the SVG itself, because GitHub strips `<script>` from READMEs. Headings are SVGs for the same reason: GitHub also strips inline `<style>` from markdown, so an image is the only way to put this page's own typeface on them.
- The typeface is [JetBrains Mono](scripts/fonts), subset to the characters these graphics actually draw and inlined as base64 — see [`scripts/fonts/README.md`](scripts/fonts/README.md) for why that's not optional here.

**To finish the setup:**
1. Add a headshot at `assets/profile.jpg`, then run `pip install pillow numpy opencv-python-headless rembg onnxruntime` and `python3 scripts/make_portrait.py`.
2. Push this repo as `moiz-codez/moiz-codez` — the Actions workflow needs no secrets, only `permissions: contents: write`, which is already set.
3. Everything else regenerates itself; only re-run a `make_*.py` script by hand if a fact (a job, a degree, a stack item) changes.
