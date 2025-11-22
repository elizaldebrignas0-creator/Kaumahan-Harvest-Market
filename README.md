<<<<<<< HEAD
🌾 Kaumahan Harvest Market – Farm-Themed Online Marketplace

A full-featured online marketplace connecting local farmers with buyers, built with Django 4.2.7, Python 3.11, and MySQL.
Sellers pin their farm locations; buyers can search and purchase fresh products directly.

Professional Design & UX: Implements the Farm Fading Color System — a gradient-driven, environment-aligned visual identity optimized for agricultural platforms.

🌟 Features
👥 User Roles

Buyer Features:

Browse and search products

Add products to cart and checkout (COD only)

View all sellers pinned on a map of Biliran

Click on seller pins to see seller info and products

Rate and comment on products

Seller Features:

Register and pin location on a map during registration

Upload business permit for admin approval

Manage products (CRUD) and upload images

View and manage orders

Update order status and track earnings

Admin Features:

Manage all users, approve/reject sellers

Manage products and orders

Monitor platform analytics and site activity

Admin dashboard integrated inside the system (not default Django admin)

Farm-Themed UI:

Modern, gradient-based color system

Mobile-first and desktop-friendly

TikTok-style login/register pages (formal sizes)

Visual hierarchy, readability, and clarity prioritized

🎨 Farm Fading Color System — Professional Design Overview

The Farm Fading Color System is a refined gradient visual theme designed for agricultural platforms, farm management systems, and nature-focused applications. It blends natural tones, organic textures, and smooth gradient transitions for a modern, trustworthy, and environment-aligned user experience.

🌅 Core Gradient Palettes

A. Sunrise Over the Fields
Warm, inviting gradient reflecting early morning farmland.

#FFB56B → #FF7E5F — Sunrise Warmth

#FFD27F → #F6AE2D — Golden Harvest
Usage: Headers, hero sections, onboarding screens

B. Fresh Green Fields
Vibrant green fade symbolizing healthy crops.

#A8E063 → #56AB2F — Pasture to Crop

#E8F5E9 → #C8E6C9 — Soft Natural Greens
Usage: Dashboards, analytics cards, action buttons

C. Wheat & Soil
Grounded, earthy gradient representing soil and grain.

#F2E1A8 → #D2B48C — Wheat & Barley

#8D6E63 → #4E342E — Soil Depth
Usage: Navigation, sidebars, backgrounds

D. Weather & Sky
Clean blue gradient referencing weather tracking.

#89CFF0 → #4682B4 — Clear Sky Fade

#F0FFF0 → #E0F2F1 — Mist to Aqua
Usage: Monitoring interfaces, irrigation tools, forecasting modules

E. Fresh Produce Vibrant Fade
Vivid, energetic gradient representing crops and farm markets.

#FFCF33 → #FFA000 — Sunflower to Orange

#8BC34A → #558B2F — Veggie Green to Organic Green
Usage: Highlights, icons, call-to-actions

🧩 Functional Design Principles

Clarity & Accessibility:

High-contrast text overlays on gradients

WCAG-compliant color choices

Consistency Across Systems:

Structured stop points for UI cards, panels, charts, microinteractions

Adaptable for light/dark modes

Scalable for Data-Heavy Interfaces:
Ideal for farm dashboards, weather/sensor telemetry, inventory, crop planning, and food supply chain apps

Professional Usage Guidelines:

Warm gradients → branding & hero sections

Green/earth fades → functional system elements

Bright produce gradients → call-to-action elements

Maintain consistent gradient directions

🛠️ Tech Stack

Backend: Python (Django 4.2.7)

Database: MySQL 8.0+

Frontend: HTML5, CSS3, JavaScript, Bootstrap 5

Maps: Leaflet.js (OpenStreetMap) for seller location pinning

Image Handling: Pillow

Authentication: Django CustomUser model

📋 Prerequisites

Python 3.11+

MySQL Server

pip (Python package manager)

VS Code (recommended)

🚀 Installation & Setup

Clone repository

Create virtual environment and activate

Install dependencies

Configure .env with database credentials

Run migrations

Create admin user (createsuperuser or create_admin)

Run development server

Access application:

Main site: http://127.0.0.1:8000/

Admin dashboard: http://127.0.0.1:8000/admin-dashboard/

🏗️ Project Structure
kaumahan-harvest-market/
├── kaumahan/                # Project configuration
├── marketplace/            # Main app
│   ├── management/         # Custom commands
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/                  # User-uploaded files
├── static/                 # Global static files
├── templates/              # Global templates
├── .env
├── manage.py
└── requirements.txt

🌟 UX / UI Highlights

TikTok-style login/register forms with buyer/seller selection

Seller pins their location during registration using Leaflet map

Buyer can view seller pins, search by seller, and see products

Formal standard sizes for login/register pages (desktop/mobile)

Farm Fading Color System applied across dashboards, product cards, CTAs

🔐 Default Admin Credentials (for development)

Email: elizaldepelaez0@gmail.com

Password: admin123

📧 Contact

For questions or support: elizaldepelaez0@gmail.com

Kaumahan Harvest Market – Harvest Freshness, From Farm to You 🌾

This now combines:

Professional UX/UI with gradients (Farm Fading Color System)

Formal login/register with TikTok-style look

Leaflet map for seller location pinning

All user roles & dashboards

COD payment only
=======
# Kaumahan-Harvest-Market
Kaumahan Harvest Market is a Django web app connecting local farmers and buyers. Sellers can list fresh produce, while buyers can browse, add to cart, and place orders. Features include user authentication, ratings, reviews, and a responsive interface promoting local farm-to-table commerce.
>>>>>>> febb0e4c7a32b6b8e50c55c90dc1806ae686c7c9
