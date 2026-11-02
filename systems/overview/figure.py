"""全体図（cover.png）。AI に任せている仕組み全部を、データの流れで 1 枚にまとめる。
左から右へ「入口 → ChatGPT → 置き場（Gmail・Todoist・Google カレンダー・Keepa・Notion・Amazon・YouTube・GitHub）→ Claude Code → 出す物」。本人は上の中央に 1 回だけ。

再生成（リポジトリの根から）:
    python3 systems/overview/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントの道は位置引数でも受け付ける。出力は同じフォルダの cover.png）

入れた仕組み（このカタログの事例・全体構成）: cases/daily-email-triage, systems/daily-task-hub, cases/youtube-playlist-cleanup,
systems/context-reading-loop（読書の記録と自分のメモ）, cases/allowance-shopping-plan, cases/shopping-decision-notes, systems/cross-task-board,
cases/handoff-and-todo-files, cases/dev-dashboard-hub, cases/article-drafting-workflow,
メルカリのお買い得探し（ChatGPT のメルカリプラグインが Notion の欲しい物リストを読む）
外した仕組み：cases/bookmark-to-action（X → ChatGPT → Raindrop の振り分け）。今は動かしていないので描かない（今動いている流れだけを描く。2026-11-02）

描き方の決まり（AGENTS.md「見せ方と図」。2026-11-01 本人が選んだ流儀）:
- 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow() だけ。ラベルは動くデータの名詞
- 読まれる側を左、AI を中央、書かれる側を右。往復の矢印は描かない
- 読み書き両方の相手は束ねず、同じロゴを左（読まれる側）と右（書かれる側）に 2 回置く
  （ChatGPT と Gmail・Todoist・GitHub・YouTube・Notion、Claude Code と Todoist・Notion・GitHub）
- 本人は ChatGPT と Claude Code の間の上に 1 回だけ置く。話した内容は左へ渡って ChatGPT の左の辺に入り、
  依頼は右へ渡って Claude Code の上の辺に入る。
  朝の報告だけ ChatGPT の右の辺から本人のスマホ（縦長。この図の中で描く）へ上がる。矢印は 1 色（fk.TEAL）。出す物（画面・記事・本棚）から本人へ戻す線は描かない
- 話した内容が ChatGPT に入る高さ（R0）は、朝の報告が出る高さ（R2）より下にずらす。
  同じ高さだと 本人 → ChatGPT → 本人 が 1 つの輪に見えるため（2 つの間を行き来する形は残る。本人へ直接返すという指示を優先した）
- AI の札の下の動詞は fk.verb()（灰色・24px）
- 定期実行のきっかけは fk.trigger() で ChatGPT の札の真上に置く。開発ダッシュボードの 30 分ごと（systemd の集計。AI ではない）は
  ダッシュボードの画面の左横に置き、Claude Code の札と動詞から離す
- ロゴの札には全部、札の下にサービスの名前を付ける（ロゴだけでは知らない人に分からない。2026-11-02 点検）。
  行の間は 125px あけ、名前と次の行の線のラベルが重ならないようにする
- ChatGPT の左の GitHub（毎回読む置き場。最初に決めて置いた物なので本人からは引かない）は、中身の違う 2 つに分ける。どちらも錠の印（非公開）：
  「手順書」＝メールの判定の手順（cases/daily-email-triage）。
  「自分のメモ」＝整理の基準（毎朝の Todoist 整理）と今の状況・目標（週次の読書レビューが読む）。
  置き場の非公開のメモも「自分のメモ」と呼ぶ（同じ物は同じ名前。本文も「自分のメモ」）。
  錠の無い札（公開）：読書の記録（reading-log）。
  左の GitHub は ChatGPT の右に出る線の無い高さ（Google カレンダー・Keepa の行）に置く。
  reading-log（左）は ChatGPT が reading-log へ書く行と同じ高さに置く（ほかの行の高さだと、その行の出力の元に読まれる。2026-11-02 点検）
  線の間は 64px あけ、ラベルは自分の線のすぐ上に寄せる（上下どちらの線のラベルか読み分けられるように）
- メルカリでのお買い得探しは、大きな ChatGPT の札とは別に、一番下の行に fk.plugin('openai', 'mercari') の 1 枚の札で描く
  （AI がプラグインで別のサービスを使うときは 1 枚の札。2026-11-02 本人「チャット GPT とメルカリのロゴが掛け合わさってるみたいな見せ方」）。
  Notion → プラグインの札（欲しい物。定価も入っている）→ 右の列の提案（お買い得の候補）の 1 本の鎖。
  メルカリの札を別に置かない。線のラベルに「と」で 2 つ並べない（「欲しい物と定価」は誤読されるので「欲しい物」。定価と比べるのは動詞に書く）
- 札の下から出る線（進捗・本人待ち、公開の本棚へ）は名前の下から出す。置き場の自分のメモの錠は右上の角に付ける
- 同じ高さには本当につながる物だけを並べる（ChatGPT や Claude Code を挟んで別の流れが 1 本に読めないように）。
  Gmail の行は Gmail → ChatGPT → Gmail（仕分けラベル）、Todoist の行は Todoist → ChatGPT → Todoist → Claude Code → 横断タスクボード、
  Notion の行は ChatGPT → Notion → Claude Code → 買い物の計画画面（ChatGPT が調べて比べた欲しい物を Notion に登録する。cases/allowance-shopping-plan）。
  作業メモの行は GitHub → Claude Code → GitHub → 開発ダッシュボード。Qiita・note・Notion（棚卸しの結果）・Todoist（完了）は
  Claude Code に線の入らない高さに置く
- 置き場の GitHub は 3 つに分ける：自分のメモ（錠の印。非公開。ChatGPT が今の状況・目標を書く）、
  作業のリポジトリ（Claude Code が作業メモ＝引き継ぎを読む）、reading-log（ChatGPT が読書の記録を書く。次に読む本の週次レビューも
  この記録に含めて 1 本にする。並んで走る矢印を減らすため。2026-11-02）。
  公開の読書の本棚は reading-log からだけ下を回って右へ出す（非公開の目標が公開サイトへ流れるように見せない）
- 記事は Claude Code から Qiita と note の両方へ（cases/article-drafting-workflow：AI の活用は Qiita のあと note 版、商品紹介は note だけ）
  note の線のラベルは「note 版」（Qiita と同じ「記事」の 2 本並びは同時に出しているように見えるため）。
  note の矢印は「Claude Code が note 版の下書きを書く」まで。note へ上げるのは本人（下書きの自動保存は予定なので描かず、本文に書く）
- 今動いている流れだけを描く（点線は使わない。2026-11-02）
- 並んで走る矢印を減らし、左から右への鎖で順番を読ませる（2026-11-02 本人「平行してる矢印が多すぎると、なんか順番がわかんなくなる」）
- 買い物の計画画面の入力は 3 本：Keepa（値段の履歴）・Notion（欲しい物）・Amazon（セール日程）を置き場の列に縦に並べ、Claude Code へ。
  Claude Code から Notion へ戻す線は「棚卸しの結果」（cases/allowance-shopping-plan：棚卸しの結果と点数を Claude が Notion に反映）
- 言葉は全体でそろえる（2026-11-02）：本人の確認待ちは「本人待ち」、引き継ぎは「作業メモ」、現在地は「今の状況」、出力の吹き出しは「提案」
- 線のラベルは名詞 2 つを「と」で並べず「・」でつなぐ（今の状況・目標）。12 字以内
- 縦に収まらないので、画布をこのファイルの中で 1440×2120 に広げる（上下の余白は保存の前に切り詰める）
- ロゴの数が多く、fk.save() の 128 色では Qiita の緑が茶色に落ちるので、同じ切り詰めをこのファイルで行い 256 色で保存する
"""
import argparse
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import figkit as fk  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('font_pos', nargs='?')
ap.add_argument('--font')
a = ap.parse_args()
fk.init(a.font or a.font_pos)
fk.begin()
from PIL import Image, ImageDraw  # noqa: E402
fk.im = Image.new('RGB', (1440, 2120), fk.PAPER)   # 縦に長い図なので画布だけ広げる（部品は fk のまま）
fk.d = ImageDraw.Draw(fk.im)
d = fk.d

