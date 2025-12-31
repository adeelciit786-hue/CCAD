# 🚀 QUICK GITHUB PUSH - COMMAND REFERENCE

## ONE-TIME SETUP (Copy & Paste)

```powershell
cd "c:\Users\adeel\Google ADS"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/keyword-intelligence-platform.git
git push -u origin main
```

**Replace `YOUR-USERNAME` with your GitHub username**

---

## BEFORE YOU PUSH

### 1. Create GitHub Repository
Go to GitHub.com:
1. Click **"+"** → **"New repository"**
2. Name: `keyword-intelligence-platform`
3. Choose: Public or Private
4. Click **"Create repository"**

### 2. Prepare Git
```powershell
cd "c:\Users\adeel\Google ADS"
git branch -M main
```

---

## PUSH TO GITHUB

```powershell
git remote add origin https://github.com/YOUR-USERNAME/keyword-intelligence-platform.git
git push -u origin main
```

When prompted for authentication:
- **Username**: Your GitHub username
- **Password**: Your GitHub personal access token (see below)

---

## GET PERSONAL ACCESS TOKEN

1. Go: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `Git Push Token`
4. Check: ✓ `repo` (full control)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)
7. Use as password when Git asks

---

## VERIFY PUSH SUCCESS

```powershell
git status
```

Should show:
```
On branch main
Your branch is up to date with 'origin/main'.
```

Visit: `https://github.com/YOUR-USERNAME/keyword-intelligence-platform`

You should see all your files! ✨

---

## WHAT GETS PUSHED

✅ **95 Files**:
- Source code (app.py, keyword_engine_v2/, etc.)
- Documentation (README, CONTRIBUTING, etc.)
- Configuration (requirements.txt, .env.example, etc.)
- CI/CD (GitHub Actions workflow)
- Docker files (Dockerfile, docker-compose.yml)
- License (MIT)

❌ **NOT Pushed** (excluded by .gitignore):
- Virtual environment (.venv/)
- Python cache (__pycache__/)
- Environment variables (.env)
- Temporary uploads/
- Log files
- IDE files (.vscode/, .idea/)

---

## AUTHENTICATION OPTIONS

### Option 1: Personal Access Token (Recommended)
```
Username: your-github-username
Password: ghp_XXXXXXXXXXXXXXXXXXXX (your token)
```

### Option 2: GitHub CLI
```powershell
winget install GitHub.cli
gh auth login
# Follow prompts
git push -u origin main
```

### Option 3: SSH Key (Advanced)
```powershell
ssh-keygen -t ed25519 -C "your@email.com"
# Add public key to GitHub Settings → SSH Keys
# Change remote:
git remote set-url origin git@github.com:YOUR-USERNAME/keyword-intelligence-platform.git
git push -u origin main
```

---

## TROUBLESHOOTING

### "repository not found"
Check you replaced YOUR-USERNAME:
```powershell
git remote -v
```

### "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/keyword-intelligence-platform.git
```

### "Permission denied"
Use personal access token instead (Option 1 above)

### "fatal: The remote end hung up unexpectedly"
Internet issue. Try again:
```powershell
git push -u origin main
```

---

## AFTER PUSH

1. ✅ Go to GitHub repository
2. ✅ Enable Actions/Issues/Discussions
3. ✅ Add repository topics
4. ✅ Share link with team
5. ✅ Setup branch protection (optional)

---

## USEFUL GIT COMMANDS

```powershell
# Check status
git status

# See your commits
git log --oneline

# See changes
git diff

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout branch-name

# Commit changes
git add .
git commit -m "Your message"

# Push new branch
git push -u origin branch-name

# Pull latest
git pull origin main
```

---

## REPOSITORY INFORMATION

- **Name**: keyword-intelligence-platform
- **Description**: AI-powered Google Ads keyword analysis with ROI metrics
- **License**: MIT
- **Python**: 3.10+
- **Files**: 95
- **Commits**: 1 (initial)

---

## NEXT STEPS

After push:
1. Monitor GitHub Actions (tests auto-run)
2. Set default branch to `main`
3. Create releases for versions
4. Pin important issues
5. Keep code updated

---

**Questions?** See [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) for detailed guide!
