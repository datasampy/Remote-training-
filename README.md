# GIZ-ZME Remote Work Training Programme — Registration Form

A mobile-first, accessible registration form for the **GIZ-ZME Remote Work
Training Programme**. It saves each submission to a Google Sheet and sends the
registrant a confirmation email — with **no backend server**.

```
index.html    ← the form (open this / upload this)
styles.css    ← styling (theme colours live in one :root block at the top)
script.js     ← logic + the ONE config block you edit (URLs & keys)
Code.gs       ← Google Apps Script (the "backend"), deploy as a Web App
assets/
  giz-logo.png ← drop the GIZ logo here (see step 4)
```

Everything is a static file. Once configured, you can upload it straight to
**datalead.info** or embed it in an existing page.

---

## How it fits together

```
 Registrant's browser
   │  fetch() POST (JSON as text/plain)
   ▼
 Google Apps Script Web App  ──►  appends a row to your Google Sheet
   │
   ▼
 {ok:true}   +   Apps Script emails the registrant a confirmation
   │
   ▼
 Success screen shown to the registrant
```

There is really **one thing you must do** before it works:

1. **Deploy the Apps Script and paste its URL into `script.js`.** — Steps 1–3

The confirmation email is already handled by that same Apps Script
(all-Google, no extra account). — Step 5 (nothing to configure).

---

## Step 1 — Create the Google Sheet

1. Go to <https://sheets.google.com> and create a **new blank spreadsheet**.
2. Name it something like `GIZ-ZME Registrations`.
3. Leave it empty — the script writes the header row automatically on the
   first submission.

## Step 2 — Add the Apps Script

1. In that spreadsheet: **Extensions ▸ Apps Script**.
2. Delete any starter code in `Code.gs`.
3. Open the `Code.gs` file from this project, copy **all** of it, and paste it
   in. Click the **Save** (💾) icon.

## Step 3 — Deploy as a Web App  *(the exact steps)*

1. Click **Deploy ▸ New deployment**.
2. Click the ⚙️ gear next to "Select type" and choose **Web app**.
3. Fill in:
   - **Description:** `GIZ-ZME registration` (anything).
   - **Execute as:** **Me** *(your Google account).*
   - **Who has access:** **Anyone** *(required — the form is public and
     posts anonymously).*
4. Click **Deploy**.
5. Click **Authorize access** and approve the permissions (this is Google
   asking if the script may write to your Sheet / send email on your behalf).
   You may see an "unverified app" warning — click **Advanced ▸ Go to
   (project name)** and continue. This is normal for your own scripts.
6. Copy the **Web app URL**. It ends in **`/exec`**.
   > Example: `https://script.google.com/macros/s/AKfy…long…id/exec`

**➡ Paste that URL into `script.js`:**

```js
const CONFIG = {
  APPS_SCRIPT_URL: "https://script.google.com/macros/s/AKfy…/exec",  // ← here
  ...
```

> **If you later edit `Code.gs`,** you must **Deploy ▸ Manage deployments ▸
> Edit (✏️) ▸ Version: New version ▸ Deploy** for changes to go live. The URL
> stays the same.

**Quick test:** paste the `/exec` URL into a browser. You should see
`{"ok":true,"service":"GIZ-ZME registration","ready":true}`.

## Step 4 — The GIZ logo

A vector recreation of the GIZ wordmark already ships at
**`assets/giz-logo.svg`** and is wired into the page, so the header shows a
logo out of the box.

To use the **official** GIZ asset instead (recommended for production /
brand compliance):

1. Put the official file at **`assets/giz-logo.png`**.
2. Change the `src` in `index.html`:
   ```html
   <img class="brand__logo" src="assets/giz-logo.png" alt="GIZ logo" ...>
   ```
3. If the referenced file is ever missing, the form shows a "GIZ logo goes
   here" placeholder instead of a broken image, so the page still works.

