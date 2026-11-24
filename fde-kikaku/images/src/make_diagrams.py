"""Generate v3.1 diagrams as SVG files (rendered to PNG separately)."""
import os, sys

OUT = sys.argv[1]
FONT = "'IPAPGothic','IPAGothic',sans-serif"
INK, QUIET, EDGE = "#1f2937", "#5b6472", "#9aa3ae"
BLUE, BLUE_BG = "#2563eb", "#e8f0fe"
GREEN, GREEN_BG = "#15803d", "#e7f6ec"
ORANGE, ORANGE_BG = "#c2410c", "#fdf0e6"
NAVY = "#1e3a8a"
TINT = "#f3f4f6"


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.parts = w, h, []

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill="#ffffff", stroke=EDGE, sw=1.5, rx=10, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=15, color=INK, weight=400, anchor="start"):
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>')

    def lines(self, x, y, items, size=15, color=INK, gap=None, weight=400, anchor="start"):
        gap = gap or size + 7
        for i, s in enumerate(items):
            self.text(x, y + i * gap, s, size, color, weight, anchor)

    def arrow(self, d, color=EDGE, sw=2, dash=None, both=False, marker="a"):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        ms = f' marker-start="url(#{marker})"' if both else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{ds}{ms} marker-end="url(#{marker})"/>')

    def save(self, name):
        defs = (
            '<defs>'
            f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{EDGE}"/></marker>'
            f'<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker>'
            f'<marker id="g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{GREEN}"/></marker>'
            '</defs>'
        )
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" font-family="{FONT}">'
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>{defs}' + "".join(self.parts) + "</svg>")
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


# ---------------- A. 一目で分かる全体像 ----------------
s = SVG(1200, 850)
s.rect(0, 0, 1200, 104, fill=NAVY, stroke=NAVY, rx=0)
s.text(40, 50, "ENA DX LAB（恵那市地域DX人材育成事業）統合案", 30, "#ffffff", 700)
s.text(40, 86, "人を育てながら、市役所・暮らし・事業所の課題を解く ― 恵那で学び、働き、育つ", 18, "#dbe4ff")
s.text(1160, 50, "企画案 v3.1", 18, "#ffffff", 700, "end")
s.text(1160, 80, "2026年11月24日", 15, "#dbe4ff", 400, "end")

# column 1: 課題
s.rect(40, 128, 240, 320, fill=ORANGE_BG, stroke=ORANGE)
s.text(160, 162, "課題", 20, ORANGE, 700, "middle")
s.lines(60, 206, ["若い世代が", "進学・就職で市外へ流出"], 16)
s.lines(60, 282, ["市役所にも事業所にも", "デジタルを担う人が不足"], 16)
s.lines(60, 358, ["業務の改善が", "一度きりで続かない"], 16)
s.arrow("M282 288H316")
# column 2: 取り組み
s.rect(320, 128, 420, 320, fill=BLUE_BG, stroke=BLUE, sw=2)
s.text(530, 162, "取り組み（令和9〜11年度）", 20, BLUE, 700, "middle")
for i, (name, l1, l2) in enumerate([
    ("育てる", "大学生・市職員・事業者・高校生が", "デジタルで課題を解く力をつける"),
    ("実践する", "市役所・暮らし・事業所を実践の場に", "課題分析と改善ツールを実証する"),
    ("広げる", "成果発表会・オープンソース公開で", "他の課・事業所・自治体へ展開する"),
]):
    y = 180 + i * 88
    s.rect(336, y, 388, 78, fill="#ffffff", stroke=BLUE, sw=1.2, rx=8)
    s.text(352, y + 30, name, 18, BLUE, 700)
    s.lines(450, y + 30, [l1, l2], 15, gap=24)
