# Profile setup

1. These files target the public profile repository `yeonatanRosental/yeonatanRosental`. Keep `README.md` at its root and include the `assets` directory and `.github/workflows/stats.yml`.
2. Push to the default branch. GitHub displays the README on your profile automatically while the repository is public.

The GIF loads from an external service. Technology icons are stored in `assets/tech` as padded, labeled SVG tiles; their Devicon license is included in that directory. The statistics card is stored in `assets/stats.svg`. Its initial snapshot uses public data, including visible private contribution totals. The workflow replaces it with authenticated statistics after you configure the token.

## Hourly Steam activity

The now-playing section links to `https://steamcommunity.com/id/oppoo12` and displays `assets/steam.svg` in the same retro style as the rest of the profile. Include `scripts/update_steam.py` and `.github/workflows/steam.yml` when pushing this repository.

The **Update Steam activity** workflow runs every hour at minute 17, on changes to its workflow or generator, and through **Actions → Update Steam activity → Run workflow**. Scheduled runs use the default branch; GitHub may delay them. No Steam API key or additional secret is required. The workflow uses the repository's automatic `GITHUB_TOKEN` to commit the card, so Actions must be allowed to write repository contents.

The card shows the current game when Steam exposes it, along with up to three recent games and their playtime over the last two weeks. Otherwise it displays the available online status or a private/no-activity message. In Steam's **Edit Profile → Privacy Settings**, make **My profile** and **Game details** public to share games. The checked timestamp makes the age of the snapshot visible; failed requests preserve the last successful card.

The generator uses Steam's public community XML feed. [Valve documents this feed as deprecated](https://partner.steamgames.com/doc/webapi_overview/community), so future Steam changes may require updating the integration. It currently works for this profile. Run `python3 scripts/update_steam.py` to refresh locally and `python3 -m unittest discover -s scripts -p 'test_*.py'` to check the renderer.

## Private repository statistics

1. Create a personal access token for the account whose statistics you want to display. The [stats action documents](https://github.com/stats-organization/github-readme-stats-action#inputs) classic PAT scopes `repo` and `read:user` for private repository statistics. Only authorize work repositories your organization permits you to use; organization approval or SSO authorization may also be required.
2. In this profile repository, open **Settings → Secrets and variables → Actions → New repository secret**. Name it `STATS_TOKEN` and paste the real token as its value. Do not paste the token into a committed file or share it in chat.
3. Push `.github/workflows/stats.yml` and the updated README and assets. Open **Actions → Update GitHub stats → Run workflow** on the default branch. Adding a secret by itself does not trigger a run.

The workflow contains the placeholder `example` and reports a configuration error until `STATS_TOKEN` is configured as a repository secret. Leave that placeholder in the file; the secret overrides it automatically. An Actions variable or an environment secret does not configure this workflow. The first successful authenticated run updates the card, and subsequent runs refresh it every 12 hours. Failed generation preserves the last committed image.

The card includes PRs, issues, commits, stars, contributed-to repositories, and total contributions as supported by the provider. Counts depend on token access and each metric's time window; it cannot include inaccessible repositories. Only the generated SVG is committed, but its aggregated private statistics will be public. The workflow uses the automatic `GITHUB_TOKEN` to push the SVG; `STATS_TOKEN` is passed only to the configuration check and stats generator.

The design adapts the header, bio, icons, and statistics from [Piyush Malhotra's guide](https://dev.to/thepiyushmalhotra/how-to-design-an-attractive-github-profile-readme-1ppg) to a clean layout without emojis. The supplied GIF is embedded at its original URL.

Resources: [Devicon](https://github.com/devicons/devicon), [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended).

The header, toolbox diagram, technology tiles, and footer use static SVGs styled as old desktop windows and beveled buttons. The header preserves the glowing name. The footer links back to the top of the README. Edit these assets to customize the green theme. The supplied GIF remains externally hosted.

Retro web buttons are stored in `assets/retro`. Header and footer remain static. Docker, OpenShift, and Splunk are included in the primary stack; the latter two use Simple Icons with the license stored alongside the technology tiles.
