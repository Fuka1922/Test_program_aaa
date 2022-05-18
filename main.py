#ブロック崩し 
print("[[[ Start ]]]") #きちんとここから実行される。


# 
import pygame          #メインGUI
from pygame.locals import * #おまじない
import math            #球の起動計算とか？
import sys             #安全なシステムの終了
import pygame.mixer    #

import random          #乱数発生
import time            #FPS等を記録
import datetime        #↑のサブ






""" 変数(システム) """
app_ver = 0.01
debug_mode = 1       #　[[[SW]]] デバッグモード　0=OFF(ﾘﾘｰｽ版)　　1=ON(開発版)
log_mode = 1         # [[[SW]]] コンソールにいろいろ記録（出力）します。 0=OFF / 1=ON
if debug_mode == 1:  # デバッグ時は強制的にログモードをONにします。
    log_mode = 1


Text_Qu = True       # [[[SW]]] テキスト品質    0=Low(アンチエイリアス無)    1=高(ア有)     ※重くなります。
Pic_Qu = True        # [[[SW]]] グラフィック品質  0=Low(アンチエイリアス有)    1=高（ア有）     ※重くなります。
BGM_ON = 1           # [[[SW]]] 音楽の有無    0=Mute   1=ON
SE_ON = 1            # [[[SW]]] 効果音の有無  0=Mute   1=ON
CV_ON = 1            # [[[SW]]] 声の有無      0=Mute   1=ON



#画面
(screen_x, screen_y) = (400, 800)   ##モニターサイズ（描画座標は相対座標を想定してないので基本は変更しない。）
full_screen_mode = 0 # [[[SW]]]  0=Window / 1=FullScreen
screen_redraw_type=1 #　[[[SW]]]  0=display.update  /  1=display.flip
(c1,c2,c3) = (0,0,100) # 背景色(R,G,B)

#FPS
FPS = 60             #フレームレート定義
fps_A = 0            #計測始点
fps_B = 0            #計測終点
fps_1f = 0           #B - Aによる1フレーム辺りの時間
fps_integral = 0     #積分値 1 secを越えるとリセット
fps_count = 0        #fpsカウント
fps_show = 0         #表示fps

#coma変数
coma2 = 0    #coma系はグローバル変数にしておく
coma3 = 0
coma4 = 0
coma5 = 0
coma10 = 0
coma16 = 0
coma20 = 0
coma30 = 0
coma60 = 0
coma120 = 0
coma240 = 0
coma480 = 0


#マウスポインタ用変数
(mouse_x, mouse_y) = ((screen_x/2), (screen_y/2))#ポインタの初期座標
mouse_click_L = 0        #通常クリック   0=待機状態    1~=クリック状態。押してるループ時間分数値が増え続ける。一瞬でも話すと0から
mouse_click_pre_L = 0    #前フレームの状態。この値との差でクリックしたかを判定
mouse_click_R = 0        #右クリック
mp_ID = 0                #描画するマウスポインタのアニメーション識別用
(mp_sx, mp_sy) = (32,32) #一応マウスポインタのサイズを格納しておく。　変動するならその都度get_rectを行なう抽出する。

carsol_trigger = 0       #マウスの位置によって発生するイベントの種類　（クリックと併用でボタン機能になる。）





#メディア用変数
bgm_ID = 0           #再生するBGMの種類   0を代入して関数をCallすると停止 （引数として利用）
bgm_ID_keep = bgm_ID #戦闘前に流れていた曲を記録
bgm_now = 0          #現在どのBGMを再生しているか記憶する。　※pygameが一部BGMをループ再生させないバグ？対策
se_ID = 0            #再生するseの種類　                              （引数として利用）







""" 変数(ゲーム) """
Stage = 1
Level = 1
Time = 0



""" 変数(セーブ部分) """









print("変数宣言終了") #きちんとここから実行される。

