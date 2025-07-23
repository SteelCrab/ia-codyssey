# 최단 경로 탐색 및 시각화
# 내 집(시작점)에서 반달곰 커피 지점(도착점)까지의 최단 경로를 구합니다.
# BFS 알고리즘을 사용하여 최단 경로를 탐색합니다.
# 건설현장이 있는 위치는 지나갈 수 없도록 구현합니다.
# 최단 경로를 CSV 파일로 저장하고 지도에 빨간 선으로 시각화합니다.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from collections import deque
from mas_map import main as load_data
import platform

# 한글 폰트 설정 함수
def setup_korean_font():
    system = platform.system()
    if system == 'Darwin':  # macOS
        try:
            korean_fonts = ['AppleGothic', 'Apple SD Gothic Neo', 'Nanum Gothic', 'Malgun Gothic']
            # 사용 가능한 한글 폰트들을 순서대로 시도
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

setup_korean_font()

# 최단 경로 탐색을 위한 클래스
class PathFinder:
    
    def __init__(self, data):
        self.data = data
        self.grid = self._create_grid()
        self.start_pos = self._find_position(3)  # MyHome
        self.end_pos = self._find_position(4)    # BandalgomCoffee
        
    # 그리드 생성 함수 (건설현장은 통행 불가)
    def _create_grid(self):
        x_min, x_max = self.data['x'].min(), self.data['x'].max()
        y_min, y_max = self.data['y'].min(), self.data['y'].max()
        
        # 그리드 초기화 (0: 통행가능, 1: 통행불가)
        grid = {}
        
        # 모든 데이터 행을 순회하여 그리드 생성
        for _, row in self.data.iterrows():
            x, y = int(row['x']), int(row['y'])
            # 건설현장이 있으면 통행 불가
            if row['ConstructionSite'] == 1:
                grid[(x, y)] = 1
            else:
                grid[(x, y)] = 0
                
        return grid
    
    # 특정 카테고리의 위치를 찾는 함수
    def _find_position(self, category):
        pos_data = self.data[self.data['category'] == category]
        if len(pos_data) > 0:
            row = pos_data.iloc[0]
            return (int(row['x']), int(row['y']))
        return None
    
    # 인접한 위치들을 반환하는 함수 (상하좌우)
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        
        # 상하좌우 4방향 탐색
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # 각 방향에 대해 이동 가능한지 확인
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # 그리드 범위 내에 있고 통행 가능한 경우
            if (new_x, new_y) in self.grid and self.grid[(new_x, new_y)] == 0:
                neighbors.append((new_x, new_y))
                
        return neighbors
    
    # BFS를 사용한 최단 경로 탐색 함수
    def bfs_shortest_path(self):
        if not self.start_pos or not self.end_pos:
            print("시작점 또는 도착점을 찾을 수 없습니다.")
            return None
            
        print(f"시작점: {self.start_pos}")
        print(f"도착점: {self.end_pos}")
        
        # BFS 초기화
        queue = deque([(self.start_pos, [self.start_pos])])
        visited = {self.start_pos}
        
        # 큐가 빌 때까지 탐색 진행
        while queue:
            current_pos, path = queue.popleft()
            
            # 도착점에 도달한 경우
            if current_pos == self.end_pos:
                print(f"최단 경로 발견! 길이: {len(path)}")
                return path
            
            # 인접한 위치들을 탐색
            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        print("경로를 찾을 수 없습니다.")
        return None
    
    # 모든 반달곰 커피를 방문하는 최단 경로 탐색 함수
    def find_all_coffee_shops_path(self):
        # 모든 반달곰 커피 위치 찾기
        coffee_shops = []
        coffee_data = self.data[self.data['category'] == 4]
        # 반달곰 커피 데이터를 순회하여 위치 수집
        for _, row in coffee_data.iterrows():
            if row['ConstructionSite'] != 1:  # 건설현장이 아닌 경우만
                coffee_shops.append((int(row['x']), int(row['y'])))
        
        if not coffee_shops:
            print("반달곰 커피를 찾을 수 없습니다.")
            return None
            
        print(f"반달곰 커피 위치: {coffee_shops}")
        
        if len(coffee_shops) == 1:
            # 커피숍이 1곳만 있으면 기본 최단 경로와 동일
            return self.bfs_shortest_path()
        
        # 여러 커피숍이 있는 경우 모든 조합을 시도하여 최단 경로 찾기
        from itertools import permutations
        
        min_path = None
        min_length = float('inf')
        
        # 모든 커피숍 방문 순서 조합을 시도
        for perm in permutations(coffee_shops):
            current_pos = self.start_pos
            total_path = [current_pos]
            total_length = 0
            valid_path = True
            
            # 각 커피숍을 순서대로 방문
            for coffee_pos in perm:
                path_segment = self.bfs_path_between_points(current_pos, coffee_pos)
                if not path_segment:
                    valid_path = False
                    break
                
                # 경로 추가 (시작점 제외)
                total_path.extend(path_segment[1:])
                total_length += len(path_segment) - 1
                current_pos = coffee_pos
            
            # 유효한 경로이고 더 짧은 경우 업데이트
            if valid_path and total_length < min_length:
                min_length = total_length
                min_path = total_path
        
        if min_path:
            print(f"모든 반달곰 커피 방문 최단 경로 발견! 길이: {len(min_path)}")
            return min_path
        else:
            print("모든 반달곰 커피를 방문할 수 있는 경로를 찾을 수 없습니다.")
            return None
        
    # 모든 구조물을 한 번씩 지나는 최적화된 경로 함수 (TSP 근사 해법)
    def find_all_structures_path(self):
        # 모든 구조물 위치 찾기
        structures = []
        # 아파트, 빌딩, 내집, 커피 카테고리를 순회
        for category in [1, 2, 3, 4]:  # 아파트, 빌딩, 내집, 커피
            positions = self.data[self.data['category'] == category]
            # 각 카테고리의 구조물 위치를 수집
            for _, row in positions.iterrows():
                if row['ConstructionSite'] != 1:  # 건설현장이 아닌 경우만
                    structures.append((int(row['x']), int(row['y']), category))
        
        if not structures:
            return None
            
        print(f"방문할 구조물: {len(structures)}개")
        
        # 시작점에서 가장 가까운 구조물부터 방문하는 그리디 알고리즘
        current_pos = self.start_pos
        unvisited = structures.copy()
        total_path = [current_pos]
        
        # 모든 구조물을 방문할 때까지 반복
        while unvisited:
            # 현재 위치에서 가장 가까운 구조물 찾기
            min_distance = float('inf')
            next_structure = None
            next_path = None
            
            # 방문하지 않은 모든 구조물과의 거리 계산
            for structure in unvisited:
                target_pos = (structure[0], structure[1])
                path = self.bfs_path_between_points(current_pos, target_pos)
                
                if path and len(path) < min_distance:
                    min_distance = len(path)
                    next_structure = structure
                    next_path = path
            
            if next_structure and next_path:
                # 경로 추가 (시작점 제외)
                total_path.extend(next_path[1:])
                current_pos = (next_structure[0], next_structure[1])
                unvisited.remove(next_structure)
            else:
                print("일부 구조물에 도달할 수 없습니다.")
                break
        
        return total_path
    
    # 두 점 사이의 최단 경로를 찾는 함수 (BFS 사용)
    def bfs_path_between_points(self, start, end):
        if start == end:
            return [start]
            
        queue = deque([(start, [start])])
        visited = {start}
        
        # 큐가 빌 때까지 탐색 진행
        while queue:
            current_pos, path = queue.popleft()
            
            if current_pos == end:
                return path
            
            # 인접한 위치들을 탐색
            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None


