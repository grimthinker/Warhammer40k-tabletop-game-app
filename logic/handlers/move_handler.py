from actions import Action, DragData
from basic_data.dc import ControlEvent
from basic_data.enums import ControlEventTypes, ActionTypes
from basic_data.source import GREEN
from geometry.base import BaseObject
from logic.handlers.base import BaseHandler
from utils import to_screen_scale


class MoveHandler(BaseHandler):
    def __init__(self, game_loop):
        super(MoveHandler, self).__init__(game_loop)
        self.dragged_obj = None


    def handle(self, event):
        if event.mouse_motion:
            self.handle_mouse_motion(event)

        if event.type == ControlEventTypes.MOUSE_MAIN_DOWN:
            self.handle_main_mouse_down(event)

        if event.type == ControlEventTypes.MOUSE_MAIN_UP:
            self.handle_main_mouse_up(event)



    def handle_main_mouse_down(self, event: ControlEvent):
        if not self.current_action:
            for element in self.loop.interface.elements.interactive:
                # TODO: interact with some interface element
                pass
            for obj in self.gamedata.objects:
                if obj.check_point(event.pos) and self.check_draggable(obj):
                    # pygame.mouse.set_visible(False)
                    self.set_dragging_obj(obj)
                    data = DragData(obj, start_pos=obj.position, start_pos_z=obj.position_z)
                    self.current_action = Action(ActionTypes.DRAGGING_MODEL, data)
                    obj.make_dragging_line(GREEN, obj.position)
                    obj.make_move_line(GREEN, obj.position)
                    self.loop.interface.elements.temp.extend(obj.make_move_borders(GREEN, obj.position))
                    self.loop.interface.elements.temp.append(obj.make_footprint(GREEN))
                    break
            else:
                pass


    def handle_main_mouse_up(self, event):
        if self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_MODEL:
                # pygame.mouse.set_visible(True)
                self.dragged_obj.dragging = False
                self.loop.interface.elements.temp.remove(self.dragged_obj.last_footprint)
                for border in self.dragged_obj.last_move_borders:
                    self.loop.interface.elements.temp.remove(border)
                self.current_action.data.end_pos = self.dragged_obj.position
                self.current_action.data.end_pos_z = self.dragged_obj.position_z
                self.current_action.complete = True
                self.actions.append(self.current_action)
                self.current_action = None
                self.dragged_obj = None


    def handle_mouse_motion(self, event: ControlEvent):
        new_screen_pos = to_screen_scale(event.pos, self.camera.scale, *self.camera.pos, self.camera.angle)
        if self.loop.check_mouse_inside(new_screen_pos) and self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_MODEL:
                self.dragged_obj.noncollide_pos_simplest(
                    event.pos,
                    self.gamedata.objects,
                    True
                )


    def check_draggable(self, obj: BaseObject):
        current_player = self.loop.player_profile
        player_act = self.loop.player_act.player_profile
        obj_owner = obj.owner.player_profile
        if current_player is player_act and obj_owner is current_player:
            return True
        return False



    def set_dragging_obj(self, obj):
        obj.dragging = True
        self.dragged_obj = obj
