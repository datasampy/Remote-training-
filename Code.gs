/**
 * GIZ-ZME Remote Work Training Programme — registration backend.
 *
 * Deploy this as a Web App:
 *   Deploy ▸ New deployment ▸ Type: Web app
 *     Execute as:     Me
 *     Who has access: Anyone
 *   Copy the /exec URL and paste it into script.js → CONFIG.APPS_SCRIPT_URL
 *
 * What it does:
 *   - doPost(e) receives the JSON body from the form.
 *   - Writes the header row on first run (if the sheet is empty).
 *   - Appends each submission as a new row.
 *   - Returns {ok:true} as plain text (no CORS headers needed because the
 *     form posts with Content-Type: text/plain;charset=utf-8).
 *
 * OPTION B (all-Google email): uncomment sendConfirmationEmail_() below and
 * the call to it inside doPost. Then leave the EmailJS keys blank in
 * script.js so the client does NOT also send an email. See README.
 */

// Column order for the sheet. Keep in sync with the header + row builder.
var FIELDS = [
  'submittedAt',
  'fullName',
  'gender',
  'phone',
  'email',
  'state',
  'describe',
  'occupation',
  'education',
  'experience',
  'freelanceBefore',
  'platforms',
  'digitalComfort',
  'devices',
  'internet',
  'consent'
];

var HEADERS = [
  'Timestamp',
  'Full name',
  'Gender',
  'Phone (WhatsApp)',
  'Email',
  'State of residence',
  'Best describes you',
  'Occupation / field',
  'Highest education',
  'Experience in',
  'Freelanced before?',
  'Platforms used',
  'Digital comfort',
  'Devices',
  'Internet reliability',
  'Consent'
];

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(30000); // avoid two submissions racing on the same row

    var data = JSON.parse(e.postData.contents);

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];

    // First run on an empty sheet → write the header row.
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
    }

    // Build the row in the fixed FIELDS order.
    var row = FIELDS.map(function (key) {
      var val = data[key];
      return val === undefined || val === null ? '' : val;
    });
    sheet.appendRow(row);

    // ---- OPTION B: send the confirmation email from here instead of
    // EmailJS. Uncomment the next line (and the function below). ----
    // sendConfirmationEmail_(data);

    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// Simple GET so you can eyeball that the deployment is live in a browser.
function doGet() {
  return json_({ ok: true, service: 'GIZ-ZME registration', ready: true });
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ================================================================
   OPTION B — Confirmation email straight from Google (MailApp).
   No EmailJS account needed. To use:
     1. Uncomment this whole function.
     2. Uncomment the sendConfirmationEmail_(data) call in doPost.
     3. Leave the EmailJS keys blank in script.js.
   MailApp sends from the Google account that owns this script.
   ================================================================ */
/*
function sendConfirmationEmail_(data) {
  if (!data.email) return;

  var programme = 'GIZ-ZME Remote Work Training Programme';
  var startDate = '20 July 2026';
  var location  = 'Abuja';
  var name      = data.fullName || 'there';

  var subject = 'You’re registered — ' + programme;

  var body =
    'Hi ' + name + ',\n\n' +
    'Thank you for registering for the ' + programme + '.\n\n' +
    'Your place is confirmed. Here are the key details:\n' +
    '  • Start date: ' + startDate + '\n' +
    '  • Location: ' + location + '\n' +
    '  • Duration: 2 days per batch\n\n' +
    'Our team will follow up with your batch details shortly.\n\n' +
    'Warm regards,\n' +
    'Data-Lead Africa (in partnership with GIZ-ZME)';

  var htmlBody =
    '<p>Hi ' + name + ',</p>' +
    '<p>Thank you for registering for the <strong>' + programme + '</strong>.</p>' +
    '<p>Your place is confirmed. Here are the key details:</p>' +
    '<ul>' +
      '<li><strong>Start date:</strong> ' + startDate + '</li>' +
      '<li><strong>Location:</strong> ' + location + '</li>' +
      '<li><strong>Duration:</strong> 2 days per batch</li>' +
    '</ul>' +
    '<p>Our team will follow up with your batch details shortly.</p>' +
    '<p>Warm regards,<br>Data-Lead Africa (in partnership with GIZ-ZME)</p>';

  MailApp.sendEmail({
    to: data.email,
    subject: subject,
    body: body,
    htmlBody: htmlBody,
    name: 'Data-Lead Africa'
  });
}
*/
