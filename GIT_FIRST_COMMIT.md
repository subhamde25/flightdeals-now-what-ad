# Your First Commit: Step by Step

This guide puts the whole project in **`C:\Users\deysu\flightdeals`** on GitHub as **https://github.com/subhamde25/flightdeals-now-what-ad** (public).

Every grey block is a command you copy into **Git Bash** or **PowerShell** and press Enter.

---

## 1. How Git works

| Term | What it means here |
|---|---|
| **Repository (repo)** | This project folder plus a hidden `.git` folder where Git keeps the full history. |
| **Working folder** | The files you see and edit. |
| **Staging (`git add`)** | Choosing which changes go into the next snapshot. |
| **Commit (`git commit`)** | A saved snapshot with a message. You can always go back to it. |
| **Branch (`main`)** | A line of commits. You'll work on `main`. |
| **Remote (`origin`)** | The copy of the repo on GitHub. |
| **Fetch / Push** | Fetch downloads GitHub's commits to your PC; push uploads yours to GitHub. |
| **`.gitignore`** | Files Git must never upload (renders, `node_modules`). Already set up. |
| **Git LFS** | Large File Storage. The final MP4 is stored separately and the repo keeps a small pointer. Already set up in `.gitattributes`. |

The flow is: **edit files → `git add` → `git commit` → `git push`**.

---

## 2. What gets uploaded

| Goes into Git | Size | How |
|---|---|---|
| Code and docs: `*.html`, `*.mjs`, `*.py`, `*.sh`, `*.json`, `*.md` | ~0.2 MB | normal Git (text) |
| Assets: logo `.png` files, voice `vo_raw.mp3` + `vo.wav` | ~2.4 MB | normal Git (binary) |
| Captions + contact sheet: `deliverables/*.srt`, `*.jpg` | ~0.1 MB | normal Git |
| Final ad: `deliverables/FlightDeals_16x9_NowWhat.mp4` (≈11 MB) | ~11 MB | **Git LFS** |

| Stays on your PC only | Why |
|---|---|
| `node_modules/` | Reinstalled with `npm install`. |
| `build/` | Render, mix, master, stems, stills and logs. Rebuilt with `npm run render`. |

---

## 3. Create the empty repo on GitHub

1. Go to **https://github.com/new** (signed in as `subhamde25`).
2. **Repository name:** `flightdeals-now-what-ad`
3. **Description** (optional): `AI-assisted 16:9 brand ad for FlightDeals.in: Experiences, Transfers and Rent a car, built in code with motion graphics, synthesized music and a Fish Audio voiceover.`
4. Choose **Public**.
5. Leave **Add a README**, **.gitignore** and **license** **off**, so the repo starts empty. If you did add a README, see step 8b.
6. Click **Create repository**.

---

## 4. One-time setup (already done on this PC)

Your name, your private no-reply email and Git LFS are already configured. To check:

```bash
git config --global user.name
```

```bash
git config --global user.email
```

```bash
git lfs version
```

The first two should print `subhamde25` and `139131879+subhamde25@users.noreply.github.com`.

---

## 5. Open a terminal in the project folder

The project lives in **`C:\Users\deysu\flightdeals`**. It sits outside OneDrive on purpose, because OneDrive sync can corrupt the hidden `.git` folder.

- **Easiest:** in File Explorer, right-click inside the folder → *Show more options* → **Open Git Bash here**.
- **Or** open PowerShell or Git Bash and `cd` into it:

```bash
cd "C:\Users\deysu\flightdeals"
```

---

## 6. Create the local repository and turn on LFS

```bash
git init -b main
```

```bash
git lfs install
```

---

## 7. Stage everything and check it

```bash
git add .
```

```bash
git status
```

You should see the docs, `h169/`, `audio/`, `tools/`, `assets/` and `deliverables/`, and **no** `node_modules/` or `build/`. To confirm the MP4 goes through LFS:

```bash
git lfs ls-files
```

It should list `deliverables/FlightDeals_16x9_NowWhat.mp4`.

---

## 8. Commit and push

```bash
git commit -m "Add FlightDeals Now What ad: composition, audio pipeline, assets and final 16:9 ad"
```

```bash
git remote add origin https://github.com/subhamde25/flightdeals-now-what-ad.git
```

```bash
git push -u origin main
```

The first push opens a GitHub sign-in window (Git Credential Manager). Sign in once and it's remembered.

### 8b. Only if GitHub already has an "Initial commit"

If you created the repo with a README, GitHub already has a commit your PC doesn't know about, and the push is rejected. Fix it before pushing, without touching your files:

```bash
git fetch origin
```

```bash
git reset --soft origin/main
```

```bash
git commit -m "Add FlightDeals Now What ad: composition, audio pipeline, assets and final 16:9 ad"
```

```bash
git push -u origin main
```

Our `README.md` replaces GitHub's short one.

---

## 9. Day-to-day

After you change something (a timing, an SFX cue, a caption):

```bash
npm run render
```

```bash
git add .
```

```bash
git commit -m "Describe what you changed"
```

```bash
git push
```

Use `npm run remix` instead of `npm run render` when only the audio changed.
