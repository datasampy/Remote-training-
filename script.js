/* ================================================================
   GIZ-ZME Remote Work Training Programme — Registration logic
   Vanilla JS. No framework.

   ┌────────────────────────────────────────────────────────────┐
   │  CONFIG — FILL THESE IN. This is the ONLY place secrets/URLs │
   │  live. See README.md for exactly where each value comes from.│
   └────────────────────────────────────────────────────────────┘
   ================================================================ */
const CONFIG = {
  // (1) Google Apps Script Web App URL.
  //     Deploy Code.gs as a Web App (Execute as = Me, Access = Anyone),
  //     then paste the /exec URL here.
  APPS_SCRIPT_URL: "PASTE_YOUR_APPS_SCRIPT_WEB_APP_URL_HERE",

  // (2) EmailJS — client-side confirmation email (ACTIVE DEFAULT).
  //     From your EmailJS dashboard. Leave blank to disable EmailJS
  //     (e.g. if you use Option B: MailApp inside Code.gs instead).
  EMAILJS_PUBLIC_KEY: "PASTE_YOUR_EMAILJS_PUBLIC_KEY_HERE",
  EMAILJS_SERVICE_ID: "PASTE_YOUR_EMAILJS_SERVICE_ID_HERE",
  EMAILJS_TEMPLATE_ID: "PASTE_YOUR_EMAILJS_TEMPLATE_ID_HERE",

  // Programme facts used in the confirmation email (rarely change).
  PROGRAMME_NAME: "GIZ-ZME Remote Work Training Programme",
  START_DATE: "20 July 2026",
  LOCATION: "Abuja",
};

/* ================================================================
   Boot
   ================================================================ */
document.addEventListener("DOMContentLoaded", () => {
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Initialise EmailJS if a public key was provided.
  if (
    window.emailjs &&
    CONFIG.EMAILJS_PUBLIC_KEY &&
    !CONFIG.EMAILJS_PUBLIC_KEY.startsWith("PASTE_")
  ) {
    emailjs.init({ publicKey: CONFIG.EMAILJS_PUBLIC_KEY });
  }

  wireValidation();
  wireProgress();

  document
    .getElementById("registration-form")
    .addEventListener("submit", handleSubmit);
});

/* ================================================================
   Validation
   ================================================================ */

// Map of validators. Each returns "" when valid, else an error string.
const VALIDATORS = {
  fullName: (f) =>
    getText(f, "fullName") ? "" : "Please enter your full name.",
  gender: (f) =>
    getRadio(f, "gender") ? "" : "Please select an option.",
  phone: (f) => {
    const v = getText(f, "phone");
    if (!v) return "Please enter your phone number.";
    // Accept digits, spaces, +, -, () — need at least 7 digits.
    const digits = v.replace(/[^0-9]/g, "");
    if (!/^[0-9+()\-\s]+$/.test(v) || digits.length < 7)
      return "Please enter a valid phone number.";
    return "";
  },
  email: (f) => {
    const v = getText(f, "email");
    if (!v) return "Please enter your email address.";
    // Pragmatic email pattern.
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v))
      return "Please enter a valid email address.";
    return "";
  },
  state: (f) =>
    getText(f, "state") ? "" : "Please select your state of residence.",
  describe: (f) =>
    getRadio(f, "describe") ? "" : "Please select an option.",
  freelanceBefore: (f) =>
    getRadio(f, "freelanceBefore") ? "" : "Please select Yes or No.",
  digitalComfort: (f) =>
    getRadio(f, "digitalComfort") ? "" : "Please select your comfort level.",
  devices: (f) =>
    getChecked(f, "devices").length
      ? ""
      : "Please select at least one device.",
  consent: (f) =>
    f.consent.checked ? "" : "You must consent to continue.",
};

// Which error element belongs to which field.
const ERROR_IDS = {
  fullName: "fullName-err",
  gender: "gender-err",
  phone: "phone-err",
  email: "email-err",
  state: "state-err",
  describe: "describe-err",
  freelanceBefore: "freelance-err",
  digitalComfort: "comfort-err",
  devices: "devices-err",
  consent: "consent-err",
};

