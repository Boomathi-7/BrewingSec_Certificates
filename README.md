# BrewingSec CyberDev Summit '26 Certificate Generator System

Flask-based web application that generates participant certificates from a fixed high-resolution template (`static/certificate_template.png`), uploads certificates to GitHub, embeds verification links, formats participant & institution names with a Pro UI formatter, and dispatches certificates via email.

---

##  Key Features

- **Pro UI Name & College Formatter (`formatter.py`)**:
  - **Participant Name Casing**: Auto title-cases names (`varshini s` &rarr; `Varshini S`), handles single-letter & dotted initials (`m.` &rarr; `M.`), hyphenated names (`Mary-Jane`), apostrophes (`O'Connor`), and Roman numerals (`III`).
  - **Institutional Acronym & Casing Rules**: Preserves recognized acronyms (`KGiSL`, `KITE`, `PSG`, `IIT`, `NIT`, `SKCET`, `SASTRA`, `MIT`, etc.), keeps connecting prepositions (`of`, `and`, `for`, `in`, `at`, `the`) lowercase inside names (`kgisl institute of technology` &rarr; `KGiSL Institute of Technology`), and expands shorthand (`tech.` &rarr; `Technology`, `inst.` &rarr; `Institute`).
  - **College Line Prefix**: Automatically prefixes college lines with `From : ` (e.g., `From : KGiSL Institute of Technology`).
- **Precision Certificate Layout Engine (`generator.py`)**:
  - **Participant Name**: Centered **ABOVE** the green horizontal line accent with 60px vertical clearance (`Y = 523`).
  - **College Name**: Centered **BELOW** the green horizontal line accent with `From : ` prefix (`Y = 704`).
  - **Bounding Box & Auto-Fitting**: Constrained to 68% image width with dynamic font scaling to prevent overflow or side collisions.
- **Modern Web Interface (`templates/form.html`)**:
  - Styled with Google Fonts (`Inter` & `Outfit`) and glassmorphic card design.
  - Real-time client-side live auto-formatting badge showing formatted title casing as you type.
  - Live Certificate Preview Card displaying instant formatted output.
  - Quick-fill institution chips (`KGiSL Tech`, `PSG Tech`, `SKCET`, `Amrita`).
  - Integrated drag & drop file upload and webcam snapshot capture.
- **Automated Cloud Integration**:
  - GitHub REST API integration for certificate PDF uploads (`github_upload.py`).
  - Verification link generation with fallback local inline serving (`app.py`).
  - Email delivery using Gmail SMTP with PDF attachments (`email_sender.py`).
  - Environment-based configuration with `.env` file support.

---

##  Project Structure

```
BrewingSec_Certificates/
├── app.py                          # Flask web application & routes
├── formatter.py                    # Pro UI Name & College formatting engine
├── generator.py                    # Certificate image rendering & PDF generator
├── github_upload.py                # GitHub REST API upload integration
├── email_sender.py                 # Gmail SMTP email delivery logic
├── render.yaml                     # Render cloud deployment blueprint
├── requirements.txt                # Python package dependencies
├── .env                            # Environment variables (DO NOT COMMIT)
├── .env.example                    # Example environment template
├── .gitignore                      # Git ignore rules
│
├── certificates/                   # Generated output PDF certificates
├── uploads/                        # Temporary participant photo uploads
│
├── static/
│   ├── certificate_template.png    # Summit '26 Certificate Template (2000x1414)
│   └── fonts/
│       ├── PlayfairDisplay-Bold.ttf # Header font for Participant Name
│       └── PlayfairDisplay-Regular.ttf # Body font for College Name
│
└── templates/
    ├── form.html                   # Certificate request form with live preview
    └── success.html                # Success confirmation dashboard
```

---

##  Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Flask Configuration
FLASK_SECRET_KEY=dev-secret-key-change-in-production

# GitHub Configuration
GITHUB_TOKEN=ghp_your_personal_access_token_here
GITHUB_REPO=Boomathi-7/BrewingSec_Certificates
GITHUB_BRANCH=main
GITHUB_CERT_FOLDER=generated-certificates

# SMTP Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

### 3. GitHub Personal Access Token Setup

1. Go to [GitHub Developer Settings > Personal Access Tokens](https://github.com/settings/tokens).
2. Click **Generate new token (classic)**.
3. Select scope:
   - `repo` (Full control of private repositories).
4. Copy the token (starts with `ghp_`).
5. Add to `.env` as `GITHUB_TOKEN`.

### 4. Gmail App Password Setup (For Email Delivery)

1. Enable 2-Factor Authentication on your Google Account.
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Generate an App Password for **Mail**.
4. Set `MAIL_USERNAME` to your email address and `MAIL_PASSWORD` to the 16-character App Password in `.env`.

---

## 💻 Running Locally

```bash
python app.py
```

The application will be accessible at:
- **Local**: http://127.0.0.1:5000/
- **Network**: http://<your-ip>:5000/

---

## 📐 Layout Geometry Reference

The certificate template (`static/certificate_template.png`) is **2000 &times; 1414 pixels**:

| Element | Vertical Position (Y) | Description |
| :--- | :--- | :--- |
| **`PRESENTED TO` Header** | Y = 435 – 465 | Printed on template image |
| **Participant Name** | **Y = 523** | **Above Green Line** (`int(img_height * 0.370)`) |
| **Green Accent Line** | **Y = 644** | Printed horizontal line accent |
| **College / Institution** | **Y = 704** | **Below Green Line** (`From : <College Name>`, `int(img_height * 0.498)`) |
| **`FOR COMPLETING...` Footer**| Y = 800 – 875 | Printed on template image |

---

##  Security Notes

- **Never commit `.env`** — It contains sensitive tokens.
- **Use strong `FLASK_SECRET_KEY`** in production environments.
- **`.gitignore`** is configured to ignore `.env`, temporary uploads, and generated certificates.