s.arrow("M742 288H776")
# column 3: 成果
s.rect(780, 128, 210, 320, fill=GREEN_BG, stroke=GREEN)
s.text(885, 162, "成果", 20, GREEN, 700, "middle")
for i, (a, b) in enumerate([("業務時間が減り", "住民対応が早くなる"), ("育った市職員が", "自ら改善を続ける"),
                            ("事業所の", "デジタル活用が進む"), ("育った人が", "地域に残る")]):
    s.lines(798, 200 + i * 62, [a, b], 15, gap=22)
s.arrow("M992 288H1016", color=GREEN, marker="g")
# column 4: 将来像
s.rect(1020, 128, 140, 320, fill=NAVY, stroke=NAVY)
s.text(1090, 162, "将来像", 18, "#dbe4ff", 700, "middle")
s.lines(1090, 218, ["恵那で", "学び、", "働き、", "育つ"], 24, "#ffffff", gap=36, weight=700, anchor="middle")
s.lines(1090, 384, ["地域の課題を", "自分たちで", "解き続ける"], 13, "#dbe4ff", gap=19, anchor="middle")

# row: 実践フィールド
s.text(40, 500, "実践フィールド", 18, INK, 700)
s.text(40, 524, "（1年目の範囲）", 14, QUIET)
for i, (name, l1) in enumerate([
    ("① 市役所の業務", "庁内テーマ1件（AI職員FAQなど）"),
    ("② 市民の暮らし", "住民に届くテーマ1件（地域要望の管理など）"),
    ("③ 市内事業所", "相談会と業務診断（3〜5社）"),
]):
    x = 200 + i * 324
    s.rect(x, 474, 312, 72, fill="#ffffff", stroke=EDGE)
    s.text(x + 18, 503, name, 17, INK, 700)
    s.text(x + 18, 530, l1, 14, QUIET)

# row: 育てる相手
s.text(40, 600, "育てる相手", 18, INK, 700)
for i, (name, l1) in enumerate([
    ("大学生", "有償インターンで実務"), ("市職員", "自分の課の業務を改善"),
    ("事業者", "生成AIの始め方を学ぶ"), ("高校生", "発表会・体験で関わる"),
]):
    x = 200 + i * 243
    s.rect(x, 572, 231, 48, fill=BLUE_BG, stroke=BLUE_BG, rx=24)
    s.text(x + 20, 602, name, 16, BLUE, 700)
    s.text(x + 20 + len(name) * 16 + 12, 602, l1, 14, INK)

# row: cards
cards = [
    ("体制", ["恵那市・ZEN大学・民間事業者の3者協定", "協議会が選定・評価・OSS方針を担う", "契約とお金は市から事業者へ直接"]),
    ("期間と規模", ["令和9〜11年度（3か年度）", "事業費 年約2,800万〜3,000万円", "地域未来交付金（推進型）で国が1/2"]),
    ("交付金のあとの続け方", ["市の通常予算・他自治体との共同利用", "2年目に法人化を判断し受け皿に", "奨学金で若者の定着を後押し（市単独）"]),
]
for i, (h, ls) in enumerate(cards):
    x = 40 + i * 380
    s.rect(x, 650, 360, 172, fill=TINT, stroke=TINT)
    s.text(x + 20, 686, h, 18, NAVY, 700)
    s.add(f'<line x1="{x+20}" y1="700" x2="{x+340}" y2="700" stroke="{EDGE}" stroke-width="1"/>')
    s.lines(x + 20, 732, ls, 15, gap=32)
s.save("v3-01-overview.svg")

