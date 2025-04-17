# Updating the `tast` Folder

This document outlines the process for updating the contents of the `tast` folder in this repository. The `tast` folder is kept in sync with a specific commit of the upstream [Tast](<https://chromium.googlesource.com/chromiumos/platform/tast-tests">) project.

**To update the `tast` folder:**

1.  **Identify the desired commit SHA:** Determine the specific commit SHA from the upstream Tast repository that you want to synchronize with.

2.  **Modify the `TAST_COMMIT` file:** Change commit SHA in file to selected one.

3.  **Execute the generation script:** Run the `./generate_tast_services.sh` script from your terminal. This script will download the Tast repository at the specified commit and generate the files that populate the `tast` folder in this repository.

    ```bash
    ./generate_tast_services.sh
    ```

4.  **Review the changes:** After the script has finished executing, carefully review the changes that have been made within the `tast` folder. This might involve using `git diff` to see the differences between the previous state and the newly generated files.

5.  **Create a Pull Request:** If you are satisfied with the updates in the `tast` folder, stage the changes (using `git add tast/`) and commit them along with the updated `TAST_COMMIT` . Then, create a Pull Request (PR) to merge these changes into the main branch of this repository. Your PR title should clearly indicate that it updates the `tast` folder and includes the new `TAST_COMMIT`.

    ```
    git add scripts/TAST_COMMIT tast/
    git commit -m "Update tast folder to commit <your_desired_commit_sha>"
    git push origin your-update-branch
    # Then create a Pull Request
    ```
