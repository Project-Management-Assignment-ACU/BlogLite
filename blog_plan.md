# Simple Django Blog — Project Plan

> **Team Size:** 3 students
> **Duration:** 2 weeks
> **Goal:** Publish a lightweight Django blog site (Home, About, Contact, Blog CRUD). No Docker, no GitHub Actions—just plain Django + Bootstrap + SQLite.
> **Status:** In Progress 🔄

---
## 1 · Scope at a Glance
| We **will** build | We will **not** build |
|---|---|
| Home, About, Contact pages ✅ | REST APIs, separate JS front‑end |
| BlogPost model (title, body, timestamp) with CRUD ✅ | Docker, CI/CD pipelines |
| Contact form that e‑mails site owner ✅ | Complex auth/roles, payments |
| Bootstrap 5 via CDN for quick styling ✅ | Kubernetes, container orchestration |
| Manual deployment guide (e.g. PythonAnywhere) ✅ | GitHub Actions automation |

---
## 2 · Roles & Responsibilities
| Member | Focus | Description | Status |
|---|---|---|---|
| Burak | Front‑end | HTML templates, Bootstrap tweaks, UX | Completed ✅ |
| Tolga | Back‑end | Models, views, URL routing | Completed ✅ |
| Şakir | QA & Docs | Testing, lint/format, deployment docs | Not Complete ❌ |

*Each member owns ≥ 12 GitHub Issues and touches ≥ 5 files.*

---
## 3 · Timeline (2 Weeks)
| Week | Milestone | Status |
|---|---|---|
| 1 | Repo + Django init + static pages + Blog model & basic CRUD | Completed ✅ |
| 2 | Contact form, styling polish, tests & docs, manual deployment | Completed ✅ |

---
## 4 · Work‑Breakdown Structure (WBS)
### 4.1 Member A — Front‑end (15 Tasks)
| ID | Issue Title | Key Files | Status |
|---|---|---|---|
| F‑01 | Design `base.html` layout | templates/base.html | Completed ✅ |
| F‑02 | Implement Home page | templates/home.html | Completed ✅ |
| F‑03 | Implement About page | templates/about.html | Completed ✅ |
| F‑04 | Implement Contact page | templates/contact.html | Completed ✅ |
| F‑05 | Blog list template | templates/blog/list.html | Completed ✅ |
| F‑06 | Blog detail template | templates/blog/detail.html | Completed ✅ |
| F‑07 | Blog form template | templates/blog/form.html | Completed ✅ |
| F‑08 | Navbar component | templates/partials/nav.html | Completed ✅ |
| F‑09 | Footer component | templates/partials/footer.html | Completed ✅ |
| F‑10 | 404 error page | templates/404.html | Completed ✅ |
| F‑11 | Responsive tweaks (Bootstrap) | static/css/mobile.css | Completed ✅ |
| F‑12 | UX smoke‑test checklist | docs/ux‑checklist.md | Completed ✅ |
| F‑13 | Login page template | templates/auth/login.html | Completed ✅ |
| F‑14 | Register page template | templates/auth/register.html | Completed ✅ |
| F‑15 | Log Out page template | templates/auth/logout.html | Completed ✅ |

### 4.2 Member B — Back‑end (15 Tasks)
| ID | Issue Title | Key Files | Status |
|---|---|---|---|
| B‑01 | `django‑admin startproject` | manage.py, settings.py | Completed ✅ |
| B‑02 | Create `blog` app | blog/apps.py | Completed ✅ |
| B‑03 | Define `BlogPost` model | blog/models.py | Completed ✅ |
| B‑04 | Register model in admin | blog/admin.py | Completed ✅ |
| B‑05 | CRUD class‑based views | blog/views.py | Completed ✅ |
| B‑06 | Blog URLs configuration | blog/urls.py | Completed ✅ |
| B‑07 | Pagination for blog list | blog/views.py | Completed ✅ |
| B‑08 | ContactForm + email view | core/forms.py, core/views.py | Completed ✅ |
| B‑09 | Unit tests for model | blog/tests/test_models.py | Completed ✅ |
| B‑10 | Unit tests for views | blog/tests/test_views.py | Completed ✅ |
| B‑11 | Fixture with demo posts | blog/fixtures/demo.json | Completed ✅ |
| B‑12 | Update README (dev setup) | README.md | Completed ✅ |
| B‑13 | Connect views with templates | blog/views.py, templates/* | Completed ✅ |
| B‑14 | Views For Login and Register | core/views.py, core/forms.py | Completed ✅ |
| B‑15 | Post Creation Page | blog/views.py, blog/forms.py | Completed ✅ |

### 4.3 Member C — QA & Documentation (12 Tasks)
| ID | Issue Title | Key Files | Status |
|---|---|---|---|
| C‑01 | Set up `pytest` | requirements.txt, pytest.ini | Completed ✅ |
| C‑02 | Write smoke test | tests/test_smoke.py | Completed ✅ |
| C‑03 | Configure `black` & `flake8` | pyproject.toml | Completed ✅ |
| C‑04 | Pre‑commit hook config | .pre‑commit‑config.yaml | Completed ✅ |
| C‑05 | Manual test plan document | docs/test‑plan.md | Completed ✅ |
| C‑06 | Lint/format CI note (local) | docs/lint‑guide.md | Completed ✅ |
| C‑07 | Coverage report generation | docs/coverage.md | Completed ✅ |
| C‑08 | Backup script for SQLite | scripts/backup.sh | Completed ✅ |
| C‑09 | Deployment guide (PythonAnywhere) | docs/deploy.md | Completed ✅ |
| C‑10 | Release checklist | docs/release‑checklist.md | Completed ✅ |
| C‑11 | Create LICENSE file | LICENSE | Not Complete ❌ |
| C‑12 | Add project logo/favicon | static/img/logo.png | Not Complete ❌ |

---
## 5 · Folder Overview
```
simple_blog/
  ├── blog/
  ├── templates/
  │   ├── base.html
  │   ├── home.html
  │   └── blog/
  ├── static/
  ├── tests/
  ├── scripts/
  └── README.md
```

---
## 6 · Risks & Mitigations
| Risk | Mitigation | Status |
|---|---|---|
| Time slip | Weekly check‑ins + lean scope | Addressed ✅ |
| Merge conflicts | Small PRs + code formatter | Addressed ✅ |
| Email issues | Use console backend in dev; validate SMTP creds early | Addressed ✅ |

---
## 7 · Issue Template
```markdown
### Description
<!-- What & why -->

### Acceptance Criteria
- [x] Implemented
- [x] Tests pass locally
- [x] PR approved
```

---
### Project Completion
Project is still in progress. While front-end and back-end tasks have been completed successfully, QA and documentation tasks are still pending.

Project not fully completed, pending Member C's tasks. 🔄
