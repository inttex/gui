import itertools

import dearpygui.dearpygui as dpg
import math
import numpy as np

dpg.create_context()
dpg.configure_app(init_file="custom_layout.ini")
dpg.create_viewport()
dpg.setup_dearpygui()


class Camera:

    def __init__(self, pos=dpg.mvVec4(0.0, 0.0, 0.0, 1.0), pitch=0.0, yaw=0.0):
        self.eye_radius = 20
        self.view_to = pos
        self.eye_pos = dpg.mvVec4(50.0, 50.0, 50.0, 1.0)
        self.eye_up, self.eye_right = self.get_up_right(up=np.array([0, 1, 0]))

        self.rotating = False
        self.moving = False
        self.mouse_pos = [0, 0]
        self.dirty = False
        self.travel_speed = 0.3
        self.rotation_speed = 0.024
        self.zoom_speed = 0.9
        self.field_of_view = 45.0
        self.nearClip = 0.01
        self.farClip = 400.0

    def get_up_right(self, up=None):
        eye_pos = np.array([self.eye_pos[0], self.eye_pos[1], self.eye_pos[2]])
        view_to = np.array([self.view_to[0], self.view_to[1], self.view_to[2]])
        view_vect = view_to - eye_pos
        if up is None:
            eye_up = self.eye_up
        else:
            eye_up = up
        eye_right = np.cross(view_vect, eye_up)
        eye_right = eye_right / np.linalg.norm(eye_right)
        eye_up = np.cross(eye_right, view_vect)
        eye_up = eye_up / np.linalg.norm(eye_up)
        return eye_up, eye_right

    def move_handler(self, sender, pos, user):
        dx = self.mouse_pos[0] - pos[0]
        dy = self.mouse_pos[1] - pos[1]
        if dx != 0.0 or dy != 0.0:
            if self.rotating:
                self.rotate(dx, dy)
            elif self.moving:
                self.move(dx, dy)
        self.mouse_pos = pos

    def toggle_rotating(self):
        self.rotating = not self.rotating

    def toggle_moving(self):
        self.moving = not self.moving

    def zoom(self, sender, wheel, user_data):
        zoom_factor = self.zoom_speed ** wheel
        for i in range(3):
            self.eye_pos[i] = self.eye_pos[i] * zoom_factor
        self.mark_dirty()

    def mark_dirty(self):
        self.dirty = True
        view_to = np.array([self.view_to[0], self.view_to[1], self.view_to[2]])
        dpg.configure_item(dpg.get_item_alias('up'), p1=10 * view_to, p2=10 * (self.eye_up + view_to))
        dpg.configure_item(dpg.get_item_alias('right'), p1=10 * view_to, p2=10 * (self.eye_right + view_to))
        dpg.set_value("Camera X", f'{self.eye_pos[0]:0.2f}')
        dpg.set_value("Camera Y", f'{self.eye_pos[1]:0.2f}')
        dpg.set_value("Camera Z", f'{self.eye_pos[2]:0.2f}')

    def view_matrix(self):
        return dpg.create_lookat_matrix([self.eye_pos[_] for _ in range(4)],
                                        [self.view_to[_] for _ in range(4)],
                                        self.eye_up)

    def projection_matrix(self, width, height):
        return dpg.create_perspective_matrix(math.pi * self.field_of_view / 180.0, width / height,
                                             self.nearClip,
                                             self.farClip)

    def move(self, dx, dy):
        eye_pos = np.array([self.eye_pos[0], self.eye_pos[1], self.eye_pos[2]])
        view_to = np.array([self.view_to[0], self.view_to[1], self.view_to[2]])
        view_vect = view_to - eye_pos
        motion_vect = self.travel_speed * np.linalg.norm(view_vect) / 300 * (self.eye_right * dx - self.eye_up * dy)
        self.eye_pos[0] += motion_vect[0]
        self.eye_pos[1] += motion_vect[1]
        self.eye_pos[2] += motion_vect[2]
        self.view_to[0] += motion_vect[0]
        self.view_to[1] += motion_vect[1]
        self.view_to[2] += motion_vect[2]
        self.mark_dirty()
        dpg.set_value("Camera X", f'{self.eye_pos[0]:0.2f}')
        dpg.set_value("Camera Y", f'{self.eye_pos[1]:0.2f}')
        dpg.set_value("Camera Z", f'{self.eye_pos[2]:0.2f}')

    def rotate(self, dx, dy):
        rot_around_y = dx * self.rotation_speed
        rot_around_x = dy * self.rotation_speed

        self.eye_up, self.eye_right = self.get_up_right()
        self.eye_pos = dpg.create_rotation_matrix(rot_around_x, self.eye_right) * \
                       dpg.create_rotation_matrix(rot_around_y, self.eye_up) * \
                       self.eye_pos

        dpg.set_value(dpg.get_item_alias('up'), ((10, 10, 10), (0, 0, 0)))

        self.mark_dirty()

    def _set_field_of_view(self, value):
        self.field_of_view = float(value)
        self.dirty = True

    def _set_near(self, value):
        self.nearClip = value
        self.dirty = True

    def _set_far(self, value):
        self.farClip = value
        self.dirty = True

    def show_controls(self):

        with dpg.window(label="Camera Controls", width=500, height=500):
            dpg.add_text(str(self.eye_pos[0]), label="Camera X", show_label=True, tag="Camera X")
            dpg.add_text(str(self.eye_pos[1]), label="Camera Y", show_label=True, tag="Camera Y")
            dpg.add_text(str(self.eye_pos[2]), label="Camera Z", show_label=True, tag="Camera Z")
            dpg.add_slider_float(label="near_clip", min_value=0.1, max_value=100, default_value=self.nearClip,
                                 callback=lambda s, a: self._set_near(a))
            dpg.add_slider_float(label="far_clip", min_value=0.2, max_value=1000, default_value=self.farClip,
                                 callback=lambda s, a: self._set_far(a))
            dpg.add_text("field_of_view")
            dpg.add_radio_button(["45.0", "60.0", "90.0"], default_value="45.0", label="field of view",
                                 callback=lambda s, a: self._set_field_of_view(a))