## Step 5 — Confirmation email (already set up — all-Google, no extra account)

**Nothing to do here.** The confirmation email is sent by the Apps Script
itself using Google's `MailApp`, from the Google account that owns the script.
It fires automatically after each submission is saved, warmly confirms the
place, restates the programme / start date (20 July 2026) / location (Abuja),
and promises batch-details follow-up. No EmailJS account, no extra keys.

> Quota note: `MailApp` sends up to ~100 emails/day on a free Gmail account
> (higher on Google Workspace). That's plenty for batch registration; if you
> expect more, use the EmailJS alternative below.

<details>
<summary><strong>Alternative — send the email via EmailJS instead</strong> (nicer templating, its own quota, but needs a separate account)</summary>

1. In `Code.gs`, comment out the `sendConfirmationEmail_(data);` call inside
   `doPost` (so Google doesn't also send an email), then **re-deploy** a new
   version.
2. Create a free account at <https://www.emailjs.com>, add an email service
   (e.g. Gmail) and copy the **Service ID**.
3. Create an email template using these **exact** variable names:

   | Variable        | What it holds                | Where to use it            |
   |-----------------|------------------------------|----------------------------|
   | `{{to_name}}`   | Registrant's full name       | Greeting                   |
   | `{{to_email}}`  | Registrant's email address   | **To** field of the template |
   | `{{programme}}` | "GIZ-ZME Remote Work Training Programme" | Body           |
   | `{{start_date}}`| "20 July 2026"               | Body                       |
   | `{{location}}`  | "Abuja"                      | Body                       |

   Set the template's **To** field to `{{to_email}}`.
4. Copy your **Public Key**, **Service ID**, and **Template ID** into
   `script.js`:
   ```js
   EMAILJS_PUBLIC_KEY:  "your_public_key",
   EMAILJS_SERVICE_ID:  "your_service_id",
   EMAILJS_TEMPLATE_ID: "your_template_id",
   ```
   The browser fires the EmailJS email only after a successful save.
</details>

## Step 6 — Publish to datalead.info

Upload these to your web host (same folder, keeping the structure):

```
index.html
styles.css
script.js
assets/giz-logo.png
```

- To make it your registration page, place them where you want the URL to be
  (e.g. `datalead.info/register/` → upload into a `/register/` folder).
- To **embed** in an existing page instead, host the files somewhere on the
  site and use an `<iframe src="…/index.html">`, or paste the `<form>` markup
  and include `styles.css` + `script.js`.
- `Code.gs` is **not** uploaded to your website — it lives inside Google.

**That's it.** Load the page, submit a test entry, and confirm (a) a new row
appears in your Sheet and (b) the confirmation email arrives.

---

## Privacy note (by design)

This form **never** asks for BVN, NIN, government ID, or bank details. Those
are handled in person during training — a public web form is the wrong place
for them. Please don't add fields for them.

## Anti-spam

A hidden "honeypot" field (`company_website`) is included. Real users never see
or fill it; bots often do. If it's filled, the submission is **silently
rejected** — nothing is saved and the bot sees a normal success screen.

---

## Quick reference — where each value goes

| Value                 | Comes from            | Goes into                                   |
|-----------------------|-----------------------|---------------------------------------------|
| Apps Script `/exec` URL | Step 3 (Deploy)     | `script.js` → `CONFIG.APPS_SCRIPT_URL` **(the only required value)** |
| Confirmation email    | Sent by the Apps Script (all-Google) | Nothing to configure        |
| GIZ logo image        | Ships as `assets/giz-logo.svg`; swap in official `assets/giz-logo.png` if desired | `index.html` `<img src>` |

*(EmailJS is optional — only if you switch to it per Step 5's collapsible
alternative.)*

## Customising the look

All theme colours and fonts are in **one place** — the `:root { … }` block at
the top of `styles.css`. Change `--cream`, `--forest`, `--teal`, `--gold`,
and the font variables to re-skin the whole page.
