# Upload instructions for Sean

Suggested repository name:

`alpoge-fable-jacobian-counterexample`

## GitHub web upload

1. Create a new empty repository; do not initialize it with a README, license, or `.gitignore`.
2. Extract the ZIP locally.
3. Upload the contents of the top-level `alpoge-fable-jacobian-counterexample/` folder—not the folder itself if GitHub would create an extra nesting level.
4. Commit to the default branch.
5. Open the **Actions** tab and confirm that **Exact verification** passes.
6. Add repository topics such as `jacobian-conjecture`, `algebraic-geometry`, `computer-algebra`, and `sympy`.

## Git command line

```bash
git init
git add .
git commit -m "Publish frozen Alpöge–Fable verification package"
git branch -M main
git remote add origin https://github.com/SEAN-IAMAI/alpoge-fable-jacobian-counterexample.git
git push -u origin main
```

After upload, verify the release archive:

```bash
make frozen-files-integrity
make frozen-archive-integrity
make verify
```

The license is intentionally left as a review-only notice pending a contributor decision. Choose a formal license before advertising the repository as open source.