##############################################################################################################
"★★　Pygameモジュールの初期化　★★"
##############################################################################################################
"▼▼ pygameモジュール全体の初期化"
pygame.init()                                                           # 初期化(pygame.xxx系の関数が以降有効)
#screen.set_alpha(None)#アルファ合成？をOFF ←半透明は使いたい

"▼▼　ウインドウ画面を設定"
if full_screen_mode == 0:
    screen = pygame.display.set_mode((screen_x, screen_y), DOUBLEBUF)               # 画面初期化(ウインドウ)
if full_screen_mode == 1:
    screen = pygame.display.set_mode((screen_x, screen_y), FULLSCREEN | DOUBLEBUF)  # 画面初期化(ウインドウ)


"▼▼ windowsのマウスポインタを非表示化"
#pygame.mouse.set_visible(False) # マウスカーソルを消す


"▼▼　ウインドウタイトルを設定"
nn = "スマホサイズの動的アプリの基礎  /  Ver." + str(app_ver)
pygame.display.set_caption(nn)             




##############################################################################################################
"★★　日本語フォントの読込　★★"
##############################################################################################################
"各種フォントを読込"
font0 = pygame.font.Font(None, 24)                              # デフォルトフォント （日本語無し）
font1 = pygame.font.Font("font/1__nicoca_v1.ttf", 28)           # ニコカフォント　  （人型キャラクター）
font2 = pygame.font.Font("font/2__mitsubachi_font_v1.ttf", 20)  # みつばちフォント （ぼたもちキャラクター）

















"▼▼ 効果音を読込　　　容量の嵩張る音楽と違い、一度に全部読込む"
oto_se = [0] * 50


oto_se[0]   = pygame.mixer.Sound("se/000.wav") # 無音
oto_se[10]  = pygame.mixer.Sound("se/010.wav") #反射音1
oto_se[20]  = pygame.mixer.Sound("se/020.wav") #破壊音1-1
oto_se[21]  = pygame.mixer.Sound("se/021.wav") #破壊音1-2







##############################################################################################################
##############################################################################################################
"★★★　各種サブルーチンの処理　★★★　　　アプリ本編となる、main() 関数からコールされたときのみ処理する。"
##############################################################################################################
##############################################################################################################




