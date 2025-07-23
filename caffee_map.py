import os
import zipfile
import pandas as pd


# 현재 폴더 경로에서 dataFile.zip 파일을 찾음
def find_zip_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    zip_file_path = os.path.join(current_dir, 'dataFile.zip')
    
    if os.path.exists(zip_file_path):
        return zip_file_path
    else:
        raise FileNotFoundError("dataFile.zip을 찾을 수 없음. 현재 폴더에 파일이 있는지 확인할 것.")


# dataFile.zip 압축 해제
def extract_zip_file(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_file_path))
    print(f"{zip_file_path} 압축 해제 완료.")


# 구조물 ID를 area_category.csv 기준으로 이름으로 변환
# merge(): 두 DataFrame을 병합하는 함수
def merge_area_struct_to_category(area_struct, area_category):
    merged_area = area_struct.merge(
        area_category,
        on='category',
        how='left'
    )
    return merged_area


# 세 데이터를 하나의 DataFrame으로 병합하고, area 기준으로 정렬
# merge(): 두 DataFrame을 병합하는 함수
def merge_dataframes(area_struct_with_category, area_map):
    merged_df = area_struct_with_category.merge(
        area_map,
        on=['x', 'y'],
        how='outer'
    )
    # na_last 매개변수 제거하고 NaN 처리 개선
    merged_df = merged_df.sort_values(by='area')
    merged_df = merged_df.reset_index(drop=True)
    return merged_df


# area 0~3에 대한 데이터 필터링 (수정: area 1만 -> area 0~3)
def filter_area_data(merged_df):
    # area 0~3 데이터 필터링
    area_filtered_data = merged_df[merged_df['area'].isin([0, 1, 2, 3])].copy()
    print(f"Area 0~3 데이터: {len(area_filtered_data)}개 좌표")
    
    # area별 데이터 개수 출력
    area_counts = area_filtered_data['area'].value_counts().sort_index()
    print("Area별 분포:")
    for area_num, count in area_counts.items():
        print(f"  Area {area_num}: {count}개")
    
    return area_filtered_data


# 구조물 종류별 요약 통계 (보너스)
def generate_summary_report(merged_df):
    print("\n=== 구조물 종류별 요약 통계 ===")
    
    # 전체 통계
    print(f"총 좌표 개수: {len(merged_df)}")
    print(f"Area 분포:")
    print(merged_df['area'].value_counts().sort_index())
    
    # 구조물별 통계 (category와 struct 컬럼 기준)
    if 'category' in merged_df.columns and 'struct' in merged_df.columns:
        print(f"\n구조물 종류별 개수:")
        
        # category별로 그룹화하여 통계 생성
        category_stats = merged_df.groupby(['category', 'struct']).size().reset_index(name='count')
        
        # category별로 정렬하여 출력
        for _, row in category_stats.iterrows():
            category_num = int(row['category']) if pd.notna(row['category']) else 0
            struct_name = row['struct'] if pd.notna(row['struct']) else 'Unknown'
            count = row['count']
            print(f"#{category_num} {struct_name}: {count}개")
        
        # 건설현장 통계
        if 'ConstructionSite' in merged_df.columns:
            construction_count = merged_df[merged_df['ConstructionSite'] == 1].shape[0]
            print(f"\n건설현장 개수: {construction_count}개")


def main():
    # ZIP 파일 찾기
    zip_file = find_zip_file()
    print(f"찾은 ZIP 파일 경로: {zip_file}")
    
    # ZIP 파일 압축 해제
    extract_zip_file(zip_file)
    
    # 압축 해제 후 CSV 파일 경로 설정
    base_dir = os.path.dirname(zip_file)
    area_category_csv = os.path.join(base_dir, 'area_category.csv')
    area_map_csv = os.path.join(base_dir, 'area_map.csv')
    area_struct_csv = os.path.join(base_dir, 'area_struct.csv')
    
    # CSV 파일 읽기
    area_category = pd.read_csv(area_category_csv)
    area_map = pd.read_csv(area_map_csv)
    area_struct = pd.read_csv(area_struct_csv)
    
    # 데이터 출력
    print("=== 원본 데이터 확인 ===")
    print("area_category.csv 내용:")
    print(area_category.head())
    print("----------------------")
    print("area_map.csv 내용:")
    print(area_map.head())
    print("----------------------")
    print("area_struct.csv 내용:")
    print(area_struct.head())
    print("----------------------")
    
    # 구조물 ID를 카테고리 이름으로 변환
    area_struct_with_category = merge_area_struct_to_category(area_struct, area_category)
    print("구조물 ID 변환 결과:")
    print(area_struct_with_category.head())
    print("----------------------")
    
    # 세 데이터를 하나의 DataFrame으로 병합하고, area 기준으로 정렬
    merged_df = merge_dataframes(area_struct_with_category, area_map)
    print("병합된 DataFrame 내용:")
    print(merged_df.head(10))
    print(f"전체 데이터 크기: {merged_df.shape}")
    print("----------------------")
    
    # area 0~3 데이터 필터링
    area_filtered_data = filter_area_data(merged_df)
    print("Area 0~3 필터링 결과:")
    print(area_filtered_data.head(10))
    print("----------------------")
    
    # 요약 통계 생성 (보너스) - 에러 처리 추가
    try:
        generate_summary_report(merged_df)
    except Exception as e:
        print(f"요약 통계 생성 중 에러 발생: {e}")
        print("에러 무시하고 계속 진행...")
    
    # 결과를 mas_map.py로 저장하기 위한 변수 반환
    return merged_df, area_filtered_data


# 메인 함수 실행
if __name__ == "__main__":
    merged_data, area_1_filtered = main()