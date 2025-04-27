# Simple Django Blog — Project Plan

> **Team Size:** 3 students  
> **Duration:** 2 weeks  
> **Goal:** Publish a lightweight Django blog site (Home, About, Contact, Blog CRUD). No Docker, no GitHub Actions—just plain Django + Bootstrap + SQLite.

---
## 1 · Scope at a Glance
| We **will** build | We will **not** build |
|---|---|
| Home, About, Contact pages | REST APIs, separate JS front‑end |
| BlogPost model (title, body, timestamp) with CRUD | Docker, CI/CD pipelines |
| Contact form that e‑mails site owner | Complex auth/roles, payments |
| Bootstrap 5 via CDN for quick styling | Kubernetes, container orchestration |
| Manual deployment guide (e.g. PythonAnywhere) | GitHub Actions automation |

---
## 2 · Roles & Responsibilities
| Member | Focus | Description |
|---|---|---|
| **Member A** | Front‑end | HTML templates, Bootstrap tweaks, UX |
| **Member B** | Back‑end | Models, views, URL routing |
| **Member C** | QA & Docs | Testing, lint/format, deployment docs |

*Each member owns ≥ 12 GitHub Issues and touches ≥ 5 files.*

---
## 3 · Timeline (2 Weeks)
| Week | Milestone |
|---|---|
| 1 | Repo + Django init + static pages + Blog model & basic CRUD |
| 2 | Contact form, styling polish, tests & docs, manual deployment |

---
## 4 · Work‑Breakdown Structure (WBS)
### 4.1 Member A — Front‑end (14 Tasks)
| ID | Issue Title | Key Files |
|---|---|---|
| F‑01 | Design `base.html` layout | templates/base.html |
| F‑02 | Implement Home page | templates/home.html |
| F‑03 | Implement About page | templates/about.html |
| F‑04 | Implement Contact page | templates/contact.html |
| F‑05 | Blog list template | templates/blog/list.html |
| F‑06 | Blog detail template | templates/blog/detail.html |
| F‑07 | Blog form template | templates/blog/form.html |
| F‑08 | Navbar component | templates/partials/nav.html |
| F‑09 | Footer component | templates/partials/footer.html |
| F‑10 | 404 error page | templates/404.html |
| F‑11 | Responsive tweaks (Bootstrap) | static/css/mobile.css |
| F‑12 | UX smoke‑test checklist | docs/ux‑checklist.md |
| F‑13 | Login page template | templates/auth/login.html |
| F‑14 | Register page template | templates/auth/register.html |

### 4.2 Member B — Back‑end (14 Tasks)
| ID | Issue Title | Key Files |
|---|---|---|
| B‑01 | `django‑admin startproject` | manage.py, settings.py |
| B‑02 | Create `blog` app | blog/apps.py |
| B‑03 | Define `BlogPost` model | blog/models.py |
| B‑04 | Register model in admin | blog/admin.py |
| B‑05 | CRUD class‑based views | blog/views.py |
| B‑06 | Blog URLs configuration | blog/urls.py |
| B‑07 | Pagination for blog list | blog/views.py |
| B‑08 | ContactForm + email view | core/forms.py, core/views.py |
| B‑09 | Unit tests for model | blog/tests/test_models.py |
| B‑10 | Unit tests for views | blog/tests/test_views.py |
| B‑11 | Fixture with demo posts | blog/fixtures/demo.json |
| B‑12 | Update README (dev setup) | README.md |
| B‑13 | Connect views with templates | blog/views.py, templates/* |
| B‑14 | Views For Login and Register | core/views.py, core/forms.py |

### 4.3 Member C — QA & Documentation (12 Tasks)
| ID | Issue Title | Key Files |
|---|---|---|
| C‑01 | Set up `pytest` | requirements.txt, pytest.ini |
| C‑02 | Write smoke test | tests/test_smoke.py |
| C‑03 | Configure `black` & `flake8` | pyproject.toml |
| C‑04 | Pre‑commit hook config | .pre‑commit‑config.yaml |
| C‑05 | Manual test plan document | docs/test‑plan.md |
| C‑06 | Lint/format CI note (local) | docs/lint‑guide.md |
| C‑07 | Coverage report generation | docs/coverage.md |
| C‑08 | Backup script for SQLite | scripts/backup.sh |
| C‑09 | Deployment guide (PythonAnywhere) | docs/deploy.md |
| C‑10 | Release checklist | docs/release‑checklist.md |
| C‑11 | Create LICENSE file | LICENSE |
| C‑12 | Add project logo/favicon | static/img/logo.png |

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
| Risk | Mitigation |
|---|---|
| Time slip | Weekly check‑ins + lean scope |
| Merge conflicts | Small PRs + code formatter |
| Email issues | Use console backend in dev; validate SMTP creds early |

---
## 7 · Issue Template
```markdown
### Description
<!-- What & why -->

### Acceptance Criteria
- [ ] Implemented
- [ ] Tests pass locally
- [ ] PR approved
```

---
### Next Steps
1. Replace **Member A/B/C** with real names.  
2. Create 39 GitHub Issues from WBS and organise them on a Kanban board.  
3. Start Week‑1 tasks: repo → Django init → basic pages.

Happy coding! 🎉
