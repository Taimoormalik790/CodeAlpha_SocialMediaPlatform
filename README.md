# Pulse — Social Media Platform
### CodeAlpha Full Stack Internship · Task 2

A full-featured social media web application built with **Django** (backend) and **HTML/CSS/JS** (frontend).

---

## Features

- **Authentication** — Secure signup, login, and logout
- **User Profiles** — Bio, profile picture, website, location
- **Posts** — Create text and image posts
- **Newsfeed** — See posts from users you follow
- **Comments** — Leave comments on any post
- **Likes** — Like/unlike posts with live AJAX updates
- **Follow System** — Follow/unfollow users (Many-to-Many)
- **Explore** — Discover posts from all users
- **Search** — Find users by username
- **Responsive** — Works on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.2 |
| Database | SQLite (default) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Image Handling | Pillow |
| Forms | django-crispy-forms + Bootstrap 5 |
| Static Files | WhiteNoise |

---

## Folder Structure

```
CodeAlpha_Social_Media_Platform/
├── manage.py
├── requirements.txt
├── sample_data.json
├── db.sqlite3                   # Auto-generated on first migrate
│
├── social_media/                # Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                       # Users app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py                # Profile model (bio, pic, followers M2M)
│   ├── urls.py
│   └── views.py
│
├── posts/                       # Posts app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py                # Post, Comment models + Likes M2M
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── base.html                # Sidebar layout, flash messages
│   ├── users/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── profile.html
│   │   ├── edit_profile.html
│   │   ├── search.html
│   │   └── followers_list.html
│   └── posts/
│       ├── feed.html            # Newsfeed
│       ├── explore.html
│       └── post_detail.html
│
├── static/
│   ├── css/
│   │   └── style.css            # Full design system
│   └── js/
│       └── main.js              # Like, follow, preview, AJAX
│
└── media/                       # User-uploaded files (auto-created)
    └── profile_pics/
```

---

## Setup & Installation

### 1. Clone or unzip the project

```bash
cd CodeAlpha_Social_Media_Platform
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py makemigrations users posts
python manage.py migrate
```

### 5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. (Optional) Load sample data

> ⚠️ The fixture uses hashed dummy passwords. After loading, create real users via signup instead.

```bash
python manage.py loaddata sample_data.json
```

### 7. Collect static files (for production)

```bash
python manage.py collectstatic
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## Database Models

### `users.Profile`
| Field | Type | Description |
|-------|------|-------------|
| user | OneToOne → User | Linked Django user |
| bio | TextField | User biography |
| profile_picture | ImageField | Uploaded avatar |
| website | URLField | Personal link |
| location | CharField | City/country |
| followers | ManyToMany → User | Follow relationships |

### `posts.Post`
| Field | Type | Description |
|-------|------|-------------|
| author | FK → User | Post creator |
| content | TextField | Post text (max 2000) |
| image | ImageField | Optional photo |
| likes | ManyToMany → User | Users who liked |
| created_at | DateTimeField | Timestamp |

### `posts.Comment`
| Field | Type | Description |
|-------|------|-------------|
| post | FK → Post | Parent post |
| author | FK → User | Commenter |
| content | TextField | Comment text |
| created_at | DateTimeField | Timestamp |

---

## URL Routes

| URL | View | Name |
|-----|------|------|
| `/` | Feed (newsfeed) | `feed` |
| `/explore/` | All posts | `explore` |
| `/post/<id>/` | Post detail + comments | `post_detail` |
| `/post/<id>/like/` | Toggle like (AJAX) | `like_toggle` |
| `/post/<id>/comment/` | Add comment | `add_comment` |
| `/users/signup/` | Register | `signup` |
| `/users/login/` | Login | `login` |
| `/users/logout/` | Logout | `logout` |
| `/users/<username>/` | User profile | `profile` |
| `/users/<username>/follow/` | Follow/unfollow (AJAX) | `follow_toggle` |
| `/users/edit-profile/` | Edit own profile | `edit_profile` |
| `/users/search/` | Search users | `search_users` |

---


Log in with your superuser credentials to manage users, profiles, posts, and comments.

---

*Built with ❤️ for CodeAlpha Internship — Task 2: Social Media Platform*
