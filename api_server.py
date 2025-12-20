def save_to_github_gist(user_name, criteria, results):
    """Save results to GitHub Gist (CSV format)"""
    if not GITHUB_TOKEN:
        print("⚠️ GITHUB_TOKEN not set - skipping Gist save")
        return False

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build row data
        row_data = {
            'timestamp': timestamp,
            'user_name': user_name,
            'consistency_ratio': results['cr'],
            'consistency_index': results['ci'],
            'lambda_max': results['lambdaMax'],
            'is_consistent': results['isConsistent']
        }

        # Add weights for each criterion
        for criterion, weight in results['weights'].items():
            row_data[f'weight_{criterion}'] = weight

        df_new = pd.DataFrame([row_data])

        # Use "Bearer" or "token" - GitHub supports both, but Bearer is more modern
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        gist_id = GIST_ID
        csv_content = ""

        if gist_id:
            # 1. FETCH current content (GET)
            response = requests.get(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers
            )

            if response.status_code == 200:
                gist_data = response.json()
                # Check if the file exists in the Gist
                if GIST_FILENAME in gist_data["files"]:
                    existing_content = gist_data["files"][GIST_FILENAME]["content"]
                    
                    try:
                        # Append to existing CSV
                        df_existing = pd.read_csv(pd.io.common.StringIO(existing_content))
                        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                        csv_content = df_combined.to_csv(index=False)
                    except Exception as parse_error:
                        print(f"⚠️ Could not parse existing CSV, starting fresh: {parse_error}")
                        csv_content = df_new.to_csv(index=False)
                else:
                    csv_content = df_new.to_csv(index=False)
            else:
                print(f"⚠️ Gist ID provided but fetch failed (Status {response.status_code}). Creating new.")
                gist_id = None
                csv_content = df_new.to_csv(index=False)
        else:
            csv_content = df_new.to_csv(index=False)

        # 2. SAVE content (PATCH if update, POST if create)
        payload = {
            "description": "AHP Questionnaire Results",
            "files": {
                GIST_FILENAME: {
                    "content": csv_content
                }
            }
        }

        if gist_id:
            # CORRECT METHOD: PATCH for updates
            response = requests.patch(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers,
                json=payload
            )
        else:
            # CORRECT METHOD: POST for new gists
            payload["public"] = False
            response = requests.post(
                "https://api.github.com/gists",
                headers=headers,
                json=payload
            )

        if response.status_code in [200, 201]:
            print(f"✅ Saved to GitHub Gist: {response.json().get('html_url')}")
            return True
        else:
            # This will show in Railway logs if it fails
            print(f"❌ GitHub API Error ({response.status_code}): {response.text}")
            return False

    except Exception as e:
        print(f"❌ System Error saving to Gist: {str(e)}")
        return False