# ---------------- B. 事業スキーム ----------------
s = SVG(1200, 860)
s.text(40, 46, "契約とお金は市から事業者へ直接。協議会は「決める・評価する場」として支える", 22, INK, 700)
# 国
s.rect(420, 76, 360, 70, fill="#ffffff", stroke=EDGE)
s.text(600, 105, "国（内閣府）", 18, INK, 700, "middle")
s.text(600, 131, "地域未来交付金（地域未来推進型）", 14, QUIET, 400, "middle")
s.arrow("M600 148V204")
s.text(612, 182, "交付金（事業費の1/2）", 14, QUIET)
# 市
s.rect(420, 206, 360, 78, fill="#ffffff", stroke=EDGE)
s.text(600, 236, "恵那市（申請・事業の主体）", 18, INK, 700, "middle")
s.text(600, 264, "実践の場・予算・地域再生計画", 14, QUIET, 400, "middle")
# 奨学金
s.rect(40, 206, 260, 78, fill=GREEN_BG, stroke=GREEN)
s.text(170, 236, "地域DX人材育成奨学金", 16, GREEN, 700, "middle")
s.text(170, 262, "市単独（交付金の対象外）", 14, INK, 400, "middle")
s.arrow("M418 245H302")
# 高校生
s.rect(40, 350, 260, 86, fill="#ffffff", stroke=EDGE)
s.text(170, 382, "市内の高校生", 17, INK, 700, "middle")
s.text(170, 408, "発表会・体験で事業に関わる", 14, QUIET, 400, "middle")
s.arrow("M170 286V348", color=GREEN, marker="g")
s.text(180, 324, "進学を支援", 13, GREEN)
# 受託者
s.rect(420, 340, 360, 122, fill=BLUE_BG, stroke=BLUE, sw=2.5)
s.text(600, 372, "受託者（単一事業者 または 共同企業体）", 18, INK, 700, "middle")
s.text(600, 400, "事業の実施・技術指導・成果への責任", 14, INK, 400, "middle")
s.text(600, 424, "学生の雇用と労務管理・市内に拠点", 14, INK, 400, "middle")
s.text(600, 448, "地元IT事業者へ再委託・協業", 14, INK, 400, "middle")
s.arrow("M600 286V338", color=BLUE, marker="b", sw=2.5)
s.text(612, 318, "業務委託（学生の人件費を含む）", 14, BLUE, 700)
# ZEN大学
s.rect(900, 340, 260, 120, fill="#ffffff", stroke=EDGE)
s.text(1030, 368, "ZEN大学", 18, INK, 700, "middle")
s.text(1030, 392, "学生への周知・選考の協力", 14, QUIET, 400, "middle")
s.text(1030, 414, "学びとキャリアの見守り", 14, QUIET, 400, "middle")
s.text(1030, 440, "他の大学・高専にも開く", 13, QUIET, 400, "middle")
# 3者協定 dashed
s.add(f'<path d="M780 245H1030V338" fill="none" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="6 5"/>')
s.add(f'<path d="M782 394H898" fill="none" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="6 5"/>')
s.text(840, 234, "3者協定（役割・学生の保護・成果の扱い）", 13, NAVY, 700)
s.text(790, 386, "覚書", 13, NAVY)
# 学生
s.rect(420, 506, 360, 78, fill="#ffffff", stroke=BLUE, sw=1.5)
s.text(600, 536, "学生（有償インターン）", 18, INK, 700, "middle")
s.text(600, 562, "勤務時間は学業を優先して大学と相談", 14, QUIET, 400, "middle")
s.arrow("M600 464V504", color=BLUE, marker="b")
s.text(612, 488, "雇用・賃金・指導", 14, BLUE)
s.arrow("M1030 462V545H782", dash="6 5")
s.text(1040, 520, "在学（学費は本人負担）", 13, QUIET)
s.arrow("M302 393H360V545H418")
s.text(312, 470, "進学", 13, QUIET)
# 市職員
s.rect(40, 506, 260, 78, fill="#ffffff", stroke=EDGE)
s.text(170, 536, "市職員（育成の対象）", 17, INK, 700, "middle")
s.text(170, 562, "自分の課の業務を一緒に改善", 14, QUIET, 400, "middle")
# bus to fields
s.add(f'<path d="M170 586V622M600 586V622M170 622H990" fill="none" stroke="{EDGE}" stroke-width="2"/>')
for cx in (210, 600, 990):
    s.arrow(f"M{cx} 622V652")
