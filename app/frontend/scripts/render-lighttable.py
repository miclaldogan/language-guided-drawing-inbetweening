"""Cue — animator's light table, rendered headless.

blender --background --factory-startup --python lighttable.py -- <tex_dir> <out_dir> [samples]
"""

import math
import os
import random
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1 :]
TEX, OUT = argv[0], argv[1]
SAMPLES = int(argv[2]) if len(argv) > 2 else 160
os.makedirs(OUT, exist_ok=True)
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
for dev_type in ("OPTIX", "CUDA"):
    try:
        prefs.compute_device_type = dev_type
        prefs.get_devices()
        if any(d.type == dev_type for d in prefs.devices):
            for d in prefs.devices:
                d.use = d.type == dev_type
            sc.cycles.device = "GPU"
            print("device:", dev_type)
            break
    except TypeError:
        continue
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Medium High Contrast"
except TypeError:
    pass
sc.render.film_transparent = False

world = bpy.data.worlds.new("night")
world.use_nodes = True
bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (0.006, 0.004, 0.007, 1)
bg.inputs[1].default_value = 1.0
sc.world = world


def mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m, m.node_tree.nodes, m.node_tree.links


def bsdf_of(nodes):
    return next(n for n in nodes if n.type == "BSDF_PRINCIPLED")


def principled(name, color, rough=0.5, metal=0.0):
    m, n, _ = mat(name)
    b = bsdf_of(n)
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def box(name, size, loc, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(material)
    bev = o.modifiers.new("bevel", "BEVEL")
    bev.width = min(size) * 0.08
    bev.segments = 3
    return o


# ---------- desk: dark stained wood ----------
m_desk, n, lk = mat("desk")
b = bsdf_of(n)
noise = n.new("ShaderNodeTexWave")
noise.wave_type = "BANDS"
noise.inputs["Scale"].default_value = 2.2
noise.inputs["Distortion"].default_value = 6.0
noise.inputs["Detail"].default_value = 4.0
ramp = n.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.018, 0.011, 0.010, 1)
ramp.color_ramp.elements[1].color = (0.055, 0.032, 0.024, 1)
lk.new(noise.outputs["Color"], ramp.inputs[0])
lk.new(ramp.outputs["Color"], b.inputs["Base Color"])
b.inputs["Roughness"].default_value = 0.42
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
desk = bpy.context.object
desk.data.materials.append(m_desk)

# ---------- light table: a frame with a glowing glass top ----------
m_frame = principled("table-frame", (0.035, 0.032, 0.036), 0.35, 0.6)
box("table", (0.62, 0.48, 0.05), (0, 0, 0.025), m_frame)
m_glow, n, lk = mat("glow")
for x in list(n):
    n.remove(x)
em = n.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (1.0, 0.86, 0.68, 1)
em.inputs["Strength"].default_value = 1.7
out = n.new("ShaderNodeOutputMaterial")
lk.new(em.outputs[0], out.inputs[0])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.015, 0.0505))
glass = bpy.context.object
glass.scale = (0.54, 0.38, 1)
glass.data.materials.append(m_glow)

# ---------- peg bar: brushed metal with round-flat-round pegs ----------
m_metal = principled("peg-metal", (0.62, 0.6, 0.58), 0.28, 1.0)
box("pegbar", (0.32, 0.024, 0.006), (0, 0.205, 0.054), m_metal)
for x, w in ((-0.105, 0.0065), (0, 0.016), (0.105, 0.0065)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=w / 2 if w < 0.01 else 0.003, depth=0.007, location=(x, 0.205, 0.059)
    )
    peg = bpy.context.object
    if w > 0.01:
        peg.scale = (w / 0.006, 1, 1)
    peg.data.materials.append(m_metal)


