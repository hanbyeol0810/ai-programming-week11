import pandas as pd
from pathlib import Path

###########################
###########################
def 정제(df):
    cleaned = df.copy()  # 원본을 바꾸지 않도록 복사본을 만든다.

    cleaned = cleaned.dropna(subset=["점수"])  # 점수가 비어 있는 행을 삭제한다.
    print(len(cleaned))

    cleaned = cleaned.drop_duplicates()  # 완전히 같은 중복 행을 하나만 남긴다.
    print(len(cleaned))

    cleaned["반"] = cleaned["반"].str.strip()  # 반의 앞뒤 공백을 제거한다.
    cleaned["과목"] = cleaned["과목"].str.strip()  # 과목의 앞뒤 공백을 제거한다.
    print(len(cleaned))

    cleaned["점수"] = pd.to_numeric(cleaned["점수"], errors="coerce")  # 점수를 숫자로 변환한다.
    cleaned = cleaned[(cleaned["점수"] >= 0) & (cleaned["점수"] <= 100)]  # 점수 범위 밖의 행을 삭제한다.
    print(len(cleaned))

    return cleaned


# 스크립트 파일이 있는 폴더를 기준으로 CSV를 찾는다.
csv_path = Path(__file__).resolve().with_name("scores_2026.csv")
df = pd.read_csv(csv_path)
df = 정제(df)

# 과목이 '수학'인 행만 남긴다.
df = df[df["과목"] == "수학"].copy()
print(len(df))

print(sorted(df["반"].unique()))       # ['1반', '2반'] ← 세 개에서 두 개로
print(sorted(df["과목"].unique()))      # ['수학', '영어', '프로그래밍'] ← 네 개에서 세 개로


# 시작        114
# 빈 칸 제거  108      ← 114 - 108 = 6    진단표의 「빈 칸」과 같은가?
# 중복 제거   104      ← 108 - 104 = 4    진단표의 「중복」과 같은가?
# 범위 밖 제거 100     ← 104 - 100 = 4    999 세 개 + 음수 하나

# '반'을 기준으로 점수 평균을 계산한다.
반별_평균 = df.groupby("반")["점수"].mean()
print(반별_평균)

# '과목'과 '반'을 기준으로 점수 평균을 계산한다.
과목_반별_평균 = df.groupby(["과목", "반"])["점수"].mean()
print(과목_반별_평균)

# '반'별 개수, 평균, 중앙값, 최댓값을 한 표로 출력한다.
반별_통계 = df.groupby("반")["점수"].agg(
    개수="count",
    평균="mean",
    중앙값="median",
    최댓값="max",
).round(2)
print(반별_통계)


