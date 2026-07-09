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
 {ok:true}
   │
   ▼
 Browser fires EmailJS confirmation email  ──►  registrant's inbox
```

There are **two things you must configure** before it works:

1. The **Apps Script URL** (so submissions are saved). — Steps 1–3
2. **EmailJS** (so confirmation emails send). — Step 5
   *(or use Option B: send email from Apps Script instead — no EmailJS.)*

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

## Step 5 — Configure the confirmation email (EmailJS — the default)

EmailJS sends the confirmation email from the browser, right after the save
succeeds.

1. Create a free account at <https://www.emailjs.com>.
2. **Add an email service** (e.g. connect a Gmail account) →
   copy the **Service ID**.
3. **Create an email template** (Email Templates ▸ Create New Template).
   In the template, use these **exact variable names** (with double braces):

   | Variable        | What it holds                | Where to use it            |
   |-----------------|------------------------------|----------------------------|
   | `{{to_name}}`   | Registrant's full name       | Greeting                   |
   | `{{to_email}}`  | Registrant's email address   | **To** field of the template |
   | `{{programme}}` | "GIZ-ZME Remote Work Training Programme" | Body           |
   | `{{start_date}}`| "20 July 2026"               | Body                       |
   | `{{location}}`  | "Abuja"                      | Body                       |

   **Set the template's "To email" field to `{{to_email}}`.**

   Suggested template body (warm, restates the facts, promises follow-up):

   ```
   Subject: You're registered — {{programme}}

   Hi {{to_name}},

   Thank you for registering for the {{programme}}. Your place is confirmed.

   Here are the key details:
     • Start date: {{start_date}}
     • Location: {{location}}
     • Duration: 2 days per batch

   Our team will follow up shortly with your batch details.

   Warm regards,
   Data-Lead Africa (in partnership with GIZ-ZME)
   ```
4. Copy your **Public Key** (Account ▸ General ▸ API Keys), the **Service ID**,
   and the **Template ID**.

**➡ Paste all three into `script.js`:**

```js
EMAILJS_PUBLIC_KEY:  "your_public_key",
EMAILJS_SERVICE_ID:  "your_service_id",
EMAILJS_TEMPLATE_ID: "your_template_id",
```

> The confirmation email fires **only after** the submission is saved to the
> Sheet. If email fails, the registration is still saved (email is treated as
> non-fatal) and the registrant still sees the success screen.

### Option B — Skip EmailJS, send the email from Apps Script instead

Simpler and all-Google — no EmailJS account. The email is sent by the Google
account that owns the script (`MailApp`).

1. In `Code.gs`, **uncomment** the `sendConfirmationEmail_` function block at
   the bottom.
2. **Uncomment** the call inside `doPost`:
   ```js
   // sendConfirmationEmail_(data);   →   sendConfirmationEmail_(data);
   ```
3. **Re-deploy** the new version (Step 3's re-deploy note).
4. In `script.js`, **leave the EmailJS keys blank / as the `PASTE_…`
   placeholders** so the browser does **not** also send an email. The client
   detects the unconfigured keys and skips EmailJS automatically.

> Trade-offs: `MailApp` has a daily send quota (typically ~100/day on free
> Gmail, higher on Workspace) and emails come from your Google address.
> EmailJS gives you nicer templating and its own quota/branding.

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
| Apps Script `/exec` URL | Step 3 (Deploy)     | `script.js` → `CONFIG.APPS_SCRIPT_URL`      |
| EmailJS Public Key    | EmailJS ▸ Account     | `script.js` → `CONFIG.EMAILJS_PUBLIC_KEY`   |
| EmailJS Service ID    | EmailJS ▸ Services    | `script.js` → `CONFIG.EMAILJS_SERVICE_ID`   |
| EmailJS Template ID   | EmailJS ▸ Templates   | `script.js` → `CONFIG.EMAILJS_TEMPLATE_ID`  |
| GIZ logo image        | Ships as `assets/giz-logo.svg`; swap in official `assets/giz-logo.png` if desired | `index.html` `<img src>` |

## Customising the look

All theme colours and fonts are in **one place** — the `:root { … }` block at
the top of `styles.css`. Change `--cream`, `--forest`, `--teal`, `--gold`,
and the font variables to re-skin the whole page.