# ---------- animation paper with a pencil frame, lit from below ----------
def paper_material(name, img_path, tint=(0.96, 0.93, 0.88)):
    m, n, lk = mat(name)
    for x in list(n):
        n.remove(x)
    outn = n.new("ShaderNodeOutputMaterial")
    tex = n.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(img_path)
    tex.extension = "CLIP"
    mapping = n.new("ShaderNodeMapping")
    coord = n.new("ShaderNodeTexCoord")
    # drawing sits in the lower 80% of the sheet, under the peg holes
    mapping.inputs["Scale"].default_value = (1.22, 1.52, 1)
    mapping.inputs["Location"].default_value = (-0.11, -0.2, 0)
    lk.new(coord.outputs["UV"], mapping.inputs[0])
    lk.new(mapping.outputs[0], tex.inputs[0])
    graphite = (0.06, 0.05, 0.065, 1)
    mix = n.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = (*tint, 1)
    mix.inputs["B"].default_value = graphite
    lk.new(tex.outputs["Alpha"], mix.inputs["Factor"])
    diff = n.new("ShaderNodeBsdfDiffuse")
    trans = n.new("ShaderNodeBsdfTranslucent")
    lk.new(mix.outputs["Result"], diff.inputs["Color"])
    lk.new(mix.outputs["Result"], trans.inputs["Color"])
    sh = n.new("ShaderNodeMixShader")
    sh.inputs[0].default_value = 0.6
    lk.new(diff.outputs[0], sh.inputs[1])
    lk.new(trans.outputs[0], sh.inputs[2])
    # thin animation bond: lower drawings show through as onion skin
    clear = n.new("ShaderNodeBsdfTransparent")
    sh2 = n.new("ShaderNodeMixShader")
    sh2.inputs[0].default_value = 0.34
    lk.new(sh.outputs[0], sh2.inputs[1])
    lk.new(clear.outputs[0], sh2.inputs[2])
    lk.new(sh2.outputs[0], outn.inputs[0])
    return m


def sheet(name, img, loc, rot_deg, curl=0.0):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=24, y_subdivisions=24, size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (0.305, 0.25, 1)  # roughly 12 x 10 field paper
    bpy.ops.object.transform_apply(scale=True)
    if curl:
        for v in o.data.vertices:
            t = max(0.0, v.co.x / 0.15)
            v.co.z += curl * t * t
    o.rotation_euler.z = math.radians(rot_deg)
    o.data.materials.append(paper_material(name + "-m", img))
    return o


frames = ["f01", "f04", "f07", "f10", "f13", "f16"]
stack = []
for i, f in enumerate(frames):
    jitter = (random.uniform(-0.004, 0.004), random.uniform(-0.003, 0.003))
    stack.append(
        sheet(
            f"sheet-{f}",
            os.path.join(TEX, f + ".png"),
            (jitter[0], 0.075 + jitter[1], 0.0515 + i * 0.0004),
            random.uniform(-0.8, 0.8),
            curl=0.006 if i == len(frames) - 1 else 0.0,
        )
    )
# the top sheet is lifted at its corner, the way an animator flips it
top = stack[-1]
top.rotation_euler.z = math.radians(-2.2)

# ---------- pencil: graphite-black hex body, pink eraser ----------
m_pencil = principled("pencil", (0.02, 0.018, 0.022), 0.35)
m_wood = principled("wood", (0.72, 0.52, 0.34), 0.6)
m_pink = principled("pink", (1.0, 0.12, 0.33), 0.55)
m_lead = principled("lead", (0.05, 0.05, 0.05), 0.3, 0.6)
pen = []
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.0042, depth=0.15, location=(0, 0, 0))
pen.append(bpy.context.object)
pen[-1].data.materials.append(m_pencil)
bpy.ops.mesh.primitive_cone_add(
    vertices=24, radius1=0.0042, radius2=0.0012, depth=0.018, location=(0, 0, 0.084)
)
pen.append(bpy.context.object)
pen[-1].data.materials.append(m_wood)
bpy.ops.mesh.primitive_cone_add(
    vertices=16, radius1=0.0012, radius2=0.0002, depth=0.005, location=(0, 0, 0.0955)
)
pen.append(bpy.context.object)
pen[-1].data.materials.append(m_lead)
bpy.ops.mesh.primitive_cylinder_add(radius=0.0044, depth=0.012, location=(0, 0, -0.081))
pen.append(bpy.context.object)
pen[-1].data.materials.append(m_pink)
bpy.ops.object.select_all(action="DESELECT")
for p in pen:
    p.select_set(True)
