# threejs

Hard fork of [cloudai-x/threejs-skills](https://github.com/cloudai-x/threejs-skills) at commit
`b1c6230` (2026-01-20).

The ten `SKILL.md` files under `skills/` are verbatim copies of the upstream `skills/` directory.
Everything else in this directory is packaging to fit the layout of this marketplace. Upstream
ships the skills as a bare repo you clone or submodule into a project; here they live under
`plugins/threejs/skills/` so they install as one plugin alongside the others.

The upstream `README.md` was not carried over — it documents the clone-and-submodule install flow,
which does not apply here. Its skill table is reproduced below.

## What it does

Gives Claude Code Three.js API details, constructor signatures, import paths, and working examples
so it stops guessing at the library. Each skill loads on demand when the request matches its area —
ask for a rotating cube and `threejs-fundamentals` loads; ask for a fresnel effect and
`threejs-shaders` does.

| Skill                      | Covers                                                                  |
| -------------------------- | ----------------------------------------------------------------------- |
| **threejs-fundamentals**   | Scene setup, cameras, renderer, Object3D hierarchy, coordinate systems  |
| **threejs-geometry**       | Built-in shapes, BufferGeometry, custom geometry, instancing            |
| **threejs-materials**      | PBR materials, basic/phong/standard materials, shader materials         |
| **threejs-lighting**       | Light types, shadows, environment lighting, light helpers               |
| **threejs-textures**       | Texture types, UV mapping, environment maps, render targets             |
| **threejs-animation**      | Keyframe animation, skeletal animation, morph targets, animation mixing |
| **threejs-loaders**        | GLTF/GLB loading, texture loading, async patterns, caching              |
| **threejs-shaders**        | GLSL basics, ShaderMaterial, uniforms, custom effects                   |
| **threejs-postprocessing** | EffectComposer, bloom, DOF, screen effects, custom passes               |
| **threejs-interaction**    | Raycasting, camera controls, mouse/touch input, object selection        |

Upstream states the skills were audited against the official Three.js documentation for r160+.

## Install

```text
/plugin marketplace add punitarani/skills
/plugin install threejs@skills
```

## License

MIT. Upstream declares MIT in its README but ships no LICENSE file and names no copyright holder;
see [LICENSE](LICENSE) for the notice retained here and a note on that gap.

The skills document [Three.js](https://threejs.org/), which is itself MIT licensed.
