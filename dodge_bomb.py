import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
            pg.K_UP:(0, -5),
            pg.K_DOWN:(0, +5),
            pg.K_LEFT:(-5, 0),
            pg.K_RIGHT:(+5, 0),
        }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横，縦）/ 画面内：True，画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，
    泣いているこうかとん画像を貼り付ける関数
    引数：こうかとんSurface or 爆弾Surface 
    """
    # ブラックアウト
    bo_img = pg.Surface((WIDTH, HEIGHT))  # ブラックアウトのSurface
    pg.draw.rect(bo_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))  # 四角の描写
    bo_img.set_alpha(150)  # 透明度設定
    bo_rct = bo_img.get_rect()  # 四角の抽出
    screen.blit(bo_img, bo_rct) 
    #テキスト
    fonto = pg.font.Font(None, 80)   # フォント設定
    txt = fonto.render("Game Over", True, (255, 255, 255))  
    txt_rct = txt.get_rect(center = (WIDTH//2, HEIGHT//2))  # テキスト抽出と位置
    screen.blit(txt, txt_rct)
    #泣きこうかとん
    kk_TT_img = pg.image.load("fig/8.png")  
    TT_rct = kk_TT_img.get_rect(center = (WIDTH//3, HEIGHT//2))  # 泣きこうかとん抽出と位置
    TT_rct2 = kk_TT_img.get_rect(center = (WIDTH*2//3, HEIGHT//2))
    screen.blit(kk_TT_img, TT_rct)
    screen.blit(kk_TT_img, TT_rct2)


#def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
   # """
   # サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
   # """
    #accs = [a for a in range(1, 11)]
    #for r in range(1, 11):
        #bb_img = pg.Surface((20*r, 20*r))
        #pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        #演習２途中



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10),10)  #爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過
    bb_rct = bb_img.get_rect()  #爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  #爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0

    #bb_imgs, bb_accs = init_bb_imgs()
    #avx = vx*bb_accs[min(tmr//500, 9)]
    #bb_img = bb_imgs[min(tmr//500, 9)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # 練習3    
        #if kk_rct.colliderect(bb_rct):
           # print("ゲームオーバー")
           # return
        # ゲームオーバー呼出
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            pg.display.update()
            time.sleep(5)  #５秒間表示
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        # 爆弾は画面内
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
