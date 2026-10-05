# Post-Execution

After all stages complete, ask:

1. **Would you like to create a change branch?** (yes/no)
2. _(If yes)_ What branch should we base it on? (e.g., `main`, `develop`)
3. Create or switch to the change branch:
   - Use `{{TASK_ID}}` as the branch name
   - If the branch already exists, switch to it and add the changes there
   - If it doesn't exist, create it from the specified base branch
4. Commit all generated files with a summary of what was created/modified, and push the branch to the remote. Branch name must match a given regex pattern: ^(main|master|develop|dev|qa|staging|uat|prod|production|feature/.+|bugfix/.+|fix/.+|dependabot/.+|chore/.+|hotfix/.+|release/.+|gs-pipeline/.+|gs-bundle/.+|gs-bundle-feature/.+|gs-bundle-base/.+|gs-gitflow-release/.+|gs-gitflow-baseline-release/.+|gs-project/.+|gs-sandbox/.+|story/.+|RC-.+|DEV-.+|QA-.+|dev.+|qa.+|UAT-.+|[A-Z]+-[0-9]+(_.*)?|gh-readonly-queue/.+|copilot/.+|pr-#-[a-zA-Z0-9]+|techdebt/.+|renovate/.+|copyOfmaster/.+|createdOutOfGitTag/.+)$