def getxyz_sphere(r, theta, phi):
    y = r * np.sin(theta)
    radius = r * np.cos(theta)
    x = radius * np.cos(phi)
    z = radius * np.sin(phi)
    return [x, y, z]


def get_4_pt_groups_sphere(radius, nb_thetas, nb_phis):
    d_theta = np.pi / nb_thetas
    d_phi = 2 * np.pi / nb_phis
    groups = []
    for theta in np.linspace(-np.pi / 2, np.pi / 2, nb_thetas, endpoint=False):
        for phi in np.linspace(0, 2 * np.pi, nb_phis, endpoint=False):
            pts4 = [
                getxyz_sphere(radius, theta, phi + d_phi),
                getxyz_sphere(radius, theta + d_theta, phi + d_phi),
                getxyz_sphere(radius, theta + d_theta, phi),
                getxyz_sphere(radius, theta, phi),
            ]
            groups.append(pts4)
    return groups


def get_4_pts_groups_cylinder_2pt(radius, pt1, pt2, nb_thetas):
    get_4_pts_groups_cylinder(radius, 1, nb_thetas)
    transform_pts


def get_4_pts_groups_cylinder(radius, height, nb_thetas):
    todo


def get_4_pts_groups_polyline(pts, radius, nb_corners=6):
    groups = []
    for pt1, pt2 in itertools.pairwise(pts):
        for corner:
            get_4_pts_groups_cylinder_2pt(radius, pt1, pt2, nb_corners)


def draw_4_pt_groups(groups, color, fill, thickness):
    for pts4 in groups:
        dpg.draw_triangle(pts4[0], pts4[1], pts4[2], color=color,
                          fill=fill, thickness=thickness)
        dpg.draw_triangle(pts4[2], pts4[3], pts4[0], color=color,
                          fill=fill, thickness=thickness)