class Subs:



    def fps_reset():
        "■　FPS算出に関連する変数を初期化"
        #グローバル変数を継承
        global fps_A, fps_B, fps_1f, fps_integral, fps_count, fps_show
        #各変数のクリア
        fps_A = 0            #計測始点
        fps_B = 0            #計測終点
        fps_1f = 0           #B - Aによる1フレーム辺りの時間
        fps_integral = 0     #積分値 1 secを越えるとリセット
        fps_count = 0        #fpsカウント
        fps_show = 0         #表示fps



    def fps_calc():
        "■　FPS算出　※timeモジュール使用"
        #グローバル変数を継承
        global fps_A, fps_B, fps_1f, fps_integral, fps_count, fps_show
        #FPSの計算
        fps_count += 1             #とりあえずフレーム数カウント
        fps_B = time.time()        #時間計測-終点-
        fps_1f = fps_B - fps_A     #始点から終点までの時間をナノ秒で取得
        fps_A = time.time()        #時間計測-始点-
        
        fps_integral += fps_1f     #求めた経過時間を積算値へ加算
        if fps_integral >= 1.000000:
            fps_show = fps_count   #積算値が1秒を越えたら表示用フレームレートへ代入
            fps_count = 0          #カウントをﾘｾｯﾄ
            fps_integral = 0       #積算値をリセット


    def fps_UI(nnn):
        global mouse_x, mouse_y
        
        "■　FPS表示"
        " Subs.fps_UI(p1)  /   p1:nnn=0:黒色フォント, =1白色フォント　int型　(現状2～は全て1と見なし白色)"
        for i in range(1,3,1): #i=0,1,2とループする。
            "色の指定"
            if nnn == 0: #黒メイン
                nn = 255#枠色
                if i==2:
                    nn = (0+(coma10*1))
            if nnn > 0:  #白メイン
                nn= 0#枠色
                if i==2:
                    nn = (255-(coma10*1))
            "差分位置の指定"
            nnnn = -1 + (i * 2)#枠
            if i==2:
                nnnn = 0
            "描画"
            text = font1.render(("FPS"), Text_Qu, (int(nn*0.9), int(nn*0.9), nn))
            screen.blit(text, [5+nnnn, 0+nnnn])   # 文字列の表示位置
            text = font1.render(("{}".format(fps_show)), Text_Qu, (int(nn*0.9), int(nn*0.9), nn))
            screen.blit(text, [72+nnnn, 1+nnnn])  # 文字列の表示位置
            
            "mouse"
            #mm = ("Mouse X:" & str(mouse_x) + "  Y:" + str(mouse_y))
            text = font0.render(("Mouse:"), Text_Qu, (int(nn*0.9), int(nn*0.9), nn))
            screen.blit(text, [5+nnnn, 30+nnnn])   # 文字列の表示位置
            text = font0.render((str(int(mouse_x))), Text_Qu, (int(nn*0.9), int(nn*0.9), nn))
            screen.blit(text, [70+nnnn, 30+nnnn])   # 文字列の表示位置
            text = font0.render((str(int(mouse_y))), Text_Qu, (int(nn*0.9), int(nn*0.9), nn))
            screen.blit(text, [110+nnnn, 30+nnnn])   # 文字列の表示位置



    "▼01 画面の更新"
    def screen_redraw():
        "■　画面の更新"
        # 反映フェーズ
        if screen_redraw_type == 0:
            pygame.display.update(Rect(2, 2, (screen_x - 4), (screen_y - 4))) # 指定領域の画面を更新
        elif screen_redraw_type == 1:
            pygame.display.flip()             # 画面を更新（こっちの方が速い？）
        else:
            pygame.display.update()           # どの条件にも合致しない場合はupdateで処理
        # 待機フェーズ
        #fps_clock.tick(FPS)              # 60fps ※採用するとなぜかエラー終了するので暫く様子見
        pygame.time.wait(int(900 / FPS))  # ウェイト待ち ／　割ると少数点が出るのでエラー回避のためにint型でキャスト
        #pygame.time.wait(16)

    def comas_reset():
        "■　coma系をクリア"
        #グローバル変数を継承
        global coma2, coma3, coma4, coma5, coma10, coma16, coma20, coma30, coma60, coma120, coma240, coma480
        #各comaのクリア　何となく単位毎に分ける
        (coma2, coma3, coma4, coma5) = (0,0,0,0)
        (coma10, coma16, coma20, coma30, coma60) = (0,0,0,0,0)
        (coma120, coma240, coma480) = (0,0,0)


    def comas_add():
        "■　coma系の加算"
        #グローバル変数を継承
        global coma2, coma3, coma4, coma5, coma10, coma16, coma20, coma30, coma60, coma120, coma240, coma480
        #各comaの加算
        coma2 += 1
        if coma2 == 2:
            coma2 = 0
        coma3 += 1
        if coma3 == 3:
            coma3 = 0
        coma4 += 1
        if coma4 == 4:
            coma4 = 0
        coma5 += 1
        if coma5 == 5:
            coma5 = 0
        coma10 += 1
        if coma10 == 10:
            coma10 = 0
        coma16 += 1
        if coma16 == 16:
            coma16 = 0
        coma20 += 1
        if coma20 == 20:
            coma20 = 0
        coma30 += 1
        if coma30 == 30:
            coma30 = 0
        coma60 += 1
        if coma60 == 60:
            coma60 = 0
        coma120 += 1
        if coma120 == 120:
            coma120 = 0
        coma240 += 1
        if coma240 == 240:
            coma240 = 0
        coma480 += 1
        if coma480 == 480:
            coma480 = 0












    def event_controll():
        "■ マウスやキーボードの入力検出に関連するイベント"
        "  メニュー画面と併用しても誤作動が起きないような処理にしたい。。"
        # グローバル変数を継承
        global mouse_click_L, mouse_click_pre_L, mouse_click_R #マウス関連
        global screen_page, t_time, break_time
        global m_mode, m_time #メニュー関連
        global b_mode, b_time #戦闘関連
        #
        "▼前フレームのマウスクリック時間を検出"
        mouse_click_pre_L = mouse_click_L
        #
        for event in pygame.event.get():
            "▼▼▼ 強制終了[×]ボタン終了 ▼▼▼"
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                #[Log] メニューを終了させた旨
                if log_mode == 1:
                    print("[[[ End ]]]")
                pygame.quit()       # Pygameモジュールの終了宣言
                sys.exit()          # 穏便にアプリを終了

            "▼▼▼ キーボードのボタンに対応 ▼▼▼"
            if event.type == KEYDOWN:
                "[Esc]強制終了 or タイトルに戻る？"
                if event.key == K_ESCAPE:
                    print("[[[ End ]]]")
                    pygame.quit()   # Pygameモジュールの終了宣言
                    sys.exit()      # 穏便にアプリを終了


            #             "▼ それ以外はタイトル画面へ"
            #             if screen_page > 5:
            #                 screen_page = 5 #タイトルページを指定
            #                 break_time = 60 #ブレイクタイムをMAXにする。コールしたメインループでの60fpsを待たない。
            #                 #[Log] メニューを終了させた旨
            #                 if log_mode == 1:
            #                     print ("Pressed ESC key, goto title page.")
            #                 break
            #                 #pygame.quit()   # Pygameモジュールの終了宣言
            #                 #sys.exit()      # 穏便にアプリを終了
            #         "▼▼ メニューモードで時の処理"
            #         if m_mode == 1:
            #             if m_time < 1000000:
            #                 Subs.se_run(22)          #[Call][SE] メニューClose
            #                 m_time = 1000000

            #     "[[P]]スクリーンショット"
            #     if event.key == K_p:
            #         #参考：　https://www.sejuku.net/blog/23606
            #         mm = datetime.datetime.now()                        #日時の取得
            #         mmm = mm.strftime("%Y-%m-%d_%H-%M-%S")              #指定した体裁に変更　＆　日付型から文字列型へ変更
            #         mmmm = "___Screen_shot/Screen_shot_" + mmm + ".png" #パス＆ファイル名を指定
            #         pygame.image.save(screen, str(mmmm))                #キャプチャ映像の保存

            #     "[[M]]メニューの呼び出し"
            #     if event.key == K_m:
            #         "呼び出し可能なページを指定"
            #         if (screen_page == 20)|(screen_page == 30):
            #             "メニュー画面IN"
            #             if m_mode == 0:
            #                 "メインループはここで止まる。ネストが狂わないように注意する。"
            #                 Subs.menu_top()
            #             "メニュー画面OUT"
            #             if m_mode == 1:
            #                 if m_time < 1000000:
            #                     Subs.se_run(22)          #[Call][SE] メニューClose
            #                     m_time = 1000000

            #     "[[B]]戦闘画面の呼び出し"
            #     if debug_mode == 1:
            #         if event.key == K_b:
            #             if b_mode == 0:
            #                 "戦闘イベントモジュール"
            #                 b_mode = 1              #戦闘モードON
            #                 Subs.se_run(38)        #[Call][SE]
            #                 Subs.fade_out_eff(2,0)  #エンカウントエフェクト
            #                 Battle.battle_main(1)   #戦闘パート / p1:0=逃走不可,1=可 / p2:
            #                 "↑ 引数1 (b_esc) :  0=撤退NG（ボス・イベント戦等用）　　／　　1=撤退OK"

            #             elif b_mode == 1:
            #                 "特に何もしない？　強制終了はありかも"
            #                 b_time = 100000 #終了

            #     "[[S]]デバッグ用　セーブ"
            #     if debug_mode == 1:
            #         if event.key == K_s:
            #             nn = 0#エラー回避
            #             "ファイルは保存されるがフリーズする。。"
            #             #dill.dump_session('___Save_data/userdata.pkl')

            #     "[[L]]デバッグ用　ロード"
            #     if debug_mode == 1:
            #         if event.key == K_l:
            #             nn = 0#エラー回避
            #             #dill.load_session('___Save_data/userdata.pkl')

            #     "[[T]]デバッグ用　色々な試験機能"
            #     if debug_mode == 1:
            #         if event.key == K_t:
            #             nn = 0 #Blank対策
            #             "暗転機能 30fps"
            #             "備考：　キー入力を指定していないが、入力した場合、エフェクト後に処理してくれる。"
            #             "　　　　　マウスポインタは残像が残るので関数を呼ばない。"
            #             Subs.fade_out_eff(1,coma2) #[Call][Wall] ランダムフェードアウトテスト



            "▼▼▼ マウス操作 ▼▼▼   （ハイブリッド方式　下記どちらかを満たせばｸﾘｯｸ・ｸﾘｯｸ中の判定）"
            hits = 0
            "▼ マウス操作　（イベントハンドラタイプ　※ドラッグが難しいので現状は没）"
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                hits = 1

            "▼ マウス操作　（関数タイプ　※ドラッグしながらの反応が鈍い）"
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                hits = 1

            "▼ どちらかが有効ならクリック中扱い"
            if hits == 1:
                mouse_click_L += 1
                if mouse_click_L == 1:
                    ""
                    #Subs.se_run(1 + coma3)     #[Call][SE] クリック音(3種から疑似ランダム)
            else:
                mouse_click_L = 0 #未入力ならすぐ０に戻る。