function validateField(form, name) {
  const validator = VALIDATORS[name];
  if (!validator) return true;
  const msg = validator(form);
  showError(name, msg);
  markInvalid(form, name, !!msg);
  return !msg;
}

function validateAll(form) {
  let firstInvalid = null;
  for (const name of Object.keys(VALIDATORS)) {
    const ok = validateField(form, name);
    if (!ok && !firstInvalid) firstInvalid = name;
  }
  return firstInvalid;
}

function wireValidation() {
  const form = document.getElementById("registration-form");
  for (const name of Object.keys(VALIDATORS)) {
    const els = form.elements[name];
    if (!els) continue;
    const list = els.length ? Array.from(els) : [els];
    list.forEach((el) => {
      const evt = el.type === "radio" || el.type === "checkbox" ? "change" : "blur";
      el.addEventListener(evt, () => validateField(form, name));
    });
  }
}

/* ================================================================
   Progress indicator (fills as required sections get completed)
   ================================================================ */
const SECTION_REQUIRED = {
  1: ["fullName", "gender", "phone", "email", "state"],
  2: ["describe"],
  3: ["freelanceBefore"],
  4: ["digitalComfort", "devices"],
  5: ["consent"],
};

function isSectionComplete(form, fields) {
  return fields.every((name) => VALIDATORS[name] && VALIDATORS[name](form) === "");
}

function updateProgress() {
  const form = document.getElementById("registration-form");
  let done = 0;
  for (const key of Object.keys(SECTION_REQUIRED)) {
    if (isSectionComplete(form, SECTION_REQUIRED[key])) done++;
  }
  const pct = (done / 5) * 100;
  document.getElementById("progressFill").style.width = pct + "%";
  document.getElementById("progressCount").textContent = done;
}

function wireProgress() {
  const form = document.getElementById("registration-form");
  form.addEventListener("input", updateProgress);
  form.addEventListener("change", updateProgress);
  updateProgress();
}

/* ================================================================
   Submit flow: validate → save to Sheet → send email → success
   ================================================================ */
async function handleSubmit(e) {
  e.preventDefault();
  const form = e.currentTarget;

  // --- Honeypot: if filled, silently reject (pretend success to bot). ---
  if (form.company_website && form.company_website.value.trim() !== "") {
    showSuccess(); // silent — bot thinks it worked, nothing is saved.
    return;
  }

  clearFormError();

  const firstInvalid = validateAll(form);
  if (firstInvalid) {
    showFormError("Please fix the highlighted fields and try again.");
    focusField(form, firstInvalid);
    return;
  }

  const payload = collectData(form);

  setLoading(true);
  try {
    // (1) Save to Google Sheet via Apps Script.
    await saveToSheet(payload);

    // (2) Fire confirmation email (EmailJS default). Non-fatal on failure.
    await sendConfirmationEmail(payload);

    // (3) Success screen.
    showSuccess();
  } catch (err) {
    console.error(err);
    setLoading(false);
    showFormError(
      "Sorry — we couldn't submit your registration. Please check your internet connection and try again. Your answers are still here."
    );
  }
}

function collectData(form) {
  return {
    fullName: getText(form, "fullName"),
    gender: getRadio(form, "gender"),
    phone: getText(form, "phone"),
    email: getText(form, "email"),
    state: getText(form, "state"),
    describe: getRadio(form, "describe"),
    occupation: getText(form, "occupation"),
    education: getRadio(form, "education"),
    experience: getChecked(form, "experience").join(", "),
    freelanceBefore: getRadio(form, "freelanceBefore"),
    platforms: getChecked(form, "platforms").join(", "),
    digitalComfort: getRadio(form, "digitalComfort"),
    devices: getChecked(form, "devices").join(", "),
    internet: getRadio(form, "internet"),
    consent: form.consent.checked ? "Yes" : "No",
    submittedAt: new Date().toISOString(),
  };
}

/* ----- (1) Save to Google Sheet -----
   CORS gotcha: post as a JSON *string* with text/plain content type so
   Apps Script accepts it without needing to return CORS headers. */