# 경로를 CSV 파일로 저장하는 함수
def save_path_to_csv(path, filename="home_to_cafe.csv"):
    if not path:
        print("저장할 경로가 없습니다.")
        return
    
    # 경로 데이터를 DataFrame으로 변환
    path_data = []
    # 경로의 각 지점을 순회하여 데이터 생성
    for i, (x, y) in enumerate(path):
        path_data.append({
            'step': i + 1,
            'x': x,
            'y': y,
            'description': '시작점' if i == 0 else ('도착점' if i == len(path)-1 else f'경로점 {i}')
        })
    
    df = pd.DataFrame(path_data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"경로가 {filename} 파일로 저장되었습니다.")


# 경로가 포함된 지도 시각화 메인 함수
def create_map_with_path():
    
    # 데이터 로드
    print("데이터 로딩 중...")
    merged_data, area_filtered_data = load_data()
    
    # 경로 탐색
    path_finder = PathFinder(merged_data)
    
    # 1. 모든 반달곰 커피를 방문하는 최단 경로
    print("=== 모든 반달곰 커피 방문 최단 경로 탐색 ===")
    all_coffee_path = path_finder.find_all_coffee_shops_path()
    
    # 2. 보너스: 모든 구조물을 지나는 경로
    print("\n=== 보너스: 모든 구조물 방문 경로 탐색 ===")
    all_structures_path = path_finder.find_all_structures_path()
    
    if not all_coffee_path:
        print("반달곰 커피 경로를 찾을 수 없어 지도만 생성합니다.")
        return
    
    # 경로를 CSV로 저장
    save_path_to_csv(all_coffee_path, "home_to_cafe.csv")
    
    if all_structures_path:
        save_path_to_csv(all_structures_path, "all_structures_path.csv")
        print(f"모든 구조물 방문 경로 길이: {len(all_structures_path)}")
    
    # 좌표 범위 확인
    x_min, x_max = merged_data['x'].min(), merged_data['x'].max()
    y_min, y_max = merged_data['y'].min(), merged_data['y'].max()
    
    print(f"좌표 범위: X({x_min}~{x_max}), Y({y_min}~{y_max})")
    
    # 그림 크기 설정 - 오른쪽 여백을 위해 폭 증가
    fig_width = max(20, (x_max - x_min + 1) * 1.2)  # 폭 증가
    fig_height = max(14, (y_max - y_min + 1) * 1.0)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # 배경색 설정
    ax.set_facecolor('#f8f9fa')
    
    # 그리드 라인 그리기
    draw_grid_lines(ax, x_min, x_max, y_min, y_max)
    
    # 건설 현장 먼저 그리기
    draw_construction_sites(ax, merged_data)
    
    # 구조물 그리기
    draw_structures(ax, merged_data)
    
    # 경로 그리기 (겹침 처리)
    draw_paths_with_overlap_handling(ax, all_coffee_path, all_structures_path)
    
    # 축 설정 (좌측 상단이 (1,1)이 되도록)
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_max + 0.5, y_min - 0.5)  # Y축 뒤집기
    
    # 축 레이블 설정
    ax.set_xlabel('X 좌표', fontsize=14, fontweight='bold')
    ax.set_ylabel('Y 좌표', fontsize=14, fontweight='bold')
    ax.set_title('지역 지도 - 최단 경로 시각화', fontsize=18, fontweight='bold', pad=20)
    
    # 축 눈금 설정
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    
    # 그리드 스타일
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # 범례 추가 (오른쪽 밖)
    add_legend_with_path(ax, has_bonus_path=bool(all_structures_path))
    
    # 경로 정보 추가 (오른쪽 밖)
    add_path_info(ax, merged_data, all_coffee_path, all_structures_path, x_max, y_min)
    
    # 레이아웃 조정 - 오른쪽 여백 확보
    plt.subplots_adjust(right=0.75)  # 오른쪽 25% 여백 확보
    
    # 이미지 저장
    plt.savefig('map_final.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("최종 지도가 map_final.png 파일로 저장되었습니다.")
    
    try:
        plt.show()
    except:
        print("GUI 환경이 아니므로 화면 표시를 건너뜁니다.")
    
    plt.close()


# 그리드 라인을 그리는 함수
def draw_grid_lines(ax, x_min, x_max, y_min, y_max):
    # 세로 그리드 라인 (X축) 그리기
    for x in range(x_min, x_max + 1):
        ax.axvline(x=x, color='lightgray', linestyle='-', linewidth=0.8, alpha=0.6)
    
    # 가로 그리드 라인 (Y축) 그리기
    for y in range(y_min, y_max + 1):
        ax.axhline(y=y, color='lightgray', linestyle='-', linewidth=0.8, alpha=0.6)


# 건설 현장을 그리는 함수
def draw_construction_sites(ax, data):
    construction_sites = data[data['ConstructionSite'] == 1]
    
    # 건설 현장 데이터를 순회하여 회색 사각형 그리기
    for _, row in construction_sites.iterrows():
        x, y = row['x'], row['y']
        
        # 회색 사각형 그리기
        rect = patches.Rectangle(
            (x - 0.45, y - 0.45), 0.9, 0.9,
            linewidth=2, edgecolor='dimgray', facecolor='lightgray', 
            alpha=0.9, zorder=1
        )
        ax.add_patch(rect)


# 구조물들을 그리는 함수
def draw_structures(ax, data):
    structures = data[data['category'] > 0]
    
    # 구조물 데이터를 순회하여 각 타입별로 그리기
    for _, row in structures.iterrows():
        x, y = row['x'], row['y']
        category = row['category']
        
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
            triangle_points = np.array([
                [x, y + 0.4],
                [x - 0.35, y - 0.25],
                [x + 0.35, y - 0.25]
            ])
            triangle = patches.Polygon(
                triangle_points,
                linewidth=3, edgecolor='darkgreen', facecolor='green',
                alpha=0.9, zorder=4
            )
            ax.add_patch(triangle)
            
        elif category == 4:  # BandalgomCoffee - 녹색 사각형
            rect = patches.Rectangle(
                (x - 0.3, y - 0.3), 0.6, 0.6,
                linewidth=3, edgecolor='darkgreen', facecolor='limegreen',
                alpha=0.9, zorder=4
            )
            ax.add_patch(rect)

#두 경로에서 겹치는 선분들을 찾기
def find_overlapping_segments(path1, path2):

    if not path1 or not path2:
        return set()
    
    # 경로를 선분으로 변환
    segments1 = set()
    segments2 = set()

    # 선분을 정규화하여 작은 좌표가 먼저 오도록 함
    for i in range(len(path1) - 1):
        p1, p2 = path1[i], path1[i + 1]
        # 선분을 정규화 (작은 좌표가 먼저 오도록)
        segment = tuple(sorted([p1, p2]))
        segments1.add(segment)
    
    # 두 번째 경로의 선분도 정규화하여 저장
    for i in range(len(path2) - 1):
        p1, p2 = path2[i], path2[i + 1]
        segment = tuple(sorted([p1, p2]))
        segments2.add(segment)
    
    # 겹치는 선분 찾기
    overlapping = segments1.intersection(segments2)
    return overlapping

# 경로를 겹치는 부분을 고려하여 그리는 함수
def draw_paths_with_overlap_handling(ax, shortest_path, all_structures_path):
    if not shortest_path:
        return
    
    # 겹치는 선분 찾기
    overlapping_segments = set()
    if all_structures_path:
        overlapping_segments = find_overlapping_segments(shortest_path, all_structures_path)
    
    # 기본 최단 경로 그리기
    draw_single_path_with_overlaps(ax, shortest_path, 'red', overlapping_segments, 
                                  offset_x=0.0, offset_y=0.0, label='최단 경로')
    
    # 모든 구조물 방문 경로 그리기 (겹치는 부분은 다른 스타일)
    if all_structures_path:
        draw_single_path_with_overlaps(ax, all_structures_path, 'purple', overlapping_segments,
                                      offset_x=0.1, offset_y=0.1, label='모든 구조물 방문')

# 겹치는 부분을 고려하여 단일 경로 그리기
def draw_single_path_with_overlaps(ax, path, color, overlapping_segments, offset_x=0, offset_y=0, label=''):

    if not path or len(path) < 2:
        return
    
    # 일반 선분들과 겹치는 선분들을 분리하여 그리기
    for i in range(len(path) - 1):
        p1, p2 = path[i], path[i + 1]
        segment = tuple(sorted([p1, p2]))
        
        x1, y1 = p1[0] + offset_x, p1[1] + offset_y
        x2, y2 = p2[0] + offset_x, p2[1] + offset_y
        
        # 겹치는 선분인지 확인
        if segment in overlapping_segments:
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=2, 
                   linestyle='--', alpha=0.8, zorder=5)
        else:
            # 일반 선분은 실선으로 표시
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=3, 
                   alpha=0.8, zorder=5)
    
    # 경로 점들 표시
    path_x = [pos[0] + offset_x for pos in path]
    path_y = [pos[1] + offset_y for pos in path]
    ax.scatter(path_x, path_y, color=color, s=16, alpha=0.9, zorder=6, 
              edgecolors='white', linewidth=0.5)
    
    # 시작점과 끝점 강조 (빨간 경로만)
    if color == 'red':
        start_x, start_y = path[0]
        end_x, end_y = path[-1]
        
        ax.plot(start_x, start_y, marker='*', markersize=15, color='blue', 
                markeredgecolor='darkblue', markeredgewidth=2, zorder=7)
        
        ax.plot(end_x, end_y, marker='*', markersize=15, color='orange', 
                markeredgecolor='darkorange', markeredgewidth=2, zorder=7)