s.text(612, 612, "一緒に現場に入る", 13, QUIET)
for i, (name, l1) in enumerate([("① 市役所の業務", "庁内の改善テーマ"), ("② 市民の暮らし", "住民に届く実証テーマ"), ("③ 市内事業所", "相談会・業務診断・導入支援")]):
    x = 40 + i * 380
    s.rect(x, 654, 360, 66, fill="#ffffff", stroke=EDGE)
    s.text(x + 20, 682, name, 17, INK, 700)
    s.text(x + 20, 706, l1, 14, QUIET)
# 協議会
s.rect(40, 742, 1120, 56, fill=TINT, stroke=TINT)
s.text(600, 768, "地域の協議会（1年目に設置・お金は通さない）：市・経済団体・金融機関・大学・高校・開発事業者", 16, INK, 700, "middle")
s.text(600, 790, "テーマと支援先の選定、成果の評価、オープンソースの方針、会員制度（詳しくは協議会の図）", 14, QUIET, 400, "middle")
s.text(40, 836, "注：2年目に法人化（一般社団法人等）を判断し、共同利用・有料支援の契約主体とする。地域活性化起業人など他の制度とは経費・時間を区分する。", 13, QUIET)
s.save("v3-02-scheme.svg")

# ---------------- C. 人材の循環 ----------------
s = SVG(1200, 640)
s.text(40, 46, "恵那で学び、働き、育つ ― 進学しても地元を離れない人材の循環", 22, INK, 700)
nodes = [
    (120, 90, "① 市内の高校生", ["成果発表会や体験で", "「恵那でもできる」と知る"]),
    (740, 90, "② 恵那に住んだまま大学生に", ["ZEN大学など通信制大学へ進学", "1年目は全国のZEN大学生から"]),
    (740, 420, "③ 市役所・地域・事業所で実践", ["受託者に雇用された有償インターン", "学びながら課題を解く"]),
    (120, 420, "④ 地域で就職・活躍", ["市役所・市内事業所・IT企業へ", "市内就業で奨学金の返還免除"]),
]
for x, y, name, ls in nodes:
    s.rect(x, y, 340, 120, fill="#ffffff", stroke=BLUE, sw=2)
    s.text(x + 20, y + 36, name, 18, BLUE, 700)
    s.lines(x + 20, y + 70, ls, 15, gap=26)
s.arrow("M462 150H738", color=BLUE, marker="b", sw=2.5)
s.text(600, 140, "奨学金で進学を後押し", 14, GREEN, 700, "middle")
s.arrow("M910 212V418", color=BLUE, marker="b", sw=2.5)
s.text(922, 320, "有償インターン", 14, BLUE, 700)
s.arrow("M738 480H462", color=BLUE, marker="b", sw=2.5)
s.text(600, 470, "卒業・就職", 14, BLUE, 700, "middle")
s.arrow("M290 418V212", color=BLUE, marker="b", sw=2.5)
s.text(278, 320, "次の世代の手本に", 14, BLUE, 700, "end")
s.rect(430, 250, 340, 128, fill=NAVY, stroke=NAVY)
s.text(600, 292, "恵那で学び、働き、育つ", 20, "#ffffff", 700, "middle")
s.lines(600, 326, ["市職員も一緒に学び、", "DXを続ける力が市役所に残る"], 14, "#dbe4ff", gap=22, anchor="middle")
s.rect(40, 572, 1120, 44, fill=TINT, stroke=TINT)
s.text(600, 600, "育てる相手：大学生・市職員・市内事業者・高校生　／　学生の作業は本番データを使わず、サンプルデータで行う", 15, INK, 400, "middle")
s.save("v3-03-cycle.svg")

# ---------------- D. 3か年ロードマップ ----------------
s = SVG(1200, 720)
s.text(40, 46, "1年目は小さく育てて試し、3年目までに交付金に頼らない形へ移す", 22, INK, 700)
cols = [("準備（現在）", "令和8年11月〜9年3月"), ("1年目　育てる・試す", "令和9年度"), ("2年目　広げる", "令和10年度"),
        ("3年目　続く形にする", "令和11年度"), ("自走", "令和12年度〜")]
