# Static Site Generator 🧱

A lightweight, Python-powered static site generator that transforms your Markdown content into clean, responsive HTML pages. Ideal for personal blogs, documentation sites, and minimalist web projects.

> 🚧 This project was built as part of the [Boot.dev](https://boot.dev) Backend Developer curriculum. It serves as a practical exercise in scripting, templating, and working with file systems in Python.


## ✨ Features

- 📝 Converts `.md` files to clean HTML using a base template
- 🧩 Customizable `template.html` for consistent layout
- 📂 Supports static assets like CSS and images via the `static/` directory
- ⚙️ Easy build process using shell scripts
- 🧪 Includes a testing script for quick validation

## 📁 Project Structure

```
static-site-generator/
├── content/ # Markdown source files
├── docs/ # Output directory for generated HTML
├── src/ # Python scripts for generation logic
├── static/ # Static assets (CSS, images, etc.)
├── template.html # HTML template for all pages
├── build.sh # Script to build the site
├── test.sh # Script to test the build process
├── main.sh # Optional entry point
└── README.md # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Unix-like shell (Linux, macOS, or WSL on Windows)

### Installation

1. Clone the repo:
  ```bash
  git clone https://github.com/jacobdanielrose/static-site-generator.git
  cd static-site-generator
  ```
2. Add your Markdown files to the content/ directory.
3. Customize the template.html file to define your site's layout.
4. (Optional) Add any CSS, JS, or images to the static/ folder.

## 🔨 Build the Site

Run the build script:

```bash
./build.sh
```

## 🧪 Test the Site

To run a quick test of the generation process:

```bash
./test.sh
```

## 🌍 Deployment
You can host the site using any static hosting service:

- GitHub Pages: Serve directly from the `docs/` folder.
- Netlify / Vercel: Set the build output to `docs/`.

## 📚 About This Project
This project was created as part of the Boot.dev Backend Developer course. It’s designed to reinforce backend fundamentals using scripting, templating, and file management.

## 📝 License
This project is licensed under the MIT License.
