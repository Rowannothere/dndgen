from typing import Optional

import pygame
import pygame_gui
from pygame_gui.core import ObjectID

import scripts.game_structure.screen_settings
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.ui_elements import UISurfaceImageButton, UIImageButton
from scripts.housekeeping.version import get_version_info
from scripts.ui.generate_box import get_box, BoxStyles
from scripts.ui.generate_button import get_button_dict, ButtonStyles
from scripts.ui.get_arrow import get_arrow
from scripts.utility import (
    ui_scale,
    ui_scale_offset,
    ui_scale_dimensions,
    ui_scale_blit,
    get_text_box_theme,
)

game_frame: Optional[pygame.Surface] = None

menu_buttons = dict()

default_game_bgs = None
default_fullscreen_bgs = None

version_number = None
dev_watermark = None


def rebuild_core():
    global game_frame
    global menu_buttons
    global default_game_bgs
    global default_fullscreen_bgs
    global version_number
    global dev_watermark

    game_frame = get_box(
        BoxStyles.FRAME,
        (820, 720),
    )

    # menu buttons are used very often, so they are generated here.
    menu_buttons = dict()

    # they have to be added individually as some of them rely on others in anchors
    menu_buttons["events_screen"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((246, 60), (82, 30))),
        "Events",
        get_button_dict(ButtonStyles.MENU_LEFT, (82, 30)),
        visible=False,
        manager=MANAGER,
        object_id=ObjectID("#events_button", "@buttonstyles_menu_left"),
        starting_height=5,
    )
    menu_buttons["camp_screen"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((0, 60), (58, 30))),
        "Camp",
        get_button_dict(ButtonStyles.MENU_MIDDLE, (58, 30)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_menu_middle",
        starting_height=5,
        anchors={"left": "left", "left_target": menu_buttons["events_screen"]},
    )
    menu_buttons["catlist_screen"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((0, 60), (88, 30))),
        "Cat List",
        get_button_dict(ButtonStyles.MENU_MIDDLE, (88, 30)),
        visible=False,
        object_id="@buttonstyles_menu_middle",
        starting_height=5,
        anchors={"left": "left", "left_target": menu_buttons["camp_screen"]},
    )
    menu_buttons["patrol_screen"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((0, 60), (80, 30))),
        "Patrol",
        get_button_dict(ButtonStyles.MENU_RIGHT, (80, 30)),
        visible=False,
        manager=MANAGER,
        object_id="#patrol_button",
        starting_height=5,
        anchors={"left": "left", "left_target": menu_buttons["catlist_screen"]},
    )
    menu_buttons["main_menu"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 25), (153, 30))),
        get_arrow(3) + " Main Menu",
        get_button_dict(ButtonStyles.SQUOVAL, (153, 30)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_squoval",
        starting_height=5,
    )

    # used so we can anchor to the right with numbers that make sense
    scale_rect = ui_scale(pygame.Rect((0, 0), (118, 30)))
    scale_rect.topright = ui_scale_offset((-25, 25))
    menu_buttons["allegiances"] = UISurfaceImageButton(
        scale_rect,
        "Allegiances",
        get_button_dict(ButtonStyles.SQUOVAL, (118, 30)),
        visible=False,
        manager=MANAGER,
        object_id=ObjectID(class_id="@image_button", object_id=None),
        starting_height=5,
        anchors={"top": "top", "right": "right"},
    )

    # used so we can anchor to the right with numbers that make sense
    scale_rect = ui_scale(pygame.Rect((0, 0), (85, 30)))
    scale_rect.topright = ui_scale_offset((-25, 5))
    menu_buttons["clan_settings"] = UISurfaceImageButton(
        scale_rect,
        "Settings",
        get_button_dict(ButtonStyles.SQUOVAL, (85, 30)),
        visible=False,
        manager=MANAGER,
        object_id=ObjectID(class_id="@image_button", object_id=None),
        starting_height=5,
        anchors={"top_target": menu_buttons["allegiances"], "right": "right"},
    )
    del scale_rect

    heading_rect = ui_scale(pygame.Rect((0, 0), (190, 35)))
    heading_rect.bottomleft = ui_scale_dimensions((0, 0))
    menu_buttons["name_background"] = pygame_gui.elements.UIImage(
        heading_rect,
        pygame.transform.scale(
            image_cache.load_image("resources/images/clan_name_bg.png").convert_alpha(),
            ui_scale_dimensions((190, 35)),
        ),
        visible=False,
        manager=MANAGER,
        starting_height=5,
        anchors={
            "bottom": "bottom",
            "bottom_target": menu_buttons["camp_screen"],
            "centerx": "centerx",
        },
    )
    menu_buttons["moons_n_seasons"] = pygame_gui.elements.UIScrollingContainer(
        ui_scale(pygame.Rect((25, 60), (153, 75))),
        visible=False,
        allow_scroll_x=False,
        manager=MANAGER,
        starting_height=5,
    )
    menu_buttons["moons_n_seasons_arrow"] = UIImageButton(
        ui_scale(pygame.Rect((174, 80), (22, 34))),
        "",
        visible=False,
        manager=MANAGER,
        object_id="#arrow_mns_button",
        starting_height=5,
    )
    menu_buttons["dens_bar"] = pygame_gui.elements.UIImage(
        ui_scale(pygame.Rect((40, 60), (10, 160))),
        pygame.transform.scale(
            image_cache.load_image("resources/images/vertical_bar.png").convert_alpha(),
            ui_scale_dimensions((380, 70)),
        ),
        visible=False,
        starting_height=5,
        manager=MANAGER,
    )
    menu_buttons["dens"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 5), (71, 30))),
        "Dens",
        get_button_dict(ButtonStyles.SQUOVAL, (71, 30)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_squoval",
        starting_height=6,
        anchors={"top_target": menu_buttons["main_menu"]},
    )
    menu_buttons["lead_den"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 100), (112, 28))),
        "leader's den",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (112, 28)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_rounded_rect",
        starting_height=6,
    )
    menu_buttons["med_cat_den"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 140), (151, 28))),
        "medicine cat den",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (151, 28)),
        object_id="@buttonstyles_rounded_rect",
        visible=False,
        manager=MANAGER,
        starting_height=6,
    )
    menu_buttons["warrior_den"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 180), (121, 28))),
        "warriors' den",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (121, 28)),
        object_id="@buttonstyles_rounded_rect",
        visible=False,
        manager=MANAGER,
        starting_height=6,
    )
    menu_buttons["clearing"] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 220), (81, 28))),
        "clearing",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (81, 28)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_rounded_rect",
        starting_height=6,
    )
    heading_rect = ui_scale(pygame.Rect((0, 0), (195, 35)))
    heading_rect.bottomleft = ui_scale_offset((0, 0))
    menu_buttons["heading"] = pygame_gui.elements.UITextBox(
        "",
        heading_rect,
        visible=False,
        manager=MANAGER,
        object_id=ObjectID("#text_box_34_horizcenter", "#dark"),
        starting_height=5,
        anchors={
            "bottom": "bottom",
            "bottom_target": menu_buttons["camp_screen"],
            "centerx": "centerx",
        },
    )
    del heading_rect

    bg = pygame.Surface(scripts.game_structure.screen_settings.game_screen_size)
    bg.fill(game.config["theme"]["light_mode_background"])
    bg_dark = pygame.Surface(scripts.game_structure.screen_settings.game_screen_size)
    bg_dark.fill(game.config["theme"]["dark_mode_background"])

    default_game_bgs = {"default_light": bg, "default_dark": bg_dark}
    default_fullscreen_bgs = {
        "default_light": pygame.transform.scale(
            bg, scripts.game_structure.screen_settings.screen.get_size()
        ),
        "default_dark": pygame.transform.scale(
            bg_dark, scripts.game_structure.screen_settings.screen.get_size()
        ),
    }
    default_fullscreen_bgs["default_light"].blit(game_frame, ui_scale_blit((-10, -10)))
    default_fullscreen_bgs["default_dark"].blit(game_frame, ui_scale_blit((-10, -10)))

    version_number = pygame_gui.elements.UILabel(
        ui_scale(pygame.Rect((50, 50), (-1, -1))),
        get_version_info().version_number[0:8],
        object_id=get_text_box_theme(),
        anchors={"bottom": "bottom", "right": "right"},
    )
    # Adjust position
    version_number.set_relative_position(
        ui_scale_offset(
            (
                800 - version_number.get_relative_rect()[2],
                700 - version_number.get_relative_rect()[3],
            )
        )
    )

    if get_version_info().is_source_build or get_version_info().is_dev():
        dev_watermark = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((525, 660), (300, 50))),
            "Dev Build: " + version_number.text,
            object_id="#dev_watermark",
        )
        version_number.kill()
        version_number = None


rebuild_core()
