# BUET CSE Sessional Materials

Repo for storing offline, online and practice mats

## Recap

Repo has two versions:

- [Public](https://github.com/badnails/classmat.git)
- [Private](https://github.com/badnails/classmat-private)

---

## To setup after a clone:

### 1. Create two local branches
```bash
git checkout -b <branch-name>  # create new branch
git branch -m <branch-name>    # rename branch
```


### 2. Set the two remotes
```bash
git remote remove <remote-name>
git remote set-url <existing-remote-name> <url>  # edit existing remote url
git remote add <new-remote-name> <url>
```

### 3. Map a branch to a specific remote
   #### 3.1. Checkout into branch
   ```bash
   git checkout <branch-name>
   ```
   #### 3.2. Fetch the remote
   ```bash
   git fetch <remote-name>
   ```
   #### 3.3. Add upstream
   ```bash
   git branch --set-upstream-to=<remote-name>/<remote-branch-name>
   ```

   >**Note:** If local and remote branch names differ, pushes may get rejected.
   ```bash
   git push -u <remote> <local-branch>:<remote-branch>
   ```
   
   