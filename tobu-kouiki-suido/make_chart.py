"""東部広域水道（東濃地域・木曽川水系）
徳山ダム導水路 導入前／導入後の 許可取水量・給水量 比較図

出典: 水道用水供給事業年報（令和6年度事業報告）岐阜県都市建築部水道企業課
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch

for f in ["/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"]:
    font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = "IPAPGothic"

M3S_TO_DAY = 86400

# --- データ（m3/日） ---
kyosui = 95_623                     # 現在の給水量（東濃5市合計）
kyoka_kiso = 2.40 * M3S_TO_DAY      # 207,360 既存許可（木曽川水系）
miriyo = kyoka_kiso - kyosui        # 111,737 未利用
tokuyama = 2.56 * M3S_TO_DAY        # 221,184 徳山ダム導水路 木曽川権利分
after_total = kyoka_kiso + tokuyama # 428,544
after_unused = miriyo + tokuyama    # 332,921

C_USED = "#2a78d6"
C_UNUSED = "#a8c8ee"
C_TOKU = "#eb6834"
C_TEXT = "#0b0b0b"
C_SUB = "#52514e"
C_GRID = "#e4e3df"
SURF = "#fcfcfb"

fig, ax = plt.subplots(figsize=(10, 7.6), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

x = [0, 1]
w = 0.52
gap = 1500  # 積み上げ区間の白い隙間

def seg(xi, bottom, h, color, label_lines, text_color="white"):
    ax.bar(xi, h - gap, w, bottom=bottom, color=color, edgecolor="none", zorder=3)
    ax.text(xi, bottom + h / 2, label_lines, ha="center", va="center",
            fontsize=11.5, color=text_color, zorder=4, linespacing=1.4)

# 導入前
seg(0, 0, kyosui, C_USED, f"現在の給水量\n{kyosui:,.0f} m³/日")
seg(0, kyosui, miriyo, C_UNUSED, f"未利用水量\n{miriyo:,.0f} m³/日", C_TEXT)
# 導入後
seg(1, 0, kyosui, C_USED, f"現在の給水量\n{kyosui:,.0f} m³/日")
seg(1, kyosui, miriyo, C_UNUSED, f"未利用水量（既存）\n{miriyo:,.0f} m³/日", C_TEXT)
seg(1, kyoka_kiso, tokuyama, C_TOKU,
    f"徳山ダム導水路 追加分\n木曽川権利分 2.56 m³/s\n{tokuyama:,.0f} m³/日")

# 合計（許可水量）
ax.text(0, kyoka_kiso + 9000, f"許可取水量  {kyoka_kiso:,.0f} m³/日\n（2.40 m³/s）",
        ha="center", va="bottom", fontsize=12, color=C_TEXT, fontweight="bold")
ax.text(1, after_total + 9000, f"許可水量 合計  {after_total:,.0f} m³/日\n（2.40 + 2.56 = 4.96 m³/s）",
        ha="center", va="bottom", fontsize=12, color=C_TEXT, fontweight="bold")

# 未利用合計のブラケット（導入後）
bx = 1 + w / 2 + 0.05
y0, y1 = kyosui, after_total - gap
ax.plot([bx, bx + 0.04, bx + 0.04, bx], [y0, y0, y1, y1], color=C_SUB, lw=1.4, zorder=2)
ax.text(bx + 0.07, (y0 + y1) / 2,
        f"未利用水量 計\n{after_unused:,.0f} m³/日\n（約33万 m³/日）\n許可の約{after_unused / after_total:.0%}",
        ha="left", va="center", fontsize=12, color=C_TEXT, fontweight="bold")

# 導入前のブラケット（未利用）
bx0 = 0 + w / 2 + 0.05
ax.plot([bx0, bx0 + 0.04, bx0 + 0.04, bx0], [kyosui, kyosui, kyoka_kiso - gap, kyoka_kiso - gap],
        color=C_SUB, lw=1.4)
ax.text(bx0 + 0.06, (kyosui + kyoka_kiso) / 2,
        f"許可の\n約{miriyo / kyoka_kiso:.0%}が\n未利用",
        ha="left", va="center", fontsize=11, color=C_SUB)

# 軸
ax.set_xticks(x)
ax.set_xticklabels(["導水路 導入前（現状）", "導水路 導入後"], fontsize=13, color=C_TEXT)
ax.set_xlim(-0.55, 1.75)
ax.set_ylim(0, 500_000)
ax.set_yticks(range(0, 500_001, 100_000))
ax.set_yticklabels([f"{v//10000}万" if v else "0" for v in range(0, 500_001, 100_000)],
                   fontsize=10.5, color=C_SUB)
ax.set_ylabel("水量（m³/日）", fontsize=11, color=C_SUB)
ax.yaxis.grid(True, color=C_GRID, lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#9a9994")
ax.tick_params(axis="both", length=0)

ax.legend(handles=[Patch(color=C_USED, label="給水量（使用水量）"),
                   Patch(color=C_UNUSED, label="未利用水量（既存許可分）"),
                   Patch(color=C_TOKU, label="徳山ダム導水路 追加分（未利用）")],
          loc="upper left", frameon=False, fontsize=10.5, ncol=3,
          bbox_to_anchor=(0, 1.02))

fig.suptitle("東部広域水道（東濃地域・木曽川水系）許可水量と使用水量\n徳山ダム導水路 導入前／導入後の比較",
             fontsize=15, fontweight="bold", color=C_TEXT, x=0.07, ha="left", y=0.985)
fig.text(0.07, 0.02,
         "出典：水道用水供給事業年報（令和6年度事業報告）岐阜県都市建築部水道企業課\n"
         "注）給水量は東濃5市（中津川・恵那・瑞浪・土岐・多治見）の合計。導入後の給水量は現状と同じと仮定。\n"
         "　　徳山ダム導水路の利水容量 4.0 m³/s を東部広域の許可水量割合（木曽川2.4：飛騨川1.35）で按分 → 木曽川水系 2.56 m³/s（飛騨川水系 1.44 m³/s は本図対象外）。",
         fontsize=8.8, color=C_SUB, ha="left", va="bottom", linespacing=1.5)

plt.subplots_adjust(left=0.1, right=0.97, top=0.85, bottom=0.17)
fig.savefig(__file__.replace("make_chart.py", "導水路_導入前後_許可水量と使用水量.png"),
            facecolor=SURF)