# 경로가 포함된 범례를 추가하는 함수 - 지도 밖 오른쪽에 배치
def add_legend_with_path(ax, has_bonus_path=False):
    legend_elements = []
    
    # 기존 구조물들
    legend_elements.append(
        plt.Line2D([0], [0], marker='o', color='w', 
                  markerfacecolor='brown', markersize=12,
                  markeredgecolor='saddlebrown', markeredgewidth=2,
                  label='아파트/빌딩')
    )
    
    legend_elements.append(
        plt.Line2D([0], [0], marker='^', color='w', 
                  markerfacecolor='green', markersize=12,
                  markeredgecolor='darkgreen', markeredgewidth=2,
                  label='내 집')
    )
    
    legend_elements.append(
        plt.Line2D([0], [0], marker='s', color='w', 
                  markerfacecolor='limegreen', markersize=12,
                  markeredgecolor='darkgreen', markeredgewidth=2,
                  label='반달곰 커피')
    )
    
    legend_elements.append(
        plt.Line2D([0], [0], marker='s', color='w', 
                  markerfacecolor='lightgray', markersize=12,
                  markeredgecolor='dimgray', markeredgewidth=2,
                  label='건설 현장')
    )
    
    # 경로 관련
    legend_elements.append(
        plt.Line2D([0], [0], color='red', linewidth=3,
                  label='모든 반달곰 커피 방문 (실선)')
    )
    
    # 보너스 경로
    if has_bonus_path:
        legend_elements.append(
            plt.Line2D([0], [0], color='purple', linewidth=3,
                      label='모든 구조물 방문 (실선)')
        )
        
        legend_elements.append(
            plt.Line2D([0], [0], color='gray', linewidth=2, linestyle='--',
                      label='겹치는 경로 구간 (점선)')
        )
    legend_elements.append(
        plt.Line2D([0], [0], marker='*', color='blue', markersize=12,
                  markeredgecolor='darkblue', linestyle='None',
                  label='시작점')
    )
    
    # 도착점
    # : 도착점은 오렌지색 별표로 표시
    legend_elements.append(
        plt.Line2D([0], [0], marker='*', color='orange', markersize=12,
                  markeredgecolor='darkorange', linestyle='None',
                  label='도착점')
    )
    
    # 범례를 지도 밖 오른쪽에 배치
    ax.legend(handles=legend_elements, loc='center left', 
             bbox_to_anchor=(1.02, 0.7), fontsize=11,
             frameon=True, fancybox=True, shadow=True,
             facecolor='white', edgecolor='gray')


