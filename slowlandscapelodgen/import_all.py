# Re-imports every slowLandscapeLODGen comparison from the imgsli-style screenshot sets, then rebuilds the pages.
#
#   python slowlandscapelodgen/import_all.py "<folder with the numbered sets>"
#
# Each entry: set folder, comparison (address part), title, description, opening pair (file numbers, left first;
# include the tool's default where the set has it), optionally extra import arguments (--skip, --label).
import os, subprocess, sys

SETS = [
    ('10_color_map', 'color-map-resolution', 'Color map resolution',
     'Color map size per quad, from 512 to 16384, with tes4ll\'s color maps at 1024, 2048 and 4096 for reference.', (4, 6)),
    ('11_render_at', 'render-at', 'Render at',
     'Color maps rendered at their own size or larger and then downscaled. Rendering larger gives smoother transitions '
     'between textures.', (4, 5)),
    ('12_blending_falloff', 'blending-falloff', 'Blending falloff',
     'How much neighbouring texture samples blend into each other (color map 4096). Lower is smoother and blurrier, '
     'higher is sharper and blockier.', (4, 7)),
    ('13_ambient_occlusion', 'ambient-occlusion', 'Ambient occlusion',
     'Ambient occlusion off and on: darkens valleys and crevices.', (1, 2)),
    ('14_stochastic_tiling', 'stochastic-tiling', 'Stochastic tiling',
     'Color map 8192 with plain grid tiling and with stochastic tiling. The plain grid\'s repetition shows best from a '
     'distance.', (2, 1)),
    ('20_normal_map', 'normal-maps', 'Normal maps',
     'Vanilla and tes4ll normal maps against slowLandscapeLODGen\'s at sizes from 512 to 8192.', (1, 6)),
    ('21_normal_format', 'normal-map-format', 'Normal map format',
     'Normal maps compressed (DXT1, the default) and uncompressed, at 2048 and 4096.', (1, 2)),
    ('22_z_boost', 'z-boost', 'Z-boost',
     'How strongly the relief shows in the lighting, from 0.5 to 3, with tes4ll\'s normal maps for reference.', (2, 5)),
    ('23_fake_shadows', 'fake-shadows', 'Fake shadows',
     'Normal maps without fake shadows, at strengths 0.5, 1.0 and 2.0, and tes4ll\'s fake shadows for reference.', (1, 3)),
    ('24_detail_noise', 'detail-noise', 'Detail noise',
     'Procedural bumps added to the normal maps (normal map 4096), at intensity 4 and 8 and at two feature sizes.', (1, 4),
     ['--label', 'Off=Off (default)', 'Intensity 4=Intensity 4, scale 20', 'Intensity 8=Intensity 8, scale 20']),
    ('25_detail_noise_format', 'detail-noise-format', 'Detail noise and normal map size',
     'Detail noise at intensity 8, scale 20 on normal maps of different sizes and formats.', (1, 3)),
    ('30_mesh', 'mesh-triangles', 'Mesh triangle count',
     'Triangles per quad from 4,000 to 60,000, all with peak weighting, and tes4ll\'s mesh for reference. Differences '
     'show on ridges against the sky.', (1, 6), ['--skip', '62000, no peak weighting']),
]

src = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__)); tools = os.path.join(os.path.dirname(here), 'tools')
for folder, slug, title, desc, pair, *skip in SETS:
    subprocess.run([sys.executable, os.path.join(tools, 'import_imgsli.py'), os.path.basename(here), os.path.join(src, folder),
                    slug, title, desc, '--pair', str(pair[0]), str(pair[1])] + (skip[0] if skip else []), check=True)
subprocess.run([sys.executable, os.path.join(tools, 'build.py')], check=True)