class Sphere:
    def __init__(self, pos=(0, 0, 0), radius=1, alpha=255, color=(255, 255, 255, 10)):
        self.radius = radius
        self.alpha = alpha

        self.sphere_solid = dpg.generate_uuid()
        self.node2 = dpg.generate_uuid()

        self.nodes = []
        self.nodes.append(self.sphere_solid)
        self.nodes.append(self.node2)

        self.layer = dpg.generate_uuid()
        self.pos = pos
        self.rot = [0, 0, 0]
        self.scale = [1.0, 1.0, 1.0]
        self.color = color

        self.groups_sphere = get_4_pt_groups_sphere(radius=self.radius, nb_thetas=32, nb_phis=32)

    def submit(self, layer=None):
        if layer is None:
            dpg.push_container_stack(
                dpg.add_draw_layer(tag=self.layer, depth_clipping=True, cull_mode=dpg.mvCullMode_Back,
                                   perspective_divide=True))
        else:
            dpg.push_container_stack(layer)
            self.layer = layer

        with dpg.draw_node(tag=self.sphere_solid):
            draw_4_pt_groups(groups=self.groups_sphere, color=[255, 255, 255, 10],
                             fill=self.color, thickness=1)

            draw_quarter_lines = False
            if draw_quarter_lines:
                thetas = np.linspace(-np.pi / 250, np.pi / 250, 2, endpoint=False)
                d_theta = thetas[1] - thetas[0]
                for theta in thetas:
                    for phi in np.linspace(0, 2 * np.pi, nb_phis, endpoint=False):
                        pts4 = [
                            self.getxyz(self.radius, theta, phi + d_phi),
                            self.getxyz(self.radius, theta + d_theta, phi + d_phi),
                            self.getxyz(self.radius, theta + d_theta, phi),
                            self.getxyz(self.radius, theta, phi),
                        ]
                        dpg.draw_triangle(pts4[0], pts4[1], pts4[2], color=self.color,
                                          fill=[200, 50, 50, self.alpha], thickness=1)
                        dpg.draw_triangle(pts4[2], pts4[3], pts4[0], color=[255, 0, 255, 255],
                                          fill=[200, 80, 50, self.alpha], thickness=1)

                        # flip x and y axis
                        pts4b = [[-y, x, z] for x, y, z in pts4]
                        dpg.draw_triangle(pts4b[0], pts4b[1], pts4b[2], color=[50, 50, 200, self.alpha],
                                          fill=[50, 50, 200, self.alpha], thickness=1)
                        dpg.draw_triangle(pts4b[2], pts4b[3], pts4b[0], color=[50, 50, 200, self.alpha],
                                          fill=[50, 50, 200, self.alpha], thickness=1)

                        # flip x and y axis
                        pts4b = [[x, -z, y] for x, y, z in pts4]
                        dpg.draw_triangle(pts4b[0], pts4b[1], pts4b[2], color=[50, 200, 50, self.alpha],
                                          fill=[50, 200, 50, self.alpha], thickness=1)
                        dpg.draw_triangle(pts4b[2], pts4b[3], pts4b[0], color=[50, 200, 50, self.alpha],
                                          fill=[50, 200, 50, self.alpha], thickness=1)

        nb_thetas = 32
        nb_phis = 32
        with dpg.draw_node(tag=self.node2):
            theta = 0
            d_theta = np.pi / nb_thetas
            d_phi = np.pi / nb_phis
            for phi in np.linspace(0, 2 * np.pi, nb_phis, endpoint=False):
                dpg.draw_line(getxyz_sphere(self.radius, theta, phi), getxyz_sphere(self.radius, theta, phi + d_phi),
                              color=(255, 0, 0, 100))
            for phi in [0, np.pi]:
                for theta in np.linspace(-np.pi / 2, np.pi / 2, nb_thetas, endpoint=False):
                    dpg.draw_line(getxyz_sphere(self.radius, theta, phi),
                                  getxyz_sphere(self.radius, theta + d_theta, phi),
                                  color=(0, 255, 0, 100))
            for phi in [np.pi / 2, -np.pi / 2]:
                for theta in np.linspace(-np.pi / 2, np.pi / 2, nb_thetas, endpoint=False):
                    dpg.draw_line(getxyz_sphere(self.radius, theta, phi),
                                  getxyz_sphere(self.radius, theta + d_theta, phi),
                                  color=(0, 0, 255, 100))
        dpg.pop_container_stack()

    def update(self, projection, view):
        model = dpg.create_translation_matrix(list(self.pos)) \
                * dpg.create_rotation_matrix(self.rot[0], [1, 0, 0]) \
                * dpg.create_rotation_matrix(self.rot[1], [0, 1, 0]) \
                * dpg.create_rotation_matrix(self.rot[2], [0, 0, 1]) \
                * dpg.create_scale_matrix(self.scale)

        for node in self.nodes:
            dpg.apply_transform(node, projection * view * model)
        # dpg.apply_transform(self.node2, projection * view * model)

    def update_clip_space(self, top_left_x, top_left_y, width, height, min_depth, max_depth):
        dpg.set_clip_space(self.layer, top_left_x, top_left_y, width, height, min_depth, max_depth)