# 경로 정보 텍스트를 추가하는 함수 - 지도 밖 오른쪽에 배치
def add_path_info(ax, data, all_coffee_path, all_structures_path, x_max, y_min):
    
    # 구조물별 개수 계산
    apartment_count = len(data[data['category'] == 1])
    building_count = len(data[data['category'] == 2])
    myhome_count = len(data[data['category'] == 3])
    coffee_count = len(data[data['category'] == 4])
    construction_count = len(data[data['ConstructionSite'] == 1])
    
    # 경로 정보
    coffee_path_length = len(all_coffee_path) if all_coffee_path else 0
    all_structures_length = len(all_structures_path) if all_structures_path else 0
    
    info_text = f"""지도 정보:
• 아파트: {apartment_count}개
• 빌딩: {building_count}개  
• 내 집: {myhome_count}개
• 반달곰 커피: {coffee_count}개
• 건설 현장: {construction_count}개

경로 정보:
• 모든 반달곰 커피 방문: {coffee_path_length - 1}칸
• 총 이동 단계: {coffee_path_length}개"""
    
    if all_structures_path:
        info_text += f"""

보너스 경로:
• 모든 구조물 방문: {all_structures_length - 1}칸
• 총 이동 단계: {all_structures_length}개"""
    
    # 텍스트를 지도 밖 오른쪽 아래에 배치
    ax.text(1.02, 0.3, info_text, 
           fontsize=11, verticalalignment='top',
           transform=ax.transAxes,  # 축 좌표계 사용
           bbox=dict(boxstyle="round,pad=0.7", facecolor="lightyellow", 
                    alpha=0.9, edgecolor='orange', linewidth=1))


if __name__ == "__main__":
    create_map_with_path()
