# GitHub → Kaggle Dataset Sync: Noob Guide

This setup keeps **GitHub as the master project** and publishes a clean Kaggle Dataset version automatically.

## What is already automated

The workflow:

1. checks out the GitHub repository;
2. validates the canonical project files;
3. creates a clean temporary Kaggle package;
4. confirms the employee dataset contains 762 rows;
5. validates the data dictionary and notebook JSON;
6. rejects `.pbix`, credential and private-key files;
7. creates the Kaggle Dataset when it does not exist;
8. publishes a new Kaggle version when it already exists.

## One-time setup

You must complete two private GitHub settings. Do not put the token in any repository file, issue, pull request, screenshot or chat.

### Step 1 — Confirm your Kaggle username

1. Open Kaggle.
2. Click your profile picture.
3. Open **Your Profile**.
4. Look at the browser URL.

Example:

```text
https://www.kaggle.com/musabd
```

The username is the final part:

```text
musabd
```

### Step 2 — Generate a Kaggle API token

1. Open Kaggle.
2. Click your profile picture.
3. Select **Settings**.
4. Scroll to **API**.
5. Select **Generate New Token**.
6. Copy the generated token.

Keep the token private.

### Step 3 — Add the GitHub repository variable

Open this repository:

```text
https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd
```

Then open:

```text
Settings
→ Secrets and variables
→ Actions
→ Variables
→ New repository variable
```

Enter:

```text
Name: KAGGLE_USERNAME
Value: your exact Kaggle username
```

Click **Add variable**.

### Step 4 — Add the GitHub repository secret

Remain in:

```text
Settings
→ Secrets and variables
→ Actions
```

Open **Secrets**, then select **New repository secret**.

Enter:

```text
Name: KAGGLE_API_TOKEN
Secret: paste the Kaggle API token
```

Click **Add secret**.

GitHub will not show the secret value again. That is normal.

## First test

After this setup is merged into `main`:

1. Open the repository **Actions** tab.
2. Select **Sync dataset to Kaggle**.
3. Select **Run workflow**.
4. Keep branch set to `main`.
5. Click the green **Run workflow** button.
6. Wait for both jobs.

Expected result:

```text
Validate Kaggle upload package      ✅
Publish Kaggle dataset version      ✅
```

Then open:

```text
https://www.kaggle.com/datasets/YOUR_KAGGLE_USERNAME/hossain-group-hr-turnover-analytics-bd
```

## Automatic updates

After the first successful test, a new Kaggle Dataset version will be created when relevant files are pushed to `main`, including:

```text
data/**
notebooks/Hossain_Group_Turnover_Analysis.ipynb
DATA_PROVENANCE.md
DATASET_USAGE_GUIDE.md
CITATION.cff
kaggle/**
scripts/prepare_kaggle_dataset.py
.github/workflows/sync-kaggle.yml
```

Ordinary README styling, governance-file edits and unrelated repository changes do not create unnecessary Kaggle versions.

## Troubleshooting

### `KAGGLE_USERNAME is missing`

Add the repository variable under:

```text
Settings → Secrets and variables → Actions → Variables
```

### `KAGGLE_API_TOKEN is missing`

Add the repository secret under:

```text
Settings → Secrets and variables → Actions → Secrets
```

### `401 Unauthorized`

The Kaggle token is invalid, expired or copied incorrectly. Generate a new token and replace the GitHub secret.

### `403 Forbidden`

Confirm that the Kaggle account owns the dataset slug and that the username variable exactly matches the Kaggle profile URL.

### Dataset already exists under another slug

Do not create a duplicate. Update `DATASET_SLUG` in `.github/workflows/sync-kaggle.yml` and `DATASET_SLUG` in `scripts/prepare_kaggle_dataset.py` so they match the existing Kaggle URL.

## Security rules

- Never commit `kaggle.json`.
- Never commit `access_token`.
- Never paste the API token into workflow YAML.
- Never expose the token in screenshots.
- Rotate the Kaggle token immediately if it is exposed.
