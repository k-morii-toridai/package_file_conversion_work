""" This module is written for convert df_poscar_replaced_point to new POSCAR file. """

import os


def df2poscar(df, original_poscar_path="./POSCAR", generated_poscar_path="./gen_data/POSCAR"):
    """
    Writing the DataFrame(:df_poscar_ion_replaced_point) to a POSCAR file.
    param1: df=df_poscar_ion_replaced_point: DataFrame that has 'X', 'Y', 'Z' columns about coords.
    param2: original POSCAR file
    param3: generated POSCAR file
    """
    # POSCARファイルを読み込む
    with open(original_poscar_path, 'r') as file:
        lines = file.readlines()

    # 最初の5行を抽出
    comment_scalingfactor_lattice_line = lines[:5]

    # df_poscar_ion_replaced_pointから元素種を文字列として抽出
    species_line = '  ' + '   '.join(df['atom_symbol'].unique())
    num_line = '   ' + '   '.join([str(len(df[df['atom_symbol'] == specie])) for specie in df['atom_symbol'].unique()])
    ion_per_species_line = species_line + '\n' + num_line

    # 構造情報が始まる行を特定し，抽出
    for i, line in enumerate(lines):
        if ('Direct' in line) or ('Cartesian' in line):
            start_line = i
    selective_dynamics_line = lines[start_line]

    # df_poscar_ion_replaced_pointを文字列に変換
    ion_positions_line = df[['x', 'y', 'z']].to_string(col_space=3, header=False, index=False, index_names=False)
    # 列間のスペースを1つから3つに変更
    ion_positions_line = ion_positions_line.replace(' ', '   ')
    # 各行の先頭にスペースを追加
    ion_positions_line = '\n'.join('  ' + line for line in ion_positions_line.split('\n'))

    # ここから書き込みパート
    # 生成ファイル出力先を確認
    None if os.path.exists("gen_data") else os.makedirs('gen_data')
    # 新しいPOSCARファイルに書き込む
    with open(generated_poscar_path, 'w') as outfile:
        outfile.writelines(comment_scalingfactor_lattice_line)
        # すでに存在するテキストファイルに元素種を追記
        outfile.write(ion_per_species_line + '\n')
        # 元素種まで書かれたファイルにDirectという文字をを追記
        outfile.write(selective_dynamics_line)
        # 直交座標を追記
        outfile.write(ion_positions_line + '\n')

    print(f"{generated_poscar_path} に多原子イオンを点置換した情報がPOSCARに書き込まれました．")