rows = [
    ("事業の中身", [["3者協定・協議会の準備", "再生計画・交付金申請", "受託者の契約方法を決定"],
                ["課題分析・2テーマ実証", "学生と市職員の育成", "成果発表会"],
                ["ツールを他の課・地域へ", "育った職員が他課を支援", "住民向けテーマを拡大"],
                ["他自治体との共同利用", "オープンソース公開", "続け方へ移行"],
                ["市の通常予算", "共同利用・有料支援で", "継続"]]),
    ("育つ人", [["学生の募集計画", "（ZEN大学と協議）"], ["全国のZEN大学生", "市職員", "高校生は発表会で"],
             ["事業者・高校生の", "学びの場を増やす"], ["市内の高校生が", "入学して参加する流れ"], ["育った人が", "次の世代を指導"]]),
    ("事業所支援", [["協議会の構成を", "決める"], ["相談会・業務診断", "3〜5社"], ["業務診断10社程度", "導入支援"],
               ["有料メニュー化", "金融機関と連携"], ["有料支援で継続"]]),
    ("協議会・法人", [["規約・会員区分・", "OSS方針を決める"], ["協議会が発足", "選定・評価を担う"], ["開発パートナー登録", "法人化を判断"],
               ["法人を設立・移行", "共同利用・有料支援"], ["法人が受け皿"]]),
    ("事業費", [["予算要求", "（12月に数値確定）"], ["約2,800万円", "国1,400・市1,400"], ["約3,000万円", "国1,500・市1,500"],
             ["約3,000万円", "国1,500・市1,500"], ["市予算＋自主収入"]]),
]
lx, cw, top = 40, 190, 76
x0 = lx + 128
for j, (h, sub) in enumerate(cols):
    x = x0 + j * (cw + 8)
    main = j == 0
    s.rect(x, top, cw, 60, fill=BLUE if main else NAVY, stroke=BLUE if main else NAVY, rx=8)
    s.text(x + cw / 2, top + 26, h, 16, "#ffffff", 700, "middle")
    s.text(x + cw / 2, top + 48, sub, 13, "#dbe4ff", 400, "middle")
heights = [104, 86, 70, 70, 70]
y = top + 72
for (label, cells), hgt in zip(rows, heights):
    s.rect(lx, y, 120, hgt, fill=TINT, stroke=TINT, rx=8)
    s.text(lx + 60, y + hgt / 2 + 6, label, 16, INK, 700, "middle")
    for j, c in enumerate(cells):
        x = x0 + j * (cw + 8)
        s.rect(x, y, cw, hgt, fill=BLUE_BG if j == 0 else "#ffffff", stroke=EDGE, sw=1, rx=8)
        s.lines(x + 12, y + 26, c, 14, gap=24)
    y += hgt + 8
# gates
gy = y + 34
s.add(f'<line x1="{x0}" y1="{gy}" x2="{x0 + 5*cw + 32}" y2="{gy}" stroke="{EDGE}" stroke-width="2"/>')
for j, g in enumerate(["交付決定・予算議決", "1年目の成果評価", "2年目の評価・法人化判断", "自走への移行判断"]):
    gx = x0 + (j + 1) * (cw + 8) - 4
    s.add(f'<path d="M{gx} {gy-11}l11 11l-11 11l-11 -11z" fill="#ffffff" stroke="{NAVY}" stroke-width="2"/>')
    s.text(gx, gy + 36, g, 14, NAVY, 700, "middle")
s.text(40, gy + 80, "各年度の事業は、毎年度の予算議決と交付決定が前提。不採択・減額の場合は「育成＋1テーマ＋相談会」の最小構成（年約2,000万円）で実施するか見送るかを事前に決める。", 13, QUIET)
s.save("v3-04-roadmap.svg")