async function saveToSheet(payload) {
  if (!CONFIG.APPS_SCRIPT_URL || CONFIG.APPS_SCRIPT_URL.startsWith("PASTE_")) {
    throw new Error("APPS_SCRIPT_URL is not configured.");
  }
  const res = await fetch(CONFIG.APPS_SCRIPT_URL, {
    method: "POST",
    headers: { "Content-Type": "text/plain;charset=utf-8" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Sheet save failed: HTTP " + res.status);
  // Apps Script returns {ok:true}. Parse defensively.
  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error("Sheet save returned an unexpected response.");
  }
  if (!data || data.ok !== true) {
    throw new Error("Sheet save reported failure.");
  }
  return data;
}

/* ----- (2) Confirmation email -----
   PRIMARY: EmailJS (client-side).
   OPTION B: send from Apps Script (MailApp) — then leave the EmailJS
   config blank and this becomes a no-op. See README for the hook. */
async function sendConfirmationEmail(payload) {
  const configured =
    window.emailjs &&
    CONFIG.EMAILJS_PUBLIC_KEY &&
    CONFIG.EMAILJS_SERVICE_ID &&
    CONFIG.EMAILJS_TEMPLATE_ID &&
    !CONFIG.EMAILJS_PUBLIC_KEY.startsWith("PASTE_") &&
    !CONFIG.EMAILJS_SERVICE_ID.startsWith("PASTE_") &&
    !CONFIG.EMAILJS_TEMPLATE_ID.startsWith("PASTE_");

  if (!configured) {
    // EmailJS not set up. If you use Option B (MailApp), the email is
    // already sent by Apps Script — so we just skip here silently.
    return;
  }

  const templateParams = {
    to_name: payload.fullName,
    to_email: payload.email,
    programme: CONFIG.PROGRAMME_NAME,
    start_date: CONFIG.START_DATE,
    location: CONFIG.LOCATION,
  };

  try {
    await emailjs.send(
      CONFIG.EMAILJS_SERVICE_ID,
      CONFIG.EMAILJS_TEMPLATE_ID,
      templateParams
    );
  } catch (err) {
    // Email is a nice-to-have; the registration is already saved.
    // Don't fail the whole submission just because email didn't send.
    console.warn("Confirmation email failed to send:", err);
  }
}

/* ================================================================
   UI helpers
   ================================================================ */
function setLoading(isLoading) {
  const btn = document.getElementById("submitBtn");
  btn.disabled = isLoading;
  btn.classList.toggle("is-loading", isLoading);
  btn.querySelector(".btn__label").textContent = isLoading
    ? "Submitting…"
    : "Submit registration";
}

function showSuccess() {
  document.getElementById("registration-form").hidden = true;
  document.querySelector(".overview").hidden = true;
  document.querySelector(".progress").hidden = true;
  const s = document.getElementById("successScreen");
  s.hidden = false;
  s.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showError(name, msg) {
  const el = document.getElementById(ERROR_IDS[name]);
  if (el) el.textContent = msg;
}

function markInvalid(form, name, invalid) {
  const els = form.elements[name];
  if (!els) return;
  const list = els.length ? Array.from(els) : [els];
  list.forEach((el) => {
    if (invalid) el.setAttribute("aria-invalid", "true");
    else el.removeAttribute("aria-invalid");
  });
}

function focusField(form, name) {
  const els = form.elements[name];
  if (!els) return;
  const el = els.length ? els[0] : els;
  if (el && el.focus) el.focus();
}

function showFormError(msg) {
  const el = document.getElementById("formError");
  el.textContent = msg;
  el.hidden = false;
}
function clearFormError() {
  const el = document.getElementById("formError");
  el.textContent = "";
  el.hidden = true;
}

/* ----- tiny form-value getters ----- */
function getText(form, name) {
  const el = form.elements[name];
  return el ? el.value.trim() : "";
}
function getRadio(form, name) {
  const els = form.elements[name];
  if (!els) return "";
  const list = els.length ? Array.from(els) : [els];
  const checked = list.find((el) => el.checked);
  return checked ? checked.value : "";
}
function getChecked(form, name) {
  const els = form.elements[name];
  if (!els) return [];
  const list = els.length ? Array.from(els) : [els];
  return list.filter((el) => el.checked).map((el) => el.value);
}
