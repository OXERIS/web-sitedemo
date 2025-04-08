import sqlite3
import sys
from score_calculator import (
    calculate_age_score,
    calculate_education_score,
    calculate_english_score,
    calculate_french_score,
    calculate_canadian_experience_score,
    calculate_spouse_score,
    calculate_education_language_skill_transferability_score,
    calculate_education_canadian_experience_skill_transferability_score,
    calculate_foreign_canadian_experience_skill_transferability_score,
    calculate_foreign_work_experience_language_skill_transferability_score, 
    calculate_certificate_skill_transferability_score,
    calculate_sibling_in_canada_points,
    calculate_french_language_additional_points,
    calculate_arranged_employment_points,
    calculate_provincial_nomination_points,
    calculate_canadian_education_points
)

def get_user_data_from_db(user_id):
    """
    从数据库中获取用户的问卷信息。
    :param user_id: int, 用户的ID
    :return: dict, 包含用户信息的字典
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 假设 questionnaire 表中有相关字段
    cursor.execute('''
        SELECT age, hasPartner, education_level, english_reading, english_writing, 
               english_speaking, english_listening, french_reading, french_writing,
               french_speaking, french_listening, years_of_experience,
               spouse_education_level, spouse_english_reading, spouse_english_writing,
               spouse_english_speaking, spouse_english_listening, spouse_years_of_experience,
               foreign_work_experience, canadian_professional_certificate, sibling_in_canada, arranged_employment, provincial_nomination
        FROM questionnaire 
        WHERE user_id = ?
    ''', (user_id,))

    user_data = cursor.fetchone()
    
    if user_data:
        result = {
            "age": user_data[0],
            "has_partner": user_data[1],
            "education_level": user_data[2],
            "english_reading": user_data[3],
            "english_writing": user_data[4],
            "english_speaking": user_data[5],
            "english_listening": user_data[6],
            "french_reading": user_data[7],
            "french_writing": user_data[8],
            "french_speaking": user_data[9],
            "french_listening": user_data[10],
            "years_of_experience": user_data[11],
            "spouse_education_level": user_data[12],
            "spouse_english_reading": user_data[13],
            "spouse_english_writing": user_data[14],
            "spouse_english_speaking": user_data[15],
            "spouse_english_listening": user_data[16],
            "spouse_years_of_experience": user_data[17],
            "spouse_years_of_experience": user_data[17],
            "foreign_work_experience": user_data[18],  
            "canadian_professional_certificate": user_data[19],
            "sibling_in_canada": user_data[20],
            "arranged_employment": user_data[21],
            "provincial_nomination": user_data[22]  # 新增字段
        }
    else:
        result = None
    
    conn.close()
    return result

def calculate_user_score(user_id):
    """
    从数据库中获取用户数据并计算其核心人力资本得分。
    :param user_id: int, 用户的ID
    :return: dict, 包含各个评分项和总得分的字典
    """
    user_data = get_user_data_from_db(user_id)
    
    if user_data:
        # 计算各个评分项的得分
        age_score = calculate_age_score(user_data["age"], user_data["has_partner"])
        education_score = calculate_education_score(user_data["education_level"], user_data["has_partner"])
        english_score = calculate_english_score(
            user_data["english_reading"],
            user_data["english_writing"],
            user_data["english_speaking"],
            user_data["english_listening"],
            user_data["has_partner"]
        )
        french_score = calculate_french_score(
            user_data["french_reading"],
            user_data["french_writing"],
            user_data["french_speaking"],
            user_data["french_listening"],
            user_data["has_partner"]
        )
        
        # 限制法语得分在有配偶情况下最多为 22 分
        if user_data["has_partner"] == 'yes' and french_score > 22:
            french_score = 22
        
        # 计算语言能力的总分
        language_score = english_score + french_score
        
        # 计算加拿大工作经验得分
        canadian_experience_score = calculate_canadian_experience_score(
            user_data["years_of_experience"],
            user_data["has_partner"]
        )
        
        # 计算配偶或同居伴侣的得分
        if user_data["has_partner"] == 'no':
            spouse_education_score = 0
            spouse_language_score = 0
            spouse_experience_score = 0
            total_spouse_score = 0
        else:
            spouse_scores = calculate_spouse_score(
                user_data["spouse_education_level"],
                user_data["spouse_english_reading"],
                user_data["spouse_english_writing"],
                user_data["spouse_english_speaking"],
                user_data["spouse_english_listening"],
                user_data["spouse_years_of_experience"]
            )
            spouse_education_score = spouse_scores["education_score"]
            spouse_language_score = spouse_scores["language_score"]
            spouse_experience_score = spouse_scores["experience_score"]
            total_spouse_score = spouse_scores["total_score"]
        
        # 核心人力资本总得分
        core_human_capital_score = age_score + education_score + language_score + canadian_experience_score
        
        # 构建第一官方语言各项能力的得分字典
        first_language_scores = {
            'reading': user_data["english_reading"],
            'writing': user_data["english_writing"],
            'speaking': user_data["english_speaking"],
            'listening': user_data["english_listening"]
        }

        # 计算技能迁移因素得分 - 基于教育和官方语言能力的结合
        education_language_skill_transferability_score = calculate_education_language_skill_transferability_score(
            user_data["education_level"],
            first_language_scores
        )
        
        # 计算技能迁移因素得分 - 基于教育和加拿大工作经验的结合
        education_canadian_experience_score = calculate_education_canadian_experience_skill_transferability_score(
            user_data["education_level"],
            user_data["years_of_experience"]
        )

        # 计算技能迁移因素得分 - 基于海外工作经验和官方语言能力的结合
        foreign_language_skill_transferability_score = calculate_foreign_work_experience_language_skill_transferability_score(
            user_data["foreign_work_experience"],
            first_language_scores
        )

        # 计算技能迁移因素教育维度的总得分
        education_skill_transferability_total_score = (
            education_language_skill_transferability_score +
            education_canadian_experience_score +
            foreign_language_skill_transferability_score
)        

        # 技能迁移因素教育维度的总得分不超过 50 分
        education_skill_transferability_total_score = min(education_skill_transferability_total_score, 50)



        # 计算技能迁移因素得分 - 基于海外工作经验和加拿大工作经验的结合
        foreign_canadian_experience_score = calculate_foreign_canadian_experience_skill_transferability_score(
            user_data["foreign_work_experience"],
            user_data["years_of_experience"]
        )

        # 海外工作经验维度的总得分
        foreign_skill_transferability_total_score = (
            foreign_language_skill_transferability_score +
            foreign_canadian_experience_score
        )

        
        # 技能迁移因素海外工作经验维度的总得分不超过 50 分
        foreign_skill_transferability_total_score = min(foreign_skill_transferability_total_score, 50)


        # 计算技能迁移因素得分 - 证书维度
        certificate_skill_transferability_score = calculate_certificate_skill_transferability_score(
            user_data["canadian_professional_certificate"],
            first_language_scores
        )

        # 技能迁移因素 - 总得分（更新总得分计算）
        total_skill_transferability_score = (
            education_skill_transferability_total_score +
            foreign_skill_transferability_total_score +
            certificate_skill_transferability_score
        )
        # 总得分不超过 100 分
        total_skill_transferability_score = min(total_skill_transferability_score, 100)


        # 计算额外加分
        # 1. 兄弟姐妹加分
        sibling_points = calculate_sibling_in_canada_points(user_data['sibling_in_canada'])

        # 2. 法语语言能力加分
        french_scores = {
            'reading': user_data['french_reading'],
            'writing': user_data['french_writing'],
            'speaking': user_data['french_speaking'],
            'listening': user_data['french_listening']
        }
        english_scores = {
            'reading': user_data['english_reading'],
            'writing': user_data['english_writing'],
            'speaking': user_data['english_speaking'],
            'listening': user_data['english_listening']
        }
        french_language_points = calculate_french_language_additional_points(french_scores, english_scores)

        # 3. 安排好的工作加分
        arranged_employment_points = calculate_arranged_employment_points(user_data['arranged_employment'])

        # 4. 省提名加分
        provincial_nomination_points = calculate_provincial_nomination_points(user_data['provincial_nomination'])

        # 5. 加拿大教育背景加分（如果有此字段）
        canadian_education_points = calculate_canadian_education_points(user_data['education_level'])

        # 计算额外加分总分（最高 600 分）
        total_additional_points = (
            sibling_points +
            french_language_points +
            arranged_employment_points +
            provincial_nomination_points +
            canadian_education_points
        )
        total_additional_points = min(total_additional_points, 600)


        # 计算 CRS 总分
        total_crs_score = (
            core_human_capital_score +
            total_spouse_score +
            total_skill_transferability_score +
            total_additional_points
        )
        


        # 返回各项得分和总得分
        return {
            "age_score": age_score,
            "education_score": education_score,
            "english_score": english_score,
            "french_score": french_score,
            "language_score": language_score,
            "canadian_experience_score": canadian_experience_score,
            "spouse_education_score": spouse_education_score,
            "spouse_language_score": spouse_language_score,
            "spouse_experience_score": spouse_experience_score,
            "total_spouse_score": total_spouse_score,
            "core_human_capital_score": core_human_capital_score,
            "education_language_skill_transferability_score": education_language_skill_transferability_score,
            "education_canadian_experience_score": education_canadian_experience_score,
            "foreign_language_skill_transferability_score": foreign_language_skill_transferability_score,  # 同时计入两个维度
            "education_skill_transferability_total_score": education_skill_transferability_total_score,
            "foreign_canadian_experience_score": foreign_canadian_experience_score,
            "foreign_skill_transferability_total_score": foreign_skill_transferability_total_score,
            "certificate_skill_transferability_score": certificate_skill_transferability_score,
            "total_skill_transferability_score": total_skill_transferability_score,
            "sibling_points": sibling_points,
            "french_language_points": french_language_points,
            "arranged_employment_points": arranged_employment_points,
            "provincial_nomination_points": provincial_nomination_points,
            "canadian_education_points": canadian_education_points,
            "total_additional_points": total_additional_points,
            "total_crs_score": total_crs_score
        }
    else:
        raise ValueError(f"No data found for user with ID: {user_id}")

def store_user_scores(user_id, scores):
    """
    将用户的各个评分项得分和总分存储到数据库中。
    :param user_id: int, 用户的ID
    :param scores: dict, 包含各个评分项和总得分的字典
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 首先检查是否已经有对应 user_id 的记录
    cursor.execute('SELECT 1 FROM user_scores WHERE user_id = ?', (user_id,))
    existing_record = cursor.fetchone()
    
    if existing_record:
        # 更新已有记录
        cursor.execute('''
            UPDATE user_scores SET
                age_score = ?,
                education_score = ?,
                english_score = ?,
                french_score = ?,
                language_score = ?,
                canadian_experience_score = ?,
                spouse_education_score = ?,
                spouse_language_score = ?,
                spouse_experience_score = ?,
                total_spouse_score = ?,
                core_human_capital_score = ?,
                education_language_skill_transferability_score = ?,
                education_canadian_experience_score = ?,
                foreign_language_skill_transferability_score = ?,
                education_skill_transferability_total_score = ?,
                foreign_canadian_experience_score = ?,
                foreign_skill_transferability_total_score = ?,
                certificate_skill_transferability_score = ?,
                total_skill_transferability_score = ?,
                sibling_points = ?,
                french_language_points = ?,
                arranged_employment_points = ?,
                provincial_nomination_points = ?,
                canadian_education_points = ?,
                total_additional_points = ?,
                total_crs_score = ?
            WHERE user_id = ?
        ''', (
            scores["age_score"],
            scores["education_score"],
            scores["english_score"],
            scores["french_score"],
            scores["language_score"],
            scores["canadian_experience_score"],
            scores["spouse_education_score"],
            scores["spouse_language_score"],
            scores["spouse_experience_score"],
            scores["total_spouse_score"],
            scores["core_human_capital_score"],
            scores["education_language_skill_transferability_score"],
            scores["education_canadian_experience_score"],
            scores["foreign_language_skill_transferability_score"],
            scores["education_skill_transferability_total_score"],
            scores["foreign_canadian_experience_score"],
            scores["foreign_skill_transferability_total_score"],
            scores["certificate_skill_transferability_score"],
            scores["total_skill_transferability_score"],
            scores["sibling_points"],
            scores["french_language_points"],
            scores["arranged_employment_points"],
            scores["provincial_nomination_points"],
            scores["canadian_education_points"],
            scores["total_additional_points"],
            scores["total_crs_score"],
            user_id
        ))
    else:
        # 插入新记录
        cursor.execute('''
            INSERT INTO user_scores (
                user_id,
                age_score,
                education_score,
                english_score,
                french_score,
                language_score,
                canadian_experience_score,
                spouse_education_score,
                spouse_language_score,
                spouse_experience_score,
                total_spouse_score,
                core_human_capital_score,
                education_language_skill_transferability_score,
                education_canadian_experience_score,
                foreign_language_skill_transferability_score,
                education_skill_transferability_total_score,
                foreign_canadian_experience_score,
                foreign_skill_transferability_total_score,
                certificate_skill_transferability_score,
                total_skill_transferability_score,
                sibling_points,
                french_language_points,
                arranged_employment_points,
                provincial_nomination_points,
                canadian_education_points,
                total_additional_points,
                total_crs_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            scores["age_score"],
            scores["education_score"],
            scores["english_score"],
            scores["french_score"],
            scores["language_score"],
            scores["canadian_experience_score"],
            scores["spouse_education_score"],
            scores["spouse_language_score"],
            scores["spouse_experience_score"],
            scores["total_spouse_score"],
            scores["core_human_capital_score"],
            scores["education_language_skill_transferability_score"],
            scores["education_canadian_experience_score"],
            scores["foreign_language_skill_transferability_score"],
            scores["education_skill_transferability_total_score"],
            scores["foreign_canadian_experience_score"],
            scores["foreign_skill_transferability_total_score"],
            scores["certificate_skill_transferability_score"],
            scores["total_skill_transferability_score"],
            scores["sibling_points"],
            scores["french_language_points"],
            scores["arranged_employment_points"],
            scores["provincial_nomination_points"],
            scores["canadian_education_points"],
            scores["total_additional_points"],
            scores["total_crs_score"]
        ))
        
    conn.commit()
    conn.close()
    print(f"Scores for user ID {user_id} have been stored successfully.")

# Example usage with command-line arguments
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_retrieval.py <user_id>")
        sys.exit(1)
    
    try:
        user_id = int(sys.argv[1])  # 从命令行获取 user_id
        scores = calculate_user_score(user_id)  # 获取用户数据并计算得分
        store_user_scores(user_id, scores)      # 将得分存储到数据库
        print(f"User ID {user_id} Scores: {scores}")  # 打印得分
    except ValueError as e:
        print(e)