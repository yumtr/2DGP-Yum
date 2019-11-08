# coding=utf-8
from pico2d import *
import game_framework
import pause_state
import title_state

from class_Group import Group
from class_Stone import Stone
from class_Stage import Stage, handle_Stage, cac, block

MAP_WIDTH = 900
MAP_HEIGHT = 800
debug_mode = False

player = None
game_stage = None
cactus_group = None

LEFT_COLLISION, TOP_COLLISION, RIGHT_COLLISION, BOTTOM_COLLISION = range(4)
ST_X_NONE, ST_X_FORWARD, ST_X_BAKWARD, ST_Y_NONE, ST_Y_UP, ST_Y_DOWN = range(6)


def handle_events():
    global debug_mode
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_i:
                debug_mode = not debug_mode
                cactus_group.print_g()
            elif event.key == SDLK_p:
                game_framework.push_state(pause_state)
            else:
                handle_Stage(event)
                player.handle_Stone(event)
        elif event.type == SDL_KEYUP:
            handle_Stage(event)
            player.handle_Stone(event)


def enter():
    global player, game_stage, cactus_group
    player = Stone()
    cactus_group = Group()
    game_stage = Stage()
    game_stage.easy_stage()
    game_stage.setting_stage()


def exit():
    global player, game_stage, cactus_group
    del player 
    del game_stage
    del cactus_group


def pause(): pass


def resume(): pass


def update_cactus():
    # 전체 선인장
    for i in range(game_stage.cac_count):
        cac[i].update()
        cac[i].collision_to_player(i)
        for j in range(game_stage.cac_count):
            if not i == j:
                cac[i].set_collision_state(cac[j])


def update_block():
    # 벽 업데이트
    for i in range(game_stage.block_count):
        block[i].update()
    cactus_group.update()


def update():
    game_stage.check_stage_clear()
    player.update()
    update_cactus()
    update_block()
    handle_events()
    update_canvas()


def draw():
    game_stage.draw_stage()
    player.render()
    # 벽 그리기
    for i in range(game_stage.block_count):
        block[i].render()
    # 선인장 그리기
    for i in range(game_stage.cac_count):
        cac[i].render()
    delay(0.03)
