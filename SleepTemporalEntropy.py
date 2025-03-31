import pandas as pd
import numpy as np
import pyedflib
import xml.etree.ElementTree as ET

def parse_xml_annotation(annotation_file_path):
    tree = ET.parse(annotation_file_path)
    root = tree.getroot()

    sleep_stages = []
    for event in root.findall(".//ScoredEvent"):
        stage = event.find("EventConcept").text
        start = float(event.find("Start").text)
        duration = float(event.find("Duration").text)

        # 将XML中的Stage转换为我们代码中所使用的Stage名称
        stage_mapping = {
            'Stage 1 sleep': 'N1',
            'Stage 2 sleep': 'N2',
            'Stage 3 sleep': 'N3',
            'Stage 4 sleep': 'N3',  # Stage 3和Stage 4一般可以合并为N3
            'REM sleep': 'REM',
            'Wake': 'Wake'
        }

        if stage.split('|')[0] in stage_mapping:
            sleep_stage = stage_mapping[stage.split('|')[0]]
            sleep_stages.append({"Type": sleep_stage, "Start": start, "Duration": duration})

    sleep_stages_df = pd.DataFrame(sleep_stages)
    return sleep_stages_df

def calculate_SleepTemporalEntropy(edf_file_path, annotation_file_path):
    print(f"  Parsing EDF file: {edf_file_path}")
    print(f"  Parsing annotation file: {annotation_file_path}")

    # 使用 PyEDFlib 读取 EDF 文件
    with pyedflib.EdfReader(edf_file_path) as edf_reader:
        edf_info = edf_reader.getFileDuration()  # 获取EDF文件时长等信息
        print(f"EDF file duration: {edf_info} seconds")

    # 使用 xml.etree.ElementTree 解析 XML 注释文件
    sleep_stages = parse_xml_annotation(annotation_file_path)

    if sleep_stages.empty:
        print("  Error: sleep_stages DataFrame is empty")
        return {}

    print("  Sleep stages parsed successfully")

    # 过滤掉未评分的睡眠阶段
    sleep_stages = sleep_stages[sleep_stages['Type'] != 'NotScored']

    # 合并连续的相同阶段，计算总持续时间
    sleep_stages['Duration'] = sleep_stages.groupby((sleep_stages['Type'] != sleep_stages['Type'].shift()).cumsum())[
        'Duration'].transform('sum')
    sleep_stages = sleep_stages[(sleep_stages['Type'] != sleep_stages['Type'].shift()).fillna(True)]

    # 定义睡眠阶段
    states = ['Wake', 'N1', 'N2', 'N3', 'REM']
    stay_times = {state: [] for state in states}

    # 记录每个阶段的持续时间
    for index, row in sleep_stages.iterrows():
        current_stage = row['Type']
        if current_stage in stay_times:
            stay_times[current_stage].append(row['Duration'])

    def shannon_entropy(prob_distribution):
        prob_distribution = prob_distribution[prob_distribution > 0]
        return -np.sum(prob_distribution * np.log2(prob_distribution))

    time_entropies = {}
    all_durations = []
    for state, times in stay_times.items():
        all_durations.extend(times)
        if len(times) > 1:
            prob_distribution = np.array(times) / np.sum(times)
            SleepTemporalEntropy = shannon_entropy(prob_distribution)
            time_entropies[f"{state}_Time_Entropy"] = SleepTemporalEntropy
        else:
            time_entropies[f"{state}_Time_Entropy"] = None

    # 计算整体睡眠时间熵
    overall_entropy = None
    if len(all_durations) > 1:
        overall_prob_distribution = np.array(all_durations) / np.sum(all_durations)
        overall_entropy = shannon_entropy(overall_prob_distribution)
    time_entropies["Overall_Time_Entropy"] = overall_entropy

    # 计算NREM睡眠时间熵（N1, N2, N3阶段的总时间熵）
    nrem_durations = stay_times['N1'] + stay_times['N2'] + stay_times['N3']
    nrem_entropy = None
    if len(nrem_durations) > 1:
        nrem_prob_distribution = np.array(nrem_durations) / np.sum(nrem_durations)
        nrem_entropy = shannon_entropy(nrem_prob_distribution)
    time_entropies["NREM_Time_Entropy"] = nrem_entropy

    return time_entropies

if __name__ == '__main__':
    edf_file_path = './shhs1-200001.edf'
    annotation_file_path = './shhs1-200001-nsrr.xml'

    time_entropies = calculate_SleepTemporalEntropy(edf_file_path, annotation_file_path)

    print(time_entropies)
