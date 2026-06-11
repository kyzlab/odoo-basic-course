<div align="center">

# 🐾 Odoo Basic Course

**Solution code for each chapter — Odoo 19 · Python · OWL**

![Odoo](https://img.shields.io/badge/Odoo-19.0-875A7B?style=flat-square&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3.0-blue?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

</div>

## What is this?

This repository contains the **complete solution code** for each chapter of the *Odoo Basic Course* — a structured learning path for developers who are new to Odoo 19. Each chapter folder is a self-contained, runnable snapshot of the `petshop` addon at that stage of the course.

The running example throughout the course is **petshop** — a Pet Shop management addon built from scratch, growing chapter by chapter until it becomes a full-featured Odoo module.

## 📚 Course Outline

| Chapter | Topic | What you build |
|:-------:|:------|:--------------|
| **I** | Overview | Set up Odoo 19 with Docker · understand MVC architecture · install and update addons |
| **II** | Model | Create the `petshop` addon · define models and fields · relational fields (Many2one, One2many, Many2many) · computed fields · `@api` decorators · Wizard |
| **III** | View | List & Form views · Kanban (Odoo 19 `t-name="card"`) · Search / Filter / Group By · Graph & Pivot views |
| **IV** | Controller | HTTP Controller · REST API · JSON-RPC · JSON-2 API (Odoo 19) |
| **V** | Inheritance | Extend `petshop` with `petshop_plus` · Class / Prototype / Delegation model inheritance · View inheritance with `xpath` · Controller override |
| **VI** | Frontend | OWL components · custom widget `Counter` · custom widget `MyTable` · server-side calls via ORM service |
| **VII** | Other Technical & Production | Access control (groups & rules) · PDF/HTML reports · Email integration · Scheduled actions (Cron) · SQL queries · Database backup · CI/CD with Jenkins |
| **VIII** | Vibe Coding | Build Odoo addons assisted by AI — prompting patterns, review, iteration |

## 🗂 Repository Structure

Each chapter folder follows the same structure so you can spin it up immediately with Docker Compose:

```
odoo-basic-course/
├── I-Overview/
│   ├── addons/          ← Odoo addons for this chapter
│   ├── etc/
│   │   └── odoo.conf    ← Odoo server configuration
│   ├── docker-compose.yml
│   └── postgresql/
├── II-Model/
│   ├── addons/
│   │   ├── petshop/     ← Main addon (grows each chapter)
│   │   └── zoo/         ← Practice addon
│   ├── etc/
│   ├── docker-compose.yml
│   └── postgresql/
├── III-View/
├── IV-Controller/
├── V-Inheritance/       ← Includes petshop_plus extension module
├── VI-Frontend/
├── VII-Other Technical & Production/
└── VIII-Vibe Coding/
```

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Run a chapter

Pick any chapter and run it locally in minutes:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/odoo-basic-course.git
cd odoo-basic-course

# 2. Enter the chapter you want to study
cd II-Model/

# 3. Start Odoo + PostgreSQL
docker compose up -d

# 4. Open in browser
#    http://localhost:10019
#    Default credentials: admin / admin
```

> Each chapter uses **port 10019** by default. Stop one chapter before starting another to avoid port conflicts.

## 🧩 The petshop Addon

The core of this course is the `petshop` addon — a Pet Shop management system. Here is how it evolves across chapters:

| Chapter | petshop state |
|:-------:|:-------------|
| II | Models defined: `petshop.pet`, `petshop.species`, `petshop.cage`, `petshop.pet.meal` |
| III | Full UI: list, form, kanban, search views · action windows · menus |
| IV | REST API endpoints · JSON-2 API integration |
| V | Extended by `petshop_plus` using all 3 inheritance types |
| VI | Custom OWL widgets embedded in form view |
| VII | Access control · PDF reports · email · cron jobs · CI/CD |

## 🛠 Tech Stack

| Layer | Technology |
|:------|:-----------|
| Platform | [Odoo 19](https://github.com/odoo/odoo) |
| Backend | Python 3.10+ · Odoo ORM |
| Frontend | [OWL](https://github.com/odoo/owl) (Odoo Web Library) · QWeb templates |
| Database | PostgreSQL 18 |
| Infrastructure | Docker · Docker Compose |

## 📄 License

This project is licensed under the [LGPL-3.0 License](LICENSE).

<div align="center">

Made with ❤️ for the Odoo developer community

</div>