# ---------------- E. 協議会とオープンソース管理の役割分担 ----------------
s = SVG(1200, 760)
s.text(40, 46, "協議会は「ルールを決めて、つなぐ場」。権利は市、作業とサービスは事業者・法人が担う", 22, INK, 700)
roles = [
    (40, "恵那市", "権利を持つ", "#ffffff", EDGE, ["成果物の著作権を保有（委託契約で帰属）", "公開場所（GitHub等）の所有者", "受託者へ開発・保守を委託", "他自治体と共同利用の協定を結ぶ"], None),
    (430, "地域の協議会", "ルールを決める", BLUE_BG, BLUE, ["公開方針・ライセンス・公開前の確認", "改善の優先順位・要望の集約", "テーマ・支援先の選定と成果の評価", "会員制度・開発パートナーの登録基準"], "お金は通さない・著作権は持たない"),
    (820, "受託者 → 法人・開発パートナー", "作業とサービス", "#ffffff", EDGE, ["開発・保守・公開作業（1年目は受託者）", "導入支援・個別開発（開発パートナー）", "共同利用・有料サービス（法人化後）", "預かるデータの管理責任を負う"], None),
]
for x, name, role, fill, stroke, items, note in roles:
    s.rect(x, 80, 340, 250, fill=fill, stroke=stroke, sw=2 if stroke == BLUE else 1.5)
    s.text(x + 20, 112, name, 18, INK, 700)
    s.text(x + 20, 138, role, 15, BLUE if stroke == BLUE else QUIET, 700)
    s.add(f'<line x1="{x+20}" y1="152" x2="{x+320}" y2="152" stroke="{EDGE}" stroke-width="1"/>')
    s.lines(x + 20, 182, ["・" + t for t in items], 14, gap=30)
    if note:
        s.text(x + 20, 312, note, 13, BLUE, 700)
s.arrow("M428 205H384")
s.text(406, 196, "提言", 13, QUIET, 400, "middle")
s.arrow("M772 205H816")
s.text(794, 196, "基準", 13, QUIET, 400, "middle")
s.arrow("M210 332V356H990V334")
s.text(600, 350, "委託（開発・保守）　契約とお金は市から直接", 13, QUIET, 400, "middle")
# members
s.rect(40, 392, 840, 256, fill=TINT, stroke=TINT)
s.text(60, 424, "協議会の会員", 18, INK, 700)
mem = [("運営会員", ["市・経済団体・地域金融機関", "大学・高校"], "方針・優先順位・評価を決める"),
       ("開発パートナー（登録制）", ["受託者・地元IT事業者など", "条件を公開した開放型の登録"], "導入・保守・個別開発を請け負う"),
       ("利用会員", ["市内事業所・団体・自治会", "1年目は無料"], "要望・研修・事例共有・相談")]
for i, (n, ls, r) in enumerate(mem):
    x = 60 + i * 270
    s.rect(x, 442, 256, 186, fill="#ffffff", stroke=BLUE, sw=1.5)
    s.text(x + 16, 472, n, 16, BLUE, 700)
    s.lines(x + 16, 504, ls, 14, gap=24)
    s.text(x + 16, 576, "→ " + r, 14, INK, 700)
s.arrow("M428 334V390", color=BLUE, marker="b")
s.rect(910, 392, 250, 256, fill="#ffffff", stroke=EDGE, dash="6 5")
s.text(930, 424, "他の自治体", 18, INK, 700)
s.lines(930, 462, ["協議会の会員ではなく", "市との協定で関わる", "", "共同利用・費用分担は", "自治体どうしの協定や", "負担金で整理する"], 14, QUIET, gap=26)
s.rect(40, 672, 1120, 64, fill=GREEN_BG, stroke=GREEN_BG)
s.text(60, 699, "オープンソースは会員でなくても誰でも使える。会員の特典はコードではなく「支援とつながり」。", 15, INK, 700)
s.text(60, 724, "運営会員と開発パートナーを兼ねる事業者は、関係する議決から外れる。有料サービスの契約主体は法人化後の法人とする。", 14, QUIET)
s.save("v3-05-council.svg")
print("ok")
