# Repository instructions

## Inbox publishing workflow

When the user asks to publish, process, or release files from `inbox/`, treat that request as the standard publishing workflow below.

1. Inspect `inbox/` and the Git working tree before making changes. Ignore `inbox/README.md`. A top-level file is one publication unit. A top-level directory is one publication unit and may contain one main Markdown or HTML file plus related assets.
2. Read each unit and derive a concise title, description, and stable English kebab-case slug from its content. Reuse a clear existing slug when supplied. Do not overwrite an existing page; choose a distinct slug or ask when the intended relationship is genuinely ambiguous.
3. Move each publication unit to `content/<slug>/`. Name the entry file `index.md` or `index.html`. Preserve only assets that belong to that unit and update relative links after moving it.
4. For Markdown, add or normalize this UTF-8 front matter:

   ```yaml
   ---
   layout: default
   title: <page title>
   description: <short description>
   ---
   ```

5. For HTML, preserve the author's layout while ensuring it has `lang="ja"` when appropriate, UTF-8 charset, a viewport declaration, a useful `<title>`, and a description meta tag. Fix invalid local asset paths.
6. Add one card per publication inside the `CONTENT-CARDS` markers in `index.html`. Link directory pages with a trailing slash and write a short, content-based description. Keep existing cards unless the user explicitly asks to remove them.
7. Remove the processed source from `inbox/`, leaving `inbox/README.md` in place. Never publish secrets, credentials, private personal data, or unrelated files found beside an input.
8. Run `python scripts/check_site.py` and `git diff --check`. Preview affected HTML locally when the change warrants it.
9. When the user asked to publish, commit the scoped changes, push `master`, and verify both `Validate site` and `pages build and deployment` complete successfully. Confirm the new public URL returns HTTP 200 before reporting completion.

The `inbox/` directory is intentionally excluded from Jekyll and from site validation. Files become public only after they are processed into `content/` and linked from the home page.
