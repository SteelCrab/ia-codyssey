"""
분석된 데이터를 기반으로 지역 지도를 시각화
지도는 좌측 상단이 (1, 1), 우측 하단이 가장 큰 좌표가 되도록 시각화
가로/세로 방향의 그리드 라인을 그리고,
아파트와 빌딩은 갈색 원형,
반달곰 커피점 위치는 녹색 사각형,
내 집의 위치는 녹색 삼각형,
건설 현장은 회색 사각형으로 표현합니다.
건설 현장을 나타내는 회색 사각형은 바로 옆 좌표와 살짝 겹쳐도 됩니다.
건설 현장과 기타 구조물(아파트, 빌딩)과 겹치면 건설 현장으로 판단한다.
이미지로 map.png 파일로 저장합니다.
(보너스) 아파트, 빌딩, 반달곰 커피 등의 범례를 지도에 함께 표현
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from caffee_map import main as load_data
import platform

# 한글 폰트 설정 (운영체제별)
def setup_korean_font():
    system = platform.system()
    if system == 'Darwin':  # macOS
        try:
            # macOS에서 사용 가능한 한글 폰트들
            korean_fonts = ['AppleGothic', 'Apple SD Gothic Neo', 'Nanum Gothic', 'Malgun Gothic']
            for font in korean_fonts:
                try:
                    plt.rcParams['font.family'] = font
                    break
                except:
                    continue
        except:
            plt.rcParams['font.family'] = 'DejaVu Sans'
    elif system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:  # Linux
        plt.rcParams['font.family'] = 'Nanum Gothic'
    
    plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 실행
setup_korean_font()


def create_map_visualization():
    """지도 시각화 메인 함수"""
    
    # 데이터 로드
    print("데이터 로딩 중...")
    merged_data, area_filtered_data = load_data()
    
    # 좌표 범위 확인
    x_min, x_max = merged_data['x'].min(), merged_data['x'].max()
    y_min, y_max = merged_data['y'].min(), merged_data['y'].max()
    
    print(f"좌표 범위: X({x_min}~{x_max}), Y({y_min}~{y_max})")
    
    # 그림 크기 설정 (좌표 범위에 비례)
    fig_width = max(14, (x_max - x_min + 1) * 0.9)
    fig_height = max(12, (y_max - y_min + 1) * 0.9)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # 배경색 설정
    ax.set_facecolor('#f8f9fa')
    
    # 그리드 라인 그리기
    draw_grid_lines(ax, x_min, x_max, y_min, y_max)
    
    # 건설 현장 먼저 그리기 (다른 구조물보다 뒤에)
    draw_construction_sites(ax, merged_data)
    
    # 구조물 그리기
    draw_structures(ax, merged_data)
    
    # 축 설정 (좌측 상단이 (1,1)이 되도록)
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_max + 0.5, y_min - 0.5)  # Y축 뒤집기
    
    # 축 레이블 설정 (한글)
    ax.set_xlabel('X 좌표', fontsize=14, fontweight='bold')
    ax.set_ylabel('Y 좌표', fontsize=14, fontweight='bold')
    ax.set_title('지역 지도 시각화', fontsize=18, fontweight='bold', pad=20)
    
    # 축 눈금 설정
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    
    # 그리드 스타일 개선
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # 범례 추가
    add_legend(ax)
    
    # 통계 정보 추가
    add_statistics_text(ax, merged_data, x_max, y_min)
    
    # 레이아웃 조정
    plt.tight_layout()
    
    # 이미지 저장
    plt.savefig('map.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("지도가 map.png 파일로 저장되었습니다.")
    
    # 화면에 표시 (GUI 환경에서만)
    try:
        plt.show()
    except:
        print("GUI 환경이 아니므로 화면 표시를 건너뜁니다.")
    
    plt.close()

# 그리드 라인 그리기 함수
# : X축과 Y축에 대해 그리드 라인을 그립니다.
def draw_grid_lines(ax, x_min, x_max, y_min, y_max):
    
    # 세로 그리드 라인 (X축)
    for x in range(x_min, x_max + 1):
        ax.axvline(x=x, color='lightgray', linestyle='-', linewidth=0.8, alpha=0.6)
    
    # 가로 그리드 라인 (Y축)
    for y in range(y_min, y_max + 1):
        ax.axhline(y=y, color='lightgray', linestyle='-', linewidth=0.8, alpha=0.6)

# 건설 현장 그리기 (회색 사각형)
    # 회색 사각형으로 표시
    # 다른 구조물과 겹칠 때 우선 표시
    # 살짝 겹치도록 크기 조정 (0.9×0.9)
def draw_construction_sites(ax, data):
    
    construction_sites = data[data['ConstructionSite'] == 1]
    
    for _, row in construction_sites.iterrows():
        x, y = row['x'], row['y']
        
        # 회색 사각형 (살짝 겹치도록 크기 조정)
        rect = patches.Rectangle(
            (x - 0.45, y - 0.45), 0.9, 0.9, # 크기 조정
            linewidth=2, edgecolor='dimgray', facecolor='lightgray',  
            alpha=0.9, zorder=1
        )
        ax.add_patch(rect)

# 구조물 그리기
def draw_structures(ax, data):
    
    # 구조물이 있는 데이터만 필터링 (category > 0)
    structures = data[data['category'] > 0]
    
    # 각 구조물의 좌표와 종류에 따라 그리기
    for _, row in structures.iterrows():
        x, y = row['x'], row['y']
        category = row['category']
        # 컬럼명에 공백이 있을 수 있으므로 처리
        struct_name = row.get(' struct', row.get('struct', 'Unknown'))
        
        # 건설 현장과 겹치는 경우 건설 현장 우선
        if row['ConstructionSite'] == 1:
            continue
        
        if category == 1:  # Apartment - 갈색 원형
            circle = patches.Circle(
                (x, y), 0.35, linewidth=2, 
                edgecolor='saddlebrown', facecolor='brown', 
                alpha=0.9, zorder=3
            )
            ax.add_patch(circle)
            
        elif category == 2:  # Building - 갈색 원형
            circle = patches.Circle(
                (x, y), 0.35, linewidth=2, 
                edgecolor='saddlebrown', facecolor='brown', 
                alpha=0.9, zorder=3
            )
            ax.add_patch(circle)
            
        elif category == 3:  # MyHome - 녹색 삼각형
            # 삼각형을 직접 좌표로 그리기
            triangle_points = np.array([
                [x, y + 0.4],       # 위쪽 꼭짓점
                [x - 0.35, y - 0.25], # 왼쪽 아래
                [x + 0.35, y - 0.25]  # 오른쪽 아래
            ])
            triangle = patches.Polygon(
                triangle_points,
                linewidth=2, edgecolor='darkgreen', facecolor='green',
                alpha=0.9, zorder=3
            )
            ax.add_patch(triangle)
            
        elif category == 4:  # BandalgomCoffee - 녹색 사각형
            rect = patches.Rectangle(
                (x - 0.3, y - 0.3), 0.6, 0.6,
                linewidth=2, edgecolor='darkgreen', facecolor='limegreen',
                alpha=0.9, zorder=3
            )
            ax.add_patch(rect)


def add_legend(ax):
    
    legend_elements = []
    
    # 아파트/빌딩 - 갈색 원형
    legend_elements.append(
        plt.Line2D([0], [0], marker='o', color='w', 
                  markerfacecolor='brown', markersize=12,
                  markeredgecolor='saddlebrown', markeredgewidth=2,
                  label='아파트/빌딩')
    )
    
    # 내 집 - 녹색 삼각형
    legend_elements.append(
        plt.Line2D([0], [0], marker='^', color='w', 
                  markerfacecolor='green', markersize=12,
                  markeredgecolor='darkgreen', markeredgewidth=2,
                  label='내 집')
    )
    
    # 반달곰 커피 - 녹색 사각형
    legend_elements.append(
        plt.Line2D([0], [0], marker='s', color='w', 
                  markerfacecolor='limegreen', markersize=12,
                  markeredgecolor='darkgreen', markeredgewidth=2,
                  label='반달곰 커피')
    )
    
    # 건설 현장 - 회색 사각형
    legend_elements.append(
        plt.Line2D([0], [0], marker='s', color='w', 
                  markerfacecolor='lightgray', markersize=12,
                  markeredgecolor='dimgray', markeredgewidth=2,
                  label='건설 현장')
    )
    
    # 범례 위치 설정
    ax.legend(handles=legend_elements, loc='upper right', 
             bbox_to_anchor=(0.98, 0.98), fontsize=12,
             frameon=True, fancybox=True, shadow=True,
             facecolor='white', edgecolor='gray')

# 통계 정보 텍스트 추가 (한글)
def add_statistics_text(ax, data, x_max, y_min):
    
    # 구조물별 개수 계산
    apartment_count = len(data[data['category'] == 1])
    building_count = len(data[data['category'] == 2])
    myhome_count = len(data[data['category'] == 3])
    coffee_count = len(data[data['category'] == 4])
    construction_count = len(data[data['ConstructionSite'] == 1])
    
    # 통계 텍스트 생성 (한글)
    stats_text = f"""통계 정보:
• 아파트: {apartment_count}개
• 빌딩: {building_count}개  
• 내 집: {myhome_count}개
• 반달곰 커피: {coffee_count}개
• 건설 현장: {construction_count}개
• 총 좌표: {len(data)}개"""
    
    # 텍스트 박스 추가
    ax.text(x_max + 0.3, y_min + 3, stats_text, 
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle="round,pad=0.7", facecolor="lightblue", 
                    alpha=0.9, edgecolor='navy', linewidth=1))


if __name__ == "__main__":
    create_map_visualization()