camera = Camera(dpg.mvVec4(0.0, 0.0, 0.0, 1.0), 0.0, 0.0)
sphere = Sphere(radius=10, alpha=255, color=[100, 100, 100, 255])

# sphere2 = Sphere(pos=[0, 4, 6, ], radius=5, alpha=255, color=[255, 155, 155, 255])
camera.show_controls()

dpg.set_viewport_resize_callback(lambda: camera.mark_dirty())
rect = dpg.generate_uuid()

with dpg.viewport_drawlist(front=False):
    sphere.submit()
    # sphere2.submit(sphere.layer)

    dpg.draw_rectangle((0, 0), (10, 10), tag=rect)
    with dpg.draw_layer(perspective_divide=True, tag="gizmo_layer"):
        with dpg.draw_node(tag="gizmo"):
            dpg.draw_line((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), color=(255, 0, 0))
            dpg.draw_line((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), color=(0, 255, 0))
            dpg.draw_line((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), color=(0, 0, 255))

            dpg.draw_line((0.0, 0.0, 0.0), (0.0, 5.0, 0.0), color=(0, 255, 0), tag='right')
            dpg.draw_line((0.0, 0.0, 0.0), (0.0, 0.0, 5.0), color=(0, 0, 255), tag='up')

with dpg.handler_registry(tag="__demo_keyboard_handler"):
    dpg.add_key_down_handler(key=dpg.mvKey_A, callback=lambda s, a, u: camera.update(s, a, u))
    dpg.add_key_down_handler(key=dpg.mvKey_D, callback=lambda s, a, u: camera.update(s, a, u))
    dpg.add_key_down_handler(key=dpg.mvKey_R, callback=lambda s, a, u: camera.update(s, a, u))
    dpg.add_key_down_handler(key=dpg.mvKey_F, callback=lambda s, a, u: camera.update(s, a, u))
    dpg.add_key_down_handler(key=dpg.mvKey_W, callback=lambda s, a, u: camera.update(s, a, u))
    dpg.add_key_down_handler(key=dpg.mvKey_S, callback=lambda s, a, u: camera.update(s, a, u))

    dpg.add_mouse_move_handler(callback=lambda s, a, u: camera.move_handler(s, a, u))
    dpg.add_mouse_click_handler(dpg.mvMouseButton_Right, callback=lambda: camera.toggle_rotating())
    dpg.add_mouse_release_handler(dpg.mvMouseButton_Right, callback=lambda: camera.toggle_rotating())
    dpg.add_mouse_click_handler(dpg.mvMouseButton_Middle, callback=lambda: camera.toggle_moving())
    dpg.add_mouse_release_handler(dpg.mvMouseButton_Middle, callback=lambda: camera.toggle_moving())
    dpg.add_mouse_wheel_handler(callback=lambda s, a, u: camera.zoom(s, a, u))

# main loop
dpg.show_viewport()
while dpg.is_dearpygui_running():

    if camera.dirty:
        width = dpg.get_viewport_client_width()
        height = dpg.get_viewport_client_height()
        sphere.update_clip_space(width / 4, height / 4, width / 2, height / 2.0, -1.0, 1.0)
        # sphere2.update_clip_space(width / 4, height / 4, width / 2, height / 2.0, -1.0, 1.0)
        dpg.configure_item(rect, pmin=(width / 4, height / 4), pmax=(0.75 * width, 0.75 * height))
        view = camera.view_matrix()
        projection = camera.projection_matrix(width / 2, height / 2)

        dpg.apply_transform("gizmo", projection * view)
        dpg.set_clip_space("gizmo_layer", width / 4, height / 4, width / 2, height / 2.0, -1.0, 1.0)

        sphere.update(projection, view)
        # sphere2.update(projection, view)

        camera.dirty = False

    dpg.render_dearpygui_frame()

dpg.destroy_context()