bpy.context.view_layer.objects.active = pen[0]
bpy.ops.object.join()
pencil = bpy.context.object
pencil.name = "pencil"
pencil.rotation_euler = (math.radians(90), 0, math.radians(-28))
pencil.location = (0.215, -0.035, 0.0565)

# eraser crumbs and a kneaded eraser
m_crumb = principled("crumb", (0.55, 0.52, 0.55), 0.8)
for _ in range(14):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=random.uniform(0.0009, 0.0022),
        location=(random.uniform(0.05, 0.16), random.uniform(-0.15, -0.09), 0.0525),
    )
    bpy.context.object.data.materials.append(m_crumb)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.016, location=(-0.235, -0.16, 0.06))
eraser = bpy.context.object
eraser.scale = (1.3, 0.9, 0.55)
eraser.data.materials.append(principled("kneaded", (0.32, 0.31, 0.34), 0.9))

# hot pink sticky note, slightly curled
bpy.ops.mesh.primitive_grid_add(
    x_subdivisions=10, y_subdivisions=10, size=0.076, location=(-0.215, 0.03, 0.0518)
)
note = bpy.context.object
for v in note.data.vertices:
    t = max(0.0, (v.co.y + 0.038) / 0.076)
    v.co.z += 0.004 * t**3
note.rotation_euler.z = math.radians(7)
note.data.materials.append(principled("note", (1.0, 0.16, 0.38), 0.7))

# ---------- light: a warm desk lamp from the upper left, a cool rim ----------
bpy.ops.object.light_add(type="SPOT", location=(-0.55, 0.45, 0.75))
lamp = bpy.context.object
lamp.data.energy = 190
lamp.data.color = (1.0, 0.72, 0.45)
lamp.data.spot_size = math.radians(55)
lamp.data.spot_blend = 0.6
lamp.data.shadow_soft_size = 0.06
lamp.rotation_euler = (
    (Vector((0.05, 0.0, 0.05)) - lamp.location).to_track_quat("-Z", "Y").to_euler()
)
bpy.ops.object.light_add(type="AREA", location=(0.8, -0.6, 0.5))
rim = bpy.context.object
rim.data.energy = 18
rim.data.color = (0.6, 0.7, 1.0)
rim.data.size = 0.6
rim.rotation_euler = (Vector((0, 0, 0.05)) - rim.location).to_track_quat("-Z", "Y").to_euler()


def camera(name, loc, target, lens, focus_obj, fstop):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    c.data.dof.use_dof = True
    c.data.dof.focus_object = focus_obj
    c.data.dof.aperture_fstop = fstop
    return c


def render(cam, w, h, path):
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("wrote", path, flush=True)


focus = bpy.data.objects.new("focus", None)
sc.collection.objects.link(focus)
focus.location = (0.0, 0.06, 0.052)

shots = argv[3].split(",") if len(argv) > 3 else ["hero", "close", "flat"]
if "hero" in shots:
    render(
        camera("cam-hero", (0.30, -0.5, 0.36), (0.0, 0.07, 0.05), 40, focus, 2.0),
        2400,
        1350,
        os.path.join(OUT, "lighttable-hero.png"),
    )
if "close" in shots:
    focus.location = (0.0, 0.1, 0.052)
    render(
        camera("cam-close", (0.14, -0.2, 0.2), (0.0, 0.09, 0.052), 58, focus, 4.5),
        1600,
        2000,
        os.path.join(OUT, "lighttable-close.png"),
    )
if "flat" in shots:
    # flat lay: the six sheets laid out as a storyboard on the desk
    for i, o in enumerate(stack):
        o.location = (-0.84 + i * 0.336, -0.9, 0.0015)
        o.rotation_euler.z = math.radians(random.uniform(-1.6, 1.6))
    focus.location = (0, -0.9, 0)
    bpy.ops.object.light_add(type="AREA", location=(0, -0.9, 1.2))
    top_light = bpy.context.object
    top_light.data.energy = 55
    top_light.data.size = 2.2
    top_light.data.color = (1.0, 0.86, 0.72)
    cam = camera("cam-flat", (0, -0.9, 2.05), (0, -0.9, 0), 31, focus, 11)
    render(cam, 2520, 1080, os.path.join(OUT, "storyboard-flat.png"))
