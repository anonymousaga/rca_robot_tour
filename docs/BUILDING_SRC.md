## Building From Source
1. If you don't have one, set up a `python3` enviornment (3.9+). Install `git` as well.
2. Install dependencies using pip3: `pyperclip`,`toml`,`cx_Freeze` 
    > On Windows, you need to add `cxfreeze` to your PATH. pip3 will tell you the location of cxfreeze
3. Clone the repo: 
   ```
   git clone https://github.com/anonymousaga/rca_robot_tour.git
   ```
4. Enter the directory
    ```
    cd rca_robot_tour
    ```
5. Compile with cxfreeze
   * **macOS:** `cxfreeze bdist_dmg`
   * **Windows:** `cxfreeze bdist_msi`
   * **Linux:** check [cxfreeze docs](https://cx-freeze.readthedocs.io/en/stable/builtdist.html) for your distro
