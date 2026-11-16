# SCut Studio

Turn long videos and live streams into captioned vertical clips, ready to post. Free and open source: run it on
your own computer or server, with your own AI key.

Maintained by Saif Ali · [GitHub](https://github.com/saifali1035) · [Instagram](https://www.instagram.com/_.saif.ali_/)

Paste a YouTube, Twitch or Kick link (or upload a file) and SCut Studio finds the moments worth clipping, cuts them to
9:16, adds word-by-word captions and a hook, and can post them to your connected accounts. It can also record a
creator's live stream and clip the highlights while the stream is still running.

## What it does

- **Clips from any video.** Transcribes the audio, asks an AI which moments would hold a stranger's attention, and
  renders each one with captions in one of three styles.
- **Live clipping.** Records a stream into a rolling buffer and clips as it happens, using loudness, chat activity
  and the transcript.
- **Workspaces per creator.** Channels, clip settings, posting rules and an activity log for each creator you clip.
- **Posting.** Connect YouTube, Instagram and TikTok in one click, then queue or auto-post finished clips, with
  spacing and daily caps (see [DEPLOY.md](DEPLOY.md#connecting-youtube-instagram-and-tiktok) for the one-time setup).
- **No sign-in on your own computer.** It opens straight into the dashboard. On a shared server, switch accounts on
  (`PEAKCUT_ACCOUNTS=1`) for email or Google sign-in and an admin dashboard.
- **Your own AI.** Gemini, OpenAI, Grok, Groq, OpenRouter, Claude, a local model through Ollama, or anything that
  speaks the OpenAI chat format. No key at all also works: clips are then picked by loudness.

## Quick start

You need Python 3.10 or newer and `ffmpeg`. On Windows: `winget install Gyan.FFmpeg`. On a Mac: `brew install ffmpeg`.
On Linux: `sudo apt install ffmpeg`. SCut Studio finds it by itself and tells you in the dashboard if it is missing.

```bash
git clone https://github.com/saifali1035/scut-studio.git
cd scut-studio
```

```bash
python -m venv .venv
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the server:

```bash
python -m studio.server
```

The first start downloads the speech model by itself (about 480 MB, once).

Open http://127.0.0.1:8765. There is no sign-in: it opens straight into the dashboard. Go to **Settings, AI**, choose
your AI service, paste your key and press **Save and test** (see [Choose your AI](#choose-your-ai)).

## Using SCut Studio

### Add a video and choose what to make

On **All videos**, paste a YouTube, Twitch or Kick video link, or upload a video file. You can add several source
videos to one batch. Select a creator if you want that creator's saved settings and posting rules to apply. Open
**Options** before starting to choose the output format and clipping behavior.

SCut Studio has two video modes:

- **Find highlights** transcribes the source, then asks the selected AI to rank moments that can stand on their own.
  Set the number of clips and shortest/longest duration. The AI also writes clip titles, descriptions and hooks.
- **Split into parts** divides the selected video range into the number of consecutive, equal-length parts you set.
  It labels the clips **Part 1**, **Part 2**, and so on. It does not ask the AI to find highlights, and ignores the
  highlight count, clip-length limits and clip focus. Each part must be at least three seconds long.

The optional **Part of the video** start and end fields limit either mode to that range; leave them empty to use the
whole source. Times are in minutes. A split range is divided evenly, so the final part ends at the selected end time.

### Choose a clip focus

In highlight mode, **Clip focus** steers the AI toward a kind of moment:

- **Balanced** looks for broadly entertaining moments, such as humor, surprise, skill, strong reactions and stories
  with a payoff.
- **Funny** favors jokes, playful banter, mishaps and authentic laughter, while keeping enough setup for the joke to
  land.
- **Horror / suspense** favors tension, creepy reveals, jump scares, near misses and genuine fear or surprise. It
  uses only evidence available in the transcript and reactions; it cannot reliably understand every visual event.
- **Controversial** favors clearly expressed strong opinions, disagreements, heated debates and surprising takes.
  It is instructed to preserve context and not exaggerate a disagreement.
- **Scandal / revelations** favors explicit revelations, admissions, accusations or dramatic disclosures. Claims
  should remain framed as claims; the AI is instructed not to invent details or present speculation as fact.

These are selection instructions for the AI, not guarantees that a source contains a moment of that kind. Focus is
ignored in **Split into parts** mode. If no AI key is configured, SCut Studio still makes clips using loudness to select
moments, but the focus profiles and AI-written titles are not available in that fallback.

### Caption, layout and quality options

- **Caption style:** Bounce, Hype or Clean changes the word-by-word caption appearance.
- **Layout:** Blurred fill keeps the source frame visible over a blurred background; Zoomed in enlarges the frame
  over a blurred background; Fill screen centre-crops the source to fill the vertical canvas; Game split places the
  speaker video in the upper half and gameplay in the lower half.
- **Video quality:** choose 720p for faster rendering or 1080p for a sharper, slower render.

To use **Game split**, add a separate gameplay video in the **Gameplay video** field. SCut Studio treats the main video
as the speaker/source and the separate gameplay file or link as the lower panel; the gameplay is muted and the
source video's audio is kept. Uploaded gameplay loops as needed. For a gameplay link, SCut Studio uses and loops the
first 45 seconds. Add one gameplay source for the batch; it is used for every source video in that batch. A finished
YouTube, Twitch or Kick video can be used as a gameplay link; live streams, channels and playlists are not accepted.

### Review, edit, cancel and post clips

Open a video job to review the generated clips. You can preview, download, copy a clip, edit its title and hook,
choose from three suggested hooks, adjust the clip timing, or remake it with another caption style, layout or
quality. For Hindi speech, hooks and titles are written in Roman-script Hinglish. When the AI finds a short payoff
worth teasing, the clip opens with that excerpt and then replays from the original start; turn this **Cold open**
option off in the editor if you prefer a straight cut. The editor's **Shorts safe-area guide** marks approximate
areas covered by Shorts controls and lower-screen text. The split-screen layout is only available for a remake when
the job has gameplay footage attached.

While a video job is queued or running, use **Cancel clipping** to stop it. A queued job is removed from the worker
queue; a running job stops after its current download/transcription/render step. Clips already finished remain
available, and clips that did not finish are marked stopped.

Select individual clips or use **Select all clips**, then choose **Post selected** to send the finished clips to
YouTube. This starts posting as soon as the posting worker can take them. Clips already scheduled for that account
are moved to the front. The regular **Add to queue** action keeps the configured schedule. Uploads still depend on
the connected account, platform availability and YouTube's processing time; they do not make a video public
instantaneously.

### Creators, live streams and automatic posting

Create a creator workspace to keep its channels, default clip settings, post targets, score threshold, spacing,
daily cap and activity history together. A creator can be configured to auto-post clips that meet its score
threshold. Posting gaps and daily caps apply to scheduled and automatic posts.

To quickly clip a live stream, paste its direct YouTube, Twitch or Kick stream link into **All videos**. Once SCut
Studio identifies it as live, press **Watch live now** on that link. You do not need to create a creator first; with
no creator selected, the app uses its default live clipping settings. If you select a creator, its live settings apply
and the recording is filed under that creator. SCut Studio records into a rolling buffer and evaluates highlights
using the transcript, loudness and available Twitch chat activity. The live recording appears in **All videos**, where
you can clip the latest 30 or 60 seconds manually or stop recording. Automatic channel monitoring remains available
in a creator's Setup.

To post, connect the relevant account under **Settings, Connected apps**. YouTube posting needs a Google OAuth client;
Instagram and TikTok need their platform developer apps. The one-time account/app setup steps and callback addresses
are in [DEPLOY.md](DEPLOY.md#connecting-youtube-instagram-and-tiktok). A personal local install can make clips
without configuring any posting accounts.

## Setup details

### Local computer

1. Install Python 3.10 or newer and FFmpeg. On Windows, run `winget install Gyan.FFmpeg`; on macOS use
   `brew install ffmpeg`; on Ubuntu/Debian use `sudo apt install ffmpeg`.
2. Clone this repository, create a virtual environment, activate it, and install `requirements.txt` using the
   commands in [Quick start](#quick-start).
3. Run `python -m studio.server` from the repository folder.
4. Open [http://127.0.0.1:8765](http://127.0.0.1:8765). The first start downloads the speech recognition model
   (about 480 MB); later starts reuse it. To download it before launching, run `python -m studio.fetch_model`.
5. Open **Settings, AI**, choose a provider and model, enter your key and select **Save and test**. This is optional:
   without it, highlight selection falls back to loudness.

SCut Studio stores the database, downloaded source videos, gameplay uploads, generated clips and speech model under
`./data` by default. To move that data, set `PEAKCUT_DATA` in `.env` before starting the app. Copy
`.env.example` to `.env` only if you need environment settings; the dashboard is enough for a basic local install.
Keep `.env`, AI keys, OAuth secrets and the `data/` folder private. Do not commit them.

### Server or Docker

For a public/shared server, enable accounts and use HTTPS. The Docker deployment includes PostgreSQL and Caddy;
follow [DEPLOY.md](DEPLOY.md) for domain, DNS, OAuth, email and administrator setup. Do not expose a local install
with sign-in disabled to the internet. To enable sign-in for a non-Docker server, set `PEAKCUT_ACCOUNTS=1` in
`.env`; see [`.env.example`](.env.example) for available settings and resource limits.

### Posting setup

Connecting a social account alone may not be enough: the corresponding app credentials and redirect URLs must first
be configured. YouTube uses a Google OAuth web application with `/oauth/youtube/callback`; Google sign-in uses
`/auth/google/callback`. Instagram and TikTok each require their own developer application and callback URL. See
[the detailed posting setup](DEPLOY.md#connecting-youtube-instagram-and-tiktok) for provider-specific steps,
required permissions and dashboard entry points.

## Choose your AI

SCut Studio needs a chat model that can return JSON. The easy way is in the dashboard: **Settings, AI**. Pick the
service, paste your key, press **Find models** to choose from the service's own list, then **Save and test**. The
key is kept in the data folder on your machine and is never shown again.

If you prefer a file (or run a server), the same three things can go in `.env`. What is saved in the dashboard wins:

```ini
PEAKCUT_AI_PROVIDER=gemini
PEAKCUT_AI_MODELS=gemini-2.5-flash
PEAKCUT_AI_KEY=your-key-here
```

| `PEAKCUT_AI_PROVIDER` | Service | Where to get a key |
|---|---|---|
| `gemini` | Google Gemini | https://aistudio.google.com/apikey |
| `openai` | OpenAI | https://platform.openai.com/api-keys |
| `xai` | Grok (xAI) | https://console.x.ai |
| `groq` | Groq | https://console.groq.com/keys |
| `openrouter` | OpenRouter (many models, one key) | https://openrouter.ai/keys |
| `anthropic` | Claude | https://console.anthropic.com |
| `ollama` | A model on your own machine, no key | https://ollama.com |
| `custom` | Any OpenAI-compatible address: also set `PEAKCUT_AI_BASE_URL` | |

- `PEAKCUT_AI_MODELS` is the model id exactly as the service names it. Model names change often, so check the
  service's current list. Several ids separated by commas are tried in order, which gives you a fallback.
- A fast, inexpensive model is the right choice. A one-hour video is read in about four requests.
- You pay the AI service directly for what you use. The **AI usage** page in the app shows how many requests and
  tokens each video took.
- Speech to text does not use the AI service. It runs on your own machine, so audio never leaves it.

## Settings

Everything is set through environment variables, normally in a `.env` file next to this README.
[`.env.example`](.env.example) lists every setting with a short explanation. The ones that matter first:

| Setting | What it is for |
|---|---|
| `PEAKCUT_AI_PROVIDER`, `PEAKCUT_AI_MODELS`, `PEAKCUT_AI_KEY` | The AI that picks clips and writes titles (or set it in the dashboard) |
| `PEAKCUT_ACCOUNTS` | `1` makes everyone sign in. Use it on any server other people can reach |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Optional: Sign in with Google, and connecting YouTube |
| `PEAKCUT_SMTP_*`, `PEAKCUT_MAIL_FROM` | Optional: confirmation and password emails |
| `PEAKCUT_DATA` | Where videos, clips and the database are kept (default `./data`) |

`.env`, the `secrets/` folder and all user data are ignored by git. Keep keys there, never in the code.

## Admins

This only matters with accounts switched on (`PEAKCUT_ACCOUNTS=1`); without them you are the owner and can do
everything. An account is an admin only when the database says so. No email address is special in the code and no web request
can change a role. Do it on the machine that runs SCut Studio:

```bash
python -m studio.admin grant you@example.com
```

`revoke` and `list` work the same way. The admin dashboard is at `/admin` and answers "not found" to everyone else.

## How it is built

| Part | What it is |
|---|---|
| `studio/` | The server: FastAPI, the clip pipeline, live recording, accounts |
| `studio/ai.py` | The only file that talks to an AI service. Add a provider here |
| `web/` | The pages: landing, sign-in, the app, the admin dashboard (plain HTML, CSS and JavaScript, no build step) |
| `tests/` | Tests that run against a throwaway copy of the app |
| `deploy/`, `Dockerfile`, `docker-compose.yml` | One-server deployment with PostgreSQL and automatic HTTPS |

Video work is done with `ffmpeg` and `yt-dlp`. Speech is transcribed with `sherpa-onnx` and the Parakeet model.
Data is kept per user: accounts in the database (SQLite on your own computer, PostgreSQL on a server), videos and
clips in each user's own folder. [AGENTS.md](AGENTS.md) is a short map of the code for contributors and AI coding
assistants.

## Updating

SCut Studio checks GitHub once a minute while it runs. When a newer version is out, the dashboard shows a notice
within a minute or two (no restart needed), with what changed
and how to update: ask your AI coding assistant to do it (the notice has a sentence to paste), or run
`git pull && pip install -r requirements.txt` in the SCut Studio folder and restart it (with Docker:
`git pull && docker compose up -d --build`). Your `.env`, keys and clips are not touched. Only the two commit ids
are sent to GitHub; set `PEAKCUT_UPDATE_CHECK=0` to turn the check off.

## Deploy

[DEPLOY.md](DEPLOY.md) walks through a single server with Docker: the app, PostgreSQL, and Caddy for HTTPS.

```bash
docker compose up -d --build
```

## How it behaves under load

- The page asks the server one small question every few seconds. When nothing has changed, the answer comes
  straight from memory.
- Each person's videos wait in their own line and the lines take turns, so one person cannot hold everyone up.
- The server measures its own processor, memory and disk every second. Extra videos and recordings start only
  while there is room, wait briefly when it is nearly full, and continue the moment it frees up.
- There are no limits on upload size, video length, recordings, creators or storage unless you set them in
  `.env`. Five videos can be sent at once. Request sizes are always capped, so junk can't fill the memory.

## Tests

```bash
python tests/run.py
```

This starts a copy of the app on a spare port with an empty temporary data folder, runs the permission, abuse and
queue tests against it, then removes it. It needs no keys and never touches real data.

## Security

- With sign-in off, SCut Studio listens on this computer only (`127.0.0.1`), refuses changes sent by other websites,
  and only answers to its own address. Do not expose it to the internet that way: turn accounts on.
- Passwords are stored only as salted scrypt hashes. Sessions are random tokens stored hashed; cookies are HTTP-only.
- Every route works out who is asking from the session, never from the request, so users only reach their own data.
- Only known video sites are fetched, and text from videos is treated as data when it is shown to the AI.
- Found a problem? Please report it privately through the repository's security advisories instead of opening a
  public issue.

## Using it responsibly

Clip videos you made, or have permission to use. You are responsible for the rights to what you download, clip and
post, and for following the terms of the sites you fetch from and post to.

## Licence

[MIT](LICENSE). Caption fonts in `studio/fonts/` (Anton, Archivo Black, Poppins) are under the SIL Open Font
License; the licence texts are in the same folder.
