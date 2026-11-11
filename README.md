# Mod comparisons

Interactive before/after comparisons for my mods, published with GitHub Pages. Each mod has its own folder; each
comparison is one page with tabs for its scenes, linked from the mod's README:

```
https://slowpard.github.io/slowmods-imgcomparisons/<mod>/<comparison>/
https://slowpard.github.io/slowmods-imgcomparisons/<mod>/<comparison>/#<scene>/<left>-<right>
```

The address after `#` always shows the scene and pair on screen (numbers in that scene's image order), so links can
point at an exact scene and pair.

## Layout

```
assets/           shared viewer: OpenSeadragon, the curtain-sync plugin, page script and style
tools/            import and build scripts
site.json         the published address, for link previews
<mod>/
  comparisons.json  the mod's title and comparisons
  images/  previews/
  <comparison>/index.html   generated pages
  LINKS.md          generated list of all the mod's pages, to copy links from
```

## Adding a comparison

1. Import a set of screenshots laid out like this (one folder per scene, files numbered in the order to show):

   ```
   <set>/1_hills/1 - Off.jpg
   <set>/1_hills/2 - On.jpg
   <set>/2_river/...
   ```

   ```
   python tools/import_imgsli.py <mod> "<set folder>" <comparison> "<title>" "<description>" --pair 1 2
   ```

   Images are downscaled to 3840 px wide (`--width`) and copied to `<mod>/images/`. `--pair` is the pair the pages
   open with, left first. Scene names and labels can be edited in `<mod>/comparisons.json` afterwards, and a
   comparison's `main_view` (a scene) sets the scene its page opens on.

2. Rebuild the pages: `python tools/build.py`

3. Before publishing, set `base_url` in `site.json` to the site's address (for example
   `https://<user>.github.io/<repo>/`) and rebuild; link previews on Discord and forums need the full address.

Requires Python with Pillow. The pages work opened straight from disk too.

## Viewer

The viewer is [OpenSeadragon](https://openseadragon.github.io) 6.1.1 (zoom, pan, touch) with the
[curtain-sync](https://github.com/locomo/openseadragon-curtain-sync) plugin (the slider), both in `assets/vendor/` with
their BSD licenses. The plugin has two small changes for OpenSeadragon 6, marked `slowmods-imgcomparisons` in
its source: touch screens are detected by a coarse pointer, and dragging the line works on touch (without a flick pan at
the end). `assets/compare.js` only adds the page around it: scene tabs, the left/right image choice, number keys, labels, full screen
and the address.
