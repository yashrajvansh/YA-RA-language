# YA|RA language definition

Spoken name: **YA|RA**.
Filesystem name and extension: **YA-RA** / **`.YA-RA`**.
This is not [YARA](https://github.com/VirusTotal/yara) (`.yar`, `.yara`), already in GitHub Linguist.

Language implementation: [yashrajvansh/sissyphus](https://github.com/yashrajvansh/sissyphus) folder `YA-RA/`.

## What this repo is

The pack Linguist and editors need:

- `languages.yml` — proposed Linguist entry
- `grammars/ya-ra.tmLanguage.json` — TextMate grammar (`source.ya-ra`)
- `samples/` — real programs, not hello-world
- `vscode/` — editor contribution

## Linguist

GitHub will not show YA-RA on a repo language bar until `github-linguist/linguist` accepts this entry.
Their usage bar is roughly 200 unique public repos or ~2000 indexed files on the extension.
That is not met yet. The definition is ready when it is.

Do not map `.YA-RA` onto YARA. The languages collide only in English spelling.

## License

Samples and grammar in this repository are released under MIT for Linguist inclusion.