##############################################################################################################
############################################################################################################################################################################################################################
"★★★　ここからメイン関数　★★★　　　何度か行なう初期設定＆アプリの開始！"
##############################################################################################################
##############################################################################################################
def main():
    "▼01 変数以外の初期設定"
    
    "▼01 ★　変数の初期値設定　　＆　　ローカル「main()」中で値を変更させる（見込含む）グローバル関数を継承　★"
    "▽01 システム変数"
    global screen_x, screen_y
    global mouse_x, mouse_y, mouse_click_L, mouse_click_pre_L, mouse_click_R #マウス時間
    global c1,c2,c3
    global fps_A, fps_B, fps_1f, fps_integral, fps_count, fps_show
    global Time
    
    
    
    
    ###########################################################################
    "▼01 ★ メインループ ★"
    ###########################################################################
    while (10):
        "ここからメインループ"

        "▼▼ 画面を更地"
        screen.fill((c1,c2,c3))    # 画面を黒色に塗りつぶし

        "▼▼ 変数等の処理フェーズ"
        "▼ 時間の経過"
        Time += 1 #Subs.timers_add()          #[Call] time系の加算
        Subs.comas_add()           #[Call] coma系の処理
        
        "▼ fpsの算出"
        Subs.fps_calc()            #[Call] FPSの算出

        "▼ マウスポインタの座標を取得"
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        print("mouse (" + str(mouse_x) + ", " + str(mouse_y) + ")")

        
        
        
        
        "▼▼ オブジェクト等の描画フェーズ　　（オフスクリーンバッファで描画）"
        
        
        #
        "▼ イベント処理 (非トリガータイプのキー処理もここで)"
        Subs.event_controll()      #[Call] マウス・キーボードによる基本操作
        
        #
        "▼ FPSのUIを描画"
        Subs.fps_UI(1)  #[Call] FPSの描画
        
        print("Time = " + str(Time) + "  /  FPS = " + str(fps_show)) #
        
        #
        "▼ 描画したオブジェクトを一括反映"
        Subs.screen_redraw()     
        
        
        #######################################################################



























"おまじない"
#　意味について
#　https://paloma69.hatenablog.com/entry/2018/06/28/005550
if __name__ == "__main__":
    print("main : ", __name__)
    main()