LS = 21  # 線のラベルの文字の大きさ


# ── 部品（この図だけで使う） ────────────────────────────────
def ai_card(name, label, cx, top, bottom, w=150):
    """縦長の AI の札。左右の辺に何本も線を受けられるように、ロゴと名前を中に入れる。"""
    fk.rr((cx - w / 2, top, cx + w / 2, bottom), 'white', fk.LINE, 3, 22)
    mid = (top + bottom) / 2
    fk.logo(name, cx, mid - 22, 86)
    fk.centered(cx, mid + 34, label, 22)   # 「Claude Code」が札の幅に収まる大きさ


def tile(name, cx, cy, size=76):
    """サービスのロゴの札（名前は named() で下に付ける）。"""
    fk.service(name, cx, cy, tile=size)


def text_tile(label, cx, cy, w=116, h=76):
    """ロゴの無いサービスの札（名前の文字だけ）。左の辺の x を返す。"""
    fk.rr((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 'white', fk.LINE, 3, 22)
    fk.centered(cx, cy - 17, label, 23)
    return cx - w / 2


def lock(lx, ly, c=fk.BLUE):
    """非公開の印。札の角に付ける小さな錠（systems/context-reading-loop と同じ形）。"""
    d.arc((lx - 11, ly - 26, lx + 11, ly - 2), 180, 360, fill=c, width=5)
    fk.rr((lx - 16, ly - 10, lx + 16, ly + 16), 'white', c, 3, 6)
    d.ellipse((lx - 4, ly - 1, lx + 4, ly + 7), fill=c)


def screen(cx, cy, label, kind, w=130, h=56, c=fk.TEAL):
    """画面そのもの（サービスを指さない）。kind で中の絵を変える。下に名前。"""
    x, y = cx - w / 2, cy - h / 2
    fk.rr((x, y, x + w, y + h), '#eaf3f1', c, 3, 10)
    ix, iy, iw = x + 10, y + 9, w - 20
    fk.rr((ix, iy, x + w - 10, y + h - 9), 'white', c, 2, 7)
    if kind == 'board':      # 時間割：高さの違う帯
        for k in range(3):
            d.rectangle((ix + 10 + k * 34, iy + 7, ix + 34 + k * 34, iy + 15 + k * 7), fill=fk.TEAL)
    elif kind == 'plan':     # 買い物の計画：並べた行と点数の丸
        for k in range(3):
            yy = iy + 8 + k * 11
            d.ellipse((ix + 9, yy - 4, ix + 17, yy + 4), fill=fk.AMBER)
            d.line((ix + 24, yy, ix + iw - 12 - k * 18, yy), fill=fk.LINE, width=5)
    elif kind == 'dash':     # ダッシュボード：進捗の棒
        for k, frac in enumerate((.8, .45, .6)):
            yy = iy + 6 + k * 11
            d.rectangle((ix + 9, yy, ix + iw - 9, yy + 7), fill=fk.LINE)
            d.rectangle((ix + 9, yy, ix + 9 + (iw - 18) * frac, yy + 7), fill=fk.BLUE)
    elif kind == 'chat':     # 提案：候補の印と文の行
        for k in range(3):
            yy = iy + 8 + k * 11
            d.rectangle((ix + 8, yy - 4, ix + 16, yy + 4), fill=fk.NOTE, outline=fk.AMBER)
            d.line((ix + 24, yy, ix + iw - 10 - k * 22, yy), fill=fk.LINE, width=5)
    elif kind == 'shelf':    # 本棚：並んだ背表紙
        d.line((ix + 4, iy + 32, x + w - 14, iy + 32), fill=c, width=3)
        bx = ix + 10
        for bw, bh, col in ((12, 22, fk.TEAL), (15, 26, fk.AMBER), (11, 20, fk.BLUE),
                            (16, 24, fk.TEAL), (12, 22, fk.AMBER), (14, 26, fk.BLUE)):
            d.rectangle((bx, iy + 32 - bh, bx + bw, iy + 31), fill=col)
            bx += bw + 3
    fk.centered(cx, y + h + 2, label, 22)   # 名前は自分の画面に寄せる（次の物とは 20px 以上あける）


# ── 位置 ───────────────────────────────────────────────────
A, C, E = 95, 660, 1265             # 入口・置き場・出す物の列（中心）
GX, CX = 370, 915                   # ChatGPT・Claude Code の札の中心
AW = 150                            # AI の札の幅
G_L, G_R = GX - AW / 2, GX + AW / 2
C_L, C_R = CX - AW / 2, CX + AW / 2
T = 76                              # ロゴだけの札の大きさ
S_L, S_R = C - T / 2, C + T / 2     # 置き場の札の左右
SW = 130                            # 出す物の画面の幅
E_L = E - SW / 2


def lab_at(x0, x1, y, dy=-44, label=None):
    """横の線のラベルの位置（線の上。dy を正にすると線の下）。x0・x1 は線の両端の物の辺。

    label を渡すと、矢じり（右端の 26px）にかからないよう、左の物から 8px あけられる範囲で左へ寄せる。
    """
    x = (x0 + x1) / 2
    if label:
        w = fk.width(label, LS)
        x = max(min(x, x1 - 26 - w / 2), x0 + 8 + w / 2)
    return (x, y + dy)


def phone(x, y, w=66, h=112):
    """本人のスマホ（縦長）。上に受話口、下にホームの線、中に届いた知らせの札。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.INK, 4, 14)
    d.line((x + w / 2 - 9, y + 10, x + w / 2 + 9, y + 10), fill=fk.INK, width=3)
    d.line((x + w / 2 - 11, y + h - 11, x + w / 2 + 11, y + h - 11), fill=fk.INK, width=4)
    fk.rr((x + 8, y + 22, x + w - 8, y + 54), fk.NOTE, fk.AMBER, 3, 7)
    d.ellipse((x + 14, y + 33, x + 24, y + 43), fill=fk.AMBER)
    d.line((x + 29, y + 38, x + w - 15, y + 38), fill=fk.AMBER, width=4)


NS = 20  # 札の下の名前の文字の大きさ


def name_under(cx, bottom, label, gap=6):
    """札の下に付ける短い名前（サービスの名前・同じロゴの札の見分け）。名前の下端の y を返す。"""
    fk.centered(cx, bottom + gap, label, NS)
    return bottom + gap + NS + 10


def named(name, label, cx, cy, size=T):
    """ロゴの札と、その下のサービスの名前。名前の下端の y を返す。"""
    tile(name, cx, cy, size)
    return name_under(cx, cy + size / 2, label)


def tall(name, cx, cy, h):
    """縦長のロゴの札（何本も線を受ける置き場）。"""
    fk.rr((cx - T / 2, cy - h / 2, cx + T / 2, cy + h / 2), 'white', fk.LINE, 3, 22)
    fk.logo(name, cx, cy, int(T * .56))


# ── 行の高さ ───────────────────────────────────────────────
# 同じ高さには本当につながる物だけを並べる（ChatGPT を挟んで別の流れが 1 本に見えないように）
#   Gmail の行：Gmail → ChatGPT → Gmail（仕分けラベル）
#   Todoist の行：Todoist → ChatGPT → Todoist → Claude Code → 横断タスクボード
#   Google カレンダー・Keepa の行：左は手順書・自分のメモ → ChatGPT（ChatGPT から右へは出さない）。真ん中は → Claude Code
#   Notion の行：ChatGPT → Notion → Claude Code → 買い物の計画画面
#   作業メモの行：GitHub → Claude Code → GitHub → 開発ダッシュボード
# ロゴの札の下に名前を入れるので、行の間は 125px あける。YouTube と自分のメモ（右上に錠）の間は 140px
RG, RT_, RH, RKP, RN, RAZ, RY = 450, 575, 700, 825, 950, 1075, 1200
RP, RK, RB = 1340, 1470, 1620               # 自分のメモ・作業のリポジトリ・reading-log（置き場の GitHub）
LM = RH                                     # 手順書（左）から ChatGPT へ入る 1 本
LH = (RKP, RKP + 64)                        # 自分のメモ（左）から ChatGPT へ入る 2 本
LP = 22                                     # 縦長の札の上下の余白
LRL = RB                                    # reading-log（左。公開）から入る 1 本は、ChatGPT が reading-log へ書く行と同じ高さ（ほかの行の入出力と組に読まれないように）
TOP, BOT = 246, RK + 36                     # AI の札の上端・下端（Claude Code）
BOT_G = RB + 53                             # ChatGPT の札の下端（reading-log の行の下まで）
DY = RK + 196                               # 開発ダッシュボード
KY = DY + 120                               # 読書の本棚
RW = KY + 140                               # メルカリのお買い得探しの行（Notion → プラグインの札 → 提案）。読書の本棚の下

# ── AI ─────────────────────────────────────────────────────
ai_card('openai', 'ChatGPT', GX, TOP, BOT_G)
fk.trigger(GX, TOP, '毎朝6時・日曜夜')
fk.verb(GX, BOT_G + 12, '仕分け・整理・記録')
ai_card('claude', 'Claude Code', CX, TOP, BOT)
fk.verb(CX, BOT + 12, '会話の中で作業')

# ── 読まれる側（左）→ ChatGPT ─────────────────────────────
for name, label, y in (('gmail', 'Gmail', RG), ('todoist', 'Todoist', RT_), ('youtube', 'YouTube', RY)):
    named(name, label, A, y)
tile('github', A, LM)                       # 手順書（非公開）
lock(A - T / 2 + 4, LM + T / 2 - 12)        # 非公開の印。右の角は線の根元なので左下の角に付ける
name_under(A, LM + T / 2, '手順書', gap=10)  # 錠の下端とあける
tall('github', A, (LH[0] + LH[-1]) / 2, LH[-1] - LH[0] + 2 * LP)   # 自分のメモ（非公開）
lock(A - T / 2 + 4, LH[-1] + LP - 12)
name_under(A, LH[-1] + LP, '自分のメモ', gap=10)
tile('github', A, LRL)                      # reading-log（公開）
name_under(A, LRL + T / 2, 'reading-log')
IN_R = A + T / 2
for y, lab in ((RG, '新着メール'), (RT_, 'Inboxのタスク'), (RY, 'マイリスト')):
    fk.flow([(IN_R + 6, y), (G_L - 4, y)], lab, at=lab_at(IN_R, G_L, y, label=lab), size=LS)
for y, lab in ((LM, 'メールの基準'), (LH[0], '整理の基準'), (LH[1], '今の状況・目標'), (LRL, '読書の記録')):
    fk.flow([(IN_R + 6, y), (G_L - 4, y)], lab, at=lab_at(IN_R, G_L, y, dy=-40, label=lab), size=LS)

# ── ChatGPT → 置き場 ───────────────────────────────────────
for name, label, y in (('gmail', 'Gmail', RG), ('todoist', 'Todoist', RT_), ('googlecalendar', 'Googleカレンダー', RH),
                       ('keepa', 'Keepa', RKP), ('notion', 'Notion', RN), ('amazon', 'Amazon', RAZ),
                       ('youtube', 'YouTube', RY)):
    named(name, label, C, y)                # Keepa（値段の履歴）・Amazon（セール日程）は Claude Code だけが読む
tile('github', C, RP)                       # 自分のメモ（非公開）
lock(C + T / 2 - 2, RP - T / 2 + 14)        # 下の角は名前と重なるので右上の角に付ける
name_under(C, RP + T / 2, '自分のメモ')
tile('github', C, RK)                       # 作業のリポジトリ（作業メモ）
name_under(C, RK + T / 2, '作業のリポジトリ')
tile('github', C, RB)                       # reading-log（公開）
RB_NAME = name_under(C, RB + T / 2, 'reading-log')
for y, lab in ((RG, '仕分けラベル'), (RT_, 'タスク'), (RN, '欲しい物'), (RY, '整理後のリスト'),
               (RP, '今の状況・目標'), (RB, '読書の記録')):
    fk.flow([(G_R + 6, y), (S_L - 4, y)], lab, at=lab_at(G_R, S_L, y, label=lab), size=LS)

# ── 置き場 → Claude Code ───────────────────────────────────
for y, lab in ((RT_, 'タスク'), (RH, '予定'), (RKP, '値段の履歴'), (RN, '欲しい物'), (RAZ, 'セール日程'), (RK, '作業メモ')):
    fk.flow([(S_R + 6, y), (C_L - 4, y)], lab, at=lab_at(S_R, C_L, y, label=lab), size=LS)

# ── Claude Code → 書かれる側（右） ─────────────────────────
# 時間割は Todoist の行、買う順番は Notion の行、作業メモは作業メモの行。ほかは Claude Code に線の入らない高さ
OQ, ONT, OB, OP, ON, OT, OH = 300, 420, RT_, RN, RY, RP, RK
screen(E, OP, '買い物の計画画面', 'plan')
screen(E, OB, '横断タスクボード', 'board')
RT = 64                                 # 右の列のロゴの札
for name, label, y in (('qiita', 'Qiita', OQ), ('note', 'note', ONT), ('notion', 'Notion', ON), ('todoist', 'Todoist', OT)):
    named(name, label, E, y, RT)
tile('github', E, OH, RT)
OH_NAME = name_under(E, OH + RT / 2, '作業のリポジトリ')
R_L = E - RT / 2
for y, lab, end in ((OP, '買う順番', E_L), (OB, '時間割', E_L), (OQ, '記事', R_L), (ONT, 'note 版', R_L),
                    (ON, '棚卸しの結果', R_L), (OT, '完了・リスケ', R_L), (OH, '作業メモ', R_L)):
    fk.flow([(C_R + 6, y), (end - 4, y)], lab, at=lab_at(C_R, end, y, label=lab), size=LS)

# ── GitHub（右）→ 開発ダッシュボード（30 分ごと）、reading-log → 読書の本棚（公開サイト） ──
screen(E, DY, '開発ダッシュボード', 'dash', c=fk.BLUE)
TW = 2 * 26 + 12 + fk.width('30分ごと', 24)
fk.trigger(E_L - 18 - TW / 2, DY + 42, '30分ごと')   # 画面の左横（縦の中心をそろえる）。Claude Code から離す
screen(E, KY, '読書の本棚', 'shelf', c=fk.BLUE)
PRG = '進捗・本人待ち'                   # 「進捗・本人待ち・自動テスト」は 13 字で 12 字を超えるので 2 つに絞る
fk.flow([(E, OH_NAME), (E, DY - 28 - 4)], PRG, at=(E - 14 - fk.width(PRG, LS) / 2, (OH_NAME + DY) / 2 - 22), size=LS)   # 名前の下から出す。右は画布の端なので線の左に
fk.flow([(C, RB_NAME), (C, KY), (E_L - 4, KY)], '読書の記録', at=((C + E_L) / 2, KY - 36), size=LS)   # 名前の下から出す

# ── 本人（上の中央）：話す・頼む。朝の報告はスマホへ ─────────────
PX, PY, PS = 640, 120, .6
fk.person(PX, PY, PS)
P_L, P_R, P_B = PX - 68 * PS, PX + 68 * PS, PY + 118 * PS
fk.centered(PX, PY - 84 * PS - 40, '本人', 23)
# 本人 → ChatGPT（iPhone で話す）。左へ渡って降り、ChatGPT の左の辺に入る
LS_Y, LX, R0 = 150, 222, 385      # R0 は R2 より下（同じ高さだと本人との輪に見える）
fk.flow([(P_L - 6, LS_Y), (LX, LS_Y), (LX, R0), (G_L - 4, R0)], '話した内容',
        at=((LX + P_L) / 2, LS_Y - 36), size=LS)
# 本人 → Claude Code（会話で頼む）。右へ渡り、Claude Code の上の辺に入る
LQ = 140
fk.flow([(P_R + 6, LQ), (CX, LQ), (CX, TOP - 4)], '依頼', at=((P_R + CX) / 2, LQ - 36), size=LS)
R2 = 330
# ChatGPT → 本人のスマホ（朝の報告）
PH_W, PH_H = 66, 106
PH_CX = 740                                 # 本人の右下に寄せる（Claude Code の札からは離す）
PH_X, PH_Y = PH_CX - PH_W / 2, 164
phone(PH_X, PH_Y, PH_W, PH_H)
fk.flow([(G_R + 6, R2), (PH_CX, R2), (PH_CX, PH_Y + PH_H + 6)], '朝の報告',
        at=lab_at(G_R, PH_CX, R2, label='朝の報告'), size=LS)

# ── 一番下：Notion → ChatGPT のメルカリプラグイン → 提案（右の列） ──────────
PT = 100                                    # プラグインの札の高さ（幅は 1.7 倍）
named('notion', 'Notion', A, RW)
PL, PR = fk.plugin('openai', 'mercari', GX, RW, tile=PT)
fk.centered(GX, RW + PT / 2 + 8, 'メルカリプラグイン', 22)
fk.verb(GX, RW + PT / 2 + 8 + 34, '探して定価と比べる')
fk.flow([(IN_R + 6, RW), (PL - 4, RW)], '欲しい物', at=lab_at(IN_R, PL, RW, label='欲しい物'), size=LS)
screen(E, RW, '提案', 'chat')
fk.flow([(PR + 6, RW), (E_L - 4, RW)], 'お買い得の候補', at=lab_at(PR, E_L, RW, label='お買い得の候補'), size=LS)

# ロゴの数が多く、fk.save() の 128 色では Qiita の緑が茶色に落ちるので、同じ切り詰めで 256 色にして保存する
_bg = fk.Image.new('RGB', fk.im.size, fk.PAPER)
_box = fk.ImageChops.difference(fk.im, _bg).getbbox()
_out = fk.im.crop((0, max(0, _box[1] - fk.MARGIN), fk.im.size[0], min(fk.im.size[1], _box[3] + fk.MARGIN)))
_out.quantize(colors=256, method=fk.Image.Quantize.MEDIANCUT).save(Path(__file__).with_name('cover.png'), optimize=True)
